import time, os

def check(path): return os.path.exists(os.path.expanduser(path))
def run(cmd): os.system(cmd)

while True:
    if not check("~/empress/twin_profile.json"):
        run("~/empress/fallback_injector.sh")
    if os.system("pgrep -f voice_trigger.sh") != 0:
        run("~/empress/voice_trigger.sh &")
    time.sleep(10)
