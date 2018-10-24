from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from random import randint
import time


resolutionX = 1200
resolutionY = 700
janela = Window(resolutionX,resolutionY)
janela.set_title("Space Invaders")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()
tiro = []
tiro_mal = []
t = 0
linhas = 3
colunas = 8
score = 0
vida = 3
cont = 0
estado_perdeu = False
hold = False

def scrolling(fundo1, fundo2, velfundo):
    fundo1.y += velfundo * janela.delta_time()
    fundo2.y += velfundo * janela.delta_time()

    if fundo2.y >= 0:
        fundo1.y = 0
        fundo2.y = -fundo2.height

    # Renderiza as duas imagens de fundo
    fundo1.draw()
    fundo2.draw()

def Cria_Monstro(x, y):

    monstro = []
    horizontal = []
    for i in range(linhas):
        i = 0
        for j in range(colunas):
            i += 1
            mal = Sprite("mal.png")
            mal.set_position(x, y)
            horizontal.append(mal)
            x += 100
        x = 100
        y += 80

        monstro.append(horizontal)
        horizontal = []

    return monstro

def monstro_atira(monstro):
    i = randint(0,linhas-1)
    j = randint(0, colunas-1)
    global t
    t += 1 * janela.delta_time()

    if monstro[i][j].hide():
        monstro[i][j].unhide()
        if len(tiro_mal) < 15 and t > 1:
            bala_mal = Sprite("Laser.png")
            bala_mal.set_position(monstro[i][j].x + 25, monstro[i][j].y + 16)
            tiro_mal.append(bala_mal)
            t = 0

    for elemento in tiro_mal:
        if elemento.y > 700:
            tiro_mal.remove(elemento)
        else:
            elemento.y += 3
            elemento.draw()
def ganhou(monstro):
    global linhas

    global colunas
    for i in range(linhas):
        for j in range(colunas):

            monstro[i][j].unhide()

    linhas = 4

    return monstro



def perdeu():
    fundo_perdeu = GameImage("perdeu.jpg")
    fundo_perdeu.set_position(350,250)
    fundo_perdeu.draw()
    global score
    global vida

    score = 0
    vida = 3

def escreve():
    global score
    global vida

    janela.draw_text(("Pontuação = %d" %score), 10, 10, size=24, color=(200, 200 , 0), font_name="Tlwg Typist", bold = True, italic = False)
    janela.draw_text(("Vidas = %d" % vida), 1060, 10, size=24, color=(200, 0, 0), font_name="Tlwg Typist", bold = True, italic = False)


def move_monstro(monstro, vel, deltatime, x, y, aux_matriz):
    auxX = x
    auxY = y

    if aux_matriz[0] + 800 >= janela.width:
        vel = -vel
        auxX -= 10 #Segurança
        auxY += 20

    if aux_matriz[0] - 30 <= 0:
        vel = -vel
        auxX += 10 #Segurança
        auxY += 20


    for linha in monstro:
        x += vel * deltatime
        for elemento in linha:
            elemento.set_position(x, y)
            elemento.draw()
            x += 100
        x = auxX
        y += 100

    y = auxY
    x = auxX
    x += vel * deltatime
    aux_matriz[0] = x
    aux_matriz[1] = y

    return x, y, vel, aux_matriz


def testa_colisao_nave(nave):

    global vida

    for bala_mal in tiro_mal:
        if bala_mal.collided_perfect(nave):
            if vida < 0:
                return True
            else:
                vida -= 1
                tiro_mal.remove(bala_mal)
                return False


def testa_colisao(monstro, tiro, aux_monstro, SuperTiro):

    #Isso é gambiarra
    global linhas
    global colunas
    global score

    if linhas == 3:
        fim = aux_monstro[1] + 250
    elif linhas == 4:
        fim = aux_monstro[1] + 350
    elif linhas == 5:
        fim = aux_monstro[1] + 450
    direita = aux_monstro[0] + 800
    esquerda = aux_monstro[0] - 10

    for bala in tiro:
        if bala.y < fim:
            if bala.x < direita:
                if bala.x > esquerda:

                    for i in range(linhas-1, -1, -1):
                        for j in range(colunas-1,-1,-1):
                            if monstro[i][j].collided(bala):
                                if monstro[i][j].hide():
                                    score += 50
                                    tiro.remove(bala)

                            #if monstro[i][j].collided(SuperTiro):
                                    #monstro[i][j].hide()
                                    #print("ENTREIIIIIi")
                                    #score += 50


    return monstro, tiro

def shot(x, y):
    bala = Sprite("tiro.png")
    bala.set_position(x + 55,y)
    tiro.append(bala)
    return bala

def GerarSuperTiro(SuperTiro, nave):
    SuperTiro.set_position(nave.x + 100, nave.y)
    SuperTiro.draw()
    return True

