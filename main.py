import pygame 
import math
#from project_clss import * #import all classes from project_clss.py
pygame.init()


# Screen
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Window
pygame.display.set_caption("Planet Simulation")  # Window name

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
# Fonts
FONT = pygame.font.SysFont("comicsans", 16)


# Planet class
class Planet(object):
    AU = 149.6e6 * 1000 # 1 AU in meters
    G = 6.67428e-11 # Gravitational constant
    SCALE = 200 / AU # Scale to fit all planets on the screen , 1AU = 100 PIXELS
    TIMESTEP = 24 * 3600 # Simulation time step (1 day), update the position of the planet by 1 day

    def __init__(self, x ,y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) >2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun /1000,1)}km",1, WHITE)
            WIN.blit(distance_text, (x- distance_text.get_width()/2,y - distance_text.get_height()/2))


    def attraction( self, other):
        other_x, other_y = other.x, other.y
        # Calculate the distance between the two planets
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        # Calculate the direction of the force
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if planet == self:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



# pygame infinite loop
def main():
    run = True
    clock = pygame.time.Clock() #regualate the speed of the game

    sun = Planet(0,0,30, YELLOW, 1.988892E30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742E24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39E23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8 , DARK_GREY, 0.330E24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE , 4.8685E24)
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    
    while run == True:
        clock.tick(60) #maximum fps = 60
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()

    pygame.quit()


main()