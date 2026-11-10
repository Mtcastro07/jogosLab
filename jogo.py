from PPlay.window import Window
from PPlay.sprite import Sprite
import random
from datetime import datetime

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
coracao = Sprite("coracao.png")
pontos = 0

frames = 0
tempo_fps = 0
fps = 0

linhas = 4
colunas = 6
velocidade_monstro = 150
descida = 30
direcao = 1
fase = 1
multiplicador_velocidade = 0.35

modelo = Sprite("monstro.png")
passo_x = modelo.width * 1.5
passo_y = modelo.height * 1.5
origem_x = 100
origem_y = 50

def criar_monstros():
    global origem_x, origem_y
    origem_x = 100
    origem_y = 50
    matriz = []
    for l in range(linhas):
        linha = []
        for c in range(colunas):
            monstro = Sprite("monstro.png")
            x = origem_x + c * passo_x
            y = origem_y + l * passo_y
            monstro.set_position(x, y)
            linha.append(monstro)
        matriz.append(linha)
    return matriz

monstros = criar_monstros()

monstro_especial = Sprite("monstro_especial.png")
tempo_piscar = 0
pisca = True

def escolher_especial():
    vivos = []
    for linha in monstros:
        for m in linha:
            if m != None:
                vivos.append(m)
    if len(vivos) == 0:
        return None
    return random.choice(vivos)

especial = escolher_especial()

def salvar_ranking():
    nome = input("Fim de jogo! Digite seu nome: ")
    agora = datetime.now()
    data = f"{agora.day}/{agora.month}/{agora.year}"
    arquivo = open("ranking.txt", "a")
    arquivo.write(f"{nome};{pontos};{data}\n")
    arquivo.close()

def reiniciar():
    global monstros, direcao, vidas, invencivel, recarga_monstros, pontos, fase, especial
    monstros = criar_monstros()
    especial = escolher_especial()
    direcao = 1
    fase = 1
    vidas = 3
    pontos = 0
    invencivel = 0
    recarga_monstros = 0
    tiros.clear()
    tiros_monstros.clear()
    nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)

def run(janela, dificuldade, delta_time):
    global recarga, direcao, monstros, recarga_monstros, vidas, invencivel, pontos, frames, tempo_fps, fps, origem_x, origem_y, fase, especial, tempo_piscar, pisca
    janela.set_background_color((0, 0, 0))

    frames += 1
    tempo_fps += delta_time
    if tempo_fps >= 1:
        fps = frames
        frames = 0
        tempo_fps = 0

    teclado = Window.get_keyboard()
    if teclado.key_down("ESC"):
        return "MENU"

    todos = []
    for linha in monstros:
        for m in linha:
            if m != None:
                todos.append(m)

    if len(todos) == 0:
        fase += 1
        direcao = 1
        monstros = criar_monstros()
        especial = escolher_especial()
        for linha in monstros:
            for m in linha:
                todos.append(m)

    aumento = 1 + (fase - 1) * multiplicador_velocidade

    origem_x += velocidade_monstro * aumento * direcao * delta_time
    for monstro in todos:
        monstro.x += velocidade_monstro * aumento * direcao * delta_time

    esquerda = min(m.x for m in todos)
    direita = max(m.x + m.width for m in todos)

    baixo = 0
    l = linhas - 1
    while l >= 0 and baixo == 0:
        for m in monstros[l]:
            if m != None:
                baixo = m.y + m.height
        l -= 1

    if (esquerda <= 0 and direcao == -1) or (direita >= 1920 and direcao == 1):
        direcao *= -1
        origem_y += descida
        for monstro in todos:
            monstro.y += descida

    if baixo >= nave.y:
        salvar_ranking()
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
        recarga = tempo_entre_tiros[dificuldade] / aumento

    recarga_monstros -= delta_time
    if recarga_monstros <= 0:
        atirador = random.choice(todos)
        tiro = Sprite("tiro_monstro.png")
        tiro.set_position(atirador.x + atirador.width / 2 - tiro.width / 2, atirador.y + atirador.height)
        tiros_monstros.append(tiro)
        recarga_monstros = tempo_tiro_monstro[dificuldade] * random.uniform(0.7, 1.3) / aumento

    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro * delta_time
        acertou = False

        c = int((tiro.x + tiro.width / 2 - origem_x) / passo_x)
        l = int((tiro.y - origem_y) / passo_y)

        if tiro.y <= baixo and l >= 0 and l < linhas and c >= 0 and c < colunas:
            monstro = monstros[l][c]
            if monstro != None and tiro.collided(monstro):
                if monstro == especial:
                    for i in range(colunas):
                        if monstros[l][i] != None:
                            monstros[l][i] = None
                            pontos += (linhas - l) * 10 * fase
                    especial = escolher_especial()
                else:
                    monstros[l][c] = None
                    pontos += (linhas - l) * 10 * fase
                acertou = True

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
                salvar_ranking()
                reiniciar()
                return "MENU"
            nave.set_position(1920 / 2 - nave.width / 2, 1080 - nave.height - 20)
            invencivel = 2
        elif tiro.y > 1080:
            tiros_monstros.remove(tiro)
        else:
            tiro.draw()

    tempo_piscar += delta_time
    if tempo_piscar >= 0.15:
        pisca = not pisca
        tempo_piscar = 0

    for linha in monstros:
        for monstro in linha:
            if monstro != None:
                if monstro == especial and pisca == True:
                    monstro_especial.set_position(monstro.x, monstro.y)
                    monstro_especial.draw()
                else:
                    monstro.draw()

    if invencivel <= 0 or pisca == True:
        nave.draw()

    janela.draw_text(f"FPS: {fps}", 10, 10, size=30, color=(255, 255, 255))
    janela.draw_text(f"Pontos: {pontos}", 1920 / 2 - 80, 10, size=30, color=(255, 255, 255))
    janela.draw_text(f"Fase: {fase}", 1920 / 2 - 80, 50, size=30, color=(255, 255, 255))
    x = 1900 - coracao.width
    for v in range(vidas):
        coracao.set_position(x, 10)
        coracao.draw()
        x -= coracao.width + 10
    return "JOGANDO"
