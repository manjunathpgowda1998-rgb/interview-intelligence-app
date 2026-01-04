import subprocess
import webbrowser
import time
import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8501

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def start_streamlit():
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.headless=true",
            "--server.port=8501",
            "--server.runOnSave=false"
        ],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False
    )

if __name__ == "__main__":
    if not is_port_open(PORT):
        start_streamlit()
        time.sleep(4)

    webbrowser.open(f"http://localhost:{PORT}")
