import cv2
from utils.constants import HEIGHT, WIDTH

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, frame):
        cv2.rectangle(
            frame,
            (int(self.x - self.width // 2), int(self.y - self.height // 2)),
            (int(self.x + self.width // 2), int(self.y + self.height // 2)),
            self.color,
            -1,
        )

    def move(self, x, y):
        self.x = x
        self.y = y

    # Ensure the paddle stays within the frame boundaries
        # if self.x - self.width//2 < 0:
        #     self.x = self.width//2
        # if self.x + self.width//2 > WIDTH:
        #     self.x = WIDTH - self.width//2
        # self.draw(frame)

    # def reset(self):
    #     self.x = self. original_x
    #     self.y = self.original_y