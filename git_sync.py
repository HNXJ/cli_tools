import os
import subprocess
import datetime
import sys
from interaction import prompt_decision_menu

TARGET_REPOS = [
    os.path.expanduser("~/workspace/HNXJ/hnxj-gemini"),
    os.path.expanduser("~/workspace/Warehouse/Repositories/mllm"),
    os.path.expanduser("~/workspace/Computational/eye")
]

GEMINI_MD_PATH = os.path.expanduser("~/workspace/Computational/cli_tools/gemini.md")

def run_command(cmd, cwd):
    """Runs a shell command and returns the result."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return result

def get_latest_hash(repo_path):
    """Returns the latest commit hash for the repo."""
    result = run_command("git rev-parse --short HEAD", repo_path)
    return result.stdout.strip() if result.returncode == 0 else "Unknown"

def git_sync_manager():
    """Systematically syncs targeted repositories."""
    print("🚀 Starting Global Repository Synchronization...")
    
    sync_report = []

    for repo_path in TARGET_REPOS:
        if not os.path.exists(repo_path):
            summary = f"Missing Repository: {repo_path} not found."
            options = ["Clone (placeholder)", "Skip this repository"]
            choice = prompt_decision_menu(summary, options)
            if "Skip" in choice:
                print(f"Skipping {repo_path}...")
                continue
            else:
                print(f"Cloning logic not implemented. Skipping {repo_path}...")
                continue

        print(f"\n🔄 Syncing: {repo_path}")
        
        # 1. Fetch
        run_command("git fetch origin", repo_path)
        
        # 2. Check for uncommitted changes
        status = run_command("git status --porcelain", repo_path).stdout.strip()
        if status:
            summary = f"Uncommitted changes found in {os.path.basename(repo_path)}."
            options = [
                f"Commit with message 'chore: Auto-sync uncommitted changes'",
                "Stash changes",
                "Abort sync for this repository"
            ]
            choice = prompt_decision_menu(summary, options)
            
            if "Commit" in choice:
                run_command("git add .", repo_path)
                run_command("git commit -m 'chore: Auto-sync uncommitted changes'", repo_path)
            elif "Stash" in choice:
                run_command("git stash", repo_path)
            else:
                print(f"Aborting sync for {repo_path}.")
                continue

        # 3. Pull
        branch_res = run_command("git rev-parse --abbrev-ref HEAD", repo_path)
        active_branch = branch_res.stdout.strip() if branch_res.returncode == 0 else "main"
        
        pull_res = run_command(f"git pull origin {active_branch}", repo_path)
        if "CONFLICT" in pull_res.stderr or pull_res.returncode != 0:
            summary = f"Merge conflict or error in {os.path.basename(repo_path)} during pull."
            print(f"Error details: {pull_res.stderr}")
            options = ["Abort sync", "Manual resolution required (Skip push)"]
            choice = prompt_decision_menu(summary, options)
            if "Abort" in choice:
                sys.exit(1)
            else:
                print(f"Skipping push for {repo_path} due to conflicts.")
                continue

        # 4. Push
        push_res = run_command(f"git push origin {active_branch}", repo_path)
        if push_res.returncode != 0:
            summary = f"Push failed for {os.path.basename(repo_path)}."
            print(f"Error details: {push_res.stderr}")
            options = ["Retry push", "Ignore and continue"]
            choice = prompt_decision_menu(summary, options)
            if "Retry" in choice:
                run_command(f"git push origin {active_branch}", repo_path)

        sync_report.append(f"{os.path.basename(repo_path)}: {get_latest_hash(repo_path)}")

    print("\n✅ Global Synchronization Complete.")
    return sync_report

def update_gemini_md_ledger(sync_report):
    """Updates the central gemini.md with sync status."""
    if not os.path.exists(GEMINI_MD_PATH):
        print(f"Warning: {GEMINI_MD_PATH} not found.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ledger_entry = f"\n\n### 🛡️ Last Synchronized: {timestamp}\n"
    for report in sync_report:
        ledger_entry += f"- {report}\n"

    with open(GEMINI_MD_PATH, "a") as f:
        f.write(ledger_entry)
    
    print(f"Ledger updated in {GEMINI_MD_PATH}")

if __name__ == "__main__":
    report = git_sync_manager()
    update_gemini_md_ledger(report)
