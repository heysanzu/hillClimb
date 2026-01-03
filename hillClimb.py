import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hill Climb - by Sanzu")
clock = pygame.time.Clock()

# Fonts - Comic Sans
FONT_SMALL = pygame.font.SysFont("comicsansms", 18)
FONT = pygame.font.SysFont("comicsansms", 24)
FONT_LARGE = pygame.font.SysFont("comicsansms", 42)
FONT_TITLE = pygame.font.SysFont("comicsansms", 64)

# Colors (Blue, Black, White, Grey theme)
SKY_BLUE = (100, 150, 200)
DARK_BLUE = (50, 70, 100)
GROUND_GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 120, 200)
RED = (200, 50, 50)
GREEN = (50, 200, 100)

# Game states
INTRO = 0
PLAYING = 1
GAME_OVER = 2

# Global high score
high_score = 0

def load_high_score():
    """Load high score from file"""
    global high_score
    try:
        with open('hillClimb.txt', 'r') as f:
            high_score = float(f.read().strip())
    except FileNotFoundError:
        high_score = 0
    except ValueError:
        high_score = 0

def save_high_score():
    """Save high score to file"""
    try:
        with open('hillClimb.txt', 'w') as f:
            f.write(str(int(high_score)))
    except Exception as e:
        print(f"Error saving high score: {e}")

class FuelCan:
    def __init__(self, x, y):
        self.x = x
        self.ground_y = y  # Store ground position
        self.y = y - 15  # Position on surface
        self.width = 25
        self.height = 35
        self.collected = False
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
        # Update ground y based on new x position
        self.ground_y = get_path_y_at_x(self.x)
        self.y = self.ground_y - self.height // 2
    
    def draw(self, screen):
        if not self.collected:
            # Fuel can body
            pygame.draw.rect(screen, BLUE, (int(self.x - self.width/2), int(self.y - self.height/2), self.width, self.height))
            pygame.draw.rect(screen, BLACK, (int(self.x - self.width/2), int(self.y - self.height/2), self.width, self.height), 3)
            # Cap
            pygame.draw.rect(screen, DARK_GRAY, (int(self.x - 8), int(self.y - self.height/2 - 6), 16, 6))
            # F label
            label_text = FONT.render("F", True, WHITE)
            screen.blit(label_text, (int(self.x - 8), int(self.y - 12)))
    
    def check_collision(self, vehicle):
        if not self.collected:
            dist = math.sqrt((self.x - vehicle.screen_x)**2 + (self.y - vehicle.mid_y)**2)
            if dist < 45:
                self.collected = True
                return True
        return False

class HealthPack:
    def __init__(self, x, y):
        self.x = x
        self.ground_y = y  # Store ground position
        self.y = y - 15  # Position on surface
        self.size = 30
        self.collected = False
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
        # Update ground y based on new x position
        self.ground_y = get_path_y_at_x(self.x)
        self.y = self.ground_y - self.size // 2
    
    def draw(self, screen):
        if not self.collected:
            # Health pack box
            pygame.draw.rect(screen, WHITE, (int(self.x - self.size/2), int(self.y - self.size/2), self.size, self.size))
            pygame.draw.rect(screen, BLACK, (int(self.x - self.size/2), int(self.y - self.size/2), self.size, self.size), 3)
            # Red cross
            # Vertical
            pygame.draw.rect(screen, RED, (int(self.x - 4), int(self.y - self.size/2 + 6), 8, self.size - 12))
            # Horizontal
            pygame.draw.rect(screen, RED, (int(self.x - self.size/2 + 6), int(self.y - 4), self.size - 12, 8))
    
    def check_collision(self, vehicle):
        if not self.collected:
            dist = math.sqrt((self.x - vehicle.screen_x)**2 + (self.y - vehicle.mid_y)**2)
            if dist < 45:
                self.collected = True
                return True
        return False

class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 50
        self.hit = False
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
    
    def draw(self, screen):
        if not self.hit:
            # Barrier post
            pygame.draw.rect(screen, BLACK, (int(self.x - self.width/2), int(self.y - self.height), self.width, self.height))
            # Warning stripes
            stripe_height = 10
            for i in range(int(self.height / stripe_height)):
                if i % 2 == 0:
                    pygame.draw.rect(screen, WHITE, (int(self.x - self.width/2), int(self.y - self.height + i * stripe_height), self.width, stripe_height))
    
    def check_collision(self, vehicle):
        if not self.hit:
            # Check if vehicle overlaps with barrier
            if abs(self.x - vehicle.screen_x) < 40:
                if vehicle.mid_y < self.y and vehicle.mid_y > self.y - self.height:
                    self.hit = True
                    return True
        return False

