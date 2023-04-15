#!/usr/bin/env python3
import subprocess
import time
import requests

cmd = subprocess.Popen(["dbus-monitor \"type='signal',interface="
                        "'org.gnome.ScreenSaver'\""], shell=True,
                       stdout=subprocess.PIPE)
                       
response = requests.get("https://sf8do.mooo.com/habitat/p52/active")

while True:
    out = cmd.stdout.readline()
    if not out:
        break
    line = str(out.rstrip())
    print("line", line)

    if "ActiveChange" in line and "org.gnome.ScreenSaver":
        out = cmd.stdout.readline()
        if not out:
            break
        line = str(out.rstrip())
        print("line", line)
        
        if "boolean true" in line:
          response = requests.get("https://sf8do.mooo.com/habitat/p52/inactive")
          print("p52 inactive", response.status_code)
        if "boolean false" in line:
          response = requests.get("https://sf8do.mooo.com/habitat/p52/active")
          print("p52 active", response.status_code)