from planet import Planet
from assets import AssetManager
from vector import Vector2D

class Preset:
    """
    name        | Name of preset button on screen
    objects     | List of Planet objects to simulate
    space_scale | Pixel to meter conversion, increase to make one pixel cover more physical space
    dt          | Simulation delta time, for large simulation increase for FPS stability
    """
    def __init__(
        self,
        name: str,
        objects: list,
        space_scale: int,
        dt: int
    ):
        self.name = name
        self.objects = objects
        self.space_scale = space_scale
        self.dt = dt

    def reset(self):
        for object in self.objects:
            object.trajectory_points = []

def get_presets():
    return [
        ### Earth and Moon
        Preset(
            name="Earth & Moon",
            objects=[
                Planet(
                    name="Earth",
                    asset=AssetManager().get_asset("Earth"),
                    mass=5.9724 * 10**24,
                    radius=6.356 * 10**6,
                    scale=5,
                    color=(11, 227, 195),
                    position=Vector2D(5 * 10**8, 5 * 10**8),
                    velocity=Vector2D(0,0)
                ),
                Planet(
                    name="Moon",
                    asset=AssetManager().get_asset("Moon"),
                    mass=7.34767309e22,
                    radius=1.7371e6,
                    scale=3,
                    color=(180, 180, 180),
                    position=Vector2D(
                        8.992 * 10 ** 8, 5 * 10 ** 8,
                    ),
                    velocity=Vector2D(
                        0, 1022
                    )
                ),
            ],
            dt=100,
            space_scale=10**6 + 1000
        ),

        ### Binary Stars
        Preset(
            name="Binary",
            objects=[
                Planet(
                    name="Binary 0",
                    asset=AssetManager().get_asset("Jupiter"),
                    mass=5.972 * 10 ** 24,
                    radius=6.371 * 10 ** 6,
                    scale=1,
                    color=(255, 255, 255),
                    position=Vector2D(3 * 10 ** 8, 5 * 10 ** 8),
                    velocity=Vector2D(0, 600)
                ),
                Planet(
                    name="Binary 1",
                    asset=AssetManager().get_asset("Jupiter"),
                    mass=5.972 * 10 ** 24,
                    radius=6.371 * 10 ** 6,
                    scale=1,
                    color=(255, 255, 255),
                    position=Vector2D(7 * 10 ** 8, 5 * 10 ** 8),
                    velocity=Vector2D(0, -600)
                )
            ],
            dt=100,
            space_scale=10**6
        ),

        ### Solar System
        Preset(
            name="Solar System",
            objects=[
                Planet(
                    name="Sun",
                    asset=None,
                    # asset=AssetManager().get_asset("Jupiter"),
                    mass=1.989 * 10**30,
                    radius=6.957 * 10**8,
                    scale=25,
                    color=(252, 186, 3),
                    position=Vector2D(6 * 10**12, 6 * 10**12),
                    velocity=Vector2D(0, 0)
                ),

                Planet(
                    name="Mecury",
                    asset=None,
                    mass=3.285 * 10**23,
                    radius=2.4397 * 10**6,
                    scale=1000,
                    color=(180, 180, 180),
                    position=Vector2D(6 * 10**12 + 57.9 * 10**9, 6 * 10**12),
                    velocity=Vector2D(0, 47.36 * 10**3)
                ),

                Planet(
                    name="Venus",
                    asset=None,
                    mass=4.867 * 10**24,
                    radius=6.0518 * 10**6,
                    scale=1000,
                    color=(187, 183, 171),
                    position=Vector2D(6 * 10**12 - 107.48 * 10**9, 6 * 10**12),
                    velocity=Vector2D(0, -35.02 * 10**3)
                ),

                Planet(
                    name="Earth",
                    asset=AssetManager().get_asset("Earth"),
                    mass=5.9724 * 10**24,
                    radius=6.356 * 10**6,
                    scale=3,
                    color=(11, 227, 195),
                    position=Vector2D(6 * 10**12 + 151.96 * 10**9, 6 * 10**12),
                    velocity=Vector2D(0, 29.78 * 10**3)
                ),

                Planet(
                    name="Moon",
                    asset=AssetManager().get_asset("Moon"),
                    mass=7.34767309e22,
                    radius=1.7371e6,
                    scale=3,
                    color=(180, 180, 180),
                    position=Vector2D(
                        6 * 10**12 + 151.96 * 10**9 + 384400 * 10**3,
                        6 * 10**12
                    ),
                    velocity=Vector2D(
                        0,
                        29.78 * 10**3 + 1.022 * 10**3
                    )
                ),

                Planet(
                    name="Mars",
                    asset=AssetManager().get_asset("Mars"),
                    mass=64171 * 10**23,
                    radius=3.3895 * 10**6,
                    scale=1000,
                    color=(193, 68, 14),
                    position=Vector2D(6 * 10**12 - 250.17 * 10**9, 6 * 10**12),
                    velocity=Vector2D(0, -24.07 * 10**3)
                ),

                Planet(
                    name="Jupiter",
                    asset=AssetManager().get_asset("Jupiter"),
                    mass=1.89819 * 10**27,
                    radius=6.9911 * 10**7,
                    scale=200,
                    color=(211, 156, 126),
                    position=Vector2D(6 * 10**12 + 754.87 * 10**9, 6 * 10**12),
                    velocity=Vector2D(0, 13.06 * 10**3)
                ),

                Planet(
                    name="Saturn",
                    asset=None,
                    mass=5.6834 * 10**26,
                    radius=5.4364 * 10**7,
                    scale=200,
                    color=(197, 171, 110),
                    position=Vector2D(6 * 10 ** 12 - 1.4872 * 10**12, 6 * 10 ** 12),
                    velocity=Vector2D(0, -9.68 * 10**3)
                ),

                Planet(
                    name="Uranus",
                    asset=None,
                    mass=8.6813 * 10**25,
                    radius=2.4973 * 10**7,
                    scale=600,
                    color=(187, 225, 228),
                    position=Vector2D(6 * 10 ** 12 + 2.9541 * 10**12, 6 * 10 ** 12),
                    velocity=Vector2D(0, 6.80 * 10**3)
                ),

                Planet(
                    name="Neptune",
                    asset=None,
                    mass=1.02413 * 10**26,
                    radius=2.4341 * 10**7,
                    scale=600,
                    color=(62, 84, 232),
                    position=Vector2D(6 * 10 ** 12 - 4.495 * 10**12, 6 * 10 ** 12),
                    velocity=Vector2D(0, -5.43 * 10**3)
                ),

                Planet(
                    name="Pluto",
                    asset=None,
                    mass=1.303 * 10**22,
                    radius=1.188 * 10**6,
                    scale=1000,
                    color=(150, 133, 112),
                    position=Vector2D(6 * 10 ** 12 + 5.90538 * 10**12, 6 * 10 ** 12),
                    velocity=Vector2D(0, 4.67 * 10**3)
                )
            ],
            dt=5000,
            space_scale=12 * 10 ** 9
        )
    ]
