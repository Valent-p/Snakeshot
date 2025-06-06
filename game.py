import pygame as pg
from pygame import Vector2 

import random
import math
from snake import Snake, AISnake
from food import Apple

class Game:
    def __init__(self):
        # Initialize game window
        self.width = int(720*1.5)
        self.height = int(1280*1.5)
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.running = True
        self.top_score = 0

        # Initialize game objects
        self.player = Snake()
        self.snakes = [self.player, AISnake(), AISnake(), AISnake(), AISnake()]
        self.food_list = []
        self.score_font = pg.font.Font('freesansbold.ttf', 32)
        self.head_top_font = pg.font.Font('freesansbold.ttf', 24)


    def handle_events(self):
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.FINGERDOWN:
                self.touch_start = (event.x * self.width, event.y * self.height)
            elif event.type == pg.FINGERUP and hasattr(self, 'touch_start'):
                end = (event.x * self.width, event.y * self.height)
                
                dx = end[0] - self.touch_start[0]
                dy = end[1] - self.touch_start[1]
                direction = Vector2(dx, dy).normalize()
                self.player.moveto(direction.x, direction.y)
                
                """
                if abs(dx) > abs(dy):
                    self.player.moveto(1 if dx > 0 else -1, 0)
                else:
                    self.player.moveto(0, 1 if dy > 0 else -1)
                """
                
                del self.touch_start

    def update(self):
        # Add food randomly
        if random.random() < 0.05:
            self.food_list.append(Apple(random.randint(0, self.width), random.randint(0, self.height)))
        
        # Add more snakes randomly 
        if random.random() < 0.008:
            self.snakes.append(AISnake())
            
        # Update snakes
        for snake in self.snakes:
            snake.update(self)
            snake_pos = snake.body[0]
            
            # snake eat food
            for food in self.food_list[:]:
                dx = food.x - snake_pos[0]
                dy = food.y - snake_pos[1]
                dist = math.hypot(dx, dy)
                if dist < (snake.radius + food.radius):
                    food.eater = snake
                    snake.grow(5)
                    snake.score += 1
                    if snake.score > self.top_score:
                        self.top_score = snake.score
                #> if
            #> for
            
            # Snake eats snake
            for other_snake in self.snakes:
                if not len(snake.body):
                    break 
                
                # Cannot eat self
                if other_snake == snake:
                    continue 
                
                for seg in other_snake.body:
                    dx = snake_pos[0] - seg[0]
                    dy = snake_pos[1] - seg[1]
                    dist = math.hypot(dx, dy)
                    # Eats, (use the minimum radius)
                    if dist < min(other_snake.radius, snake.radius):
                        # Dead, remove it
                        snake.body.pop()
                        
                    if not len(snake.body):
                        self.snakes.remove(snake)
                        break 
                #> for
            #> for           
        #> for

        # Update food
        for food in self.food_list[:]:
            food.update(self)
            if food.removed:
                self.food_list.remove(food)

    def draw(self):
        # Draw background
        self.screen.fill("black")
        
        pg.draw.rect(self.screen, "purple", pg.Rect(0, 0, self.width, self.height)) 

        # Draw score
        self.screen.blit(self.score_font.render(f"Top Score: {self.top_score}", True, "white"), (100, 100))

        # Draw snakes
        for snake in self.snakes:
            for pos in snake.body:
                pg.draw.circle(self.screen, snake.colors[2], (int(pos[0]), int(pos[1])), snake.radius + 5)
            for pos in snake.body:
                pg.draw.circle(self.screen, snake.colors[1], (int(pos[0]), int(pos[1])), snake.radius)
            pg.draw.circle(self.screen, snake.colors[0], (int(snake.body[0][0]), int(snake.body[0][1])), snake.radius)
            self.screen.blit(
                self.head_top_font.render(f":{snake.score}", True, "white"), 
                (
                    int(snake.body[0][0]),
                    int(snake.body[0][1]-32)
                ) 
            )


        # Draw food
        for food in self.food_list:
            pg.draw.circle(self.screen, food.colors[1], (food.x, food.y), food.radius + 5)
            pg.draw.circle(self.screen, food.colors[0], (food.x, food.y), food.radius)

        pg.display.flip()

    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pg.quit()