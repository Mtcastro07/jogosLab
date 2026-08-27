from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard

width = 800
heigth = 600

teclado = Keyboard()

janela = Window(width, heigth, "Meu Jogo 2.0")
pos_x = 0

barra1 = Sprite("barraPong.png", 1)
barra2 = Sprite("barraPong.png", 1)
bola = Sprite("circle-16.png", 1)
bola.set_position(width/2, heigth/2 )
barra1.set_position(30,heigth/2 - barra1.height/2)
barra2.set_position(755, heigth/2 - barra2.height/2)

velX = 250
velY = 250
vel_barra1 = 400
vel_barra2 = 225
vel_ia = 225
ia_ativa = False
start = False

contarInimigo = 0
contarParticipante = 0

while True:
    while start == False:
        janela.set_background_color((0, 0, 255))
        barra1.draw()
        barra2.draw()
        bola.draw()
        janela.update()
        ia_ativa = False
        if teclado.key_pressed("SPACE"):
            velX = -250
            start = True

    while start == True:
        janela.set_background_color((0, 0, 255))
        bola.x = bola.x + velX*janela.delta_time()
        bola.y = bola.y + velY*janela.delta_time()

             
        if bola.y <= 0:
            velY = -velY
            bola.y = 0

        if (bola.y + bola.height >= janela.height):
            velY = -velY
            bola.y = janela.height - bola.height
        

        if bola.x <= 0 or (bola.x + bola.width >= janela.width):
            if(bola.x == 0):
                contarInimigo += 1 
            
            if(bola.x + bola.width >= janela.width):
                contarParticipante += 1
            bola.set_position(width/2, heigth/2 )   
            barra1.set_position(30,heigth/2 - barra1.height/2)
            barra2.set_position(755, heigth/2 - barra2.height/2)
            start = False

        if bola.collided(barra1):
            bola.x = barra1.x+barra1.width
            velX *= -1.025

           

        if bola.collided(barra2):
            bola.x = barra2.x - bola.width
            velX *= -1.025

        if teclado.key_pressed("W") and barra1.y > 0:
            barra1.y -= vel_barra1 * janela.delta_time()

        if teclado.key_pressed("S") and barra1.y < janela.height - barra1.height:
            barra1.y += vel_barra1 * janela.delta_time() 

        

        
        centro = barra2.y + barra2.height/2

        if bola.y > centro and barra2.y < janela.height - barra2.height:
            barra2.y += vel_barra2 * janela.delta_time()
        elif velY < centro and barra2.y > 0:
            barra2.y -= vel_barra2 * janela.delta_time()
                

        barra1.draw()
        barra2.draw()
        bola.draw()
        janela.update()