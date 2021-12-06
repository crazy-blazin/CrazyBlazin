import subprocess
import time
#subprocess.run("cd web && start python server.py", shell=True, check=True)
time.sleep(1)
subprocess.run("start python main.py", shell=True, check=True)