# Implementation Plan - Micro-Task Dispatcher (MTD) Phase 1

# Goal Description
Develop the Micro-Task Dispatcher (MTD), an autonomous AI Orchestrator, and prove its capabilities with a "Social Fan-Out" use case. The goal is to take a single user request ("post to all social platforms") and have the MTD intelligently decompose this into calls to specialized micro-tools for Threads, Bluesky, and X.

## User Review Required
> [!IMPORTANT]
> **Technology Stack**: Python 3.10+ is confirmed.
> **Strict Typing**: All code will use Python type hints (`typing` module) and follow Google-style docstrings to ensure readability and maintainability.

> [!NOTE]
> **LLM Integration**: We will use a simple LLM-based planner. We will assume the presence of a `.env` file for API keys (Gemini/Claude).

## Proposed Changes

### Monorepo Structure & Git Strategy
**Git Strategy**: We will use a **single Git repository** for the entire monorepo. This is the standard approach for monorepos (hence "mono"). It simplifies code sharing and atomic commits.
**Security**:
- **API Keys**: All secrets (LLM keys, Social Media tokens) will be stored in a `.env` file at the root.
- **.gitignore**: The `.env` file will be strictly ignored to prevent accidental commits.

**Directory Layout**:
```text
/micro_task_dispatcher (Root)
    /packages
        /orchestrator_core  # Python package (Snake case for python packages)
        /micro_tools        # Python namespace package
            /social         # Python package
    /tests                  # Global/E2E tests
    .env                    # Secrets (Gitignored)
    .gitignore
```

### Orchestrator Core (`packages/orchestrator_core`)
#### [NEW] `agent.py`
- The main entry point for the MTD Agent.
- **Responsibility**:
    - `plan(user_request: str) -> List[ToolCall]`: Decompose request.
    - `execute(plan: List[ToolCall]) -> Dict`: Execute tools.
    - `synthesize(results: Dict) -> str`: Return final response.
- **Typing**: Extensive use of `pydantic` models or `dataclasses` for structured data exchange.

### Micro-Tools (`packages/micro_tools/social`)
#### [NEW] `social_tools.py`
- Implementation of the three required functions:
    - `post_to_threads(message: str) -> SocialPostResult`
    - `post_to_bluesky(message: str) -> SocialPostResult`
    - `post_to_x(message: str) -> SocialPostResult`
- **Mocks**: Initially print to stdout and return success.

### Testing Strategy
- **Unit Tests**: We will place unit tests within each package (e.g., `packages/orchestrator_core/tests/`) to keep them close to the code.
- **E2E Tests**: Integration tests that span multiple packages will live in the root `/tests` directory.

## Verification Plan

### Automated Tests
- **End-to-End Script**: `tests/verify_social_fanout.py`
  - Instantiates the MTD Agent.
  - Mocks the LLM response (or uses real one if key provided) to avoid non-deterministic failures during initial dev.
  - Verifies the flow: Request -> Plan -> 3 Tool Calls -> Synthesis.
