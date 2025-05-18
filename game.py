import pygame as pg
import random 
import math

from snake import Snake
from food import Apple

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.running = True
        self.snake = Snake()
        self.food_list = []

    def start(self):
        touch_start = None
        score_font = pg.font.Font('freesansbold.ttf', 32)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                
                # Input
                elif event.type == pg.FINGERDOWN:
                    touch_start = (event.x * self.width, event.y * self.height)  # Scale normalized to screen

                elif event.type == pg.FINGERUP and touch_start:
                    end = (event.x * self.width, event.y * self.height)
                    dx = end[0] - touch_start[0]
                    dy = end[1] - touch_start[1]

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            self.snake.moveto(1, 0)  # Right
                        else:
                            self.snake.moveto(-1, 0)  # Left
                    else:
                        if dy > 0:
                            self.snake.moveto(0, 1)  # Down
                        else:
                            self.snake.moveto(0, -1)  # Up

                    touch_start = None
            
            # Background 
            self.screen.fill("purple")
            
            # The score
            self.screen.blit(score_font.render(f"Score: {self.snake.score}", True, "white"), (100,100))
            
            # Add food randomly 
            if random.random() < 0.01:
                self.food_list.append(Apple(random.randrange(0, self.width) , random.randrange(0, self.height)))
            
            # Snake
            self.snake.update()
            for pos in self.snake.body:
                pg.draw.circle(self.screen, self.snake.colors[2], (int(pos.x), int(pos.y)), self.snake.radius+5)
            for pos in self.snake.body:
                pg.draw.circle(self.screen, self.snake.colors[1], (int(pos.x), int(pos.y)), self.snake.radius)
            # Head
            pg.draw.circle(self.screen, self.snake.colors[0], (int(self.snake.body[0][0]), int(self.snake.body[0][1])), self.snake.radius)

     
            # Draw and update food
            snake_pos = self.snake.body[0]
            for food in self.food_list[:]:
                # Collison 
                dx = food.x - snake_pos[0]
                dy = food.y - snake_pos[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist < (self.snake.radius + food.radius):
                    food.eater = self.snake
                    self.snake.grow(1)
          
                food.update()
                # Draw food
                pg.draw.circle(self.screen, food.colors[1], (food.x, food.y), food.radius+5)
                pg.draw.circle(self.screen, food.colors[0], (food.x, food.y), food.radius)
                
                if food.removed:
                    self.food_list.remove(food)
                    # score up
                    self.snake.score += 1
   
                   
            # Food Collision 
            
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()