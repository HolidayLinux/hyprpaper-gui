import asyncio
import json
from pathlib import Path

import flet as ft
from PIL.Image import Image

from icon_creater import (
    create_cached_image_mem,
    get_files_in_directory,
    image_to_base64,
)
from imagewrapper import ImageWrapper


def load_config():
    with open("config.json") as config_json:
        config = json.load(config_json)
        return config["wallpaper_directory"]


def main(page: ft.Page):
    wallpaper_directory = load_config()
    page.title = "HYPRGUIPAPER"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    wallpaper_paths = get_files_in_directory(Path(wallpaper_directory))
    old_controls = [
        ft.Image(src="./assets/images/loading2.gif")
        for x in range(0, len(wallpaper_paths))
    ]

    page.add(
        ft.Row(controls=old_controls, wrap=True, scroll=ft.ScrollMode.AUTO, expand=True)
    )

    async def feel_image(image: ft.Image, cached_wallpaper: Path):
        cached_image = await create_cached_image_mem(cached_wallpaper)
        image.src_base64 = image_to_base64(cached_image)
        page.update()

    async def create_cached_images():
        create_images = [
            asyncio.create_task(feel_image(old_controls[x], image_path))
            for x, image_path in enumerate(wallpaper_paths)
        ]
        return asyncio.gather(*create_images)

    page.run_task(create_cached_images)


ft.app(target=main)
