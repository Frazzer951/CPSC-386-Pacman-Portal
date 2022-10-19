import json

import pygame


class SpriteSheet:
    def __init__(self, filename, json_filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

        self.meta_data = json_filename
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.set_colorkey((0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)
        return image

    def get_sprite(self, name):
        sprite = self.data["frames"][name]["frame"]
        dimensions = pygame.Rect(sprite["x"], sprite["y"], sprite["w"], sprite["h"])
        image = self.image_at(dimensions)
        image = pygame.transform.scale(image, (2 * sprite["w"], 2 * sprite["h"]))
        return image
