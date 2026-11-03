from PPlay.window import Window

janela = Window(1920, 1080)

import menu
import dificuldade
import jogo
import ranking

estado = "MENU"
nivel_dificuldade = "M" 

while True:
    delta_time = janela.delta_time()

    if estado == "MENU":
        estado = menu.run(janela)
        
    elif estado == "JOGANDO":
        estado = jogo.run(janela, nivel_dificuldade, delta_time)
        
    elif estado == "DIFICULDADE":
        estado, nivel_dificuldade = dificuldade.run(janela, nivel_dificuldade)

    elif estado == "RANKING":
        estado = ranking.run(janela)

    janela.update()
