def opengamma_communication_guide():
    """
    Returns the protocol for interacting with the 27B Reasoning Engine in the sandbox.
    """
    protocol = """
[OPENGAMMA COMMUNICATION PROTOCOL]

1. Role Definition: Address the model as 'OpenGamma Agent'.
2. Prompt Structure:
   - [TASK_TYPE]: Specify REFACTOR, TEST, or DEBUG.
   - [SANDBOX_ROOT]: Always include /Users/hamednejat/workspace/Warehouse/opengamma/
   - [RESOURCES]: Mention symlinked ./skills/ and ./gemini.md.
3. Code Delivery: Request responses in explicit ```python code blocks.
4. Tool Calling: Use <tool_call> tags for suggesting skills.
5. Confirmation: All local model suggestions require manual approval via [1] Execute.

Example Prompt:
'OpenGamma Agent, please REFACTOR the git_sync.py in ./skills/ to handle SSH timeouts. 
Operate only in the sandbox root. Provide the full code block.'
"""
    return protocol

# Schema for registration
schema = {
    "name": "opengamma_communication_guide",
    "description": "Returns the standardized protocol for interacting with the local OpenGamma agent.",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}
