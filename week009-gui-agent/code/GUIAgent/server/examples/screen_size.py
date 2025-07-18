import subprocess

def get_screen_size():
    output = subprocess.check_output(['adb', 'shell', 'wm', 'size']).decode('utf-8')
    size_str = output.strip().split(' ')[-1]
    width, heigth = size_str.split('x')

    return width, heigth

print(get_screen_size())