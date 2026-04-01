# Gemini CLI System Architecture

This document outlines the architecture, tools, and operational rules for the Gemini CLI agent, serving as its long-term memory and central documentation.

## The "Eye" Subsystem

The "Eye" subsystem is designed for local multimodal processing and command-line visual reasoning. It leverages LM Studio (`lms`) for hosting vision-language models (VLMs) on local hardware, prioritizing privacy and performance on Apple Silicon.

*   **Core Components:**
    *   `qwen_subagent.py`: Handles argument parsing and orchestrates VLM interactions.
    *   `core.py`: Contains VLM interaction logic, including image encoding, querying LM Studio API, and model loading/unloading with TTL.
    *   LM Studio (`lms` CLI): Used for starting the VLM server and managing models.
*   **Data Flow:** Images are optimized (downsampled if large), encoded to Base64, and sent to the LM Studio API for analysis. Results are processed and returned to the user.
*   **Guardrails:** Local-first processing ensures data privacy. Models are loaded with a 15-minute TTL to manage memory.

## Interactive Menus (User Decision Router)

To improve user interaction and ensure deterministic responses, the CLI employs a strict enumerated menu format for decisions and error resolutions.

*   **Protocol:** When user input is required for choices or error handling, the CLI will present a numbered list of actionable options, always concluding with an "Other (Please specify)" choice.
*   **Tool:** This functionality is managed by the `user_decision_router` skill, implemented via the `prompt_decision_menu` function in `~/workspace/Computational/cli_tools/interaction.py`.
*   **Behavior:** The CLI pauses execution, displays a concise summary (often an error message), and waits for a precise integer selection or custom input.

## Local LLM Proxy Bridge (/toggle-local)

The CLI can be toggled between "Cloud Mode" (Gemini API) and "Local Mode" (Offline via LiteLLM) to support local development and privacy-focused workflows.

*   **Logic:**
    *   **Intercept:** Standard Gemini API calls are redirected to `localhost:4000`.
    *   **Proxy:** LiteLLM serves as the bridge, translating Gemini requests into the format required by LM Studio (`openai` compatible).
    *   **Configuration:** Managed via `~/workspace/Warehouse/Repositories/mllm/proxy/litellm_config.yaml`.
*   **Behavior:**
    *   **Command:** `/toggle-local` invokes the mode selector.
    *   **Port Management:** Automatically checks for and offers to clear zombie processes on ports 4000 (LiteLLM) and 1234 (LM Studio).
    *   **Warnings:** Warns the user of potential tool-calling (MCP) degradation and mathematical hallucinations in local-only mode.
*   **Dependencies:** Requires `litellm` and a tool-capable local model (e.g., `qwen2.5-coder-7b-instruct`) loaded in LM Studio.

## Active Tool Registry

...
7.  **`CLI_router`**: Manages command interception (like `/meditate` and `/toggle-local`) and tool orchestration within the `cli_tools` module.
8.  **`toggle_local_mode` (/toggle-local)**: Implemented in `~/workspace/Computational/cli_tools/local_toggle.py`. Manages the LiteLLM proxy and environment overrides for offline operation.


---

## Rules, Cautions & Limitations

*   **Non-Destructive Generation:** Avoid overwriting working Python logic without careful reading.
*   **Enforce Interaction Rules:** Use `user_decision_router` for all user decisions, avoiding conversational filler.
*   **Documentation Clarity:** `gemini.md` is the long-term memory; ensure it is structured, readable, and accurate.


### 🛡️ Last Synchronized: 2026-04-01 14:59:41
- hnxj-gemini: f6a55e9
- eye: 8297c71
: 8297c71


### 🛡️ Last Synchronized: 2026-04-01 15:03:20
- hnxj-gemini: f6a55e9


### 🛡️ Last Synchronized: 2026-04-01 15:05:16
- hnxj-gemini: f6a55e9
- eye: eea5c19