#=++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def game(dificuldade):
    janela.set_background_color((0,0,0))
    fundo1 = GameImage("fundogame.jpg")
    fundo1.y = 0
    fundo2 = GameImage("fundogame.jpg")
    fundo2.y = -fundo2.height
    velfundo = 200
    nave = Sprite("Navemae.png")
    nave.set_position((janela.width / 2) - 100, janela.height / 2 + 180)
    t = 0
    local = -35
    x = 150
    y = 50
    aux_matriz = [x,y]
    vel = dificuldade * 5
    global tiro
    global estado_perdeu
    monstro = Cria_Monstro(x, y)
    SuperTiro = Sprite("SuperTiro.png")
    SuperTempo = 0
    SuperEstado = False
    global hold
#Game Loop
    while(not estado_perdeu):

        scrolling(fundo1, fundo2, velfundo)
        nave.draw()
#Movimentação da nave_____________________________________________________________

        if (teclado.key_pressed("RIGHT")):
            nave.x += vel * janela.delta_time()
            if nave.x > janela.width:
                nave.x = 0 - 200

        if(teclado.key_pressed("LEFT")):
            nave.x -= vel * janela.delta_time()
            if nave.x + 200 < 0:
                nave.x = janela.width

        nave.set_position(nave.x, nave.y)

#Criação dos tiros_______________________________________________________________
        if SuperEstado:
            SuperTiro.y -= 200 * janela.delta_time()
            SuperTiro.draw()
            if SuperTiro.y < 0:
                SuperTempo = 0
                SuperEstado = False

        if(teclado.key_pressed("SPACE")):

            aux = False
            if hold:
                SuperTempo += 10 * janela.delta_time()
                aux = True

            hold = True
            if SuperTempo > 15 and not SuperEstado and hold:
                SuperEstado = GerarSuperTiro(SuperTiro, nave)

            if not SuperEstado and not aux:
                if t >= 0.2:
                    if len(tiro) < 5:
                        t = 0
                        if local == 35:
                            local += 35
                        bala = shot(nave.x + local, nave.y + 40)
                        local += 35
                        if local >= (35 * (len(tiro) - 1)):
                            local = -35
        else:
            hold = False
        if len(tiro) != 0:
            for bala in tiro:
                if bala.y < 0:
                    tiro.remove(bala)
                else:
                    bala.y -= 200 * janela.delta_time()
                    bala.draw()
        t += janela.delta_time()


#Movimentação dos monstros__________________________________________________
        if len(tiro) != 0:
            monstro, tiro = testa_colisao(monstro,tiro, aux_matriz, SuperTiro)

        estado_perdeu = testa_colisao_nave(nave)

        x, y, dificuldade, aux_matriz = move_monstro(monstro, dificuldade, janela.delta_time(), x, y, aux_matriz)
        monstro_atira(monstro)

        escreve()
        global score

        if score == 1200 or score == 2800:
            monstro = ganhou(monstro)
            game(50)

        janela.update()

    bt_jogarOFF = GameImage("Botao_jogarOFF.jpg")
    bt_jogarOFF.set_position(380,420)
    bt_jogarON = GameImage("Botao_jogar.jpg")
    bt_jogarON.set_position(380,420)
    bt_exitOFF = GameImage("Botao_SairOFF.jpg")
    bt_exitOFF.set_position(620,420)
    bt_exitON = GameImage("Botao_SairON.jpg")
    bt_exitON.set_position(620,420)

    while(True):
        perdeu()
        if mouse.is_over_object(bt_jogarOFF) or mouse.is_over_object(bt_jogarON):
            bt_jogarON.draw()
            bt_exitOFF.draw()
            if mouse.is_button_pressed(1):
                estado_perdeu = False
                menu(50)
        elif mouse.is_over_object(bt_exitOFF) or mouse.is_over_object(bt_exitON):
            bt_jogarOFF.draw()
            bt_exitON.draw()
            if mouse.is_button_pressed(1):
                exit()
        else:
            bt_jogarOFF.draw()
            bt_exitOFF.draw()

        janela.update()

