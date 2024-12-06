from vector import Vector2D
import pygame

class Mouse:
    MOVE_DAMP = 0.9

    def __init__(self):
        self.mouse_position = None
        self.is_dragging = False
        self.drag_velocity = Vector2D(0.0, 0.0)

    def mouse_event(self, space_scale: float):
        camera_vector_change = Vector2D(0.0, 0.0)

        if pygame.mouse.get_pressed(3)[0]:
            pos = pygame.mouse.get_pos()
            if not self.is_dragging:
                self.is_dragging = True
                self.mouse_position = pos
                self.drag_velocity = Vector2D(0.0, 0.0)
            else:
                delta_x = self.mouse_position[0] - pos[0]
                delta_y = pos[1] - self.mouse_position[1]
                target_vector = space_scale * Vector2D(delta_x, delta_y) * 0.09
                self.drag_velocity += target_vector
                camera_vector_change = self.drag_velocity
                self.drag_velocity *= Mouse.MOVE_DAMP
                self.mouse_position = pos
        else:
            if self.drag_velocity.magnitude > 0.01:
                camera_vector_change = self.drag_velocity
                self.drag_velocity *= Mouse.MOVE_DAMP
            else:
                self.drag_velocity = Vector2D(0.0, 0.0)

            self.is_dragging = False
            self.mouse_position = None

        return camera_vector_change
