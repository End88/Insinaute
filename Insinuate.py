import pygame
import random
import math

BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
DOURADO = (218, 165, 32)
LARANJA = (250, 92, 0)

class MovimentoInimigo:
    def __init__(self, inimigo):
        self.inimigo = inimigo

    def atualizar_posicao(self):
        pass

class MovimentoCoração(MovimentoInimigo):
    def atualizar_posicao(self):
        # Atualize o tempo
        self.inimigo.t += self.inimigo.velocidade  # Ajuste a velocidade da animação

        # Calcule as coordenadas x e y com base nas equações do coração
        x = self.inimigo.a * (math.sin(self.inimigo.t) ** 3)
        y = self.inimigo.b * math.cos(self.inimigo.t) - 5 * math.cos(2 * self.inimigo.t) - 2 * math.cos(3 * self.inimigo.t) - math.cos(4 * self.inimigo.t)

        x *= self.inimigo.scale_factor
        y *= self.inimigo.scale_factor

        # Atualize a posição do inimigo em relação ao centro do coração
        self.inimigo.posicao_x = self.inimigo.posicao[0] + x
        self.inimigo.posicao_y = self.inimigo.posicao[1] - y

class MovimentoRosaPolareoito(MovimentoInimigo):
    def atualizar_posicao(self):
        self.inimigo.t += self.inimigo.velocidade  # Ajuste a velocidade da animação

        # Calcule as coordenadas x e y com base nas equações do coração
        x = self.inimigo.a * math.cos(4 * self.inimigo.t) * math.cos(self.inimigo.t)
        y = self.inimigo.b * math.cos(4 * self.inimigo.t) * math.sin(self.inimigo.t)

        x *= self.inimigo.scale_factor
        y *= self.inimigo.scale_factor

        # Atualize a posição do inimigo em relação ao centro do coração
        self.inimigo.posicao_x = self.inimigo.posicao[0] + x
        self.inimigo.posicao_y = self.inimigo.posicao[1] - y

class MovimentoRosaPolaretres(MovimentoInimigo):
    def atualizar_posicao(self):
        self.inimigo.t += self.inimigo.velocidade  # Ajuste a velocidade da animação

        # Calcule as coordenadas x e y com base nas equações do coração
        x = self.inimigo.a * math.cos(3 * self.inimigo.t) * math.cos(self.inimigo.t)
        y = self.inimigo.b * math.cos(3 * self.inimigo.t) * math.sin(self.inimigo.t)

        x *= self.inimigo.scale_factor
        y *= self.inimigo.scale_factor

        # Atualize a posição do inimigo em relação ao centro do coração
        self.inimigo.posicao_x = self.inimigo.posicao[0] + x
        self.inimigo.posicao_y = self.inimigo.posicao[1] - y

class MovimentoRosaPolareDuploCirco(MovimentoInimigo):
    def atualizar_posicao(self):
        self.inimigo.t += self.inimigo.velocidade  # Ajuste a velocidade da animação

        # Calcule as coordenadas x e y com base nas equações do coração
        x = self.inimigo.a * math.cos(3 * self.inimigo.t) * math.cos(6 * self.inimigo.t)
        y = self.inimigo.b * math.cos(3 * self.inimigo.t) * math.sin(6 * self.inimigo.t)

        x *= self.inimigo.scale_factor
        y *= self.inimigo.scale_factor

        # Atualize a posição do inimigo em relação ao centro do coração
        self.inimigo.posicao_x = self.inimigo.posicao[0] + x
        self.inimigo.posicao_y = self.inimigo.posicao[1] - y

class Parede:
    def __init__(self, cor, x, y, largura, altura):
        self.cor = cor
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        # Desenhe o inimigo na tela
        if self.cor == AZUL:
            cor = (0, 143, 203)
        elif self.cor == VERMELHO:
            cor = (255, 112, 52)
        else:
            cor = self.cor
        pygame.draw.rect(tela, cor, self.rect)

