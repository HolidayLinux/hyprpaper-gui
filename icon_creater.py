import asyncio
import base64
from io import BytesIO
from PIL import Image
from pathlib import Path

__supported_extensions = ['.jpg', '.png', '.jgep']


def get_files_in_directory(directory_path: Path):
    files = [file for file in directory_path.glob(
        '**/*') if file.suffix in __supported_extensions]
    return files


async def load_image(image_path):
    loop = asyncio.get_running_loop()
    img: Image.Image = await loop.run_in_executor(None, Image.open, image_path)
    return img


async def create_cached_image(image_path: Path, cached_path: Path):
    try:
        img = await load_image(image_path=image_path)
        img.thumbnail(size=(150, 150))
        img.save(cached_path)
        return True
    except:
        return False


async def create_cached_image_mem(image_path: Path):
    img = await load_image(image_path=image_path)
    img.thumbnail(size=(150, 150))
    return img


def image_to_base64(img: Image.Image):
    im_file = BytesIO()
    img.save(im_file, format='PNG')
    return base64.b64encode(im_file.getvalue()).decode('ASCII')


class ThumbnailCreater:
    def __init__(self, image_path: Path):
        self.__image_path = image_path
        self.__directory = image_path.parents[0]
        self.__image_name = image_path.name
        self.__cached_path = Path(
            f'{self.__directory}/.cached/{self.__image_name}')

    async def thumbnail_base64(self) -> str:
        if (await create_cached_image(self.__image_path, self.__cached_path)):
            with open(self.__cached_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('ASCII')
        return ''

    async def thumbnail_base64_mem(self) -> str:
        image = await create_cached_image_mem(self.__image_path)
        return image_to_base64(image)


class PackageThumbnailCreater:

    def __init__(self, path: str) -> None:
        self.__path = Path(path)
        self.__cached_path = Path(f'{path}/.cache')
        if self.__cached_path.exists():
            if len(get_files_in_directory(self.__path)) > 0:
                self.delete_dir(self.__cached_path)
        self.__cached_path.mkdir()

    async def start(self):
        images = []
        for image in await self.get_cached_files():
            images.append(await load_image(image))
        return images

    async def get_cached_files(self) -> list[Path]:
        files = get_files_in_directory(self.__path)
        cached_files: list[Path] = []
        for file in files:
            cached_image_path = await self._create_cached_image(file)
            if cached_image_path != Path():
                cached_files.append(cached_image_path)
        return cached_files

    async def _create_cached_image(self, image_path: Path):
        try:
            img = await load_image(image_path=image_path)
            img.thumbnail(size=(150, 150))
            cached_image_path = Path(
                f'{str(self.__cached_path)}/{image_path.name}')
            img.save(cached_image_path)
            return cached_image_path
        except:
            return Path()

    def delete_dir(self, path: Path):
        if path.is_file() or path.is_symlink():
            path.unlink()
            return
        for p in path.iterdir():
            self.delete_dir(p)

        path.rmdir()
