from config import Config
from vector import Vector2D
import pygame

class Planet:
    """
    name     | Name of planet object
    asset    | AssetManger to load sprite or None
    mass     | Mass of object in kg
    radius   | Radius of object in meters
    scale    | Sprite scale multiplier
    color    | Tuple for color of text or circle if asset == None
    position | Inital position on plane in meters
    velocity | Inital velocity of planet in m/s
    """
    def __init__(
        self,
        name: str,
        asset: pygame.Surface,
        mass: float,
        radius: float,
        scale: int,
        color: tuple[int, int, int],
        position: Vector2D,
        velocity=Vector2D(),
    ):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.scale = scale
        self.asset = asset
        self.color = color
        self.position = position
        self.velocity = velocity
        self.trajectory = []
        self.trajectory_points = []
        self.max_trajectory_points = 500

    @staticmethod
    def is_visible(planet_pos: Vector2D, planet_radius: float, screen_size):
        screen_width, screen_height = screen_size
        left = -planet_radius
        right = screen_width + planet_radius
        top = -planet_radius
        bottom = screen_height + planet_radius
        return (left <= planet_pos.x <= right) and (top <= planet_pos.y <= bottom)

    def draw_trajectory(self, window, space_scale, camera_vector):
        """
        Draw trajectory only for visible planets and reset when going out of view.
        """
        # Get window dimensions for viewport check
        window_width, window_height = window.get_size()
        screen_pos = (self.position - camera_vector) * (1 / space_scale)
        screen_pos.vector[1] = window_height - screen_pos.y

        self.trajectory_points.append(self.position.copy())
        if len(self.trajectory_points) > self.max_trajectory_points:
            self.trajectory_points.pop(0)

        # Draw trajectory
        if len(self.trajectory_points) > 1:
            points = []
            for world_pos in self.trajectory_points:
                screen_pos = (world_pos - camera_vector) * (1 / space_scale)
                screen_pos.vector[1] = window_height - screen_pos.y
                points.append(screen_pos.Args)

            pygame.draw.lines(window, self.color, False, points, 1)

    def draw(
        self,
        window: pygame.Surface,
        space_scale: float,
        camera_vector: Vector2D
    ):
        planet_radius = self.radius * self.scale / space_scale
        planet_pos = (self.position - camera_vector) * (1 / space_scale)
        planet_pos.vector[1] = window.get_height() - planet_pos.y

        # self.trajectory.append(self.position.copy())
        # if len(self.trajectory) > self.MAX_PATH_LENGTH:
        #     del self.trajectory[0]

        # # Prepare path points with y-coordinate inversion
        # path_points = []
        # for pos in self.trajectory:
        #     traj_display_pos = (pos - camera_vector) * (1 / space_scale)
        #     traj_display_pos.vector[1] = window.get_height() - traj_display_pos.y
        #     path_points.append(traj_display_pos.Args)
        # if len(path_points) > 1:
        #     pygame.draw.lines(window, self.color, False, path_points, 1)
        self.draw_trajectory(window, space_scale, camera_vector)

        x, y = planet_pos.x, planet_pos.y

        if Planet.is_visible(planet_pos, planet_radius, window.get_size()):
            if self.asset:
                image_size = int(2 * planet_radius)
                scaled_image = pygame.transform.scale(self.asset, (image_size, image_size))
                rect = scaled_image.get_rect(center=(int(x), int(y)))
                window.blit(scaled_image, rect)
            else:
                pygame.draw.circle(window, self.color, (int(x), int(y)), int(planet_radius))

            return planet_pos, planet_radius
        else:
            self.trajectory_points.clear()

        return None, None
