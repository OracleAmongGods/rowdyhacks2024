#!/usr/bin/env python3
 
#
# pygame (simple) template - by furas
#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#
 
# ---------------------------------------------------------------------
 
import pygame
 
# === CONSTANTS === (UPPER_CASE names)
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
 
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
 
SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 900
 
BLOCK_SIZE = 50
#CIRCLE_RADIUS = int(BLOCK_SIZE/2)

BLOCK_WIDTH = 75
BLOCK_HEIGHT = 50
 
# === CLASSES === (CamelCase names)
 
class Button():
 
    def __init__(self, text='OK', pos=(0,0), size=(100,50), command=None):
        font = pygame.font.SysFont(None, 35)
   
        self.text = text
        self.rect = pygame.Rect((0,0), size)
 
        self.image_normal = pygame.Surface(size)
        self.image_normal.fill(WHITE)
        txt_image = font.render(self.text, True, RED)
        txt_rect = txt_image.get_rect(center=self.rect.center)
        self.image_normal.blit(txt_image, txt_rect)
       
        self.image_hover = pygame.Surface(size)
        self.image_hover.fill(RED)
        txt_image = font.render(self.text, True, WHITE)
        txt_rect = txt_image.get_rect(center=self.rect.center)
        self.image_hover.blit(txt_image, txt_rect)
 
        self.rect.topleft = pos
       
        self.hover = False

        if command:
            self.command = command
 
    def draw(self, screen):
        if self.hover:
            screen.blit(self.image_hover, self.rect)
        else:
            screen.blit(self.image_normal, self.rect)
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
 
        if self.hover and self.command:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.command()
                   
    def command(self):
        print("Click")
 
# === FUNCTIONS === (lower_case names)
 
def print_hello():
    print("Click HELLO")
 
def print_world():
    print("Click WORLD")
 
# === MAIN === (lower_case names)
 
# --- (global) variables ---
 
# --- init ---
 
pygame.init()
pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont('bitstreamverasans', 36)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
# --- objects ---
 
# - buttons -
 
button1 = Button(text="HELLO") # create button
button1.command = print_hello # assign function to button
 
button2 = Button(text="WORLD", pos=(110,0), command=print_world) # create button and assign function
 
# - squares -
 
squares = []
 
for x in range(10):
    squares.append( pygame.Rect(x*(BLOCK_SIZE+5), BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT) )
 
# - drag -
 
selected = None
   
# --- mainloop ---
 
clock = pygame.time.Clock()
is_running = True
 
while is_running:
 
    # --- events ---
   
    for event in pygame.event.get():
 
        # --- global events ---
       
        if event.type == pygame.QUIT:
            is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, s in enumerate(squares):
                    # Pythagoras A^2 + B^2 = C^2
                    mx = event.pos[0] # A
                    my = event.pos[1] # B
 
                    if mx > s.x and my > s.y and mx < s.x + s.w and my < s.y + s.h : # C^2 <= RADIUS^2
                        selected = i
                        selected_offset_x = s.x - event.pos[0]
                        selected_offset_y = s.y - event.pos[1]
               
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = None
               
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                squares[selected].x = event.pos[0] + selected_offset_x
                squares[selected].y = event.pos[1] + selected_offset_y
               
        # --- objects events ---
 
        button1.handle_event(event)
        button2.handle_event(event)
       
    # --- updates ---
 
        # empty
       
    # --- draws ---
   
    screen.fill(BLACK)
 
    button1.draw(screen)    
    button2.draw(screen)    
   
    # draw rect
    i = 1
    for s in squares:
        tmp = DEFAULT_FONT.render(str(i), False, BLACK)
        pygame.draw.rect(screen, RED, s)
        screen.blit(tmp, (s.x, s.y))
        i += 1
       
    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(30)
 
# --- the end ---
 
pygame.quit()
pygame.font.quit()
