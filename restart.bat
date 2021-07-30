tasklist | find /i "python.exe" && taskkill /im "python.exe" /F || echo process "python.exe" not running
start python start_all.py