class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 50
        self.hit = False
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
    
    def draw(self, screen):
        if not self.hit:
            # Barrier post
            pygame.draw.rect(screen, BLACK, (int(self.x - self.width/2), int(self.y - self.height), self.width, self.height))
            # Warning stripes
            stripe_height = 10
            for i in range(int(self.height / stripe_height)):
                if i % 2 == 0:
                    pygame.draw.rect(screen, WHITE, (int(self.x - self.width/2), int(self.y - self.height + i * stripe_height), self.width, stripe_height))
    
    def check_collision(self, vehicle):
        if not self.hit:
            # Check if vehicle overlaps with barrier
            if abs(self.x - vehicle.screen_x) < 40:
                if vehicle.mid_y < self.y and vehicle.mid_y > self.y - self.height:
                    self.hit = True
                    return True
        return False

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.life = 30
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen):
        color = LIGHT_GRAY
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Vehicle:
    def __init__(self):
        self.reset()
        self.particles = []

    def reset(self):
        self.screen_x = WIDTH // 2 - 50
        self.rear_screen_x = self.screen_x - 45
        self.front_screen_x = self.screen_x + 45
        self.wheelbase = 90
        self.chassis_height = 30
        self.wheel_radius = 20
        self.v = 0.0
        self.distance = 0.0
        self.gas = 1.0
        self.health = 100.0
        self.points = 0
        self.wheel_rot = 0.0
        self.rear_y = 0
        self.front_y = 0
        self.angle = 0.0
        self.mid_y = 0
        self.crash_damage = 0

    def update(self, thrusting):
        # Get ground y for wheels
        self.rear_y = self.get_ground_y(self.rear_screen_x)
        self.front_y = self.get_ground_y(self.front_screen_x)

        dx = self.front_screen_x - self.rear_screen_x
        dy = self.front_y - self.rear_y
        old_angle = self.angle
        self.angle = math.atan2(dy, dx)

        # Damage from sudden angle changes
        angle_change = abs(self.angle - old_angle)
        if angle_change > 0.15 and abs(self.v) > 5:
            self.health -= angle_change * 20
            self.crash_damage = 10

        # Physics
        g = 0.4
        gravity_comp = g * math.sin(self.angle)
        thrust = 0.32 if thrusting and self.gas > 0 else 0
        drag = -0.0008 * self.v ** 2 if self.v > 0 else -0.0005 * self.v
        net_accel = thrust + drag - gravity_comp

        self.v += net_accel
        if self.v < 0:
            self.v *= 0.98

        # Cap speed
        if self.v > 40:
            self.v = 40

        # Update distance and points
        distance_gain = max(0, self.v) / 60
        self.distance += distance_gain
        self.points += int(distance_gain * 10)

        # Update gas
        if thrusting and self.gas > 0:
            self.gas -= 0.003  # Reduced from 0.006 to 0.003 (50% slower again)
            # Create exhaust particles
            if random.random() < 0.3:
                exhaust_x = self.rear_screen_x - 25
                exhaust_y = self.rear_y - 10
                self.particles.append(Particle(exhaust_x, exhaust_y))
        else:
            self.gas = max(0, self.gas - 0.0004)  # Reduced from 0.0008 to 0.0004 (50% slower)

        # Update particles
        self.particles = [p for p in self.particles if p.update()]

        # Update wheel rotation
        self.wheel_rot += self.v / self.wheel_radius

        # Reduce crash visual effect
        if self.crash_damage > 0:
            self.crash_damage -= 1

        # Crash conditions
        if abs(self.angle) > math.pi / 2.1:
            self.health -= 2
        
        if self.health <= 0 or self.v < -25 or self.gas <= 0:
            return True

        self.mid_y = (self.rear_y + self.front_y) / 2 - self.chassis_height
        return False

    def get_ground_y(self, sx):
        global path_points
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            if x1 <= sx <= x2:
                t = (sx - x1) / (x2 - x1)
                # Smooth interpolation using cosine
                smooth_t = (1 - math.cos(t * math.pi)) / 2
                return y1 + smooth_t * (y2 - y1)
        return path_points[-1][1] if path_points else HEIGHT - 100

    def draw(self, screen):
        # Draw particles first (behind bike)
        for p in self.particles:
            p.draw(screen)

        s_mid_x = self.screen_x
        s_mid_y = self.mid_y

        # Draw wheels
        for wx, wy in [(self.rear_screen_x, self.rear_y), (self.front_screen_x, self.front_y)]:
            # Outer tire
            pygame.draw.circle(screen, BLACK, (int(wx), int(wy)), self.wheel_radius)
            # Inner rim
            pygame.draw.circle(screen, DARK_GRAY, (int(wx), int(wy)), self.wheel_radius - 4)
            # Hub
            pygame.draw.circle(screen, LIGHT_GRAY, (int(wx), int(wy)), 8)
            
            # Spokes (3 spokes)
            for spoke_angle in [0, 2.09, 4.19]:
                spoke_len = self.wheel_radius - 8
                angle = self.wheel_rot + spoke_angle
                spoke_dx = spoke_len * math.cos(angle)
                spoke_dy = spoke_len * math.sin(angle)
                pygame.draw.line(screen, WHITE, (wx, wy), 
                               (wx + spoke_dx, wy + spoke_dy), 3)

        # Draw bike frame
        frame_points = [
            (self.rear_screen_x, self.rear_y - self.wheel_radius),
            (self.front_screen_x, self.front_y - self.wheel_radius),
            (s_mid_x, s_mid_y - 15)
        ]
        pygame.draw.polygon(screen, BLUE, frame_points)
        pygame.draw.polygon(screen, BLACK, frame_points, 3)

        # Seat
        seat_x = s_mid_x - 10
        seat_y = s_mid_y - 10
        pygame.draw.rect(screen, DARK_GRAY, (seat_x - 15, seat_y - 5, 30, 8))

        # Handlebars
        handle_x = self.front_screen_x - 10
        handle_y = self.front_y - self.wheel_radius - 10
        pygame.draw.line(screen, LIGHT_GRAY, 
                        (handle_x, handle_y), 
                        (handle_x, handle_y - 15), 5)
        pygame.draw.line(screen, LIGHT_GRAY,
                        (handle_x - 10, handle_y - 15),
                        (handle_x + 10, handle_y - 15), 4)

        # Rider
        rider_x = s_mid_x + 5
        rider_y = s_mid_y - 25
        pygame.draw.circle(screen, WHITE, (int(rider_x), int(rider_y)), 12)
        pygame.draw.circle(screen, BLACK, (int(rider_x), int(rider_y)), 12, 2)
        pygame.draw.arc(screen, DARK_BLUE, 
                       (rider_x - 8, rider_y - 3, 16, 10), 0, 3.14, 3)

        # Damage flash effect
        if self.crash_damage > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT))
            flash_surf.set_alpha(self.crash_damage * 10)
            flash_surf.fill(RED)
            screen.blit(flash_surf, (0, 0))
    
    def collect_fuel(self, amount):
        self.gas = min(1.0, self.gas + amount)
        self.points += 50
    
    def collect_health(self, amount):
        self.health = min(100.0, self.health + amount)
        self.points += 50

