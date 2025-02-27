import flet as ft
from pathlib import Path
from flet.core.text_button import OptionalControlEventCallable
from icon_creater import load_image, image_to_base64


class ImageButton(ft.TextButton):
    def __init__(self, image_path: Path, click_handler):
        self.__image = ft.Image(src=str(image_path))
        self.__image_path = image_path
        super().__init__(content=self.__image)
        self.on_click = click_handler

    @property
    def image_path(self):
        return self.__image_path

    @image_path.setter
    def image_path(self, value: Path):
        self.__image_path = value

    @image_path.getter
    def image_path(self):
        return self.__image_path

    async def change_image_async(self, image_path: Path):
        image = await load_image(image_path)
        self.change_image(image_to_base64(image), path_to_image=image_path)

    def change_image(self, base64_image: str, path_to_image: Path):
        self.__image.src_base64 = base64_image
        self.image_path = path_to_image
        if self.page != None:
            self.page.update()
