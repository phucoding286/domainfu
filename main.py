import os
import sys

if sys.platform.startswith("win"):
    os.system("python ./domainfu_new_ui/main.py")
else:
    os.system("python3 ./domainfu_new_ui/main.py")