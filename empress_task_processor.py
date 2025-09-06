import os
import subprocess
import requests
import time

TASK_FILE = os.path.expanduser("~/empress/tasks/queue.txt")
LOG_FILE = os.path.expanduser("~/logs/heartbeat.log")
MODULES_DIR = os.path.expanduser("~/empress/modules")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()}: {msg}\n")
    print(msg)

def fetch_and_execute(task):
    task = task.strip()
    if not task:
        return
    if task.startswith("http://") or task.startswith("https://"):
        log(f"🌐 Fetching script: {task}")
        filename = os.path.join(MODULES_DIR, "dynamic_task.py")
        try:
            r = requests.get(task)
            r.raise_for_status()
            with open(filename, "w") as f:
                f.write(r.text)
            subprocess.run(f"python3 {filename}", shell=True)
            log(f"✅ Completed fetched script: {task}")
        except Exception as e:
            log(f"❌ Failed fetching/executing {task}: {e}")
    else:
        log(f"💻 Executing shell command: {task}")
        try:
            subprocess.run(task, shell=True)
            log(f"✅ Completed: {task}")
        except Exception as e:
            log(f"❌ Failed: {task} — {e}")

def process_queue():
    if not os.path.isfile(TASK_FILE):
        open(TASK_FILE, "w").close()
    with open(TASK_FILE, "r") as f:
        tasks = [line.strip() for line in f if line.strip()]
    if not tasks:
        return
    task = tasks.pop(0)
    fetch_and_execute(task)
    with open(TASK_FILE, "w") as f:
        for t in tasks:
            f.write(t + "\n")
