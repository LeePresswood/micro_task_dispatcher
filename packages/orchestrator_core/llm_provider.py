import os
import json
from typing import List, Dict, Any
import google.generativeai as genai
from dataclasses import asdict
from packages.orchestrator_core.agent import ToolCall
from dotenv import load_dotenv

class LLMProvider:
    """
    Abstracts the interaction with the LLM provider.
    Currently supports: Google Gemini
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in .env")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-pro-preview')

    def generate_plan(self, user_request: str, tools_schema: List[Dict[str, Any]]) -> List[ToolCall]:
        """
        Generates a plan (list of tool calls) based on the user request and available tools.
        """
        if not self.api_key:
            return []

        prompt = self._construct_prompt(user_request, tools_schema)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            print(f"LLM Error: {e}")
            return []

    def _construct_prompt(self, user_request: str, tools_schema: List[Dict]) -> str:
        return f"""
You are an AI Orchestrator. Your goal is to decompose the USER REQUEST into a sequence of tool calls.

AVAILABLE TOOLS:
{json.dumps(tools_schema, indent=2)}

USER REQUEST:
"{user_request}"

INSTRUCTIONS:
1. Analyze the request.
2. Select the appropriate tools from the list.
3. Return a JSON object with a key "plan" containing a list of tool calls.
4. Each tool call must have "tool_name" and "arguments".
5. Output ONLY valid JSON. Do not include markdown formatting like ```json.

EXAMPLE OUTPUT:
{{
  "plan": [
    {{
      "tool_name": "post_to_x",
      "arguments": {{ "message": "Hello world" }}
    }}
  ]
}}
"""

    def _parse_response(self, response_text: str) -> List[ToolCall]:
        try:
            # Clean up potential markdown formatting
            cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_text)
            
            plan = []
            for item in data.get("plan", []):
                plan.append(ToolCall(
                    tool_name=item["tool_name"],
                    arguments=item["arguments"]
                ))
            return plan
        except json.JSONDecodeError:
            print(f"❌ Failed to parse LLM response: {response_text}")
            return []
