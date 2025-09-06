import os, subprocess, time, requests, random, sys

# === Paths ===
TASK_FILE   = os.path.expanduser("~/empress/tasks/queue.txt")
LOG_FILE    = os.path.expanduser("~/logs/heartbeat.log")
MODULES_DIR = os.path.expanduser("~/empress/modules")
CORE_FILE   = os.path.expanduser("~/empress/empress_core.py")

os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(MODULES_DIR, exist_ok=True)

# === Logging ===
def log(msg):
    timestamp = time.ctime()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp}: {msg}\n")
    print(f"{timestamp}: {msg}")

# === Task Execution ===
def fetch_and_execute(url):
    try:
        filename = os.path.join(MODULES_DIR, "dynamic_task.py")
        r = requests.get(url)
        r.raise_for_status()
        with open(filename, "w") as f:
            f.write(r.text)
        subprocess.run(f"python3 {filename}", shell=True)
        log(f"✅ Completed fetched script: {url}")
    except Exception as e:
        log(f"❌ Failed fetching/executing {url}: {e}")

def execute_command(task):
    try:
        subprocess.run(task, shell=True)
        log(f"✅ Completed shell command: {task}")
    except Exception as e:
        log(f"❌ Failed shell command: {task} — {e}")

# === Interpret Tasks ===
def interpret_task(task):
    task = task.strip()
    if not task:
        return
    if task.startswith("http://") or task.startswith("https://"):
        fetch_and_execute(task)
    else:
        execute_command(task)

# === Self-Upgrading ===
def self_upgrade():
    upgrade_url = "https://raw.githubusercontent.com/72X72/EMPRESS/main/empress_core.py"
    try:
        r = requests.get(upgrade_url)
        r.raise_for_status()
        new_code = r.text
        with open(CORE_FILE, "r") as f:
            current = f.read()
        if new_code != current:
            with open(CORE_FILE, "w") as f:
                f.write(new_code)
            log("🔄 Core upgraded successfully, restarting...")
            os.execv(sys.executable, ["python3", CORE_FILE])
    except Exception as e:
        log(f"⚠️ Self-upgrade failed: {e}")

# === Self-Task Generation ===
def generate_tasks():
    possible_tasks = [
        'echo "Auto-check at $(date)"',
        'ls -la ~/empress/tasks',
        'df -h',
        'echo "System running smoothly"',
    ]
    if random.random() < 0.3:  # 30% chance each cycle
        task = random.choice(possible_tasks)
        with open(TASK_FILE, "a") as f:
            f.write(task + "\n")
        log(f"🧠 Generated new task: {task}")

# === Process Queue ===
def process_queue():
    if not os.path.exists(TASK_FILE):
        open(TASK_FILE, "w").close()
    with open(TASK_FILE, "r") as f:
        tasks = [line.strip() for line in f if line.strip()]
    for task in tasks:
        interpret_task(task)
    open(TASK_FILE, "w").close()  # Clear queue after execution

# -------------------------------------------------------------------
# 🚧 MISSING LAYERS — Stubbed for future expansion
# -------------------------------------------------------------------

def intelligence_layer():
    """
    🔴 Currently Missing:
    - No reasoning or adaptive logic
    - Only runs predefined or fetched tasks
    
    ✅ Stubbed for future:
    Could connect to a language model, decision-tree, or rule engine.
    """
    pass

def persistence_layer():
    """
    🔴 Currently Missing:
    - No autorun if Termux/device restarts
    
    ✅ Stubbed for future:
    Add 'termux-boot' integration or crontab to relaunch automatically.
    """
    pass

def sandbox_layer():
    """
    🔴 Currently Missing:
    - No isolation when running fetched scripts (can be dangerous)
    
    ✅ Stubbed for future:
    Use Docker, venv, or restricted subprocess execution.
    """
    pass

def decision_making_layer():
    """
    🔴 Currently Missing:
    - No reasoning on when/why to evolve
    - Random chance drives behavior
    
    ✅ Stubbed for future:
    Add scoring, conditions, or goals to guide upgrades/tasks.
    """
    pass

# === Autonomous Core Loop ===
if __name__ == "__main__":
    log("🚀 EMPRESS Fully Autonomous Core Online")
    while True:
        process_queue()
        generate_tasks()
        self_upgrade()
        intelligence_layer()
        persistence_layer()
        sandbox_layer()
        decision_making_layer()
        time.sleep(5)
