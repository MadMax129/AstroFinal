import pygame
from pathlib import Path
from config import Config

class AssetManager:
    _instance = None
    ASSET_CACHE = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.load_all()

    def load_all(self):
        asset_folder = Path(Config.Assets_Folder)

        for asset_file in asset_folder.glob('*.png'):
            asset_name = asset_file.stem
            image = pygame.image.load(str(asset_file)).convert_alpha()
            self.ASSET_CACHE[asset_name] = image

    def get_asset(self, asset_name):
        return self.ASSET_CACHE.get(asset_name)
