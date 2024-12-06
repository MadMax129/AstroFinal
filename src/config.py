from dataclasses import dataclass

@dataclass
class Config:
    Name: str = "Space Sandbox"
    Font_Path: str = "../font/Lato-Regular.ttf"
    Font_Size: int = 16
    Window: tuple[int, int] = (1200, 800)
    Assets_Folder: str = "../assets"
