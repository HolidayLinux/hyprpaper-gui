import flet as ft
from imagewrapper import ImageWrapper


class ProgressBar(ft.ProgressBar):
    def __init__(self, width, init_value, controls: list[ImageWrapper]):
        super().__init__(width=width)
        self.value = init_value
        self.__progress_controls = controls

    def did_mount(self):
        self.progress()
        self.update()

    def progress(self):
        while True:
            updated = [
                image for image in self.__progress_controls if image.is_update]
            self.value = len(updated) * (len(self.__progress_controls) * 0.01)
            self.update()
            if len(updated) == len(self.__progress_controls):
                break
