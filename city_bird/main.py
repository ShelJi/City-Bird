import asyncio
import pygame
import random

import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

pygame.font.init()


class Player:
	def __init__(self, win):
		self.win = win
		
		self.image = pygame.image.load(f"Assets/red.png")
		self.image = pygame.transform.scale(self.image, (44,44))
		self.reset()
		
	def update(self):
		self.win.blit(self.image, self.rect)
		
	def reset(self):
		self.x = 145
		self.y = 270
		self.rect = self.image.get_rect(center=(self.x,self.y))

class Bar(pygame.sprite.Sprite):
	def __init__(self, x, y, width, color, win):
		super(Bar, self).__init__()
		
		self.rect = pygame.Rect(x, y, width, 20, border_radius = 8)
		self.win = win
		self.color = color
		
	def update(self, speed):
		self.rect.y += speed
		if self.rect.y >= HEIGHT:
			self.kill()
		self.win.fill(self.color, self.rect)
		
class Ball(pygame.sprite.Sprite):
	def __init__(self, x, y, type, color, win):
		super(Ball, self).__init__()
		
		self.x = x
		self.y = y
		self.color = color
		self.win = win

		color_dict = {"red" : (255, 0, 0), "white" : (255, 255, 255), "gray" : (54, 69, 79)}
		self.c = color_dict[self.color]
		self.rect = pygame.draw.circle(win, self.c, (x,y), 5)
		
		self.gray = color_dict["gray"]
		
	def update(self, speed):
		self.y += speed
		if self.y >= HEIGHT:
			self.kill()
		
		pygame.draw.circle(self.win, self.gray, (self.x+2, self.y+2), 6)
		self.rect = pygame.draw.circle(self.win, self.c, (self.x,self.y), 6)
		

class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, max, win):
		super(Block, self).__init__()
		
		self.win = win
		self.scale = 1
		self.counter = 0
		self.inc = 1
		self.x = x
		self.y = y
		self.max = max
		
		self.orig = pygame.image.load("Assets/block.jpeg")
		self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))
		self.rect = self.image.get_rect(center=(x,y))
		
	def update(self):
		self.counter += 1
		if self.counter >= 2:
			self.scale += self.inc
			if self.scale <= 0 or self.scale >= self.max:
				self.inc *= -1
			self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))
			self.rect = self.image.get_rect(center= (self.x, self.y))
			
			self.counter = 0
			
		self.win.blit(self.image, self.rect)
		
class ScoreCard:
	def __init__(self, x, y, win):
		self.win = win
		self.size = 50
		self.inc = 1
		self.animate = False
		
		self.style = "Fonts/BubblegumSans-Regular.ttf"
		self.font= pygame.font.Font(self.style, self.size)

		self.image = self.font.render("0", True, (255, 255, 255))
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow_rect = self.image.get_rect(center=(x+3, y+3))
		
	def update(self, score):
		if self.animate:
			self.size += self.inc
			self.font = pygame.font.Font(self.style, self.size)
			if self.size <= 50 or self.size >= 65:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, (255, 255, 255))
		shadow = self.font.render(f"{score}", True,(54, 69, 79) )	
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)
		

class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow = self.font.render(text, anti_alias, (54,69,79))
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self):
		self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)
		
		
class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, size, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4,7)
		if size == 0:
			xr = (-1, 2)
			yr = (-2, 2)
			f = 1
			self.life = 60
		elif size == 1:
			xr = (-3,3)
			yr = (-6,6)
			f = 2
			self.life = 60
		elif size == 2:
			xr = (-3,3)
			yr = (-3,3)
			f = 2
			self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0
			
	def update (self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y,s,s))
		else:
			self.kill()
		
		
def generate_particles(p, particles, color, win):
	particle_pos = list(p.rect.center)
	particle_pos[1] += 25
		
	particles.append([particle_pos, [random.randint(0,20) / 10 - 1, -2], random.randint(4,8)])
	for particle in particles:
		particle[0][0] -= particle [1][0]
		particle[0][1] -= particle [1][1]
		particle [2] -= 0.1
		pygame.draw.circle(win, color, particle [0], int(particle [2]))
		#pygame.draw.rect(win, color, (particle[0][0], particle [0][1], int(particle[2]), int(particle[2])))
		if particle [2] <= 0:
			particles.remove(particle)
			
	return particles


pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN)
else:
	win = pygame.display.set_mode(SCREEN)

clock = pygame.time.Clock()
FPS = 45

# COLORS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (54, 69, 79)
c_list = [RED, BLACK, WHITE]

# Fonts

pygame.font.init()
try:
    score_font = pygame.font.Font('Fonts/BubblegumSans-Regular.ttf', 50)
    print("Loaded font: BubblegumSans-Regular.ttf")
except Exception as e:
    print("Font load error:", e)
    score_font = pygame.font.SysFont(None, 50)

# Sounds

def safe_load_sound(path):
    try:
        s = pygame.mixer.Sound(path)
        print(f"Loaded sound: {path}")
        return s
    except Exception as e:
        print(f"Sound load error for {path}: {e}")
        return None

coin_fx = safe_load_sound('Sounds/coin.mp3')
death_fx = safe_load_sound('Sounds/death.mp3')
move_fx = safe_load_sound('Sounds/move.mp3')

# backgrounds

bg_list = []
for i in range(1,5):
    if i == 2:
        ext = "jpeg"
    else:
        ext = "jpg"
    try:
        img = pygame.image.load(f"Assets/Backgrounds/bg{i}.{ext}")
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        bg_list.append(img)
        print(f"Loaded background: bg{i}.{ext}")
    except Exception as e:
        print(f"Background load error for bg{i}.{ext}: {e}")

try:
    home_bg = pygame.image.load(f"Assets/Backgrounds/home.jpeg")
    print("Loaded background: home.jpeg")
except Exception as e:
    print("Background load error for home.jpeg:", e)
    home_bg = pygame.Surface((WIDTH, HEIGHT))
    home_bg.fill((0,0,0))

bg = home_bg

# objects
bar_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
destruct_group = pygame.sprite.Group()
win_particle_group = pygame.sprite.Group()
bar_gap = 120
	
particles = []

p = Player(win)
score_card = ScoreCard(140, 40, win)

# Functions

def destroy_bird():
	x, y = p.rect.center
	for i in range (50):
		c = random.choice(c_list)
		particle = Particle(x,y, 1,c, win)
		destruct_group.add(particle)
		
def win_particles():
	for x,y in [(40, 120), (WIDTH - 20, 240), (15, HEIGHT - 30)]:
		for i in range(10):
			particle = Particle (x,y, 2, WHITE, win)
			win_particle_group.add(particle)

# Messages
title_font = "Fonts/Robus-BWqOd.otf"
dodgy = Message(134, 90, 100, "City",title_font, WHITE, win)
walls = Message(164, 145, 80, "Bird",title_font, WHITE, win)

tap_to_play_font = "Fonts/DebugFreeTrial-MVdYB.otf"
tap_to_play = Message(144, 400, 32, "TAP TO PLAY",tap_to_play_font, WHITE, win)
tap_to_replay = Message(144, 400, 30, "Tap to Replay",tap_to_play_font, WHITE, win)

# Variables

bar_width_list = [i for i in range (40,150,10)]
bar_frequency = 1200
bar_speed = 4
touched = False
pos = None
home_page = True
score_page = False
bird_dead = False
score = 0
high_score = 0
move_left = False
move_right = True
prev_x = 0
p_count = 0
score_msg = None
score_point = None

