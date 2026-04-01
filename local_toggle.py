import os
import subprocess
import sys
import signal
import time
from interaction import prompt_decision_menu

PROXY_CONFIG_PATH = os.path.expanduser("~/workspace/misc/Warehouse/Repositories/mllm/proxy/litellm_config.yaml")
LITELLM_PORT = 4000
LM_STUDIO_PORT = 1234 # or 4474 per previous mandates

def get_pid_on_port(port):
    """Returns the PID of the process listening on the specified port."""
    try:
        # -t: Terse, -i: internet
        output = subprocess.check_output(["lsof", "-t", f"-i:{port}"]).decode().strip()
        return output.split('\n') if output else []
    except subprocess.CalledProcessError:
        return []

def kill_process_on_port(port):
    """Kills any processes listening on the specified port."""
    pids = get_pid_on_port(port)
    if not pids:
        return True
    
    summary = f"Port {port} is occupied by PIDs: {', '.join(pids)}. Kill them?"
    options = ["Yes, kill occupying processes.", "No, abort operation.", "Other (Please specify)"]
    choice = prompt_decision_menu(summary, options)
    
    if "Yes" in choice:
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
                print(f"Killed PID {pid} on port {port}.")
            except Exception as e:
                print(f"Failed to kill PID {pid}: {e}")
        time.sleep(1) # Wait for port release
        return True
    return False

def toggle_local_mode():
    """Toggles the CLI between Cloud Mode and Local Mode (LiteLLM Proxy)."""
    summary = "Select CLI Operating Mode:"
    options = [
        "Cloud (Gemini API)",
        "Local (LiteLLM + LM Studio)",
        "Other (Please specify)"
    ]
    choice = prompt_decision_menu(summary, options)

    if "Cloud" in choice:
        # Logic to kill the proxy if running
        pids = get_pid_on_port(LITELLM_PORT)
        if pids:
            print(f"Stopping LiteLLM proxy on port {LITELLM_PORT}...")
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
        
        # In a real environment, we'd unset env vars here.
        # For the script, we print the instructions.
        print("\n[MODE] Cloud Mode (Gemini API) active.")
        print("Note: Unset GOOGLE_GEMINI_BASE_URL and GEMINI_API_KEY if they were manually set.")
        return "CLOUD"

    elif "Local" in choice:
        print("\n⚠️ WARNING: Local Mode Active.")
        print("- Tool-calling (MCP) degradation: Local models < 30B have high failure rates.")
        print("- Mathematical Hallucinations: Verify all local code outputs.")
        
        # Port management
        if not kill_process_on_port(LITELLM_PORT):
            return "ABORTED"
        
        # Start LiteLLM as a background subprocess
        try:
            cmd = f"litellm --config {PROXY_CONFIG_PATH} --port {LITELLM_PORT}"
            print(f"Starting LiteLLM proxy: {cmd}")
            subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            
            # Allow time for proxy to initialize
            time.sleep(2)
            
            # Check if it's running
            if get_pid_on_port(LITELLM_PORT):
                print(f"✅ LiteLLM proxy started on port {LITELLM_PORT}.")
                
                # Set environment variables (for the current process and instructions for the user)
                os.environ["GOOGLE_GEMINI_BASE_URL"] = f"http://localhost:{LITELLM_PORT}"
                os.environ["GEMINI_API_KEY"] = "dummy-offline-key"
                
                print(f"\n[MODE] Local Mode (LiteLLM) active.")
                print(f"GOOGLE_GEMINI_BASE_URL: http://localhost:{LITELLM_PORT}")
                return "LOCAL"
            else:
                print("❌ Failed to start LiteLLM proxy. Check your installation.")
                return "FAILED"
                
        except Exception as e:
            print(f"Error starting LiteLLM: {e}")
            return "ERROR"
    
    return "NONE"

if __name__ == "__main__":
    toggle_local_mode()
