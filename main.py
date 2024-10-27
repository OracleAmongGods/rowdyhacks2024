#!/usr/bin/env python3
 
#
# pygame (simple) template - by furas
#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#
 
# ---------------------------------------------------------------------
 
import pygame
import math
from enum import Enum
 
# === CONSTANTS === (UPPER_CASE names)
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
 
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
 
SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 900
 
BLOCK_SIZE = 50

BLOCK_WIDTH = 75
BLOCK_HEIGHT = 50

class BLOCKS(Enum):
    START = 1
    SET_VARIABLE = 2
    DO_OP_ON_VARIABLE = 3
    OUTPUT_VARIABLE = 4
 
# === SHENANIGANS === (CamelCase names)

def spawn_block():
    pass

def gen_code_to_file():
    out = generate_code()
    with open("out.py", "w") as f:
        f.write(out)

def generate_code(top_level_block=None):
    global blocks
    if(top_level_block is None):
        top_level_block = blocks[0]
    output = ""
    stack = []
    current_block = top_level_block
    while (current_block is not None):
        print(current_block.opts["type"])
        current_line = "\t" * (len(stack))
        if(current_block.opts["type"] is BLOCKS.START):
            current_block = current_block.child
            continue
        elif(current_block.opts["type"] is BLOCKS.SET_VARIABLE):
            current_line += current_block.opts["var"] + "=" + str(current_block.opts["val"])
        elif(current_block.opts["type"] is BLOCKS.DO_OP_ON_VARIABLE):
            current_line += current_block.opts["var"] + current_block.opts["op"] + "=" + str(current_block.opts["val"])
        elif(current_block.opts["type"] is BLOCKS.OUTPUT_VARIABLE):
            current_line += "print(" + current_block.opts["var"] + ")"
        output += current_line + "\n"
        current_block = current_block.child
    return output

class Block():
    def __init__(self, col, opts={"type":BLOCKS.DEBUG}, pos=(0,0), size=(100,50), parent=None):
        self.col = col
        self.opts = opts
        
        self.font = pygame.font.SysFont("bitstreamverasans", 24)

        self.parent = parent
   
        # self.text = opts["type"]
        self.type = opts["type"]
        self.rect = pygame.Rect(pos, size)
 
        # self.image_normal = pygame.Surface(size)
        # self.image_normal.blit(self.spr, (0,0), pygame.Rect((0,0), size))
        # txt_image = self.font.render(self.text, True, BLACK)
        # txt_rect = txt_image.get_rect()
        # self.image_normal.blit(txt_image, txt_rect)
       
        # self.image_hover = pygame.Surface(size)
        # self.image_hover.blit(self.spr, (0,0), pygame.Rect((0,0), size))
        # txt_image = self.font.render(self.text, True, WHITE)
        # txt_rect = txt_image.get_rect(center=self.rect.center)
        # self.image_hover.blit(txt_image, txt_rect)

        self.rect.topleft = pos
        self.pos = pos
        self.size = size
       
        self.hover = False

        self.child = None
        
        self.update_text()

    

    def update_text(self):
        text = ""
        if(self.opts["type"] is BLOCKS.START):
            text = "Start"
        elif(self.opts["type"] is BLOCKS.SET_VARIABLE):
            text = "Set " + self.opts["var"] + " to " + str(self.opts["val"])
        elif(self.opts["type"] is BLOCKS.DO_OP_ON_VARIABLE):
            text = self.opts["var"] + " = " + self.opts["var"] + " " + self.opts["op"] + " " + str(self.opts["val"])
        elif(self.opts["type"] is BLOCKS.OUTPUT_VARIABLE):
            text = "Output " + self.opts["var"] + " to the console"
        self.text = text
        self.resize_image()

    def resize_image(self):

        txt_image = self.font.render(str(self.text), True, BLACK)
        txt_rect = txt_image.get_rect()

        self.size = (max(txt_rect.width+25, 150),50)
        self.rect = pygame.Rect((0,0), self.size)

        self.image_normal = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image_normal.fill(self.col)
        # self.image_normal.blit(self.spr, (0,0), pygame.Rect((0,0), self.size))
        self.image_normal.blit(txt_image, txt_rect)

        self.image_hover = pygame.Surface(self.size)
        # self.image_hover.blit(self.spr, (0,0), pygame.Rect((0,0), self.size))
        self.image_hover.blit(txt_image, txt_rect)
 
    def draw(self, screen):
        if self.hover:
            screen.blit(self.image_hover, self.pos)
        else:
            screen.blit(self.image_normal, self.pos)
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
 
        if self.hover and self.command:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Click")
    
    def move_to(self, pos):
        self.pos = pos
        self.rect.topleft = pos
        if(self.child is not None):
            self.child.move_to((pos[0], pos[1]+self.size[1]))

    def connect_to(self, parent):
        self.parent = parent
        parent.child = self
 
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
        self.size = size
       
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

# === MAIN === (lower_case names)
 
# --- (global) variables ---
 
# --- init ---


 
pygame.init()
pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont('bitstreamverasans', 36)


spawn_block_button = Button(text="TEST", pos=(0,0), command=spawn_block) # create button and assign function
test_button = Button(text="TEST", pos=(110,0), command=gen_code_to_file) # create button and assign function
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
blocks = []

blocks.append(Block((255, 0, 0), {
    "type":  BLOCKS.START
},(200, 100), (114, 58)))

blocks.append(Block((255, 0, 0), {
    "type":  BLOCKS.SET_VARIABLE,
    "var": "x",
    "val": 5
},(200, 100), (114, 58)))

blocks.append(Block((255, 0, 0), {
    "type":  BLOCKS.DO_OP_ON_VARIABLE,
    "var": "x",
    "op": "*",
    "val": "x"
},(200, 100), (114, 58)))

blocks.append(Block((255, 0, 0), {
    "type":  BLOCKS.OUTPUT_VARIABLE,
    "var": "x",
},(200, 100), (114, 58)))

blocks[1].connect_to(blocks[0])
blocks[2].connect_to(blocks[1])
blocks[0].move_to((200, 100))

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
                for i, s in enumerate(blocks):
                    # Pythagoras A^2 + B^2 = C^2
                    mx = event.pos[0] # A
                    my = event.pos[1] # B
 
                    if mx > s.pos[0] and my > s.pos[1] and mx < s.pos[0] + s.size[0] and my < s.pos[1] + s.size[1] :
                        selected = i
                        selected_offset_x = s.pos[0] - event.pos[0]
                        selected_offset_y = s.pos[1] - event.pos[1]
               
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if(selected is not None):
                    for i, b in enumerate(blocks):
                        if(b.rect.collidepoint(event.pos) and b is not blocks[selected] and b.child is None):
                            blocks[selected].connect_to(b)
                            blocks[selected].move_to((b.pos[0], b.pos[1] + b.size[1]))
                            break
                selected = None
               
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                if(blocks[selected].parent is not None):
                    blocks[selected].parent.child = None
                blocks[selected].move_to((event.pos[0] + selected_offset_x, event.pos[1] + selected_offset_y))
               
        # --- objects events ---
        
        test_button.handle_event(event)
       
    # --- updates ---
 
        # empty
       
    # --- draws ---
   
    screen.fill((64, 64, 64))

    
    test_button.draw(screen) 
    
   
    # draw rect
    i = 1
    for s in blocks:
        s.draw(screen)
       
    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(30)
 
# --- the end ---
 
pygame.quit()
pygame.font.quit()
