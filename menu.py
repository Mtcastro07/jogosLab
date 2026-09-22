from PPlay.uikit import Button

pos_x = (1920 - 300) / 2
pos_y = (1080 - 300) / 2

btn_iniciar = Button(600, 60, "iniciar", (0, 128, 0))
btn_iniciar.set_position(pos_x - 140, pos_y)

btn_dificuldade = Button(600, 60, "dificuldade", (80, 80, 80))
btn_dificuldade.set_position(pos_x - 140, pos_y + 100)

btn_ranking = Button(600, 60, "ranking", (80, 80, 80))
btn_ranking.set_position(pos_x - 140, pos_y + 200)

btn_sair = Button(600, 60, "sair", (128, 0, 0))
btn_sair.set_position(pos_x - 140, pos_y + 500)

def run(janela):
    janela.set_background_color((0, 0, 0))

    if btn_iniciar.is_clicked():
        return "JOGANDO"
    elif btn_dificuldade.is_clicked():
        return "DIFICULDADE"
    elif btn_sair.is_clicked():
        janela.close()

    btn_iniciar.draw()
    btn_dificuldade.draw()
    btn_ranking.draw()
    btn_sair.draw()
    
    return "MENU"
