import math
import random 
from pygame import Vector2 

class Snake:
    def __init__(self):
        self.radius_limits = (10, 25)
        self.radius = 15
        self.colors = ("teal", "green", "black") # head, body 
        self.body = []
        self.direction = Vector2(1, 0)  # Right
        self.speed = 5 # Smooth movement speed (pixels/frame)
        self.gen_body()
        
        # stats
        self.score = 0
        self.life = 100

    def gen_body(self):
        """Generate initial body"""
        for n in range(20):
            x = 300 - n * self.speed
            y = 300
            self.body.append(Vector2(x, y))
    
    def grow(self, count):
        pos = self.body[-1]
        for _ in range(count):
            self.body.append(Vector2(*pos)) 
            
    def moveto(self, x, y):
        """Change direction based on input vector"""
        new_direction = Vector2(x, y)
        if new_direction.length_squared() > 0:
            new_direction = new_direction.normalize()
            # Prevent reverse movement
            if new_direction != -self.direction:
                self.direction = new_direction

    def update(self, game):
        # Move the head
        new_head = self.body[0] + self.direction * self.speed
        if new_head[0] > game.width:
            new_head[0] = 0
        elif new_head[0] < 0:
            new_head[0] = game.width
        if new_head[1] > game.height:
            new_head[1] = 0
        elif new_head[1] < 0:
            new_head[1] = game.height

        self.body.insert(0, new_head)

        # Remove the last segment unless we're growing
        self.body.pop()


class AISnake(Snake):
    def __init__(self):
        super().__init__()
        self.colors = ("red", "blue", "black")  # head, body
        self.target = None

    def update(self, game):
        if self.target is None or self.target.removed:
            closest_food = None
            closest_distance = float('inf')
            for food in game.food_list:
                dx = food.x - self.body[0][0]
                dy = food.y - self.body[0][1]
                dist = math.hypot(dx, dy)
                if dist < closest_distance:
                    closest_food = food
                    closest_distance = dist
            self.target = closest_food

        if self.target is not None:
            dx = self.target.x - self.body[0][0]
            dy = self.target.y - self.body[0][1]
            direction = Vector2(dx, dy).normalize()
            self.moveto(direction.x, direction.y)
        else:
            if random.random() < 0.05:
                direction = Vector2(random.randint(-game.width,game.width), random.randint(-game.height,game.height) ).normalize()
                direction += self.direction
                self.moveto(direction.x, direction.y)
        super().update(game)