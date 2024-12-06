from copy import deepcopy
import pygame
import pygame.freetype
from enum import Enum, auto
from config import Config
from planet import Planet
from vector import Vector2D
from mouse import Mouse
from assets import AssetManager
from physics import PhysicsEngine
from presets import Preset, get_presets
from copy import deepcopy

from pygame.locals import K_a, K_d, K_o, K_p

class State(Enum):
    Init    = auto()
    Running = auto()
    Quit    = auto()

class Simulation:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()

        self.FONT = pygame.freetype.Font(Config.Font_Path, Config.Font_Size)
        self.window = pygame.display.set_mode(Config.Window, pygame.RESIZABLE)
        pygame.display.set_caption(Config.Name)

        self.state = State(State.Init)
        self.mouse = Mouse()

        AssetManager().load_all()

        self.background_image = AssetManager().get_asset("stars")
        self.camera_vector = Vector2D(0.0, 0.0)

        self.presets = get_presets()
        self.load_preset(Preset("empty", [], 100, 100))

        self.button_height = 40
        self.button_width = 150
        self.button_margin = 10
        self.buttons = self.create_buttons()

    def load_preset(self, preset):
        preset.reset()
        self.objects = preset.objects
        self.time_scale = preset.dt * 10
        self.time_elapsed = 0
        self.dt = preset.dt
        self.space_scale = preset.space_scale
        self.physics = PhysicsEngine(preset.objects)
        self.camera_vector = Vector2D(0.0, 0.0)

    def draw_background(self):
        image_width = self.background_image.get_width()
        image_height = self.background_image.get_height()
        window_width, window_height = self.window.get_size()
        parallax_factor = (1 / self.space_scale) * 0.02
        parallax_offset_x = self.camera_vector.x * parallax_factor
        parallax_offset_y = -self.camera_vector.y * parallax_factor
        x_tiles = window_width // image_width + 2
        y_tiles = window_height // image_height + 2
        x_start = - (parallax_offset_x % image_width)
        y_start = - (parallax_offset_y % image_height)
        for x in range(x_tiles):
            for y in range(y_tiles):
                pos_x = x_start + x * image_width
                pos_y = y_start + y * image_height
                self.window.blit(self.background_image, (pos_x, pos_y))

    def event_handler(self):
        zoom_factor = 1.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = State.Quit
                break
            elif event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_o:
                    self.time_scale *= 0.5
                elif event.key == K_p:
                    self.time_scale *= 1.5
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        self.load_preset(button['preset'])

    def handle_zoom(self):
        mouse_pos = Vector2D(*pygame.mouse.get_pos())
        mouse_pos.vector[1] = self.window.get_height() - mouse_pos.y

        world_mouse_pos = (mouse_pos * self.space_scale) + self.camera_vector

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.space_scale *= 0.99
            self.camera_vector = world_mouse_pos - (mouse_pos * self.space_scale)
        elif keys[pygame.K_d]:
            self.space_scale *= 1.01
            self.camera_vector = world_mouse_pos - (mouse_pos * self.space_scale)

    def render(self):
        for planet in self.objects:
            p_pos, p_rad = planet.draw(self.window, self.space_scale, self.camera_vector)
            if p_pos and p_rad:
                label_x, label_y = p_pos.vector
                label_surface, label_rect = self.FONT.render(planet.name, planet.color)
                label_rect.center = (label_x, label_y + p_rad + 10)
                self.window.blit(label_surface, label_rect)

    def display_ui(self, fps: float):
        line_length_pixels = 100
        line_distance = (line_length_pixels * self.space_scale) / 1000

        text_surface, rect = self.FONT.render(f"Scale: {line_distance:,.0f} km", (255, 255, 255))
        rect.topleft = (10, 10)
        self.window.blit(text_surface, rect)

        line_start = (10, rect.bottom + 10)
        line_end = (10 + line_length_pixels, rect.bottom + 10)
        pygame.draw.line(self.window, (255, 255, 255), line_start, line_end, 2)

        fps_text, fps_rect = self.FONT.render(f"{fps:.0f}", (255, 255, 255))
        fps_rect.topright = (self.window.get_width() - 10, 10)
        self.window.blit(fps_text, fps_rect)

        years, _ = divmod(self.time_elapsed, 31536000)
        months, _ = divmod(self.time_elapsed, 2628000)
        days, _ = divmod(self.time_elapsed, 86400)
        sim_time_text, sim_time_rect = self.FONT.render(f"Time: {int(years)}y {int(months)}m {int(days)}d", (255, 255, 255))
        sim_time_rect.bottomleft = (10, self.window.get_height() - 10)
        self.window.blit(sim_time_text, sim_time_rect)

    def create_buttons(self):
        buttons = []
        for i, preset in enumerate(self.presets):
            name = preset.name
            x = self.button_margin
            y = self.button_margin + i * (self.button_height + self.button_margin)
            buttons.append({
                'rect': pygame.Rect(x, y + 40, self.button_width, self.button_height),
                'text': name,
                'preset': preset
            })
        return buttons

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.window, (100, 100, 100), button['rect'])
            pygame.draw.rect(self.window, (150, 150, 150), button['rect'], 2)
            text_surface, text_rect = self.FONT.render(button['text'], (255, 255, 255))
            text_rect.center = button['rect'].center
            self.window.blit(text_surface, text_rect)

    def loop(self):
        clock = pygame.time.Clock()
        accumulator = 0.0

        while self.state != State.Quit:
            frame_time = clock.tick(60) / 1000.0

            if frame_time > 0.25:
                frame_time = 0.25

            scaled_frame_time = frame_time * self.time_scale
            accumulator += scaled_frame_time

            self.event_handler()

            self.handle_zoom()
            self.camera_vector += self.mouse.mouse_event(self.space_scale)
            self.draw_background()

            # Physics
            while accumulator >= self.dt:
                self.physics.update_objects(self.dt)
                accumulator -= self.dt
                self.time_elapsed += self.dt

            self.render()
            self.draw_buttons()
            self.display_ui(clock.get_fps())

            pygame.display.update()

if __name__ == "__main__":
    Simulation().loop()
