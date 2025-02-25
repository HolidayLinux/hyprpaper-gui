from pathlib import Path

import flet as ft

from icon_creater import ThumbnailCreater


class ImageWrapper(ft.Image):
    def __init__(self, image_load_path: Path):
        super().__init__(src=".\\assets\\images\\loading.gif")
        self.__thumbnail_creater = ThumbnailCreater(image_load_path)
        self.__is_update = False

    async def update_image(self):
        self.src_base64 = await self.__thumbnail_creater.thumbnail_base64_mem()
        self.__is_update = True
        self.update()

    @property
    def is_update(self) -> bool:
        return self.__is_update

    def did_mount(self):
        if self.page != None:
            self.page.run_thread(self.update_image)
        # self.__page_worker(self.update_image)
