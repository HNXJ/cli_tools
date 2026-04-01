import os
import json
import re

def compress_cli_context():
    """
    Reads GEMINI.md for hot context and scans the active_skills directory 
    to generate a compressed XML-tagged system prompt for local models.
    """
    workspace_root = os.path.expanduser("~/workspace")
    gemini_path = os.path.join(workspace_root, "GEMINI.md")
    skills_dir = os.path.join(workspace_root, "Computational/cli_tools/active_skills")
    
    # 1. Extract Hot Context from GEMINI.md
    hot_context = "No active objectives found."
    if os.path.exists(gemini_path):
        try:
            with open(gemini_path, "r") as f:
                content = f.read()
                # Look for '## Active Objectives (Working Set)' section
                match = re.search(r"## Active Objectives \(Working Set\)(.*?)##", content, re.DOTALL)
                if match:
                    hot_context = match.group(1).strip()
        except Exception as e:
            hot_context = f"Error reading GEMINI.md: {e}"

    # 2. Scan for Active Tools
    tools_xml = ""
    if os.path.exists(skills_dir):
        try:
            for filename in os.listdir(skills_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(skills_dir, filename), "r") as f:
                        schema = json.load(f)
                        name = schema.get("name", "Unknown")
                        desc = schema.get("description", "No description provided.")
                        tools_xml += f"<tool>\n  <name>{name}</name>\n  <description>{desc}</description>\n</tool>\n"
        except Exception as e:
            tools_xml = f"<!-- Error reading tools: {e} -->"

    # 3. Assemble the Final Compressed Prompt
    system_prompt = f"""You are the Gemini CLI operating in OFFLINE fallback mode. 
Current Active Project Context:
{hot_context}

Available Tools:
{tools_xml}

WARNING: Running on 27B Local Model. Safe for code refactoring and CLI ops. 
DO NOT trust for biophysical math, novel differential equations, or extracting quantitative data from papers. 
Verify all mathematical outputs.
"""
    return system_prompt

if __name__ == "__main__":
    print(compress_cli_context())
