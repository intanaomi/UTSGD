import pygame,sys,random
from pygame.math import Vector2
import main

#membuat ular/ snake
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]#MEMBUAT BADAN ULAR
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_upB.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_downB.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_rightB.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_leftB.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_verticalb.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontalb.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()


        self.crunch_sound = pygame.mixer.Sound('Sound/suara.wav')# MEMBUAT SUARA KETIKA ULAR MEMAKAN BUAH

    def draw_snake(self):#MEMBUAT BADAN ULAR
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            # 1. We Still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            #2.  what direction is the face heading
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:     
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)                   
                    

    def update_head_graphics(self):# membuat kepala ular
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down




    def move_snake(self):#UNTUK MENGGERAKKAN ULAR
        if self.new_block == True:#memanjangkan tubuh ular tidak teratur(panjang nya ngawur)
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False #mengatur panjang tubuh ular setiap makan buah(fruit) secara teratur
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):#memanjangkan tubuh ular
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):# JIKA ULAR MENABRAK SUDUT ATAU BADANYA SENDIRI MAKA AKAN MERESTRART ATAU MULAI AWAL LAGI
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]


#Objek yang akan dikejar oleh ular
class FRUIT:
    def __init__(self): 
        self.randomize()#digunakan untuk memidahkan fruit secara random

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(255, 20, 147, 1),fruit_rect)

    def randomize(self):#digunakan untuk memidahkan fruit secara random SETELAH DIMAKAN OLEH ULAR
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:#DIGUNAKAN UNTUK MENGONTROL GAMENYA
      def __init__(self):
          self.snake = SNAKE()
          self.fruit = FRUIT()

      def update(self):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()# JIKA ULAR MENABRAK SUDUT2 MAKA LANGSUNG KELUAR GAME

      def draw_element(self):
           self.draw_grass()
           self.fruit.draw_fruit()
           self.snake.draw_snake()
           self.draw_score()

      def check_collision(self):
          if self.fruit.pos == self.snake.body[0]:
              self.fruit.randomize()#digunakan untuk memidahkan fruit secara random
              self.snake.add_block()
              self.snake.play_crunch_sound()# MEMBUAT SUARA KETIKA ULAR MEMAKAN BUAH
             
          for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()
              # reposition the fruit
              # add another block to the snake

      def check_fail(self):# JIKA ULAR MENABRAK SUDUT2 MAKA LANGSUNG KELUAR GAME
           if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                self.game_over()

           for block in self.snake.body[1:]:# JIKA ULAR MENABRAK DIRINYA SENDIRI MAKA LANGSUNG KELUAR GAME
               if block == self.snake.body[0]:
                   self.game_over()

            
          # CHECK IF SNAKE THIS HITS ITSELF
      def game_over(self):# JIKA ULAR MENABRAK SUDUT2 MAKA LANGSUNG KELUAR GAME
          self.snake.reset()#JIKA ULAR MENABRAK SUDUT2 MAKA AKAN MERESTRART

      def draw_grass(self):# DIGUNAKAN UNTUK MEMBUAT KOTAK-KOTAK DALAM LAYAR
          grass_color = (19, 109, 21) 
          for row in range(cell_number):
               if row & 2 == 0:
                    for col in range(cell_number):
                        if col % 2 == 0:
                         grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size) # ROW * CELL_SIZE UNTUK MEMBUAT KOTAK KOTAK HITAM DI DALAM GAME
                        pygame.draw.rect(screen,grass_color,grass_rect)

               else: #MEMBUAT TAMPLAN KOTAK LEBIH BERDEMPETAN
                    for col in range(cell_number):
                        if col % 2 != 0:
                         grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size) # ROW * CELL_SIZE UNTUK MEMBUAT KOTAK KOTAK HITAM DI DALAM GAME
                        pygame.draw.rect(screen,grass_color,grass_rect)

      def draw_score(self): # MEMBUAT ANGKA / SCORE YANG TERUS BERTAMBAH JIKA ULAR MEMAKAN BUAH
          score_text = str(len(self.snake.body) - 3) 
          score_surface = game_font.render(score_text,True,(0, 0, 255, 1))#WARNA ANGKA
          score_x = int(cell_size * cell_number - 60)
          score_y = int(cell_size * cell_number - 40)
          score_rect = score_surface.get_rect(center = (score_x,score_y))
          apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))#MEMBUAT GAMBAR DISAMPING ANGKA
          bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width ,apple_rect.height)#MEMBUAT GARIS KOTAK DI DALAM ANGKA DAN GAMBAR
          
          pygame.draw.rect(screen,(167,209,61),bg_rect) #BACKGROUND WARNA DALAM ANGKA
          screen.blit(score_surface,score_rect) 
          screen.blit(apple,apple_rect) #MEMBUAT GAMBAR DISAMPING ANGKA               
          pygame.draw.rect(screen,(56,74,12),bg_rect,2)#WARNA KOTAK DALAM ANGKA DAN GAMBAR
          
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 25
cell_number = 28
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apel2.png').convert_alpha() #UNTUK MEMASUKAN GAMBAR BUAH(OBJEK YANG AKAN DIMAKAN OLEH ULAR)
game_font = pygame.font.Font('Font/Romelio.ttf', 25) #UNTUK MEMASUKAN FONT

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
                main_game.update()
                #UNTUK MENGARAHKAN ULAR DENGAN TOMBOL DI KEYBOARD ATAS,BAWAH,KANAN,KIRI
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1: #DIGUNAKAN AGAR SAAT MENEKAN ARAH TIDAK LANGSUNG KELUAR GAME
                     main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                     main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                     main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                     main_game.snake.direction = Vector2(-1,0)

    screen.fill((65, 152, 10))
    main_game.draw_element()
    pygame.display.update()
    clock.tick(60)

