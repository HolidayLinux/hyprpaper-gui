import subprocess


def get_monitor():
    result = subprocess.run(
        ["hyprctl", "monitors"], stdout=subprocess.PIPE
    ).stdout.splitlines()
    monitorLine = result[0].decode("UTF-8")
    monitor = monitorLine.split(" ")[1]
    return monitor


def new_hyprpaprc_config(image_path: str, hyrppaper_config_path: str):
    wallpaper = f"{get_monitor()},{image_path}"
    subprocess.run(["hyprctl", "hyprpaper", f"preload {image_path}"])
    subprocess.run(["hyprctl", "hyprpaper", f"wallpaper {wallpaper}"])
    with open(hyrppaper_config_path, "r+") as hyprpaper_config:
        hyprpaper_config.truncate()
        hyprpaper_config.seek(0)
        hyprpaper_config.writelines(
            [f"preload = {image_path}", "\n", f"wallpaper = {wallpaper}"]
        )
