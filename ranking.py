from PPlay.uikit import Button
from PPlay.window import Window
import os

pos_x = (1920 - 300) / 2
pos_y = (1080 - 300) / 2

btn_voltar = Button(600, 60, "voltar", (128, 0, 0))
btn_voltar.set_position(pos_x - 140, pos_y + 500)

def run(janela):
    janela.set_background_color((0, 0, 0))

    teclado = Window.get_keyboard()
    if teclado.key_down("ESC"):
        return "MENU"

    if btn_voltar.is_clicked():
        return "MENU"

    jogadores = []
    if os.path.exists("ranking.txt"):
        arquivo = open("ranking.txt")
        for linha in arquivo:
            partes = linha.strip().split(";")
            jogadores.append([int(partes[1]), partes[0], partes[2]])
        arquivo.close()

    jogadores.sort(reverse=True)

    janela.draw_text("RANKING", 1920 / 2 - 100, 100, size=60, color=(255, 255, 255))

    y = 250
    for i in range(5):
        if i < len(jogadores):
            pontos = jogadores[i][0]
            nome = jogadores[i][1]
            data = jogadores[i][2]
            janela.draw_text(f"{i + 1}. {nome}   {pontos} pts   {data}", 1920 / 2 - 350, y, size=40, color=(255, 255, 255))
            y += 70

    btn_voltar.draw()

    return "RANKING"
