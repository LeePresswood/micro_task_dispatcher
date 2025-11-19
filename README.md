# Micro-Task Dispatcher (MTD) 🤖✨

> **Vibe Coded by Gemini 1.5 Pro & Antigravity** 🚀

Welcome to the **Micro-Task Dispatcher**, an autonomous AI Orchestrator designed to break down complex human requests into precise, parallel micro-tasks.

This project is an exploration into **Agentic Architecture**, built with a "vibe-coded" philosophy: fast, iterative, and AI-driven development.

## 🌟 The Concept

The MTD acts as the central brain. You give it a high-level goal (e.g., "Tell the world about our launch!"), and it:
1.  **Plans**: Decomposes the request into specific tool calls.
2.  **Executes**: Dispatches these calls to specialized "micro-tools" (like social media APIs).
3.  **Synthesizes**: Returns a unified summary of the results.

## 🏗️ Architecture

-   **Monorepo**: Single repository for core logic and all tool packages.
-   **Orchestrator Core**: Python-based agent logic (`packages/orchestrator_core`).
-   **Micro-Tools**: Independent, single-purpose functions (`packages/micro_tools`).
-   **Stack**: Python 3.10+, Pydantic, and strict typing.

## 🚀 Phase 1: Social Fan-Out (Complete)

The initial Proof-of-Concept demonstrates a **Social Fan-Out** workflow.
-   **Input**: "Post this message to X, Threads, and Bluesky."
-   **Action**: The Agent identifies the intent and calls three separate mock tools in parallel.
-   **Result**: A confirmed broadcast summary.

## 📂 Documentation

We believe in building in public. Check out our development artifacts in the `docs/` folder:
-   [Task List](docs/task.md): The step-by-step checklist used to build this.
-   [Implementation Plan](docs/implementation_plan.md): The technical blueprint approved before coding.

## 🤝 Contributing

This project is "vibe-coded," meaning we move fast and let the AI do the heavy lifting. If you want to contribute, just open an issue or PR!

---
*Built with ❤️ by LeePresswood & Gemini*
