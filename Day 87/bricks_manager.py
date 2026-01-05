from brick import Brick
colors = ["red", "orange", "green", "yellow"]

class BricksManager:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.bricks_in_row = self.width // 80
        self.all_bricks = []
        y = h / 2 - 50

        for color in colors:
            for row in range(2):
                x = -w / 2 + 35
                for i in range(self.bricks_in_row):
                    brick = Brick(x, y, color)
                    self.all_bricks.append(brick)
                    x += 80
                y -= 40