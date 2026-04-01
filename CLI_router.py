import os
import json
import re
import subprocess
import requests

def auto_register_skills(json_tools_array, tool_directory="/Users/hamednejat/workspace/Computational/cli_tools/active_skills/"):
    """
    Saves extracted tools as Python scripts and registers their JSON schemas.
    Silently overwrites existing versions to ensure the most recent 'meditated' version is active.
    """
    if not os.path.exists(tool_directory):
        os.makedirs(tool_directory)

    for tool in json_tools_array:
        name = tool.get("tool_name")
        code = tool.get("python_code")
        desc = tool.get("description")

        if not name or not code:
            continue

        # Save the Python implementation
        script_path = os.path.join(tool_directory, f"{name}.py")
        # Wrapped in a broad try/except to prevent import hallucinations from crashing the loop
        wrapped_code = f"""
try:
{code}
except ImportError as e:
    print(f"Skill '{name}' failed due to missing dependency: {{e}}")
except Exception as e:
    print(f"Skill '{name}' failed during execution: {{e}}")
"""
        with open(script_path, "w") as f:
            f.write(wrapped_code)

        # Save the schema (placeholder for MCP registration)
        schema_path = os.path.join(tool_directory, f"{name}.json")
        schema = {
            "name": name,
            "description": desc,
            "input_schema": {
                "type": "object",
                "properties": {
                    "args": {"type": "object"}
                }
            }
        }
        with open(schema_path, "w") as f:
            json.dump(schema, f, indent=2)
            
        print(f"Registered tool: {name} to {tool_directory}")

def execute_meditation(current_messages_array, gemini_client):
    """
    Halts conversational processing, scans the context for Python logic, 
    extracts it as MCP-compatible tools, and registers them.
    """
    print("Meditating... Scanning history for undocumented skills to auto-register.")
    
    audit_prompt = """
    SYSTEM DIRECTIVE: CONTEXT AUDIT & TOOL EXTRACTION. 
    Review all prior messages. Identify any Python functions, JAX logic, or computational scripts we discussed. 
    Extract them and format them as MCP-compatible skills. 
    Output ONLY valid JSON in this format: 
    [{"tool_name": "name", "description": "desc", "python_code": "code"}]
    """
    
    audit_context = current_messages_array.copy()
    audit_context.append({"role": "user", "content": audit_prompt})
    
    try:
        # Note: This requires the gemini_client to be configured and authenticated
        response = gemini_client.generate_content(audit_context)
        # Use simple regex/parsing as per GAMMA directive
        clean_json_string = re.sub(r'```json|```', '', response.text).strip()
        tools = json.loads(clean_json_string)
        
        auto_register_skills(tools)
        return f"Meditation successful: Registered {len(tools)} tools."
        
    except Exception as e:
        print(f"Meditation failed: {e}")
        return f"Meditation failed: {e}"

# Placeholder for the main loop interceptor
def handle_input(user_input, state):
    if user_input.strip() == "/meditate":
        # Extract messages from state
        messages = state.get("messages", [])
        client = state.get("client")
        return execute_meditation(messages, client)
    return None
