import os
import subprocess

"""
库：import os
使用命令：os.system('')
缺点：每次使用一次os.system('')命令都会弹出一个cmd窗口，然后执行完毕后关闭
"""
def execute_os_system(cmd):
    adb_shell = "adb shell {cmd_str}"
    str = adb_shell.format(cmd_str=cmd)
    os.system(str)

"""
库：import subprocess
使用命令：subprocess.run("",shell=True)
缺点：解决os库的问题，cmd窗口静默后台执行，不会弹出来烦你。shell=True表示命令将通过shell执行（默认shell=False）
"""
def execute_subprocess():
    subprocess.run("adb shell input keyevent 4",shell=True)


if __name__ == "__main__":
    # os.system("adb shell input keyevent 4")

    # execute_os_system("input keyevent 4")

    execute_subprocess()