def generate_smooth_path():
    global path_points
    path_points = []
    x = 0
    y = HEIGHT - 200
    
    # Generate control points for smooth curves
    control_points = [(x, y)]
    
    for _ in range(20):
        x += random.randint(80, 150)
        y_change = random.randint(-80, 80)
        y = max(HEIGHT - 450, min(HEIGHT - 150, y + y_change))
        control_points.append((x, y))
    
    # Interpolate smooth curve through control points
    path_points = []
    for i in range(len(control_points) - 1):
        x1, y1 = control_points[i]
        x2, y2 = control_points[i + 1]
        
        # Create smooth curve segments
        steps = 20
        for step in range(steps):
            t = step / steps
            # Smooth interpolation
            smooth_t = (1 - math.cos(t * math.pi)) / 2
            px = x1 + (x2 - x1) * t
            py = y1 + (y2 - y1) * smooth_t
            path_points.append((px, py))

path_points = []
fuel_cans = []
health_packs = []

def spawn_objects():
    global fuel_cans, health_packs, path_points
    
    if path_points and len(path_points) > 0:
        last_x = path_points[-1][0]
        
        # Get last spawned positions to avoid clustering
        last_fuel_x = fuel_cans[-1].x if fuel_cans else 0
        last_health_x = health_packs[-1].x if health_packs else 0
        
        # Spawn fuel can - with minimum spacing, on ground surface
        if random.random() < 0.025 and (last_x - last_fuel_x) > 200:
            x = last_x + random.randint(100, 300)
            y = get_path_y_at_x(x)  # Ground level
            fuel_cans.append(FuelCan(x, y))
        
        # Spawn health pack - with minimum spacing, on ground surface
        if random.random() < 0.015 and (last_x - last_health_x) > 250:
            x = last_x + random.randint(150, 350)
            y = get_path_y_at_x(x)  # Ground level
            health_packs.append(HealthPack(x, y))

