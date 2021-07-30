import subprocess
import time
#subprocess.run("cd web && start python server.py", shell=True, check=True)
time.sleep(20)
subprocess.run("echo running!", shell=True, check=True)
subprocess.run("start python main.py", shell=True, check=True)
# subprocess.run("cd web && start python server.py", shell=True, check=True)