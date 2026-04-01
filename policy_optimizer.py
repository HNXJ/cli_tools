# policy_optimizer.py
# Script to flush auto-saved.toml and inject generalized regex rules.
import toml
import os
import subprocess
import re

def generate_optimized_config():
    # Define the target path for the CLI config
    target_path = os.path.expanduser("~/.gemini/auto-saved.toml")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    config = {
        "policies": [
            {"tool": "run_shell_command", "args_match": ".*", "priority": 5.0},
            {"tool": "write_file", "args_match": ".*/(jbiophysics|workspace)/.*", "priority": 5.0},
            {"tool": "save_memory", "args_match": ".*\.gemini/GEMINI\.md", "priority": 5.0},
            {"tool": "activate_skill", "args_match": ".*", "priority": 5.0}
        ]
    }
    
    try:
        with open(target_path, "w") as f:
            toml.dump(config, f)
        print(f"Successfully updated {target_path} with generalized policies.")
    except Exception as e:
        print(f"Error writing to {target_path}: {e}")

if __name__ == "__main__":
    generate_optimized_config()
