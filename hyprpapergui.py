import json
import hyprctlwrp as hyprctl
from pathlib import Path

import flet as ft

from fletimgbtn import ImageButton
from icon_creater import (
    create_cached_image_mem,
    get_files_in_directory,
    image_to_base64,
)


def load_config(param: str):
    with open("config.json") as config_json:
        config = json.load(config_json)
        return config[param]


def set_wallpaper(e):
    image_path = str(e.control.image_path.absolute())
    hyprctl.new_hyprpaprc_config(image_path, load_config("hyprpaper_config_path"))


def main(page: ft.Page):
    wallpaper_directory = load_config("wallpaper_directory")
    page.title = "HYPRGUIPAPER"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    wallpaper_paths = get_files_in_directory(Path(wallpaper_directory))

    image_buttons = [
        ImageButton(
            image_path=load_config("default_wallpaper"), click_handler=set_wallpaper
        )
        for _ in range(0, len(wallpaper_paths))
    ]
    images = [
        ft.Image(src=load_config("default_wallpaper"))
        for _ in range(0, len(wallpaper_paths))
    ]
    old_controls = [ft.TextButton(content=image) for image in images]
    image_row = ft.Row(
        controls=image_buttons, wrap=True, scroll=ft.ScrollMode.AUTO, expand=True
    )

    async def feel_image(image: ImageButton, cached_wallpaper: Path):
        cached_image = await create_cached_image_mem(cached_wallpaper)
        image.change_image(
            image_to_base64(cached_image), path_to_image=cached_wallpaper
        )
        print(f"end of work : {cached_wallpaper}")
        if image.page != None:
            image.page.update()

    async def create_cached_images():
        create_images = [
            feel_image(image_buttons[x], image_path)
            for x, image_path in enumerate(wallpaper_paths)
        ]

        for coroutine in create_images:
            await coroutine
            page.update()
        # await asyncio.gather(*create_images)

    page.add(image_row)

    page.run_task(create_cached_images)


ft.app(target=main)