running = True
async def main():
    print("main() started")
    global running, home_page, score_page, bird_dead, score, high_score, move_left, move_right, prev_x, p_count, particles, bar_speed, bar_frequency, touched, pos, last_bar, next_bar, score_list, bg, score_msg, score_point
    try:
        while running:
            print(f"Loop: running={running}, home_page={home_page}, score_page={score_page}, bird_dead={bird_dead}, score={score}")
            win.blit(bg, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and (home_page or score_page):
                    print("Game reset/replay triggered")
                    home_page = False
                    score_page = False
                    win_particle_group.empty()
                    bg = random.choice(bg_list)
                    particles = []
                    last_bar = pygame.time.get_ticks() - bar_frequency
                    next_bar = 0
                    bar_speed = 4
                    bar_frequency = 1200
                    bird_dead = False
                    score = 0
                    p_count = 0
                    score_list = []
                    score_msg = None
                    score_point = None
                    for _ in range(15):
                        x = random.randint(30, WIDTH - 30)
                        y = random.randint(60, HEIGHT - 60)
                        max = random.randint(8,16)
                        b = Block(x,y,max, win)
                        block_group.add(b)
                if event.type == pygame.MOUSEBUTTONDOWN and not home_page:
                    if p.rect.collidepoint(event.pos):
                        touched = True
                        x, y = event.pos
                        offset_x = p.rect.x - x
                if event.type == pygame.MOUSEBUTTONUP and not home_page:
                    touched = False
                if event.type == pygame.MOUSEMOTION and not home_page:
                    if touched:
                        x, y = event.pos
                        if move_right and prev_x > x:
                            move_right = False
                            move_left = True
                            if move_fx:
                                move_fx.play()
                        if move_left and  prev_x < x:
                            move_right = True
                            move_left = False
                            if move_fx:
                                move_fx.play()
                        prev_x = x
                        p.rect.x =  x + offset_x
            if home_page:
                bg = home_bg
                particles = generate_particles(p, particles, WHITE, win)
                dodgy.update()
                walls.update()
                tap_to_play.update()
                p.update()
            elif score_page:
                bg = home_bg
                particles = generate_particles(p, particles, WHITE, win)
                tap_to_replay.update()
                p.update()
                if score_msg is not None:
                    score_msg.update()
                if score_point is not None:
                    score_point.update()
                if p_count % 5 == 0:
                    win_particles()
                p_count += 1
                win_particle_group.update()
            else:
                next_bar = pygame.time.get_ticks()
                if next_bar - last_bar >= bar_frequency and not bird_dead:
                    bwidth = random.choice(bar_width_list)
                    b1prime = Bar(0,0,bwidth+3,GRAY, win)
                    b1 = Bar(0,-3,bwidth,WHITE,win)
                    b2prime = Bar(bwidth+bar_gap+3, 0, WIDTH - bwidth - bar_gap, GRAY, win)
                    b2 = Bar(bwidth+bar_gap, -3, WIDTH - bwidth - bar_gap, WHITE, win)
                    bar_group.add(b1prime)
                    bar_group.add(b1)
                    bar_group.add(b2prime)
                    bar_group.add(b2)
                    color = random.choice(["red", "white"])
                    pos = random.choice([0,1])
                    if pos == 0:
                        x = bwidth + 12
                    elif pos == 1:
                        x = bwidth + bar_gap - 12
                    ball = Ball(x, 10, 1, color, win)
                    ball_group.add(ball)
                    last_bar = next_bar
                for ball in ball_group:
                    if ball.rect.colliderect(p):
                        if ball.color == "white":
                            ball.kill()
                            if coin_fx:
                                coin_fx.play()
                            score += 1
                            if score > high_score:
                                high_score += 1
                            score_card.animate = True
                        elif ball.color == "red":
                            if not bird_dead:
                                if death_fx:
                                    death_fx.play()
                                destroy_bird()
                            bird_dead = True
                            bar_speed = 0
                if pygame.sprite.spritecollide(p, bar_group, False):
                    if not bird_dead:
                        if death_fx:
                            death_fx.play()
                        destroy_bird()
                    bird_dead = True
                    bar_speed = 0
                block_group.update()
                bar_group.update(bar_speed)
                ball_group.update(bar_speed)
                if bird_dead:
                    destruct_group.update()
                score_card.update(score)
                if not bird_dead:
                    particles = generate_particles(p, particles, WHITE, win)
                    p.update()
                if score and score % 10 == 0:
                    rem = score // 10
                    if rem not in score_list:
                        score_list.append(rem)
                        bar_speed += 1
                        bar_frequency -= 200
                if bird_dead and len(destruct_group) == 0:
                    print("Switching to score_page")
                    score_page = True
                    font =  "Fonts/BubblegumSans-Regular.ttf"
                    if score < high_score:
                        score_msg = Message(144, 60, 55, "Score",font, WHITE, win)
                    else:
                        score_msg = Message(144, 60, 55, "New High",font, WHITE, win)
                    score_point = Message(144, 110, 45, f"{score}", font, WHITE, win)
                if score_page:
                    block_group.empty()
                    bar_group.empty()
                    ball_group.empty()
                    p.reset()
            clock.tick(FPS)
            pygame.display.update()
            await asyncio.sleep(0)
    except Exception as e:
        import traceback
        print("Exception in main loop:", e)
        traceback.print_exc()
    print("main() ended")
    pygame.quit()

asyncio.run(main())