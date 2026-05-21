import subprocess
import os

FBINK_BIN = "/mnt/us/fbink/bin/fbink"
FBINK_LIB = "/mnt/us/fbink/lib"

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = FBINK_LIB

def run(args):
    cmd = [FBINK_BIN] + args
    subprocess.run(cmd, env=env)

def clear():
    run(["-c"])

def print_text(text, x=0, y=0, centered=False):
    args = []
    if centered:
        args += ["-m"]
    else:
        args += [f"-x {x}", f"-y {y}"]
    args += [text]
    run(args)

def refresh():
    run(["-f", "-m", ""])