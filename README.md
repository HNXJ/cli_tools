# CLI Tools Interaction Utility

This module provides a standardized way for the Gemini CLI to interact with the user for decision-making and error resolution. It ensures that user prompts are presented in a clear, enumerated menu format, guaranteeing deterministic responses and graceful handling of custom inputs.

## User Decision Router Protocol

This protocol mandates the use of the `prompt_decision_menu` function whenever the CLI requires user input for selecting an action, resolving an error, or providing a preference.

### Functions:

*   **`prompt_decision_menu(summary: str, options: list[str]) -> str`**:
    *   Displays a summary message (often an error) and a numbered list of predefined options.
    *   Automatically appends an "Other (Please specify)" option.
    *   Captures user input and returns the selected option or custom text.

## Usage Example:

When an error occurs, instead of a free-form question, the CLI should call this utility:

```python
# Assuming an error occurred that requires user input for resolution
error_summary = "Git repository 'eye' already exists on GitHub."
resolution_options = [
    "Push current local branch to the existing HNXJ/eye remote.",
    "Rename local repository and attempt to create a new remote.",
    "Abort Git setup and continue local execution."
]

# Call the utility function
user_choice = prompt_decision_menu(error_summary, resolution_options)

# The agent then processes the user_choice
print(f"\nAgent received user choice: {user_choice}")
```

## Rules:

*   **Zero Conversational Filler:** Always pass precise option strings directly to `prompt_decision_menu`. Avoid conversational preambles.
*   **State Preservation:** Ensure context is maintained when execution pauses for user input.
*   **Menu Clarity:** Options must be actionable and specific.

