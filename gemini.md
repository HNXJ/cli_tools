# Gemini CLI System Architecture

This document outlines the architecture, tools, and operational rules for the Gemini CLI agent, serving as its long-term memory and central documentation.

## The "Eye" Subsystem

The "Eye" subsystem is designed for local multimodal processing and command-line visual reasoning. It leverages LM Studio (`lms`) for hosting vision-language models (VLMs) on local hardware, prioritizing privacy and performance on Apple Silicon.

*   **Core Components:**
    *   `qwen_subagent.py`: Handles argument parsing and orchestrates VLM interactions.
    *   `core.py`: Contains VLM interaction logic, including image encoding, querying LM Studio API, and model loading/unloading with TTL.
    *   LM Studio (`lms` CLI): Used for starting the VLM server and managing models.
*   **Data Flow:** Images are optimized (downsampled if large), encoded to Base64, and sent to the LM Studio API for analysis. Results are processed and returned to the user.
*   **Guardrails:** Local-first processing ensures data privacy. Models are loaded with a 10-minute TTL to manage memory.

## Interactive Menus (User Decision Router)

To improve user interaction and ensure deterministic responses, the CLI employs a strict enumerated menu format for decisions and error resolutions.

*   **Protocol:** When user input is required for choices or error handling, the CLI will present a numbered list of actionable options, always concluding with an "Other (Please specify)" choice.
*   **Tool:** This functionality is managed by the `user_decision_router` skill, implemented via the `prompt_decision_menu` function in `~/workspace/Computational/cli_tools/interaction.py`.
*   **Behavior:** The CLI pauses execution, displays a concise summary (often an error message), and waits for a precise integer selection or custom input.

## The GAMMA Protocol

The GAMMA protocol (`Guide And Model Mapped Actions`) is the standard format for providing the Gemini CLI with complex engineering instructions.

*   **Specification:** GAMMA documents define a problem, propose a solution architecture, outline skills/tools, detail version control steps, and list rules/cautions.
*   **Purpose:** It ensures instructions are atomic, scope-preserving, and executable through the CLI's toolset, facilitating robust and repeatable task execution.

## Active Tool Registry

This section lists the core skills and tools that are implemented and verified within the Gemini CLI.

1.  **`mlx_lms_vlm_local`**: Initializes the LM Studio server (Port 4474) and loads VLM models (`qwen3.5-vl` with TTL). This is handled via `lms` CLI commands.
2.  **`mlx_lms_eye_local`**: Orchestrates image analysis via `qwen_subagent.py` and `core.py`, including Base64 encoding and fetching descriptions from LM Studio. Image optimization is a planned feature.
3.  **`mlx_lms_view`**: A placeholder tool for analyzing visual output and generating code patches. Implementation details are pending.
4.  **`optimize_asset_tool`**: A placeholder tool for optimizing images and stripping bloat from HTML/SVG files. Implementation details are pending.
5.  **`context_audit_extractor`**: A placeholder tool for scanning chat context to extract and save undocumented Python functions. Implementation details are pending.
6.  **`user_decision_router`**: Implemented via `prompt_decision_menu` in `~/workspace/Computational/cli_tools/interaction.py`, providing structured interactive menus for user input.

---

## Rules, Cautions & Limitations

*   **Non-Destructive Generation:** Avoid overwriting working Python logic without careful reading.
*   **Enforce Interaction Rules:** Use `user_decision_router` for all user decisions, avoiding conversational filler.
*   **Documentation Clarity:** `gemini.md` is the long-term memory; ensure it is structured, readable, and accurate.
