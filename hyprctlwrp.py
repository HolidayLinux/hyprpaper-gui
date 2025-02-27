import subprocess


def get_monitor():
    result = subprocess.run(
        ["hyprctl", "monitors"], stdout=subprocess.PIPE
    ).stdout.splitlines()
    monitorLine = result[0].decode("UTF-8")
    monitor = monitorLine.split(" ")[1]
    return monitor


def new_hyprpaprc_config(image_path: str):
    subprocess.run(["hyprctl", "hyprpaper", "preload", image_path])
    subprocess.run(
        ["hyprctl", "hyprpaper", "wallpaper", f"{get_monitor()},{image_path}"]
    )
