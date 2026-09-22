from PPlay.uikit import Button
from PPlay.window import Window

pos_x = (1920 - 300) / 2
pos_y = (1080 - 300) / 2

btn_f = Button(600, 60, "F", (80, 80, 80))
btn_f.set_position(pos_x - 140, pos_y)

btn_m = Button(600, 60, "M", (80, 80, 80), )
btn_m.set_position(pos_x - 140, pos_y + 100)

btn_d = Button(600, 60, "D", (80, 80, 80),)
btn_d.set_position(pos_x - 140, pos_y + 200)

btn_voltar = Button(600, 60, "voltar", (128, 0, 0))
btn_voltar.set_position(pos_x - 140, pos_y + 500)

def run(janela, dificuldade_atual):
    janela.set_background_color((0,0,0))
    
    teclado = Window.get_keyboard()
    if teclado.key_down("ESC"):
        return "MENU", dificuldade_atual
    

    if btn_f.is_clicked():
        dificuldade_atual = "F"
    elif btn_m.is_clicked():
        dificuldade_atual = "M"
    elif btn_d.is_clicked():
        dificuldade_atual = "D"
    elif btn_voltar.is_clicked():
        return "MENU", dificuldade_atual

    btn_f.draw()
    btn_m.draw()
    btn_d.draw()
    btn_voltar.draw()

    
    return "DIFICULDADE", dificuldade_atual