def nivel():
    print("nivel")
    fundo = GameImage("background.jpg")

    bt_dificilOFF = GameImage("Dificil_ OFF.jpg")
    bt_dificilOFF.set_position(((janela.width/2) - (bt_dificilOFF.width/ 2)), ((janela.height / 2)) - 100)
    bt_dificilON = GameImage("Dificil_ ON.jpg")
    bt_dificilON.set_position(((janela.width / 2) - (bt_dificilON.width / 2)), ((janela.height / 2)) - 100)

    bt_medioOFF = GameImage("Medio_OFF.jpg")
    bt_medioOFF.set_position(((janela.width/2) - (bt_medioOFF.width/ 2)), (janela.height / 2))
    bt_medioON = GameImage("Medio_ON.jpg")
    bt_medioON.set_position(((janela.width/2) - (bt_medioON.width/ 2)), (janela.height / 2))

    bt_facilOFF = GameImage("Facil_OFF.jpg")
    bt_facilOFF.set_position(((janela.width/2) - (bt_facilOFF.width/ 2)), ((janela.height / 2)) + 100)
    bt_facilON = GameImage("Facil_ON.jpg")
    bt_facilON.set_position(((janela.width/2) - (bt_facilON.width/ 2)), ((janela.height / 2)) + 100)
    print("Cheguei aqui")
    while(True):
        time.sleep(2)

        fundo.draw()
        print("Looppppp")
        if mouse.is_over_object(bt_dificilOFF) or mouse.is_over_object(bt_dificilON):
            bt_dificilON.draw()
            bt_medioOFF.draw()
            bt_facilOFF.draw()

            if mouse.is_button_pressed(1):
                return 2


        elif mouse.is_over_object(bt_medioOFF) or mouse.is_over_object(bt_medioON):
            bt_medioON.draw()
            bt_dificilOFF.draw()
            bt_facilOFF.draw()

            if mouse.is_button_pressed(1):
                print("2")
                return 1;

        elif mouse.is_over_object(bt_facilOFF) or mouse.is_over_object(bt_facilON):
            bt_facilON.draw()
            bt_dificilOFF.draw()
            bt_medioOFF.draw()

            if mouse.is_button_pressed(1):
               return 0;


        else:
            bt_facilOFF.draw()
            bt_medioOFF.draw()
            bt_dificilOFF.draw()

        janela.update()


def ranking():
    print("ranking")

def menu(dificuldade):
    # botoes 400x150
    fundo = GameImage("background.jpg")
    flag = 0
    bt_jogarOFF = GameImage("Botao_jogarOFF.jpg")
    bt_jogarOFF.set_position(((janela.width/2) - (bt_jogarOFF.width/ 2)), ((janela.height / 2)) - 100)
    bt_jogarON = GameImage("Botao_jogar.jpg")
    bt_jogarON.set_position(((janela.width / 2) - (bt_jogarON.width / 2)), ((janela.height / 2) - 100))

    bt_dificuldadeOFF = GameImage("Botao_dificuldadeOFF.jpg")
    bt_dificuldadeOFF.set_position(((janela.width / 2) - (bt_dificuldadeOFF.width / 2)), (janela.height / 2))
    bt_dificuldadeON = GameImage("Botao_dificuldadeOn.jpg")
    bt_dificuldadeON.set_position(((janela.width / 2) - (bt_dificuldadeON.width / 2)), (janela.height / 2))

    bt_rankingOFF = GameImage("Botao_RankingOFF.jpg")
    bt_rankingOFF.set_position(((janela.width / 2) - (bt_rankingOFF.width / 2)), ((janela.height / 2) + 100))
    bt_rankingON = GameImage("Botao_RankingON.jpg")
    bt_rankingON.set_position(((janela.width / 2) - (bt_rankingON.width / 2)), ((janela.height / 2) + 100))

    bt_sairOFF = GameImage("Botao_SairOFF.jpg")
    bt_sairOFF.set_position(((janela.width / 2) - (bt_sairOFF.width / 2)), ((janela.height / 2) + 200))
    bt_sairON = GameImage("Botao_SairON.jpg")
    bt_sairON.set_position(((janela.width / 2) - (bt_sairON.width / 2)), ((janela.height / 2) + 200))


    while(True):
        fundo.draw()
        if mouse.is_over_object(bt_jogarOFF) or mouse.is_over_object(bt_jogarON):
            bt_jogarON.draw()
            bt_sairOFF.draw()
            bt_rankingOFF.draw()
            bt_dificuldadeOFF.draw()

            if mouse.is_button_pressed(1):
                game(dificuldade)


        elif mouse.is_over_object(bt_dificuldadeOFF) or mouse.is_over_object(bt_dificuldadeON):
            bt_dificuldadeON.draw()
            bt_jogarOFF.draw()
            bt_sairOFF.draw()
            bt_rankingOFF.draw()

            if mouse.is_button_pressed(1):
                dificuldade = int(nivel())


        elif mouse.is_over_object(bt_rankingOFF) or mouse.is_over_object(bt_rankingON):
            bt_rankingON.draw()
            bt_jogarOFF.draw()
            bt_sairOFF.draw()
            bt_dificuldadeOFF.draw()

            if mouse.is_button_pressed(1):
                ranking()


        elif mouse.is_over_object(bt_sairOFF) or mouse.is_over_object(bt_sairON):
            bt_sairON.draw()
            bt_jogarOFF.draw()
            bt_rankingOFF.draw()
            bt_dificuldadeOFF.draw()
            if mouse.is_button_pressed(1):
                exit()
        else:
            bt_jogarOFF.draw()
            bt_sairOFF.draw()
            bt_rankingOFF.draw()
            bt_dificuldadeOFF.draw()

        janela.update()

dificuldade = 50
menu(dificuldade)
