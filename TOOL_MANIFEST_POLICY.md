# Tool Manifest Policy

**Status:** v1.0
**Plane:** Control / Inventory
**Scope:** Policy governing all tools created, updated, or hosted in the `gamma-tools` repository.

## 1. Purpose
This policy enforces the Tool Manifest boundary rules defined by the Gamma Labyrinth protocol. `gamma-tools` is an agent-only toolbox designed to host reusable utilities, adapters, and validators. This policy ensures tools remain strictly decoupled from Truth-plane execution state.

## 2. Manifest Requirements
Every tool introduced to `gamma-tools` MUST declare the following in its file docstring or accompanying README:

*   **Purpose:** A concise description of the tool's goal.
*   **Inputs:** Expected parameters, files, or state.
*   **Outputs:** Expected returns, logs, or generated artifacts.
*   **Dependencies:** Required libraries or other tools.
*   **Safety Boundary:** Explicitly describe the plane the tool operates within (e.g., Execution, Observation, Analysis) and confirm no Truth-plane boundary violations.

## 3. Hash & Manifest Behavior
*   Any tool that produces scientific evidence or intermediate artifacts MUST generate a cryptographic hash (e.g., SHA-256) of its outputs.
*   The tool MUST output a JSON artifact manifest containing paths to generated files, their hashes, and the runtime version.
*   Tools MUST NOT overwrite existing artifacts without appending a new identifier or incrementing a versioned namespace, preserving provenance.

## 4. No-Truth-Promotion Rule
*   **Absolute Restriction:** No tool in `gamma-tools` may hardcode scientific state, assert biological facts, or push direct updates to Truth-plane state (the `gamma` receipt spine).
*   Tools may only act as adapters or validators. Their output is strictly a `proposal_value`, `simulation_result`, or `tool_improvement`.
*   A candidate only becomes accepted state via the formal `gamma` runtime receipt path.