class Personagem:
    def __init__(self, cor, posicao_inicial):
        self.cor = cor
        self.posicao_inicial = tuple(posicao_inicial)  # Armazenado como tupla
        self.posicao = posicao_inicial
        self.velocidade = 3

        # Poder de acelerar/desacelerar inimigos
        self.poder_usando = False
        self.charge_power = False
        self.poder_cooldown = 50
        self.poder_duration = 2  # Duração do poder em segundos
        self.poder_max_duration = 100

    def inverter_posicoes(self, outro_personagem):
        self.posicao, outro_personagem.posicao = outro_personagem.posicao, self.posicao

    # Métodos para verificar se o jogador pode usar o poder e iniciar o poder
    def pode_usar_poder(self):
        return self.poder_usando and not self.charge_power

    def usar_poder(self, tipo_poder):
        if self.pode_usar_poder():
            custo = 1
            if self.poder_cooldown - custo >= 0:
                self.poder_cooldown -= custo
            else:
                self.charge_power = True
            self.tipo_poder = tipo_poder

    def atualizar_poder_cooldown(self, inimigos):
        if not self.poder_usando or self.charge_power:
            if self.poder_cooldown < self.poder_max_duration:
                self.poder_cooldown += 1

                for inimigo in inimigos:
                    inimigo.velocidade = inimigo.velocidade_inicial

                self.tipo_poder = ""
            elif self.poder_cooldown > self.poder_max_duration:
                self.poder_cooldown = self.poder_max_duration
            elif self.poder_cooldown == self.poder_max_duration:
                self.charge_power = False

    def esta_carregando(self):
        if not self.poder_usando and self.poder_cooldown < self.poder_max_duration:
            self.charge_power = True

    def colide_com_parede(self, parede):
        # Verifica se o jogador colide com uma parede
        return pygame.Rect(*self.posicao, 5, 10).colliderect(parede)

    def colide_com_inimigo(self, inimigo):
        # Verifica se o jogador colidiu com um inimigo
        raio_bolinha = 10
        raio_inimigo = 10

        # Coordenadas do centro da bolinha
        x_bolinha = self.posicao[0] + raio_bolinha
        y_bolinha = self.posicao[1] + raio_bolinha

        # Coordenadas do centro do inimigo
        x_inimigo = inimigo.posicao_x + raio_inimigo
        y_inimigo = inimigo.posicao_y + raio_inimigo

        # Distância entre o centro da bolinha e o centro do inimigo
        distancia = math.sqrt((x_inimigo - x_bolinha)**2 + (y_inimigo - y_bolinha)**2)

        # Soma dos raios da bolinha e do inimigo
        soma_raios = raio_bolinha + raio_inimigo

        # Verifica se ocorreu colisão
        colisao = distancia < soma_raios

        return colisao

    def mover_teclado(self, teclas, paredes, posicao_inicial):
        # Mover o personagem com base nas teclas pressionadas
        direcao = [0, 0]
        if teclas[pygame.K_w]:
            direcao[1] -= 1
        if teclas[pygame.K_s]:
            direcao[1] += 1
        if teclas[pygame.K_a]:
            direcao[0] -= 1
        if teclas[pygame.K_d]:
            direcao[0] += 1

        # Normalizar a direção para evitar movimento diagonal mais rápido
        if direcao[0] != 0 and direcao[1] != 0:
            direcao[0] /= 1.414
            direcao[1] /= 1.414

        # Atualizar a posição do personagem com base na direção e velocidade
        self.posicao[0] += direcao[0] * self.velocidade
        self.posicao[1] += direcao[1] * self.velocidade

    def mover_setas(self, teclas, paredes, posicao_inicial):
        # Mover o personagem com base nas teclas pressionadas
        direcao = [0, 0]
        if teclas[pygame.K_UP]:
            direcao[1] -= 1
        if teclas[pygame.K_DOWN]:
            direcao[1] += 1
        if teclas[pygame.K_LEFT]:
            direcao[0] -= 1
        if teclas[pygame.K_RIGHT]:
            direcao[0] += 1

        # Normalizar a direção para evitar movimento diagonal mais rápido
        if direcao[0] != 0 and direcao[1] != 0:
            direcao[0] /= 1.414
            direcao[1] /= 1.414

        # Atualizar a posição do personagem com base na direção e velocidade
        self.posicao[0] += direcao[0] * self.velocidade
        self.posicao[1] += direcao[1] * self.velocidade

    def mover_controle(self, joystick, paredes, posicao_inicial):
        # Mover o personagem com base no analógico esquerdo do controle
        direcao = [joystick.get_axis(0), joystick.get_axis(1)]

        # Verificar se o analógico está sendo movido significativamente
        if abs(direcao[0]) < 0.2:
            direcao[0] = 0
        if abs(direcao[1]) < 0.2:
            direcao[1] = 0

        # Normalizar a direção para evitar movimento diagonal mais rápido
        if direcao[0] != 0 and direcao[1] != 0:
            direcao[0] /= 1.414
            direcao[1] /= 1.414

        # Atualizar a posição do personagem com base na direção e velocidade
        self.posicao[0] += direcao[0] * self.velocidade
        self.posicao[1] += direcao[1] * self.velocidade

    def renderizar(self, tela):
        # Desenhar o personagem na tela
        pygame.draw.circle(tela, self.cor, [int(self.posicao[0]), int(self.posicao[1])], 10)

