import subprocess
import time
#subprocess.run("cd web && start python server.py", shell=True, check=True)
time.sleep(10)
subprocess.run("start python main.py", shell=True, check=True)