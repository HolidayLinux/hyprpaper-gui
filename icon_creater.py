import asyncio
from pathlib import Path
from PIL import Image


class IconCreater:
    __supported_extensions = ['.jpg', '.png', '.jgep']

    def get_files_in_directory(self, dir: Path):
        files = [file for file in dir.glob(
            '**/*') if file.suffix in self.__supported_extensions]
        return files

    def __init__(self, path: str) -> None:
        self.__path = Path(path)
        self.__cached_path = Path(f'{path}/.cache')
        if self.__cached_path.exists():
            if len(self.get_files_in_directory(self.__path)) > 0:
                self.delete_dir(self.__cached_path)
        self.__cached_path.mkdir()

    async def start(self):
        files = self.get_files_in_directory(self.__path)
        cached_files: list[Image.Image] = []
        for file in files:
            cached_image_path = await self._create_cached_image(file)
            if cached_image_path != Path():
                cached_files.append(await self._load_image(cached_image_path))
        return cached_files

    async def _create_cached_image(self, image_path: Path):
        try:
            img = await self._load_image(image_path=image_path)
            img.thumbnail(size=(150, 150))
            cached_image_path = Path(
                f'{str(self.__cached_path)}/{image_path.name}')
            img.save(cached_image_path)
            return cached_image_path
        except:
            return Path()

    async def _load_image(self, image_path):
        loop = asyncio.get_running_loop()
        img: Image.Image = await loop.run_in_executor(None, Image.open, image_path)
        return img

    def delete_dir(self, path: Path):
        if path.is_file() or path.is_symlink():
            path.unlink()
            return
        for p in path.iterdir():
            self.delete_dir(p)

        path.rmdir()
