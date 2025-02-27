import flet as ft
from pathlib import Path
from flet.core.text_button import OptionalControlEventCallable
from icon_creater import load_image, image_to_base64


class ImageButton(ft.TextButton):
    def __init__(
        self,
        image_path: Path,
    ):
        self.__image = ft.Image(src=str(image_path))
        super().__init__(content=self.__image)
        # self.on_click = click_handler

    async def change_image_async(self, image_path: Path):
        image = await load_image(image_path)
        self.change_image(image_to_base64(image))

    def change_image(self, base64_image: str):
        self.__image.src_base64 = base64_image
        if self.page != None:
            self.page.update()
