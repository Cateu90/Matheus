import pygame
import sys
import random
import json

pygame.init()

BRANCO = (255, 255, 255)
PRETO = (1, 1, 1)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

LARGURA, ALTURA = 800, 600
TAMANHO_ALVO = 50
TAMANHO_JOGADOR = 25
FPS = 60

FONTE = pygame.font.SysFont('arial', 40, True, True)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tiro ao Alvo")

relogio = pygame.time.Clock()

class Alvo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TAMANHO_ALVO, TAMANHO_ALVO), pygame.SRCALPHA)
        self.desenhar_alvo()
        self.rect = self.image.get_rect()
        self.resetar()

    def desenhar_alvo(self):
        raio_grande = TAMANHO_ALVO // 2
        raio_pequeno = raio_grande // 5
        cores = [(0, 0, 0), (255, 255, 255)]
        for i, raio in enumerate(range(raio_grande, 0, -raio_pequeno * 2)):
            cor = cores[i % len(cores)]
            pygame.draw.circle(self.image, cor, (TAMANHO_ALVO // 2, TAMANHO_ALVO // 2), raio)

    def resetar(self):
        self.rect.center = (random.randint(TAMANHO_ALVO, LARGURA - TAMANHO_ALVO), random.randint(TAMANHO_ALVO, ALTURA - TAMANHO_ALVO))


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TAMANHO_JOGADOR, TAMANHO_JOGADOR))
        pygame.draw.line(self.image, BRANCO, (0, TAMANHO_JOGADOR // 2), (TAMANHO_JOGADOR, TAMANHO_JOGADOR // 2), 3)
        pygame.draw.line(self.image, BRANCO, (TAMANHO_JOGADOR // 2, 0), (TAMANHO_JOGADOR // 2, TAMANHO_JOGADOR), 3)
        pygame.draw.circle(self.image, BRANCO, (TAMANHO_JOGADOR // 2, TAMANHO_JOGADOR // 2), int(TAMANHO_JOGADOR * 0.75), 3)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA // 2, ALTURA // 2)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


todos_sprites = pygame.sprite.Group()
jogador = Jogador()
todos_sprites.add(jogador)
alvo = Alvo()
todos_sprites.add(alvo)

with open ('pontuacao.json','r+') as arquivo:
  contador = json.load(arquivo)


executando = True
while executando:
    relogio.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
            with open ('pontuacao.json','w+') as arquivo:
              json.dump(contador,arquivo)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if jogador.rect.colliderect(alvo.rect):
                alvo.resetar()
                contador += 1

    
    todos_sprites.update()

    
    tela.fill(BRANCO)
    todos_sprites.draw(tela)
    mensagem = f'Pontos: {contador}'
    texto = FONTE.render(mensagem, True, VERMELHO)
    tela.blit(texto, (10, 10))  
    pygame.display.flip()

pygame.quit()
sys.exit()