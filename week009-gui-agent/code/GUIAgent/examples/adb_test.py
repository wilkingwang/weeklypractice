import os

def execute(cmd):
    adb_shell = "adb shell {cmd_str}"
    str = adb_shell.format(cmd_str=cmd)
    os.system(str)

if __name__ == "__main__":
    os.system("adb shell input keyevent 4")

    # execute("input keyevent 4")
