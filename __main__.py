import base64
from io import BytesIO
from PIL import Image
import flet as ft
from icon_creater import IconCreater


def image_to_base64(img: Image.Image):
    im_file = BytesIO()
    img.save(im_file, format='PNG')
    return base64.b64encode(im_file.getvalue()).decode('ASCII')


async def main(page: ft.Page):
    page.title = "HYPRGUIPAPER"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    images = await IconCreater('c:\\Users\\Holiday\\.dotfiles\\wallpapers\\Wallpaper-Bank').start()

    controls = [ft.Image(src_base64=image_to_base64(image))
                for image in images]

    page.add(ft.Row(controls=controls, wrap=True, scroll=ft.ScrollMode.AUTO, expand=True
                    ))


ft.app(target=main)
