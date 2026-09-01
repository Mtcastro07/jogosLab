from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import random

width = 800
height = 600
janela = Window(width, height, "Meu Jogo 2.0")
teclado = Keyboard()

barra1 = Sprite("barraPong.png", 1)
barra2 = Sprite("barraPong.png", 1)
barra3 = Sprite("barraPong.png", 1)
bola = Sprite("circle-16.png", 1)

bola.set_position(width / 2, height / 2)
barra1.set_position(30, height / 2 - barra1.height / 2)
barra2.set_position(755, height / 2 - barra2.height / 2)
barra3.set_position(random.uniform(width / 3, 2 * width / 3) , random.uniform(0, height - barra3.height))

velX = 300
velY = 300
vel_barra1 = 400
vel_barra2 = 270
start = False
barra3_visivel = False
tempo = 0.0
tempoJogo = 0.0
contarParticipante = 0
contarInimigo = 0

while True:
    janela.set_background_color((0, 0, 255))
    dt = janela.delta_time()

    if not start:
        if teclado.key_pressed("SPACE"):
            velX = -250
            start = True
    else:
        tempo += dt
        tempoJogo += dt
        if tempo >= 3.0:
            barra3_visivel = not barra3_visivel
            tempo = 0.0
            if barra3_visivel:
                barra3.set_position(random.uniform(width / 3, 2 * width / 3),random.uniform(0, height - barra3.height))

        bola.x += velX * dt
        bola.y += velY * dt

        if bola.y <= 0:
            velY = -velY
            bola.y = 0
        elif bola.y + bola.height >= janela.height:
            velY = -velY
            bola.y = janela.height - bola.height

        if bola.x <= 0 or bola.x + bola.width >= janela.width:
            if bola.x <= 0:
                contarInimigo += 1
            else:
                contarParticipante += 1

            bola.set_position(width / 2, height / 2)
            barra1.set_position(30, height / 2 - barra1.height / 2)
            barra2.set_position(755, height / 2 - barra2.height / 2)
            barra3.set_position(random.uniform(width / 3, 2 * width / 3), random.uniform(0, height - barra3.height))
            barra3_visivel = False
            tempo = 0.0
            start = False

        if bola.collided(barra1):
            bola.x = barra1.x + barra1.width
            velX *= -1.025

        if bola.collided(barra2):
            bola.x = barra2.x - bola.width
            velX *= -1.025

        if barra3_visivel and bola.collided(barra3):
            if velX > 0:
                bola.x = barra3.x - bola.width
            else:
                bola.x = barra3.x + barra3.width
            velX *= -1.025

        if teclado.key_pressed("W") and barra1.y > 0:
            barra1.y -= vel_barra1 * dt
        if teclado.key_pressed("S") and barra1.y < janela.height - barra1.height:
            barra1.y += vel_barra1 * dt

        centro = barra2.y + barra2.height / 2
        if bola.y > centro and barra2.y < janela.height - barra2.height:
            barra2.y += vel_barra2 * dt
        elif velY < centro and barra2.y > 0:
            barra2.y -= vel_barra2 * dt

    barra1.draw()
    barra2.draw()
    if barra3_visivel:
        barra3.draw()
    bola.draw()
    janela.draw_text(str(f"Tempo: {int(tempoJogo)}"), width - 200, 25, size=24, color=(255,255,255), font_name="Arial", bold=False)
    janela.draw_text(str(contarParticipante), width / 2 - 100, 50, size=48, color=(255, 255, 255), font_name="Arial", bold=True)
    janela.draw_text(str(contarInimigo), width / 2 + 100, 50, size=48, color=(255, 255, 255), font_name="Arial", bold=True)

    janela.update()