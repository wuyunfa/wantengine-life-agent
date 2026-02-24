import subprocess
from dataclasses import dataclass


@dataclass
class TaskExecutor:
    enable_openclaw_call: bool = False
    openclaw_cli_path: str = r"C:\Users\wuyun\AppData\Roaming\npm\openclaw.cmd"

    def check_cli_availability(self) -> bool:
        if not self.enable_openclaw_call:
            return False
        try:
            result = subprocess.run(
                [self.openclaw_cli_path, "--version"],
                capture_output=True,
                text=True,
                timeout=8,
            )
            return result.returncode == 0
        except Exception:
            return False

    def execute(self, task: str) -> bool:
        if not self.enable_openclaw_call:
            print(f"[SIM] {task}")
            return True
        try:
            cmd = [
                self.openclaw_cli_path,
                "message",
                "send",
                "--channel",
                "telegram",
                "--to",
                "6250633698",
                "--message",
                task,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True
            print(f"[WARN] send failed: {result.stderr.strip()}")
            print(f"[SIM-FALLBACK] {task}")
            return False
        except Exception as e:
            print(f"[ERR] executor exception: {type(e).__name__}: {e}")
            print(f"[SIM-FALLBACK] {task}")
            return False
