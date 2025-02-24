import json
import flet as ft
from pathlib import Path
from icon_creater import get_files_in_directory
from imagewrapper import ImageWrapper

def load_config():
    with open('config.json') as config_json:
        config = json.load(config_json)
        return config['wallpaper_directory']

        
        
def main(page: ft.Page):
    wallpaper_directory = load_config() 
    page.title = "HYPRGUIPAPER"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    new_controls = [ImageWrapper(image,  page.run_task)
                    for image in get_files_in_directory(Path(wallpaper_directory))]

    page.add(ft.Row(controls=new_controls, wrap=True,
                    scroll=ft.ScrollMode.AUTO, expand=True))

ft.app(target=main)
