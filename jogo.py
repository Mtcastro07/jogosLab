from PPlay.window import Window
from PPlay.sprite import Sprite

velocidade_nave = {"F": 500, "M": 700, "D": 900}
tempo_entre_tiros = {"F": 0.5, "M": 0.3, "D": 0.15}
velocidade_tiro = 1000

nave = Sprite("nave.png")
nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)

tiros = []
recarga = 0

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

def run(janela, dificuldade, delta_time):
    global recarga, direcao, monstros
    janela.set_background_color((0, 0, 0))

    teclado = Window.get_keyboard()
    if teclado.key_down("ESC"):
        return "MENU"

    for linha in monstros:
        for monstro in linha:
            monstro.x += velocidade_monstro * direcao * delta_time

    esquerda = monstros[0][0]
    direita = monstros[0][-1]
    baixo = monstros[-1][0]

    if (esquerda.x <= 0 and direcao == -1) or (direita.x + direita.width >= 1920 and direcao == 1):
        direcao *= -1
        for linha in monstros:
            for monstro in linha:
                monstro.y += descida

    if baixo.y + baixo.height >= nave.y:
        monstros = criar_monstros()
        direcao = 1
        return "MENU"

    for linha in monstros:
        for monstro in linha:
            monstro.draw()

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

    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro * delta_time
        if tiro.y + tiro.height < 0:
            tiros.remove(tiro)
        else:
            tiro.draw()

    nave.draw()
    janela.draw_text(f"FPS: {int(janela.get_fps())}", 10, 10, size=30, color=(255, 255, 255))
    return "JOGANDO"
