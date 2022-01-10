import pygame
from time import sleep
import os
import pickle #permite salvar listas e em seguida carrega facilmente de volta


pygame.init()

#---------------------------------------------Definindo os diretorios--------------------------------------------------#

diretorio_principal = os.path.dirname(__file__)
diretorio_audio = os.path.join(diretorio_principal, 'sons_menu')
diretorio_audio2 = os.path.join(diretorio_principal, 'sons_mygame')
diretorio_imagens = os.path.join(diretorio_principal, 'sprites_mygame')

#--------------------------------------------Mixer no som--------------------------------------------------------------#

pygame.mixer.init()

jazz_loop = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'jazz_loop.mp3'))
jazz_loop.set_volume(0.2)
jazz_loop.play(-1)

music_in_game = pygame.mixer.music.load(os.path.join(diretorio_audio2, 'music_game.wav'))
pygame.mixer.music.set_volume(0.1)

som_change = pygame.mixer.Sound(os.path.join(diretorio_audio, 'menu_change.wav'))
som_change.set_volume(0.2)

som_back = pygame.mixer.Sound(os.path.join(diretorio_audio, 'menu_back.wav'))
som_back.set_volume(0.2)

som_select = pygame.mixer.Sound(os.path.join(diretorio_audio, 'menu_validate.wav'))
som_select.set_volume(0.2)

som_exit = pygame.mixer.Sound(os.path.join(diretorio_audio, 'som_exit.wav'))
som_exit.set_volume(0.2)

som_go = pygame.mixer.Sound(os.path.join(diretorio_audio, 'som_letsgo.wav'))
som_go.set_volume(0.1)

male_jump = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'male_jump.wav'))
male_jump.set_volume(0.4)

female_jump = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'female_jump.wav'))
female_jump.set_volume(0.4)

som_ok_male = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'ok_male.wav'))
som_ok_male.set_volume(0.8)

som_ok_female = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'ok_female.wav'))
som_ok_female.set_volume(0.8)

som_serra = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'serra_sound.wav'))
som_serra.set_volume(0.5)

som_bloco = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'bloco_mal_sound.wav'))
som_bloco.set_volume(0.5)

som_tesoura = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'tesoura_sound.wav'))
som_tesoura.set_volume(0.5)

som_lava = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'lava_sound.wav'))
som_lava.set_volume(0.5)

som_portal = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'portal_sound.wav'))
som_portal.set_volume(0.5)

complete_game = pygame.mixer.Sound(os.path.join(diretorio_audio2, 'complete_game.wav'))
complete_game.set_volume(0.5)

#------------------------------------------------Carregando imagens----------------------------------------------------#

controles_img = pygame.image.load('sprites_mygame/teclas.png')

player1_img = pygame.image.load('sprites_mygame/p1.png')
p1_char = 'sprites_mygame/p1_img.png'

player2_img = pygame.image.load('sprites_mygame/p2.png')
p2_char = 'sprites_mygame/p2_img.png'

restart_img = pygame.image.load('sprites_mygame/restart_botao.png')
restart_img = pygame.transform.scale(restart_img, (100, 50))
#--------------------------------------------DIVERSAS VARIÁVEIS--------------------------------------------------------#

escolha_do_player = []
personagem = []

relogio = pygame.time.Clock()

corte = 40
largura, altura = 400, 400
tela1 = pygame.display.set_mode((largura, altura))

game_over = 0

level = 1

#----------------------------------CRIANDO A FUNÇÃO DE IR PARA O PRÓXIMO NÍVEL-----------------------------------------#
def reset_level(level):
    player.reset(50, 360)
    portal_group.empty()
    lava_group.empty()
    serra_group.empty()
    tesoura_group.empty()
    bloco_mal_group.empty()

    # carregando os levels e criando o mundo
    if os.path.join(f'level{level}_data', 'rb'):
        pickle_in = open(f'level{level}_data', 'rb')
        mapa = pickle.load(pickle_in)
    mundo = Mapas(mapa)

    return mundo

#--------------------------------------CRIANDO O BOTAO DE RESET DO GAME------------------------------------------------#
class Botao():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False

    def draw(self):
        acao = False

        #obetendo a posição do mouse
        pos_mouse = pygame.mouse.get_pos()

        #verificando click do mouse

        if self.rect.collidepoint(pos_mouse):

            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                acao = True
                self.click = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        #desenhando botao na tela
        tela1.blit(self.image, self.rect)

        return acao

