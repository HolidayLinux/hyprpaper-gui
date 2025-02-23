from pathlib import Path
from icon_creater import ThumbnailCreater
import flet as ft


class ImageWrapper(ft.Image):
    def __init__(self, image_load_path: Path, run_task):
        super().__init__(src='.\\assets\\images\\loading2.gif')
        self.__page_worker = run_task
        self.__thumbnail_creater = ThumbnailCreater(image_load_path)
        self.__is_update = False

    async def update_image(self):
        self.src_base64 = await self.__thumbnail_creater.thumbnail_base64_mem()
        self.__is_update = True
        self.update()

    @property
    def is_update(self):
        return self.__is_update

    def did_mount(self):
        self.__page_worker(self.update_image)
