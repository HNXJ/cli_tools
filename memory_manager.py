import os
import re
import datetime
import shutil

GEMINI_PATH = "/Users/hamednejat/workspace/HNXJ/hnxj-gemini/GEMINI.md"
VMEMORY_PATH = "/Users/hamednejat/workspace/HNXJ/hnxj-gemini/VMEMORY.md"

def backup_gemini():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{GEMINI_PATH}.backup_{timestamp}"
    shutil.copy2(GEMINI_PATH, backup_path)
    return backup_path

def optimize_memory():
    if not os.path.exists(GEMINI_PATH):
        print(f"Error: {GEMINI_PATH} not found.")
        return

    backup_path = backup_gemini()
    print(f"Backup created: {backup_path}")

    # Hierarchical Schema Implementation
    infrastructure = """[00_INFRASTRUCTURE]
- Tailscale Office M3-Max: 100.69.184.42
- Hardware: Apple Silicon (128GB RAM / 100GB VRAM Ceiling)
- Environment: ~/miniconda3/envs/mllm/bin/python
- SSH: Multiplexing (ControlMaster) enabled.
- Network: Port 4474 (Main), Port 4475 (VLM), Port 8081 (Monitor).
"""

    core_directives = """[01_CORE_DIRECTIVES]
- Tone: Critical Electrical Engineer. Concise, direct (<40 words). No filler.
- Stack: Strictly MLX/mlx-lm for LLMs. Strictly JAX/Optax for Biophysics.
- Pathing: Use ONLY relative paths for code. EXCEPTION: MLX models MUST use absolute paths in ~/workspace/Warehouse/mlx_models/.
- Aesthetic: Madelane Golden Dark (#CFB87C Gold / #9400D3 Violet).
"""

    toolkit = """[02_ACTIVE_TOOLKIT]
- CLI_router: Tool orchestration and command interception.
- warehouse_manager: Global model storage standardization (sync_model_warehouse).
- local_toggle: LiteLLM proxy bridge for offline operation (/toggle-local).
- interaction: Strict enumerated decision menus (user_decision_router).
- memory_manager: Hierarchical schema enforcement (sync_and_prune_memory).
- eye: Local vision processing (qwen_subagent).
"""

    with open(GEMINI_PATH, 'r') as f:
        content = f.read()

    # Extract Active Objectives
    objectives_match = re.search(r'## Active Objectives \(Working Set\)(.*?)##', content, re.DOTALL)
    hot_bullets = []
    if objectives_match:
        raw_bullets = re.findall(r'- (.*?)\n', objectives_match.group(1))
        hot_bullets = [b.strip() for b in raw_bullets if b.strip()][:5]

    hot_context = "[03_HOT_CONTEXT]\n" + "\n".join([f"- {b}" for b in hot_bullets]) + "\n"

    # Move overflows to COLD_POINTERS
    upcoming_match = re.search(r'## Upcoming \(Pipeline\)(.*?)(\n\n|$)', content, re.DOTALL)
    cold_items = []
    if upcoming_match:
        raw_upcoming = re.findall(r'- (.*?)\n', upcoming_match.group(1))
        cold_items = [b.strip() for b in raw_upcoming]

    cold_pointers = "[04_COLD_POINTERS]\n" + "\n".join([f"- {b} (Ref: VMEMORY.md)" for b in cold_items]) + "\n"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_memory = f"# GEMINI CLI SYSTEM MEMORY (Hierarchical)\n{infrastructure}\n{core_directives}\n{toolkit}\n{hot_context}\n{cold_pointers}\n\n### 🛡️ Last Optimized: {timestamp}\n"

    try:
        with open(GEMINI_PATH, 'w') as f:
            f.write(new_memory)
        print("✅ GEMINI.md optimized and restructured into hierarchical schema.")
    except Exception as e:
        print(f"Error: Optimization failed, restoring backup. {e}")
        shutil.copy2(backup_path, GEMINI_PATH)

if __name__ == "__main__":
    optimize_memory()
