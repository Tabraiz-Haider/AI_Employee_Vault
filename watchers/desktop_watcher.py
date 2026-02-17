import os
import time

# Jis folder ko monitor karna hai (Desktop)
path_to_watch = os.path.expanduser("~/Desktop")
# Obsidian file jahan update jayegi
log_file = "Desktop_Log.md"

print(f"Monitoring: {path_to_watch}")

before = dict([(f, None) for f in os.listdir(path_to_watch)])
while True:
    time.sleep(5)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    if added:
        with open(log_file, "a") as f:
            for file in added:
                f.write(f"\n- New file detected: {file} at {time.ctime()}")
        print(f"Added: {', '.join(added)}")
    before = after