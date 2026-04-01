import os
import shutil
import sys

# Setup interaction for the CLI
try:
    from interaction import prompt_decision_menu
except ImportError:
    # fallback if run directly
    def prompt_decision_menu(summary, options):
        print(f"WARNING: {summary}")
        for i, opt in enumerate(options):
            print(f"[{i+1}] {opt}")
        choice = input("Select an option: ")
        try:
            return options[int(choice)-1]
        except:
            return "Cancel"

def sync_model_warehouse():
    warehouse_root = "/Users/hamednejat/workspace/Warehouse/mlx_models"
    lm_studio_format_dir = os.path.join(warehouse_root, "lm_studio_format")
    hf_cache_dir = os.path.join(warehouse_root, "hf_cache")

    # Initialization
    os.makedirs(lm_studio_format_dir, exist_ok=True)
    os.makedirs(hf_cache_dir, exist_ok=True)

    lmstudio_default = os.path.expanduser("~/.lmstudio/models")

    # Check if ~/.lmstudio/models exists and is a real directory
    if os.path.exists(lmstudio_default) and not os.path.islink(lmstudio_default):
        print(f"Found real directory at {lmstudio_default}. Preparing migration...")
        
        # Guardrail prompt
        choice = prompt_decision_menu(
            summary=f"CRITICAL: About to move models from {lmstudio_default} to {lm_studio_format_dir}. This could be hundreds of GBs. Do you have enough disk space and approve this migration?",
            options=["Yes, proceed with migration.", "No, cancel."]
        )
        
        if choice != "Yes, proceed with migration.":
            print("Migration cancelled by user.")
            sys.exit(0)

        # Move contents
        for item in os.listdir(lmstudio_default):
            s = os.path.join(lmstudio_default, item)
            d = os.path.join(lm_studio_format_dir, item)
            print(f"Moving {s} to {d}...")
            shutil.move(s, d)
        
        # Delete empty original folder
        try:
            os.rmdir(lmstudio_default)
        except OSError as e:
            print(f"Warning: Could not remove {lmstudio_default}. It may not be empty. Error: {e}")

    # LM Studio Symlink Logic
    if not os.path.exists(lmstudio_default) and not os.path.islink(lmstudio_default):
        print(f"Creating symlink from {lm_studio_format_dir} to {lmstudio_default}...")
        try:
            os.symlink(lm_studio_format_dir, lmstudio_default)
        except OSError as e:
            print(f"Symlink failed: {e}")
            print("Please ensure your terminal has 'Full Disk Access' in macOS System Settings > Privacy & Security.")
            sys.exit(1)
    else:
        if os.path.islink(lmstudio_default):
            target = os.readlink(lmstudio_default)
            if target == lm_studio_format_dir:
                print("Symlink is already correctly configured.")
            else:
                print(f"Warning: Symlink points to {target}, expected {lm_studio_format_dir}.")
        else:
            print(f"Warning: {lmstudio_default} exists but is not a symlink and was not migrated.")

    # Python Environment Overrides
    os.environ["HF_HOME"] = hf_cache_dir
    print(f"Environment variable HF_HOME set to: {os.environ['HF_HOME']}")
    print("✅ Model warehouse synchronization complete.")

if __name__ == "__main__":
    sync_model_warehouse()