class Inimigo:
    def __init__(self, cor, posicao_init, a, b, velocidade, movimento="", scale_factor=5):
        self.cor = cor
        self.posicao = posicao_init
        self.a = a
        self.b = b
        self.t = 0
        self.raio = 5
        self.velocidade = velocidade
        self.velocidade_inicial = velocidade
        self.scale_factor = scale_factor
        self.movimento = movimento

    def atualizar_posicao(self):
        self.movimento.atualizar_posicao()


    def renderizar(self, tela):
        # Desenhe o inimigo na tela
        if self.cor == AZUL:
            cor = (0, 143, 203)
        elif self.cor == VERMELHO:
            cor = (255, 112, 52)
        else:
            cor = self.cor
        pygame.draw.circle(tela, cor, [int(self.posicao_x), int(self.posicao_y)], self.raio)

class FaseTeste:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.bolinha1 = Personagem(VERMELHO, [self.largura // 4, self.altura // 2])
        self.bolinha2 = Personagem(AZUL, [self.largura * 3 // 4, self.altura // 2])
        self.paredes = [
            # Exemplo de paredes com cores diferentes
            Parede(BRANCO, largura // 2 - 100, altura // 4, 200, 20),
            Parede(BRANCO, largura // 2 - 100, altura * 3 // 4, 200, 20)
        ]
        # Exemplo de paredes com a mesma cor das bolinhas, onde não haverá colisão
        self.paredes.append(Parede(VERMELHO, largura // 4, altura // 2 - 100, 20, 200))
        self.paredes.append(Parede(AZUL, largura * 3 // 4, altura // 2 - 100, 20, 200))
        # Atribuir a cor da parede igual à cor do jogador correspondente
        self.paredes[-2].cor = VERMELHO  # Cor da parede igual à cor da bolinha1
        self.paredes[-1].cor = AZUL  # Cor da parede igual à cor da bolinha2

        self.inimigos = []

        # para coração: a=16 b=13
        # Rosas polares: a=20 b=20
        # Adicionar um inimigo
        for i in range(10):
            velocidade = i/200
            inimigo = Inimigo(CINZA, (largura // 2, altura // 2), a=20, b=20, velocidade=velocidade, scale_factor=5)
            movimento = MovimentoRosaPolaretres(inimigo)
            inimigo.movimento = movimento
            self.inimigos.append(inimigo)

    def aplicar_poderes(self, inimigos):
        if self.bolinha1.poder_usando and not self.bolinha1.charge_power:
            self.aplicar_poder(self.bolinha1)
        else:
            self.bolinha1.atualizar_poder_cooldown(inimigos)

        if self.bolinha2.poder_usando and not self.bolinha2.charge_power:
            self.aplicar_poder(self.bolinha2)
        else:
            self.bolinha2.atualizar_poder_cooldown(inimigos)

    def aplicar_poder(self, jogador):
        for idx, inimigo in enumerate(self.inimigos):

            if inimigo.cor == CINZA:
                # Bolinhas cinzas são afetadas somente se ambos os jogadores usarem o poder juntos
                if self.bolinha1.poder_usando and self.bolinha2.poder_usando:
                    if jogador.tipo_poder == 'acelerar':
                        velocidade_max = idx / 50
                        if inimigo.velocidade <= velocidade_max:
                            if inimigo.velocidade != 0:
                                inimigo.velocidade = inimigo.velocidade * 1.1
                    elif jogador.tipo_poder == 'desacelerar':
                        velocidade_min = idx / 300
                        if inimigo.velocidade >= velocidade_min:
                            inimigo.velocidade = inimigo.velocidade * 0.9

            elif inimigo.cor == jogador.cor:
                if jogador.tipo_poder == 'acelerar':
                    velocidade_max = idx / 50
                    if inimigo.velocidade <= velocidade_max:
                        if inimigo.velocidade != 0:
                            inimigo.velocidade = inimigo.velocidade * 1.1
                elif jogador.tipo_poder == 'desacelerar':
                    velocidade_min = idx / 300
                    if inimigo.velocidade >= velocidade_min:
                        inimigo.velocidade = inimigo.velocidade * 0.9

    def verificar_colisao_paredes(self):
        # Verifica a colisão entre os personagens e as paredes
        for personagem in [self.bolinha1, self.bolinha2]:
            for parede in self.paredes:
                if personagem.colide_com_parede(parede):
                    if personagem.cor != parede.cor:
                        # Efeito da colisão: retornar à posição inicial
                        personagem.posicao[0], personagem.posicao[1] = personagem.posicao_inicial

    def atualizar(self):
        # Atualize a lógica da fase, movimentação dos inimigos, etc.
        # Verifica colisão entre jogadores e inimigos
        for inimigo in self.inimigos:
            inimigo.atualizar_posicao()
            if self.bolinha1.colide_com_inimigo(inimigo):
                self.bolinha1.posicao[0], self.bolinha1.posicao[1] = self.bolinha1.posicao_inicial

            if self.bolinha2.colide_com_inimigo(inimigo):
                self.bolinha2.posicao[0], self.bolinha2.posicao[1] = self.bolinha2.posicao_inicial
        self.verificar_colisao_paredes()
        self.aplicar_poderes(self.inimigos)


    def renderizar(self, tela):
        # Renderizar os elementos da fase na tela
        # Renderizar as bolinhas dos jogadores
        self.bolinha1.renderizar(tela)
        self.bolinha2.renderizar(tela)

        # Renderizar as paredes
        for parede in self.paredes:
            parede.desenhar(tela)

        # Renderize os inimigos
        for inimigo in self.inimigos:
            inimigo.renderizar(tela)

class FaseUm:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.bolinha1 = Personagem(VERMELHO, [self.largura // 7.5, self.altura // 10 * 9])
        self.bolinha2 = Personagem(AZUL, [self.largura * 7 // 8, self.altura // 10 * 9])
        self.paredes = [
            # Exemplo de paredes com cores diferentes
            Parede(BRANCO, 0, 0, largura, 10),
            Parede(BRANCO, 0, 0, 10, altura),
            Parede(BRANCO, largura - 10, 0, 10, altura),
            Parede(BRANCO, 0, altura - 10, largura, 10),
            Parede(BRANCO, largura // 4, 100, 10, altura),
            Parede(BRANCO, largura // 4 * 3, 100, 10, altura),

            Parede(AZUL, 10, altura // 4, largura // 4-10, altura // 4),
            Parede(VERMELHO, largura // 4 * 3 + 10, altura // 4, largura // 4-20, altura // 4),

            Parede(VERMELHO, 10, altura // 4 * 2.5, largura // 4 - 10, altura // 4),
            Parede(AZUL, largura // 4 * 3 + 10, altura // 4 * 2.5, largura // 4 - 20, altura // 4)
        ]

        self.inimigos = []

        # para coração: a=16 b=13
        # Rosas polares: a=20 b=20
        # Adicionar um inimigo
        for i in range(10):
            velocidade = i/250
            inimigo = Inimigo(CINZA, (largura // 2, altura // 2), a=20, b=20, velocidade=velocidade, scale_factor=9)
            movimento = MovimentoRosaPolareoito(inimigo)
            inimigo.movimento = movimento
            self.inimigos.append(inimigo)

        for i in range(10):
            velocidade = i/500
            inimigo = Inimigo(VERMELHO, (largura // 8.5, altura // 2.65), a=25, b=20, velocidade=velocidade, scale_factor=5)
            movimento = MovimentoRosaPolareDuploCirco(inimigo)
            inimigo.movimento = movimento
            self.inimigos.append(inimigo)

        for i in range(10):
            velocidade = i/500
            inimigo = Inimigo(AZUL, (largura // 8.5 * 7.5 - 20, altura // 2.65), a=25, b=20, velocidade=velocidade, scale_factor=5)
            movimento = MovimentoRosaPolareDuploCirco(inimigo)
            inimigo.movimento = movimento
            self.inimigos.append(inimigo)

    def aplicar_poderes(self, inimigos):
        if self.bolinha1.poder_usando and not self.bolinha1.charge_power:
            self.aplicar_poder(self.bolinha1)
        else:
            self.bolinha1.atualizar_poder_cooldown(inimigos)

        if self.bolinha2.poder_usando and not self.bolinha2.charge_power:
            self.aplicar_poder(self.bolinha2)
        else:
            self.bolinha2.atualizar_poder_cooldown(inimigos)

    def aplicar_poder(self, jogador):
        for idx, inimigo in enumerate(self.inimigos):

            if inimigo.cor == CINZA:
                # Bolinhas cinzas são afetadas somente se ambos os jogadores usarem o poder juntos
                if self.bolinha1.poder_usando and self.bolinha2.poder_usando:
                    if jogador.tipo_poder == 'acelerar':
                        velocidade_max = idx / 50
                        if inimigo.velocidade <= velocidade_max:
                            if inimigo.velocidade != 0:
                                inimigo.velocidade = inimigo.velocidade * 1.1
                    elif jogador.tipo_poder == 'desacelerar':
                        velocidade_min = idx / 300
                        if inimigo.velocidade >= velocidade_min:
                            inimigo.velocidade = inimigo.velocidade * 0.9

            elif inimigo.cor == jogador.cor:
                if jogador.tipo_poder == 'acelerar':
                    velocidade_max = idx / 50
                    if inimigo.velocidade <= velocidade_max:
                        if inimigo.velocidade != 0:
                            inimigo.velocidade = inimigo.velocidade * 1.1
                elif jogador.tipo_poder == 'desacelerar':
                    velocidade_min = idx / 300
                    if inimigo.velocidade >= velocidade_min:
                        inimigo.velocidade = inimigo.velocidade * 0.9

    def verificar_colisao_paredes(self):
        # Verifica a colisão entre os personagens e as paredes
        for personagem in [self.bolinha1, self.bolinha2]:
            for parede in self.paredes:
                if personagem.colide_com_parede(parede):
                    if personagem.cor != parede.cor:
                        # Efeito da colisão: retornar à posição inicial
                        personagem.posicao[0], personagem.posicao[1] = personagem.posicao_inicial

    def atualizar(self):
        # Atualize a lógica da fase, movimentação dos inimigos, etc.
        # Verifica colisão entre jogadores e inimigos
        for inimigo in self.inimigos:
            inimigo.atualizar_posicao()
            if self.bolinha1.colide_com_inimigo(inimigo):
                self.bolinha1.posicao[0], self.bolinha1.posicao[1] = self.bolinha1.posicao_inicial

            if self.bolinha2.colide_com_inimigo(inimigo):
                self.bolinha2.posicao[0], self.bolinha2.posicao[1] = self.bolinha2.posicao_inicial
        self.verificar_colisao_paredes()
        self.aplicar_poderes(self.inimigos)


    def renderizar(self, tela):
        # Renderizar os elementos da fase na tela
        # Renderizar as paredes
        for parede in self.paredes:
            parede.desenhar(tela)

        # Renderize os inimigos
        for inimigo in self.inimigos:
            inimigo.renderizar(tela)

        # Renderizar as bolinhas dos jogadores
        self.bolinha1.renderizar(tela)
        self.bolinha2.renderizar(tela)

class GameManager:
    def __init__(self, largura, altura, fps):
        self.largura = largura
        self.altura = altura
        self.fps = fps
        self.tela = pygame.display.set_mode((largura, altura))

        # ________________________________________________ Define ícone e nome do jogo
        icone = pygame.image.load('data/images/Icone.ico')
        pygame.display.set_caption("Insinuate 0.1")
        pygame.display.set_icon(icone)

        pygame.mixer.init()
        pygame.mixer.music.load("data/musics/rainbow_falls.wav")
        pygame.mixer.music.set_volume(0.1)

        # Inicialize o controle de joystick
        pygame.joystick.init()
        self.controllers = []
        for i in range(pygame.joystick.get_count()):
            controller = pygame.joystick.Joystick(i)
            controller.init()
            self.controllers.append(controller)

        self.clock = pygame.time.Clock()

        self.executando = False
        self.fase_atual = None

        self.o_is_pressed = 0
        self.f_is_pressed = 0
        self.button3_player_1_is_pressed = 0
        self.button3_player_2_is_pressed = 0

        self.x_is_pressed = 0
        self.l_is_pressed = 0
        self.z_is_pressed = 0
        self.k_is_pressed = 0
        self.botton4_player_1_is_pressed = 0
        self.botton4_player_2_is_pressed = 0
        self.botton5_player_1_is_pressed = 0
        self.botton5_player_2_is_pressed = 0

    def _inicializar_controles(self):
        controllers = []
        for i in range(pygame.joystick.get_count()):
            controller = pygame.joystick.Joystick(i)
            controller.init()
            controllers.append(controller)
        return controllers

    def iniciar(self):
        self.executando = True
        self.fase_atual = FaseUm(self.largura, self.altura)
        # Inicie a nova música com fade in
        pygame.mixer.music.play(fade_ms=2000)  # Fade-in de 2 segundos


        while self.executando:
            self._lidar_eventos(self.fase_atual.paredes)
            self._atualizar()
            self._renderizar()
            
        pygame.mixer.music.fadeout(2000)  # Fade out de 2 segundos
        pygame.quit()

    def _lidar_eventos(self, paredes):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False

            # Verifica se um novo controle foi adicionado
            elif evento.type == pygame.JOYDEVICEADDED:
                self.controllers = self._inicializar_controles()

            # Verifica se um controle foi removido
            elif evento.type == pygame.JOYDEVICEREMOVED:
                self.controllers = self._inicializar_controles()

        # Capturar as teclas pressionadas
        teclas = pygame.key.get_pressed()

        # Movimentar o jogador 1 usando o teclado
        self.fase_atual.bolinha1.mover_teclado(teclas, paredes, self.fase_atual.bolinha1.posicao_inicial)

        # Movimentar o jogador 2 usando as setas
        self.fase_atual.bolinha2.mover_setas(teclas, paredes, self.fase_atual.bolinha2.posicao_inicial)

        # ____________________________________________________ Teclado
        # Verificar os poderes de acelerar/desacelerar inimigos
        if teclas[pygame.K_x]:
            self.x_is_pressed = 1
            self.fase_atual.bolinha1.poder_usando = True
            self.fase_atual.bolinha1.usar_poder('acelerar')
        else:
            if self.x_is_pressed == 1:
                self.x_is_pressed = 0
                self.fase_atual.bolinha1.poder_usando = False
                self.fase_atual.bolinha1.esta_carregando()

        if teclas[pygame.K_l]:
            self.l_is_pressed = 1
            self.fase_atual.bolinha2.poder_usando = True
            self.fase_atual.bolinha2.usar_poder('acelerar')
        else:
            if self.l_is_pressed == 1:
                self.l_is_pressed = 0
                self.fase_atual.bolinha2.poder_usando = False
                self.fase_atual.bolinha2.esta_carregando()

        if teclas[pygame.K_z]:
            self.z_is_pressed = 1
            self.fase_atual.bolinha1.poder_usando = True
            self.fase_atual.bolinha1.usar_poder('desacelerar')
        else:
            if self.z_is_pressed == 1:
                self.z_is_pressed = 0
                self.fase_atual.bolinha1.poder_usando = False
                self.fase_atual.bolinha1.esta_carregando()

        if teclas[pygame.K_k]:
            self.k_is_pressed = 1
            self.fase_atual.bolinha2.poder_usando = True
            self.fase_atual.bolinha2.usar_poder('desacelerar')
        else:
            if self.k_is_pressed == 1:
                self.k_is_pressed = 0
                self.fase_atual.bolinha2.poder_usando = False
                self.fase_atual.bolinha2.esta_carregando()

        # Inverter posições usando teclado
        if teclas[pygame.K_f]:
            if not self.f_is_pressed:
                self.fase_atual.bolinha1.inverter_posicoes(self.fase_atual.bolinha2)
                self.f_is_pressed = True
        else:
            self.f_is_pressed = False

        if teclas[pygame.K_o]:
            if not self.o_is_pressed:
                self.fase_atual.bolinha2.inverter_posicoes(self.fase_atual.bolinha1)
                self.o_is_pressed = True
        else:
            self.o_is_pressed = False

        # ____________________________________________________________ Controle
        # Movimentar o jogador 1 usando o controle
        if self.controllers and self.controllers[0].get_numaxes() >= 2:
            self.fase_atual.bolinha1.mover_controle(self.controllers[0], self.fase_atual.paredes, self.fase_atual.bolinha1.posicao_inicial)

            if self.controllers[0].get_button(3):
                if not self.button3_player_1_is_pressed:
                    self.fase_atual.bolinha1.inverter_posicoes(self.fase_atual.bolinha2)
                self.button3_player_1_is_pressed = True
            else:
                self.button3_player_1_is_pressed = False

            # Player 1 acelera ao pressionar RB/ R1
            if self.controllers[0].get_button(5):
                self.botton5_player_1_is_pressed = 1
                self.fase_atual.bolinha1.poder_usando = True
                self.fase_atual.bolinha1.usar_poder('acelerar')
            else:
                if self.botton5_player_1_is_pressed == 1:
                    self.botton5_player_1_is_pressed = 0
                    self.fase_atual.bolinha1.poder_usando = False
                    self.fase_atual.bolinha1.esta_carregando()

            # Player 1 desacelera ao pressionar LB/ L1
            if self.controllers[0].get_button(4):
                self.botton4_player_1_is_pressed = 1
                self.fase_atual.bolinha1.poder_usando = True
                self.fase_atual.bolinha1.usar_poder('desacelerar')
            else:
                if self.botton4_player_1_is_pressed == 1:
                    self.botton4_player_1_is_pressed = 0
                    self.fase_atual.bolinha1.poder_usando = False
                    self.fase_atual.bolinha1.esta_carregando()


        # Movimentar o jogador 2 usando o controle
        if len(self.controllers) > 1 and self.controllers[1].get_numaxes() >= 2:
            self.fase_atual.bolinha2.mover_controle(self.controllers[1], self.fase_atual.paredes, self.fase_atual.bolinha1.posicao_inicial)

            if self.controllers[1].get_button(3):
                if not self.button3_player_2_is_pressed:
                    self.fase_atual.bolinha2.inverter_posicoes(self.fase_atual.bolinha1)
                self.button3_player_2_is_pressed = True
            else:
                self.button3_player_2_is_pressed = False

            # Player 2 acelera ao pressionar RB/ R1
            if self.controllers[1].get_button(5):
                self.botton5_player_2_is_pressed = 1
                self.fase_atual.bolinha2.poder_usando = True
                self.fase_atual.bolinha2.usar_poder('acelerar')
            else:
                if self.botton5_player_2_is_pressed == 1:
                    self.botton5_player_2_is_pressed = 0
                    self.fase_atual.bolinha2.poder_usando = False
                    self.fase_atual.bolinha2.esta_carregando()

            # Player 2 desacelera ao pressionar LB/ L1
            if self.controllers[1].get_button(4):
                self.botton4_player_2_is_pressed = 1
                self.fase_atual.bolinha2.poder_usando = True
                self.fase_atual.bolinha2.usar_poder('desacelerar')
            else:
                if self.botton4_player_2_is_pressed == 1:
                    self.botton4_player_2_is_pressed = 0
                    self.fase_atual.bolinha2.poder_usando = False
                    self.fase_atual.bolinha2.esta_carregando()


    def _atualizar(self):
        self.fase_atual.atualizar()

    def _renderizar(self):
        self.tela.fill((0, 0, 0))

        # Renderizar a fase atual
        self.fase_atual.renderizar(self.tela)
        if self.fase_atual.bolinha1.charge_power:
            self.cor_barra_1 = LARANJA
        else:
            self.cor_barra_1 = DOURADO

        if self.fase_atual.bolinha2.charge_power:
            self.cor_barra_2 = LARANJA
        else:
            self.cor_barra_2 = DOURADO

        pygame.draw.rect(self.tela, self.cor_barra_1, [50, 50, self.fase_atual.bolinha1.poder_cooldown, 10])
        pygame.draw.rect(self.tela, self.cor_barra_2, [width-self.fase_atual.bolinha2.poder_max_duration-50, 50, self.fase_atual.bolinha2.poder_cooldown, 10])

        pygame.display.flip()
        self.clock.tick(self.fps)

# Defina as dimensões da janela
width = 800
height = 600

game = GameManager(width, height, 30)
game.iniciar()