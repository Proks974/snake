import pygame, sys, random
from pygame.math import Vector2  #así no estamos todo el rato escribiendo pygame.math cada vez que queramos manipular el vector

# CLASES

class Fruta:
    def __init__(self):
        #creamos posicion x,y 
        self.randomize()
        
    def dibujar_fruta(self):
        fruta_rect= pygame.Rect(int(self.pos.x * size_cel), int(self.pos.y * size_cel), size_cel, size_cel)
        screen.blit(manzana, fruta_rect)
        #pygame.draw.rect(screen, (126,166,114), fruta_rect)
        
    def randomize(self):
        self.x = random.randint(0, number_cel - 1)
        self.y = random.randint(0, number_cel - 1)
        self.pos= Vector2(self.x, self.y)
        
class Snake:
    def __init__(self):
        self.cuerpo = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direccion = Vector2(0,0) 
        self.new_block = False
        
        #CABEZA
        self.cabezaup = pygame.image.load('imagenes/cabezaup.png').convert_alpha()
        self.cabezadown = pygame.image.load('imagenes/cabezadown.png').convert_alpha()
        self.cabezader = pygame.image.load('imagenes/cabezader.png').convert_alpha()
        self.cabezaizq = pygame.image.load('imagenes/cabezaizq.png').convert_alpha()
        
        #COLA
        self.puntacolaup = pygame.image.load('imagenes/puntacolaup.png').convert_alpha()
        self.puntacoladown = pygame.image.load('imagenes/puntacoladown.png').convert_alpha()
        self.puntacolader = pygame.image.load('imagenes/puntacolader.png').convert_alpha()
        self.puntacolaizq = pygame.image.load('imagenes/puntacolaizq.png').convert_alpha()
        
        #CUERPO
        self.cuerpohorizontal = pygame.image.load('imagenes/cuerpohorizontal.png').convert_alpha()
        self.cuerpovertical = pygame.image.load('imagenes/cuerpovertical.png').convert_alpha()
        
        #GIROS
        self.giroarribader = pygame.image.load('imagenes/giroarribader.png').convert_alpha()
        self.giroarribaizq = pygame.image.load('imagenes/giroarribaizq.png').convert_alpha()
        self.giroabajoder = pygame.image.load('imagenes/giroabajoder.png').convert_alpha()
        self.giroabajoizq = pygame.image.load('imagenes/giroabajoizq.png').convert_alpha()
               
    def dibujar_snake(self):
        self.update_cabeza_graf()
        self.update_puntacola_graf()
        
        for index, block in enumerate(self.cuerpo):
            # necesitamos rectangulo por posicionamiento
            x_pos = int(block.x * size_cel)
            y_pos = int(block.y * size_cel)
            block_rect = pygame.Rect(x_pos, y_pos, size_cel, size_cel)
            # luego editamos la direccion y el sentido
            if index == 0:
                screen.blit(self.cabeza, block_rect)
                # tenemos que actualizar la imagen en funcion de la direccion
            elif index == len(self.cuerpo) -1:
                screen.blit(self.puntacola, block_rect)
            else:
                block_previo = self.cuerpo[index + 1] - block
                block_siguiente = self.cuerpo[index - 1] - block
                if block_previo.x == block_siguiente.x:
                    screen.blit(self.cuerpovertical, block_rect)
                elif block_previo.y == block_siguiente.y:
                    screen.blit(self.cuerpohorizontal, block_rect)
                else:
                    if block_previo.x == -1 and block_siguiente.y == -1 or block_previo.y == -1 and block_siguiente.x == -1:
                        screen.blit(self.giroabajoizq, block_rect)
                    elif block_previo.x == -1 and block_siguiente.y == 1 or block_previo.y == 1 and block_siguiente.x == -1:
                        screen.blit(self.giroarribaizq, block_rect)
                    elif block_previo.x == 1 and block_siguiente.y == -1 or block_previo.y == -1 and block_siguiente.x == 1:
                        screen.blit(self.giroabajoder, block_rect)
                    elif block_previo.x == 1 and block_siguiente.y == 1 or block_previo.y == 1 and block_siguiente.x == 1:
                        screen.blit(self.giroarribader, block_rect)
                
    
            
    def update_cabeza_graf(self):
        cabeza_rel= self.cuerpo[1] - self.cuerpo[0]
        if cabeza_rel == Vector2(1,0):
            self.cabeza = self.cabezaizq
        elif cabeza_rel == Vector2(-1,0):
            self.cabeza = self.cabezader
        elif cabeza_rel == Vector2(0,1):
            self.cabeza = self.cabezaup
        elif cabeza_rel == Vector2(0,-1):
            self.cabeza = self.cabezadown
    
    def update_puntacola_graf(self):
        puntacola_rel = self.cuerpo[-2] - self.cuerpo[-1]
        if puntacola_rel == Vector2(1,0):
            self.puntacola = self.puntacolaizq
        elif puntacola_rel == Vector2(-1,0):
            self.puntacola = self.puntacolader
        elif puntacola_rel == Vector2(0,1):
            self.puntacola = self.puntacolaup
        elif puntacola_rel == Vector2(0,-1):
            self.puntacola = self.puntacoladown
            
            
            
    def mov_snake(self):
        if self.new_block == True:
            cuerpo_copy = self.cuerpo[:] 
            cuerpo_copy.insert(0, cuerpo_copy[0] + self.direccion ) #le añade un vector con input del jugador
            self.cuerpo = cuerpo_copy[:]
            self.new_block = False
        else:
            cuerpo_copy = self.cuerpo[:-1] #para eliminar el ultimo vector del cuerpo
            cuerpo_copy.insert(0, cuerpo_copy[0] + self.direccion ) #le añade un vector con input del jugador
            self.cuerpo = cuerpo_copy[:]
        
    def add_block(self):
        self.new_block = True
        
    def reset(self):
        self.cuerpo = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direccion = Vector2(0,0)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruta = Fruta()
        
    def update(self):
        self.snake.mov_snake()
        self.check_colision()
        self.check_fail()
        
    def dibujar_elementos(self):
        self.dibujar_hierba()
        self.fruta.dibujar_fruta()
        self.snake.dibujar_snake()
        self.dibujar_score()
        
    def check_colision(self):
        if self.fruta.pos == self.snake.cuerpo[0]:
            self.fruta.randomize()
            self.snake.add_block()
            
        for block in self.snake.cuerpo[1:]:
            if block == self.fruta.pos:
                self.fruta.randomize()
            
    def check_fail(self):
        if not 0 <= self.snake.cuerpo[0].x < number_cel or not 0 <= self.snake.cuerpo[0].y < number_cel:  #pierdes cuando chocas con el borde
            self.game_over()
            
        for block in self.snake.cuerpo[1:]: #pierdes cuando chocas contigo mismo
            if block == self.snake.cuerpo[0]:
                self.game_over()
            
    def game_over(self):
        self.snake.reset()
        
    def dibujar_hierba(self):   # le damos patron de dibujo a la hierba
        hierba_color = (167,209,61) #mas oscuro
        for row in range (number_cel):
            if row %2 == 0:
                for col in range(number_cel):
                    if col % 2 == 0:
                        hierba_rect = pygame.Rect(col * size_cel, row * size_cel, size_cel, size_cel)
                        pygame.draw.rect(screen, hierba_color, hierba_rect)
            else:
                for col in range(number_cel):
                    if col % 2 != 0:
                        hierba_rect = pygame.Rect(col * size_cel, row * size_cel, size_cel, size_cel)
                        pygame.draw.rect(screen, hierba_color, hierba_rect)
    
    def dibujar_score(self):
        score_text = str(len(self.snake.cuerpo) - 3)
        score_surface = fuente.render(score_text, False, (56,74,12))
        score_x= int(size_cel * number_cel - 60)
        score_y= int(size_cel * number_cel - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        manzana_rect = manzana.get_rect(midright = (score_rect.left, score_rect.centery))
        fondo_rect= pygame.Rect(manzana_rect.left, manzana_rect.top, manzana_rect.width + score_rect.w + 6, manzana_rect.height)
        
        pygame.draw.rect(screen, (167, 209, 61), fondo_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(manzana, manzana_rect)
        pygame.draw.rect(screen, (56,74,12), fondo_rect, 2)
        
# ALGUNAS VARIABLES
            
pygame.init() #starts pygame, es como encender el coche para que vaya
size_cel = 40
number_cel = 20
screen= pygame.display.set_mode((size_cel * number_cel ,size_cel * number_cel)) #creamos pantalla para el juego
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
manzana = pygame.image.load('imagenes/manzana.png').convert_alpha()
fuente= pygame.font.Font('fuente/PixeloidSans-mLxMm.ttf', 25)



#TIMER
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #para cerrar la ventana, es contrario al .init
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direccion.y != 1:  #hacemos esto para no "destruirnos" simplemente por decirel ir en el sentido opuesto
                    main_game.snake.direccion = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direccion.y != -1:
                    main_game.snake.direccion = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direccion.x != -1:
                    main_game.snake.direccion = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direccion.x != 1:
                    main_game.snake.direccion = Vector2(-1,0)



    screen.fill((175,215,70))
    main_game.dibujar_elementos()
    pygame.display.update()
    clock.tick(60)