#criando botao de restart
restart_botao = Botao(170, 350, restart_img)
#-----------------------------------------------CRIANDO OS PLAYERS-----------------------------------------------------#
#----------------------------------------------------player 1----------------------------------------------------------#
class PlayerO(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.reset(x, y)

    def update(self):
        global game_over

        mov_x = 0
        mov_y = 0

        if game_over == 0:

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_SPACE] and self.pulo == False and self.no_ar == False:
                male_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_UP] and self.pulo == False and self.no_ar == False:
                male_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_w] and self.pulo == False and self.no_ar == False:
                male_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_SPACE] == False and tecla[pygame.K_w] == False and tecla[pygame.K_UP] == False:
                self.pulo = False

            if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                if self.index_lista > 8:
                    self.index_lista = 0
                self.index_lista += 0.30
                self.image = self.imagens_p1[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))
                mov_x += 5

            if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                if self.index_lista <= 8:
                    self.index_lista = 10
                if self.index_lista > 18:
                    self.index_lista = 10
                self.index_lista += 0.30
                self.image = self.imagens_p1[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))
                mov_x -= 5

            if tecla[pygame.K_LEFT] == False and tecla[pygame.K_a] == False and tecla[pygame.K_RIGHT] == False\
            and tecla[pygame.K_d] == False:
                self.index_lista = 18
                self.image = self.imagens_p1[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))

            #adicionando gravidade
            self.grav_y += 1
            if self.grav_y > 13.1:
                self.grav_y = 13.1
            mov_y += self.grav_y

            # checando colisão
            self.no_ar = True
            for pixel in mundo.pixels_lista:
                #checando colisão na direção x
                if pixel[1].colliderect(self.rect.x + mov_x, self.rect.y, self.width, self.height):
                    mov_x = 0

                #checando colisão na direção y
                if pixel[1].colliderect(self.rect.x, self.rect.y + mov_y, self.width, self.height):
                    # checando se está pulando
                    if self.grav_y >= 0:
                        mov_y = pixel[1].top - self.rect.bottom
                        self.grav_y = 0
                        self.no_ar = False
                    # checando se está caindo
                    elif self.grav_y < 0:
                        mov_y = pixel[1].bottom - self.rect.top
                        self.grav_y = 0

            #checando colisão com os inimigos
            if pygame.sprite.spritecollide(self, serra_group, False):
                som_serra.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                som_lava.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, tesoura_group, False):
                som_tesoura.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, bloco_mal_group, False):
                som_bloco.play()
                game_over = -1

            # checando colisão com o portal
            if pygame.sprite.spritecollide(self, portal_group, False):
                som_portal.play()
                game_over = 1

            #atualizando as cordenadas do player de acordo com as interações
            self.rect.x += mov_x
            self.rect.y += mov_y

        elif game_over == -1:
            self.image = self.player_dead
            if self.rect.y > 50:
                self.rect.y -= 5

        tela1.blit(self.image, self.rect)

    def reset(self,x ,y):
        self.imagens_p1 = []

        for num in range(1, 20):
            self.imagens_p1.append(pygame.image.load(f'sprites_mygame/p1_walk{num}.png'))

        self.player_dead = pygame.image.load('sprites_mygame/ghost_dead.png')
        self.player_dead = pygame.transform.scale(self.player_dead, (30, 30))
        self.index_lista = 0
        self.image = self.imagens_p1[self.index_lista]
        self.image = pygame.transform.scale(self.image, (29, 29))
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.grav_y = 0
        self.pulo = False
        self.no_ar = True
        pygame.mixer.music.play(-1, 0, 5000)


