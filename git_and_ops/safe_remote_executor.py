import os
import subprocess
import tempfile

def execute_remote_script(target_ip: str, user: str, script_content: str, remote_dest_path: str):
    """
    Safely writes a script locally, transfers it via SCP, and executes it via SSH.
    Prevents ReDoS crashes in CLI auto-saved policies.
    """
    try:
        # 1. Write the complex logic to a safe local temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
            temp_file.write(script_content)
            local_temp_path = temp_file.name

        print(f"[INFO] Script written securely to local temp file: {local_temp_path}")

        # 2. Transfer via SCP (Avoids bash escaping nightmare)
        scp_cmd = ["scp", "-o", "ControlMaster=auto", "-o", "ControlPersist=600", 
                   local_temp_path, f"{user}@{target_ip}:{remote_dest_path}"]
        subprocess.run(scp_cmd, check=True)
        print(f"[INFO] Script transferred to {target_ip}:{remote_dest_path}")

        # 3. Execute via simple SSH (Short command, safe for auto-saved.toml)
        ssh_cmd = ["ssh", "-o", "ControlMaster=auto", "-o", "ControlPersist=600", 
                   f"{user}@{target_ip}", f"python3 {remote_dest_path}"]
        
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        
        # 4. Cleanup local temp file
        os.remove(local_temp_path)
        
        return f"Execution Successful:\n{result.stdout}"

    except subprocess.CalledProcessError as e:
        return f"[ERROR] Remote Execution Failed:\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}"
    except Exception as e:
        return f"[ERROR] Framework Exception: {str(e)}"
