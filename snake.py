from pygame import Vector2 

class Snake:
    def __init__(self):
        self.radius_limits = (10, 25)
        self.radius = 15
        self.colors = ("teal", "green", "black") # head, body 
        self.body = []
        self.direction = Vector2(1, 0)  # Right
        self.speed = 5 # Smooth movement speed (pixels/frame)
        self.target_direction = self.direction.copy()
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
                self.target_direction = new_direction

    def update(self):
        # Smoothly apply direction change
        self.direction = self.target_direction

        # Move the head
        new_head = self.body[0] + self.direction * self.speed
        self.body.insert(0, new_head)

        # Remove the last segment unless we're growing
        self.body.pop()

   