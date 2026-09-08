from PPlay.window import Window

def run(janela, dificuldade):
    janela.set_background_color((0, 0, 0))
    teclado = Window.get_keyboard()
    
    if teclado.key_down("ESC"):
        return "MENU"
    
    return "JOGANDO"
