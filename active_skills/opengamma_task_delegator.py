import os
import json
from infrastructure.mlx_offline_router import call_native_mlx_fallback
from memory_and_logic.context_compressor import compress_cli_context
from infrastructure.opengamma_bridge import sync_opengamma_sandbox

def opengamma_task_delegator(task_objective: str):
    """
    Orchestrates the full delegation pipeline to the OpenGamma sandbox.
    1. Syncs sandbox state.
    2. Compresses workspace context.
    3. Triggers the 27B MLX engine with sandbox constraints.
    """
    # 1. Sync Sandbox
    sync_opengamma_sandbox()
    
    # 2. Get Context
    system_context = compress_cli_context()
    
    # 3. Format Sandbox Prompt
    sandbox_prompt = f"""
[SYSTEM DIRECTIVE: OPENGAMMA DELEGATION]
You are operating within a restricted SANDBOX: /Users/hamednejat/workspace/Warehouse/opengamma/
You have access to symlinked skills in ./skills/ and context in ./gemini.md.

TASK OBJECTIVE:
{task_objective}

CONSTRAINTS:
1. ONLY modify files within /Users/hamednejat/workspace/Warehouse/opengamma/
2. Use relative paths for all operations.
3. If you need to run a tool, provide the exact JSON payload.
4. Always provide a brief rationale before code blocks.
"""

    print(f"\n[DELEGATION] Sending task to OpenGamma 27B Engine...")
    response = call_native_mlx_fallback(sandbox_prompt, system_context)
    
    return response

# Schema for registration
schema = {
    "name": "opengamma_task_delegator",
    "description": "Delegates a complex task to the 27B local model within the OpenGamma sandbox environment.",
    "input_schema": {
        "type": "object",
        "properties": {
            "task_objective": {"type": "string", "description": "Detailed description of the task to be performed in the sandbox."}
        },
        "required": ["task_objective"]
    }
}

if __name__ == "__main__":
    # Example usage
    # print(opengamma_task_delegator("Refactor the memory_manager to use a more efficient regex for context extraction."))
    pass