def get_path_y_at_x(target_x):
    global path_points
    for i in range(len(path_points) - 1):
        x1, y1 = path_points[i]
        x2, y2 = path_points[i + 1]
        if x1 <= target_x <= x2:
            t = (target_x - x1) / (x2 - x1)
            smooth_t = (1 - math.cos(t * math.pi)) / 2
            return y1 + smooth_t * (y2 - y1)
    return path_points[-1][1] if path_points else HEIGHT - 200

def draw_intro(screen):
    screen.fill(DARK_BLUE)
    
    title = "HILL CLIMB RACING"
    title_text = FONT_TITLE.render(title, True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)
    
    made_by = "Made by Sanzu"
    made_text = FONT_LARGE.render(made_by, True, BLUE)
    made_rect = made_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(made_text, made_rect)
    
    inst1 = "RIGHT ARROW or D - Accelerate"
    inst1_text = FONT.render(inst1, True, LIGHT_GRAY)
    inst1_rect = inst1_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(inst1_text, inst1_rect)
    
    inst2 = "Collect Fuel & Health Packs"
    inst2_text = FONT.render(inst2, True, LIGHT_GRAY)
    inst2_rect = inst2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
    screen.blit(inst2_text, inst2_rect)
    
    start = "Press SPACE to Start"
    start_text = FONT_LARGE.render(start, True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))
    screen.blit(start_text, start_rect)

def draw_ui(screen, vehicle, score, game_state):
    # Distance
    distance_text = FONT.render(f"Distance: {int(vehicle.distance)}m", True, BLACK)
    screen.blit(distance_text, (20, 20))
    
    # Points
    points_text = FONT.render(f"Points: {vehicle.points}", True, BLACK)
    screen.blit(points_text, (20, 55))
    
    # High Score
    hi_text = FONT.render(f"Best: {int(high_score)}m", True, BLACK)
    hi_rect = hi_text.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(hi_text, hi_rect)
    
    # Health bar
    health_x = WIDTH - 220
    health_y = 55
    health_w = 200
    health_h = 25
    
    pygame.draw.rect(screen, DARK_GRAY, (health_x, health_y, health_w, health_h))
    health_fill = int(health_w * (vehicle.health / 100))
    health_color = BLUE if vehicle.health > 50 else (RED if vehicle.health < 25 else LIGHT_GRAY)
    pygame.draw.rect(screen, health_color, (health_x, health_y, health_fill, health_h))
    pygame.draw.rect(screen, BLACK, (health_x, health_y, health_w, health_h), 3)
    health_label = FONT_SMALL.render("Health", True, BLACK)
    screen.blit(health_label, (health_x, health_y - 20))
    
    # Fuel bar
    fuel_x = 20
    fuel_y = HEIGHT - 60
    fuel_w = 200
    fuel_h = 25
    
    pygame.draw.rect(screen, DARK_GRAY, (fuel_x, fuel_y, fuel_w, fuel_h))
    fuel_fill = int(fuel_w * vehicle.gas)
    fuel_color = BLUE if vehicle.gas > 0.3 else RED
    pygame.draw.rect(screen, fuel_color, (fuel_x, fuel_y, fuel_fill, fuel_h))
    pygame.draw.rect(screen, BLACK, (fuel_x, fuel_y, fuel_w, fuel_h), 3)
    fuel_label = FONT_SMALL.render("Fuel", True, BLACK)
    screen.blit(fuel_label, (fuel_x, fuel_y - 20))

