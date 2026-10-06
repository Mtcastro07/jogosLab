from PPlay.window import Window
from PPlay.sprite import Sprite
import random

velocidade_nave = {"F": 500, "M": 700, "D": 900}
tempo_entre_tiros = {"F": 0.5, "M": 0.3, "D": 0.15}
tempo_tiro_monstro = {"F": 1.5, "M": 1.0, "D": 0.6}
velocidade_tiro = 1000
velocidade_tiro_monstro = 500

nave = Sprite("nave.png")
nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)

tiros = []
recarga = 0

tiros_monstros = []
recarga_monstros = 0

vidas = 3
invencivel = 0

linhas = 4
colunas = 6
velocidade_monstro = 150
descida = 30
direcao = 1

def criar_monstros():
    matriz = []
    for l in range(linhas):
        linha = []
        for c in range(colunas):
            monstro = Sprite("monstro.png")
            x = 100 + c * monstro.width * 1.5
            y = 50 + l * monstro.height * 1.5
            monstro.set_position(x, y)
            linha.append(monstro)
        matriz.append(linha)
    return matriz

monstros = criar_monstros()

def reiniciar():
    global monstros, direcao, vidas, invencivel, recarga_monstros
    monstros = criar_monstros()
    direcao = 1
    vidas = 3
    invencivel = 0
    recarga_monstros = 0
    tiros.clear()
    tiros_monstros.clear()
    nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)

def run(janela, dificuldade, delta_time):
    global recarga, direcao, monstros, recarga_monstros, vidas, invencivel
    janela.set_background_color((0, 0, 0))

    teclado = Window.get_keyboard()
    if teclado.key_down("ESC"):
        return "MENU"

    todos = [m for linha in monstros for m in linha]
    if len(todos) == 0:
        monstros = criar_monstros()
        todos = [m for linha in monstros for m in linha]

    for monstro in todos:
        monstro.x += velocidade_monstro * direcao * delta_time

    esquerda = min(m.x for m in todos)
    direita = max(m.x + m.width for m in todos)
    baixo = max(m.y + m.height for m in todos)

    if (esquerda <= 0 and direcao == -1) or (direita >= 1920 and direcao == 1):
        direcao *= -1
        for monstro in todos:
            monstro.y += descida

    if baixo >= nave.y:
        reiniciar()
        return "MENU"

    if teclado.key_pressed("LEFT"):
        nave.x -= velocidade_nave[dificuldade] * delta_time
    if teclado.key_pressed("RIGHT"):
        nave.x += velocidade_nave[dificuldade] * delta_time

    if nave.x < 0:
        nave.x = 0
    if nave.x + nave.width > 1920:
        nave.x = 1920 - nave.width

    recarga -= delta_time
    if teclado.key_pressed("SPACE") and recarga <= 0:
        tiro = Sprite("tiro.png")
        tiro.set_position(nave.x + nave.width / 2 - tiro.width / 2, nave.y)
        tiros.append(tiro)
        recarga = tempo_entre_tiros[dificuldade]

    recarga_monstros -= delta_time
    if recarga_monstros <= 0:
        atirador = random.choice(todos)
        tiro = Sprite("tiro_monstro.png")
        tiro.set_position(atirador.x + atirador.width / 2 - tiro.width / 2, atirador.y + atirador.height)
        tiros_monstros.append(tiro)
        recarga_monstros = tempo_tiro_monstro[dificuldade] * random.uniform(0.7, 1.3)

    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro * delta_time
        acertou = False
        for linha in monstros:
            for monstro in linha:
                if tiro.collided(monstro):
                    linha.remove(monstro)
                    acertou = True
                    break
            if acertou:
                break

        if acertou or tiro.y + tiro.height < 0:
            tiros.remove(tiro)
        else:
            tiro.draw()

    invencivel -= delta_time
    for tiro in tiros_monstros[:]:
        tiro.y += velocidade_tiro_monstro * delta_time

        if invencivel <= 0 and tiro.collided(nave):
            tiros_monstros.remove(tiro)
            vidas -= 1
            if vidas == 0:
                reiniciar()
                return "MENU"
            nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)
            invencivel = 2
        elif tiro.y > 1080:
            tiros_monstros.remove(tiro)
        else:
            tiro.draw()

    for linha in monstros:
        for monstro in linha:
            monstro.draw()

    if invencivel <= 0 or int(invencivel * 10) % 2 == 0:
        nave.draw()

    janela.draw_text(f"FPS: {int(janela.get_fps())}", 10, 10, size=30, color=(255, 255, 255))
    janela.draw_text(f"Vidas: {vidas}", 1750, 10, size=30, color=(255, 255, 255))
    return "JOGANDO"
