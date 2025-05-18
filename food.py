import math

class Eatable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = ("red", "black") 
        self.radius = 20
        self.eater = None
        self.removed = False
    
    def update(self):
        if self.eater is None:
            return

        # Calculate direction vector
        eater_pos = self.eater.body[0]
        dx = eater_pos[0] - self.x
        dy = eater_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize direction vector
        if distance > 0:
            dx /= distance
            dy /= distance

            # Move towards the eater
            self.x += dx * 10
            self.y += dy * 10

            # Check if eaten (to remove)
            if distance < self.radius/2:
                self.removed = True
                
class Apple(Eatable): 
    def __init__(self, x, y): 
        super().__init__(x, y)
  