def draw_game_over(screen, vehicle):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    crashed_text = FONT_TITLE.render("CRASHED!", True, WHITE)
    crashed_rect = crashed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(crashed_text, crashed_rect)
    
    dist_text = FONT_LARGE.render(f"Distance: {int(vehicle.distance)}m", True, BLUE)
    dist_rect = dist_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(dist_text, dist_rect)
    
    pts_text = FONT_LARGE.render(f"Points: {vehicle.points}", True, BLUE)
    pts_rect = pts_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(pts_text, pts_rect)
    
    best_text = FONT.render(f"Best: {int(high_score)}m", True, LIGHT_GRAY)
    best_rect = best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(best_text, best_rect)
    
    restart_text = FONT_LARGE.render("Press SPACE to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))
    screen.blit(restart_text, restart_rect)

def main():
    global high_score, path_points, fuel_cans, health_packs

    # Load high score at start
    load_high_score()

    vehicle = Vehicle()
    generate_smooth_path()
    score = 0
    game_state = INTRO

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        keys = pygame.key.get_pressed()
        thrusting = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == INTRO:
                        game_state = PLAYING
                    elif game_state == GAME_OVER:
                        vehicle.reset()
                        generate_smooth_path()
                        fuel_cans.clear()
                        health_packs.clear()
                        score = 0
                        game_state = PLAYING

        if game_state == INTRO:
            draw_intro(screen)
        
        elif game_state == PLAYING:
            screen.fill(SKY_BLUE)
            
            crashed = vehicle.update(thrusting)
            if crashed:
                game_state = GAME_OVER
                if vehicle.distance > high_score:
                    high_score = vehicle.distance
                    save_high_score()  # Save when new high score is achieved

            # Scroll speed
            scroll_speed = vehicle.v * math.cos(vehicle.angle)
            
            # Scroll path
            for i in range(len(path_points)):
                path_points[i] = (path_points[i][0] - scroll_speed, path_points[i][1])

            # Remove offscreen left
            while path_points and path_points[0][0] < -50:
                path_points.pop(0)

            # Add new path segments
            if len(path_points) < 100:
                last_x, last_y = path_points[-1]
                new_x = last_x + random.randint(80, 150)
                y_change = random.randint(-80, 80)
                new_y = max(HEIGHT - 450, min(HEIGHT - 150, last_y + y_change))
                
                # Add interpolated points
                steps = 20
                for step in range(1, steps + 1):
                    t = step / steps
                    smooth_t = (1 - math.cos(t * math.pi)) / 2
                    px = last_x + (new_x - last_x) * t
                    py = last_y + (new_y - last_y) * smooth_t
                    path_points.append((px, py))

            # Spawn objects
            spawn_objects()
            
            # Update and check fuel cans
            for fuel in fuel_cans[:]:
                fuel.update(scroll_speed)
                if fuel.check_collision(vehicle):
                    vehicle.collect_fuel(0.4)  # Increased from 0.3 to 0.4 (40% refill)
                if fuel.x < -50:
                    fuel_cans.remove(fuel)
            
            # Update and check health packs
            for health in health_packs[:]:
                health.update(scroll_speed)
                if health.check_collision(vehicle):
                    vehicle.collect_health(30)
                if health.x < -50:
                    health_packs.remove(health)

            # Draw smooth path
            if path_points:
                # Draw path surface
                visible_points = [(max(0, p[0]), p[1]) for p in path_points if -50 <= p[0] <= WIDTH + 50]
                if len(visible_points) > 2:
                    # Smooth curve
                    pygame.draw.lines(screen, BLACK, False, visible_points, 8)
                    # Fill below
                    ground_poly = visible_points + [(WIDTH, HEIGHT), (0, HEIGHT)]
                    pygame.draw.polygon(screen, GROUND_GRAY, ground_poly)

            # Draw objects
            for fuel in fuel_cans:
                fuel.draw(screen)
            for health in health_packs:
                health.draw(screen)

            vehicle.draw(screen)
            draw_ui(screen, vehicle, score, game_state)
        
        elif game_state == GAME_OVER:
            screen.fill(SKY_BLUE)
            
            if path_points:
                visible_points = [(max(0, p[0]), p[1]) for p in path_points if -50 <= p[0] <= WIDTH + 50]
                if len(visible_points) > 2:
                    pygame.draw.lines(screen, BLACK, False, visible_points, 8)
                ground_poly = visible_points + [(WIDTH, HEIGHT), (0, HEIGHT)]
                pygame.draw.polygon(screen, GROUND_GRAY, ground_poly)
            
            for fuel in fuel_cans:
                fuel.draw(screen)
            for health in health_packs:
                health.draw(screen)
            
            vehicle.draw(screen)
            draw_ui(screen, vehicle, score, game_state)
            draw_game_over(screen, vehicle)

        pygame.display.flip()

if __name__ == "__main__":
    main()