#---------------------------------------------------------player 2-----------------------------------------------------#
class PlayerT(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, ):
        global game_over, level
        mov_x = 0
        mov_y = 0

        if game_over == 0:
            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_SPACE] and self.pulo == False and self.no_ar == False:
                female_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_UP] and self.pulo == False and self.no_ar == False:
                female_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_w] and self.pulo == False and self.no_ar == False:
                female_jump.play()
                self.grav_y = -13.1
                self.pulo = True
            if tecla[pygame.K_SPACE] == False and tecla[pygame.K_w] == False and tecla[pygame.K_UP] == False:
                self.pulo = False

            if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                if self.index_lista > 10:
                    self.index_lista = 0
                self.index_lista += 0.30
                self.image = self.imagens_p2[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))
                mov_x += 5

            if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                if self.index_lista <= 10:
                    self.index_lista = 11
                if self.index_lista > 20:
                    self.index_lista = 11
                self.index_lista += 0.30
                self.image = self.imagens_p2[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))
                mov_x -= 5

            if tecla[pygame.K_LEFT] == False and tecla[pygame.K_a] == False and tecla[pygame.K_RIGHT] == False\
            and tecla[pygame.K_d] == False:
                self.index_lista = 21
                self.image = self.imagens_p2[int(self.index_lista)]
                self.image = pygame.transform.scale(self.image, (29, 29))

            #adicionando gravidade
            self.grav_y += 1
            if self.grav_y > 13.01:
                self.grav_y = 13.01
            mov_y += self.grav_y

            # checando colisão
            self.no_ar = True
            for pixel in mundo.pixels_lista:
                # checando colisão na direção x
                if pixel[1].colliderect(self.rect.x + mov_x, self.rect.y, self.width, self.height):
                    mov_x = 0
                # checando colisão na direção y
                if pixel[1].colliderect(self.rect.x, self.rect.y + mov_y, self.width, self.height):
                    # checando se está pulando
                    if self.grav_y >= 0:
                        mov_y = pixel[1].top - self.rect.bottom
                        self.grav_y = 0
                        self.no_ar = False
                    # checando se está caindo
                    elif self.grav_y < 0:
                        mov_y = pixel[1].bottom - self.rect.top
                        self.grav_y = 0

            #checando colisão com os inimigos
            if pygame.sprite.spritecollide(self, serra_group, False):
                som_serra.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                som_lava.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, tesoura_group, False):
                som_tesoura.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, bloco_mal_group, False):
                som_bloco.play()
                game_over = -1

            #checando colisão com o portal
            if pygame.sprite.spritecollide(self, portal_group, False):
                som_portal.play()
                game_over = 1


            #atualizando as cordenadas do player
            self.rect.x += mov_x
            self.rect.y += mov_y

        elif game_over == -1:
            self.image = self.player_dead
            if self.rect.y > 50:
                self.rect.y -= 5

        tela1.blit(self.image, self.rect)

    def reset(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_p2 = []

        for num in range(1, 23):
            self.imagens_p2.append(pygame.image.load(f'sprites_mygame/p2_walk{num}.png'))

        self.player_dead = pygame.image.load('sprites_mygame/ghost_dead.png')
        self.player_dead = pygame.transform.scale(self.player_dead, (30, 30))
        self.index_lista = 0
        self.image = self.imagens_p2[self.index_lista]
        self.image = pygame.transform.scale(self.image, (29, 29))
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.grav_y = 0
        self.pulo = False
        self.no_ar = True
        pygame.mixer.music.play(-1, 0, 5000)

#------------------------------------------------CRIANDO OS INIMIGOS---------------------------------------------------#
class Tesoura(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_tesoura = []

        for num in range(1, 3):
            self.imagens_tesoura.append(pygame.image.load(f'sprites_mygame/barnacle{num}.png'))

        self.index_lista = 0
        self.image = self.imagens_tesoura[self.index_lista]
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.20
        self.image = self.imagens_tesoura[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (40, 40))

class Serra(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_serra = []

        for num in range (1, 3):
            self.imagens_serra.append(pygame.image.load(f'sprites_mygame/spinnerHalf{num}.png'))

        self.index_lista = 0
        self.image = self.imagens_serra[self.index_lista]
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.20
        self.image = self.imagens_serra[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (40, 40))

class BlocoMal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites_mygame/blockerMad.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = 3
        self.count_move = 0

    def update(self):
        self.rect.x += self.move_x
        self.count_move += 1
        if abs(self.count_move) > 27:
            self.move_x *= -1
            self.count_move = 0

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('sprites_mygame/lava.png')
        self.image = pygame.transform.scale(image, (40, 40//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

lava_group = pygame.sprite.Group()
serra_group = pygame.sprite.Group()
tesoura_group = pygame.sprite.Group()
bloco_mal_group = pygame.sprite.Group()

#-------------------------------------------------CRIANDO O PORTAL-----------------------------------------------------#
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f'sprites_mygame/windowOpen.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

portal_group = pygame.sprite.Group()
#------------------------------------------------CRIANDO OS MAPAS------------------------------------------------------#
class Mapas():
    def __init__(self, dados):
        self.pixels_lista = []
        #---------------------------------------------Carregando imagens-----------------------------------------------#
        bloco_grama = pygame.image.load('sprites_mygame/grass.png')
        bloco_terra = pygame.image.load('sprites_mygame/brickWall.png')

        #-------------------------------Inserindo as imagens em cada respectivel pixel---------------------------------#
        count_linhas = 0
        for linha in dados:
            count_colunas = 0
            for pixel in linha:
                if pixel == 1:
                    grama = pygame.transform.scale(bloco_grama, (corte, corte))
                    grama_rect = grama.get_rect()
                    grama_rect.x = count_colunas * corte
                    grama_rect.y = count_linhas * corte
                    pixel = (grama, grama_rect)
                    self.pixels_lista.append(pixel)

                if pixel == 2:
                    tesoura = Tesoura(count_colunas * corte, count_linhas * corte)
                    tesoura_group.add(tesoura)

                if pixel == 3:
                    terra = pygame.transform.scale(bloco_terra, (corte, corte))
                    terra_rect = terra.get_rect()
                    terra_rect.x = count_colunas * corte
                    terra_rect.y = count_linhas * corte
                    pixel = (terra, terra_rect)
                    self.pixels_lista.append(pixel)

                if pixel == 4:
                    serra = Serra(count_colunas * corte, count_linhas * corte)
                    serra_group.add(serra)

                if pixel == 5:
                    portal = Portal(count_colunas * corte, count_linhas * corte)
                    portal_group.add(portal)

                if pixel == 6:
                   lava = Lava(count_colunas * corte, count_linhas * corte + (corte // 2))
                   lava_group.add(lava)

                if pixel == 7:
                    bloco_mal = BlocoMal(count_colunas * corte, count_linhas * corte)
                    bloco_mal_group.add(bloco_mal)


                count_colunas += 1
            count_linhas += 1

    def desenhar_pixel(self):
        for pixel in self.pixels_lista:
            tela1.blit(pixel[0], pixel[1])

#carregando os levels e criando o mundo
if os.path.join(f'level{level}_data', 'rb'):
    pickle_in = open(f'level{level}_data', 'rb')
    mapa = pickle.load(pickle_in)
mundo = Mapas(mapa)

#---------------------------------Criando a classe do game e inserindo o que vai conter nela---------------------------#

class Game():
    def __init__(self):
        self.abrindo, self.jogando = True, False
        self.tecla_cima, self.tecla_baixo, self.tecla_start, self.tecla_back = False, False, False, False
        self.tecla_esq, self.tecla_dir = False, False
        self.largura, self.altura = 440, 440
        self.tela = pygame.Surface((self.largura, self.altura))
        self.janela = pygame.display.set_mode(((self.largura, self.altura)))
        pygame.display.set_caption('Arcade game')
        self.fonte_name = '8-BIT WONDER.TTF'
        self.preto, self.branco = (0,0,0), (255,255,255)
        self.main_menu = MainMenu(self)
        self.curva_menu = self.main_menu
        self.controles = ControlesMenu(self)
        self.creditos = CreditosMenu(self)
        self.sair = SairMenu(self)
        self.saindo = SaindoMenu(self)
        self.preparar = Preparar(self)
        self.atencao = Atencao(self)
        self.pause = Pause(self)
        self.sair_pause = SairPause(self)
        self.confirmar_player = CertezaPlayer(self)
        self.the_end = TheEnd(self)

#----------------------------------------Criando função do loop do game.-----------------------------------------------#

    def loop_do_game(self):
        global game_over, level_next, level, mundo, mapa
        while self.jogando:
            game.checando_interacoes()

            #Dentro do jogo
            tela = pygame.display.set_mode((self.largura, self.altura))
            cenario_base = pygame.image.load('sprites_mygame/cenario1.png').convert()
            cenario = pygame.transform.scale(cenario_base, (self.largura, self.altura))
            pygame.display.set_caption('Arcade')
            tela.blit(cenario, (0, 0))
            relogio.tick(30)
            lava_group.draw(tela)
            bloco_mal_group.draw(tela)
            tesoura_group.draw(tela)
            serra_group.draw(tela)

            #enquanto o player não morre, atualize todos os grupos
            if game_over == 0:
                lava_group.update()
                bloco_mal_group.update()
                tesoura_group.update()
                serra_group.update()

                if self.tecla_back:
                    pygame.mixer.music.stop()
                    som_back.play()
                    self.jogando = False
                    self.curva_menu = self.pause

            #se o jogador morrer, faça isso
            if game_over == -1:
                pygame.mixer.music.stop()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            mapa = []
                            mundo = reset_level(level)
                            game_over = 0
                        if event.key == pygame.QUIT:
                            som_exit.play()
                if restart_botao.draw():
                    mapa = []
                    mundo = reset_level(level)
                    game_over = 0
                if self.tecla_back:
                    pass
            #se o jogador completar o nível e tiver mais adianta, faça:
            if game_over == 1:
                level += 1
                if level <= 6:
                    mapa = []
                    mundo = reset_level(level)
                    game_over = 0

                #se não tiver mais nível disponível, faça:
                else:
                    pygame.mixer.music.stop()
                    som_portal.stop()
                    complete_game.play()
                    level = 1
                    mapa = []
                    mundo = reset_level(level)
                    game_over = 0
                    self.curva_menu = self.the_end
                    self.jogando = False

            #atualizações 
            portal_group.draw(tela)
            mundo.desenhar_pixel()
            player.update()
            pygame.display.flip()
            self.resetando_botoes()

#-------------------------------------Criando função pra checar as interações.-----------------------------------------#

    def checando_interacoes(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando_tela = False
                som_exit.play()
                sleep(0.7)
                self.abrindo, self.jogando = False, False
                self.curva_menu.rodando_tela = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.tecla_start = True
                if event.key == pygame.K_BACKSPACE:
                    self.tecla_back = True
                if event.key == pygame.K_DOWN:
                    self.tecla_baixo = True
                if event.key == pygame.K_UP:
                    self.tecla_cima = True
                if event.key == pygame.K_RIGHT:
                    self.tecla_dir = True
                if event.key == pygame.K_LEFT:
                    self.tecla_esq = True


    def resetando_botoes(self):
        self.tecla_start, self.tecla_cima, self.tecla_baixo, self.tecla_back = False, False, False, False
        self.tecla_dir, self.tecla_esq = False, False

    def desenhando_texto(self, texto, tamanho, x, y):
        fonte = pygame.font.Font(self.fonte_name, tamanho)
        texto_surface = fonte.render(texto, True, self.preto)
        texto_rect = texto_surface.get_rect()
        texto_rect.center = (x, y)
        self.tela.blit(texto_surface, texto_rect)

#-----------------------------------------------Criando a base do menu.------------------------------------------------#

class Menu():
    def __init__(self, game):
        self.game = game
        self.meia_largura, self.meia_altura = self.game.largura / 2, self.game.altura / 2
        self.rodando_tela = True
        self.cursor = pygame.Rect(0, 0, 20, 20)
        self.deslocamento = -100

    def desenhando_cursor(self):
        self.game.desenhando_texto('*', 15, self.cursor.x, self.cursor.y)

    def menu_na_tela(self): #
        self.game.janela.blit(self.game.tela, (0, 0))
        pygame.display.update()
        self.game.resetando_botoes()

#----------------------------------------------Criando classe do menu -------------------------------------------------#

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = "Jogar"
        self.iniciarx, self.iniciary = self.meia_largura, self.meia_altura + 30
        self.controlesx, self.controlesy = self.meia_largura, self.meia_altura + 60
        self.creditosx, self.creditosy = self.meia_largura, self.meia_altura + 90
        self.enterx, self.entery = self.meia_largura, self.meia_altura + 230
        self.cursor.midtop = (self.iniciarx + 35) + self.deslocamento, (self.iniciary - 1)
        self.sairx, self.sairy = self.meia_largura, self.meia_altura + 120

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:

            self.game.checando_interacoes()
            self.checar_move_cursor()
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Arcade', 40, self.game.largura / 2, self.game.altura / 2 - 135)
            self.game.desenhando_texto('Game', 40, self.game.largura / 2, self.game.altura / 2 - 100)
            self.game.desenhando_texto('Jogar', 25, self.iniciarx, self.iniciary)
            self.game.desenhando_texto('Controles', 25, self.controlesx, self.controlesy)
            self.game.desenhando_texto('Creditos', 25, self.creditosx, self.creditosy)
            self.game.desenhando_texto('Sair', 25, self.sairx, self.sairy)
            self.game.desenhando_texto('Acesse com Enter', 13, self.enterx, self.entery)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Jogar':
                self.cursor.midtop = (self.controlesx - 20) + self.deslocamento ,self.controlesy
                self.modo = 'Controles'
            elif self.modo == 'Controles':
                self.cursor.midtop = (self.creditosx + self.deslocamento, self.creditosy)
                self.modo = 'Créditos'
            elif self.modo == 'Créditos':
                self.cursor.midtop = (self.sairx + 50) + self.deslocamento, (self.sairy + 1)
                self.modo = 'Sair'
            elif self.modo == 'Sair':
                self.cursor.midtop = (self.iniciarx + 35) + self.deslocamento, (self.iniciary + 1)
                self.modo = 'Jogar'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Jogar':
                self.cursor.midtop = (self.sairx + 50) + self.deslocamento, (self.sairy + 1)
                self.modo = 'Sair'
            elif self.modo == 'Controles':
                self.cursor.midtop = (self.iniciarx + 35) + self.deslocamento, (self.iniciary + 1)
                self.modo = 'Jogar'
            elif self.modo == 'Créditos':
                self.cursor.midtop = (self.controlesx - 20) + self.deslocamento, self.controlesy
                self.modo = 'Controles'
            elif self.modo == 'Sair':
                self.cursor.midtop = self.creditosx + self.deslocamento, self.creditosy
                self.modo = 'Créditos'

    def checar_move_cursor(self):
        self.mover_cursor()
        if self.game.tecla_start:
            som_select.play()
            if self.modo == 'Jogar':

                self.game.curva_menu = self.game.preparar
            elif self.modo == 'Controles':
                self.game.curva_menu = self.game.controles
            elif self.modo == 'Créditos':
                self.game.curva_menu = self.game.creditos
            elif self.modo == 'Sair':
                self.game.curva_menu = self.game.sair
            self.rodando_tela = False

#-------------------------------------Criando classe dos controles do menu---------------------------------------------#
class ControlesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            if self.game.tecla_back:
                som_back.play()
                self.game.curva_menu = self.game.main_menu
                self.rodando_tela = False
            self.game.tela.fill(self.game.branco)
            self.game.tela.blit(controles_img, (35, 20))
            self.game.desenhando_texto('Controles', 30, self.game.largura / 2, self.game.altura / 2 - 180)
            self.game.desenhando_texto('Restart', 20, 340, 325)
            self.game.desenhando_texto('Volte com backspace', 12, self.meia_largura, self.meia_altura + 180)
            self.menu_na_tela()

#--------------------------------Criando opção de créditos que vai ser inserida no menu--------------------------------#
class CreditosMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            if self.game.tecla_back:
                som_back.play()
                self.game.curva_menu = self.game.main_menu
                self.rodando_tela = False
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Creditos', 30, self.game.largura / 2, self.game.altura / 2 - 125)
            self.game.desenhando_texto('Desenvolvido por', 20, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Herbert Kauan ', 20, self.game.largura / 2, self.game.altura / 2 + 50)
            self.game.desenhando_texto('Volte com backspace', 12, self.meia_largura, self.meia_altura + 180)
            self.menu_na_tela()

#---------------------------------------Criando a opção de Sair do menu------------------------------------------------#
class SairMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'Sim'
        self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()
            if game.tecla_start and self.modo == 'Nao':
                som_select.play()
                self.game.curva_menu = self.game.main_menu
                self.rodando_tela = False
            if game.tecla_start and self.modo == 'Sim':
                som_exit.play()
                self.game.curva_menu = self.game.saindo
                self.rodando_tela = False
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Sair do jogo', 30, self.game.largura / 2, self.game.altura / 2 - 60)
            self.game.desenhando_texto('Sim', 20, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Nao', 20, self.game.largura / 2, self.game.altura / 2 + 50)
            self.game.desenhando_texto('Acesse com Enter', 12, self.game.largura / 2, self.game.altura / 2 + 180)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento , self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

    def checar_move_cursor(self):
        self.mover_cursor()

#---------------------------------------Criando a tela da mensangem de Saindo do game----------------------------------#
class SaindoMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Finalizando gameplay', 20, self.game.largura / 2, self.game.altura / 2)
            self.menu_na_tela()
            sleep(2)
            self.rodando_tela = False
            self.game.abrindo, self.game.jogando = False, False

#------------------------------------Criando a tela de seleção do personagem-------------------------------------------#
class Preparar(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'P1'
        self.cursor.midtop = 190, 220


    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Escolha seu Personagem', 20, self.game.largura / 2, self.game.altura / 2 - 125)
            self.game.tela.blit(player1_img, (200, 200))
            self.game.tela.blit(player2_img, (200, 260))
            self.game.desenhando_texto('Selecione com Enter', 12, self.meia_largura, self.meia_altura + 165)
            self.game.desenhando_texto('Volte com backspace', 12, self.meia_largura, self.meia_altura + 180)
            self.desenhando_cursor()

            if game.tecla_start and self.modo == 'P1':
                som_ok_male.play()
                escolha_do_player.append(player1_img)
                personagem.append(p1_char)
                self.rodando_tela = False
                self.game.curva_menu = self.game.confirmar_player

            if game.tecla_start and self.modo == 'P2':
                som_ok_female.play()
                escolha_do_player.append(player2_img)
                personagem.append(p2_char)
                self.rodando_tela = False
                self.game.curva_menu = self.game.confirmar_player

            if game.tecla_back:
                som_back.play()
                self.rodando_tela = False
                self.game.curva_menu = self.game.main_menu
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'P1':
                self.cursor.midtop = 190, 285
                self.modo = 'P2'
            elif self.modo == 'P2':
                self.cursor.midtop = 190, 220
                self.modo = 'P1'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'P1':
                self.cursor.midtop = 190, 285
                self.modo = 'P2'
            elif self.modo == 'P2':
                self.cursor.midtop = 190, 220
                self.modo = 'P1'

    def checar_move_cursor(self):
        self.mover_cursor()
#----------------------------------------CRIANDO A TELA DE CONFIRMAR O PLAYER------------------------------------------#
class CertezaPlayer(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'Sim'
        self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20

    def menu_na_tela2(self):
        global player
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()

            if game.tecla_start and self.modo == 'Nao':
                som_select.play()
                self.game.curva_menu = self.game.preparar
                self.rodando_tela = False

            if game.tecla_start and self.modo == 'Sim' and personagem[len(personagem) - 1] == p1_char:
                player = PlayerO(0, altura - 80)
                som_select.play()
                self.game.curva_menu = self.game.atencao
                self.rodando_tela = False

            if game.tecla_start and self.modo == 'Sim' and personagem[len(personagem) - 1] == p2_char:
                player = PlayerT(0, altura - 80)
                som_select.play()
                self.game.curva_menu = self.game.atencao
                self.rodando_tela = False


            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Confirma', 20, self.game.largura / 2 - 40, self.game.altura / 2 - 60)
            self.game.tela.blit(escolha_do_player[len(escolha_do_player)-1], (self.game.largura / 2 + 50, self.game.altura / 2 - 80))
            self.game.desenhando_texto('Sim', 20, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Nao', 20, self.game.largura / 2, self.game.altura / 2 + 50)
            self.game.desenhando_texto('Acesse com Enter', 12, self.game.largura / 2, self.game.altura / 2 + 180)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento , self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

    def checar_move_cursor(self):
        self.mover_cursor()

#-------------------------------------Criando a tela de atenção após o start-------------------------------------------#
class Atencao(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            jazz_loop.stop()
            self.game.checando_interacoes()
            if game.tecla_back:
                pass
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('ATENCAO', 40, self.game.largura / 2, self.game.altura / 2)
            self.menu_na_tela()
            sleep(1)
            som_go.play()
            sleep(2)
            self.rodando_tela = False
            self.game.jogando = True


#---------------------------------------Criando a opção de Pause após o Start------------------------------------------#
class Pause(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'Continuar'
        self.cursor.midtop = (self.game.largura / 2 - 115), self.game.altura / 2 + 20

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()

            if game.tecla_start and self.modo == 'Continuar':

                som_select.play()
                pygame.mixer.music.play(-1, 0, 5000)
                self.rodando_tela = False
                self.game.jogando = True

            if game.tecla_start and self.modo == 'Sair':
                som_select.play()
                self.game.curva_menu = self.game.sair_pause
                self.rodando_tela = False

            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Pause', 50, self.game.largura / 2, self.game.altura / 2 - 125)
            self.game.desenhando_texto('Continuar', 25, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Sair', 25, self.game.largura / 2, self.game.altura / 2 + 80)
            self.game.desenhando_texto('Acesse com Enter', 12, self.game.largura / 2, self.game.altura / 2 + 180)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Continuar':
                self.cursor.midtop = (self.game.largura / 2 - 50), self.game.altura / 2 + 80
                self.modo = 'Sair'
            elif self.modo == 'Sair':
                self.cursor.midtop = (self.game.largura / 2 - 115), self.game.altura / 2 + 20
                self.modo = 'Continuar'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Continuar':
                self.cursor.midtop = (self.game.largura / 2 - 50), self.game.altura / 2 + 80
                self.modo = 'Sair'
            elif self.modo == 'Sair':
                self.cursor.midtop = (self.game.largura / 2 - 115), self.game.altura / 2 + 20
                self.modo = 'Continuar'

    def checar_move_cursor(self):
        self.mover_cursor()

#-------------------------------------Criando a opção de Sair durante o pause------------------------------------------#
class SairPause(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'Sim'
        self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20

    def menu_na_tela2(self):
        self.rodando_tela = True
        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()
            if game.tecla_start and self.modo == 'Nao':
                som_select.play()
                self.game.curva_menu = self.game.pause
                self.rodando_tela = False
            if game.tecla_start and self.modo == 'Sim':
                som_exit.play()
                self.game.curva_menu = self.game.saindo
                self.rodando_tela = False
            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('Sair do jogo', 40, self.game.largura / 2, self.game.altura / 2 - 60)
            self.game.desenhando_texto('Sim', 20, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Nao', 20, self.game.largura / 2, self.game.altura / 2 + 50)
            self.game.desenhando_texto('Acesse com Enter', 12, self.game.largura / 2, self.game.altura / 2 + 180)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento , self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Sim':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 50
                self.modo = 'Nao'
            elif self.modo == 'Nao':
                self.cursor.midtop = (self.game.largura / 2 + 60) + self.deslocamento, self.game.altura / 2 + 20
                self.modo = 'Sim'

    def checar_move_cursor(self):
        self.mover_cursor()

#-----------------------------------------CRIANDO TELA DE ZERANDO O JOGO-----------------------------------------------#
class TheEnd(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.modo = 'Reiniciar Game'
        self.cursor.midtop = self.game.largura / 2 - 170, self.game.altura / 2 + 20

    def menu_na_tela2(self):
        self.rodando_tela = True
        pygame.mixer.music.stop()

        while self.rodando_tela:
            self.game.checando_interacoes()
            self.checar_move_cursor()

            if game.tecla_start and self.modo == 'Menu Principal':
                som_select.play()
                jazz_loop.play(-1)
                self.rodando_tela = False
                self.game.curva_menu = self.game.main_menu

            if game.tecla_start and self.modo == 'Reiniciar Game' and personagem[len(personagem) - 1] == p1_char:
                som_ok_male.play()
                pygame.mixer.music.play(-1, 0, 5000)
                self.rodando_tela = False
                self.game.curva_menu = self.game.atencao

            if game.tecla_start and self.modo == 'Reiniciar Game' and personagem[len(personagem) - 1] == p2_char:
                som_ok_female.play()
                pygame.mixer.music.play(-1, 0, 5000)
                self.rodando_tela = False
                self.game.curva_menu = self.game.atencao


            self.game.tela.fill(self.game.branco)
            self.game.desenhando_texto('THE END', 50, self.game.largura / 2, self.game.altura / 2 - 125)
            self.game.desenhando_texto('Reiniciar Game', 25, self.game.largura / 2, self.game.altura / 2 + 20)
            self.game.desenhando_texto('Menu Principal', 25, self.game.largura / 2, self.game.altura / 2 + 50)
            self.game.desenhando_texto('Acesse com Enter', 12, self.game.largura / 2, self.game.altura / 2 + 180)
            self.desenhando_cursor()
            self.menu_na_tela()

    def mover_cursor(self):
        if self.game.tecla_baixo:
            som_change.play()
            if self.modo == 'Reiniciar Game':
                self.cursor.midtop = self.game.largura / 2 - 170, self.game.altura / 2 + 50
                self.modo = 'Menu Principal'
            elif self.modo == 'Menu Principal':
                self.cursor.midtop = self.game.largura / 2 - 170, self.game.altura / 2 + 20
                self.modo = 'Reiniciar Game'

        elif self.game.tecla_cima:
            som_change.play()
            if self.modo == 'Reiniciar Game':
                self.cursor.midtop = self.game.largura / 2 - 170, self.game.altura / 2 + 50
                self.modo = 'Menu Principal'
            elif self.modo == 'Menu Principal':
                self.cursor.midtop = self.game.largura / 2 - 170, self.game.altura / 2 + 20
                self.modo = 'Reiniciar Game'

    def checar_move_cursor(self):
        self.mover_cursor()
#----------------------------------------------INICIALIZANDO O GAME!---------------------------------------------------#
game = Game()
while game.abrindo:
    game.curva_menu.menu_na_tela2()
    game.loop_do_game()

