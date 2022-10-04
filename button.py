class Button:
    def __init__(self, pos, text, font, base_color, hover_color):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hover_color = base_color, hover_color
        self.text_str = text
        self.text = self.font.render(self.text_str, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)

    def onButton(self, pos):
        return pos[0] in range(self.text_rect.left, self.text_rect.right) and pos[1] in range(
            self.text_rect.top, self.text_rect.bottom
        )

    def setHover(self, pos):
        if self.onButton(pos):
            self.text = self.font.render(self.text_str, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_str, True, self.base_color)
