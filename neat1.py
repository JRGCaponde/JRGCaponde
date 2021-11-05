import pygame
from random import randrange
import os
import neat


branco = (255, 255, 255)
preto = (0, 0, 0) 
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

geracao = 0
velocidade_x = 10
velocidade_y = 10
CobraXY = []
pos_x = 0
pos_y = 0
maca_x = 0
maca_y = 0

try:
	pygame.init()
except:
	print('o modolo pygame não foi inicializado com sucesso')

largura = 800
altura = 800
tamanho = 10

relogio = pygame.time.Clock()
fundo = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 50)

def texto (msg, cor):
	texto = font.render(msg, True, cor)
	fundo.blit(texto, [largura /20, altura /20])

def texto2 (msg, cor):
	texto = font.render(msg, True, cor)
	fundo.blit(texto, [largura/2, altura/20])


def Cobra (CobraXY):
	for XY in CobraXY:
		pygame.draw.rect(fundo, azul, [XY[0], XY[1], tamanho, tamanho])

def caminhar():
	if velocidade_x != tamanho:
		velocidade_y= 0
		velocidade_x =-tamanho

	if velocidade_x != -tamanho:
		velocidade_y= 0
		velocidade_x = tamanho

	if velocidade_y != tamanho:
		velocidade_x= 0
		velocidade_y =-tamanho

	if velocidade_y != -tamanho:
		velocidade_x= 0
		velocidade_y = tamanho

def mover():
	global velocidade_x
	global velocidade_y
	velocidade_y= 0
	velocidade_x = tamanho

def mover1():
	global velocidade_x
	global velocidade_y
	velocidade_y= 0
	velocidade_x =-tamanho

def mover2():
	global velocidade_x
	global velocidade_y
	velocidade_x= 0
	velocidade_y = tamanho

def mover3():
	global velocidade_x
	global velocidade_y
	velocidade_x= 0
	velocidade_y =-tamanho

def Maca(pos_x, pos_y):
		pygame.draw.rect(fundo, vermelho, [pos_x, pos_y, tamanho, tamanho])

def main(genomas, config):

	global geracao
	geracao += 1
	pontuacao = 0

	redes = []
	lista_genomas = []
	cobras = []
	for _, genoma in genomas:
		rede = neat.nn.FeedForwardNetwork.create(genoma, config)
		redes.append(rede)
		genoma.fitness = 0
		lista_genomas.append(genoma)
		cobras.append(Cobra)
		CobraComp = 1

	jogar = True
	Fim_Do_Jogo = False
	global pos_x 
	global pos_y 
	global maca_x 
	global maca_y 
	global velocidade_x
	global velocidade_y
	global CobraXY
	
	
	while jogar:
		
		fundo.fill(branco)
		
		# sair do jogo
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				jogar = False
				pygame.quit()
				quit()

			jogar = True
			pos_x = randrange(0,largura - tamanho, 10)
			pos_y = randrange(0,altura - tamanho, 10)
			maca_x = randrange(0,largura - tamanho, 10)
			maca_y = randrange(0,altura - tamanho, 10)
			velocidade_x = 0
			velocidade_y = 0
			CobraXY = []
			CobraComp = 1
		

		for i ,cobra in enumerate(cobras):
			# aumentar um pouquinho a fitness do passaro
			lista_genomas[i].fitness += 0.1
			output = redes[i].activate((pos_x, pos_y, maca_x, maca_y,
										abs(pos_x - tamanho ),
										abs(pos_y - tamanho)))
			#print('output',output)
			# mover par direita
			if output[0] > 0.5 and pos_x < maca_x and pos_y == maca_y or pos_x < maca_x and pos_y > maca_y or pos_x < maca_x and pos_y < maca_y:
				mover()
			# mover par esquerda
			elif output[0] > 0.5 and pos_x > maca_x and pos_y < maca_y or pos_x > maca_x and pos_y > maca_y or pos_x > maca_x and pos_y == maca_y:
				mover1()
			# mover par baixo
			elif output[0] > 0.5 and pos_x == maca_x and pos_y < maca_y :
				mover2()
			# mover par cima
			elif output[0] > 0.5 and pos_x == maca_x and pos_y > maca_y :
				mover3()



		fundo.fill(branco)
		pos_x += velocidade_x
		pos_y += velocidade_y
		

		if pos_x == maca_x and pos_y == maca_y:
			maca_x = randrange(0,largura - tamanho, 10)
			maca_y = randrange(0,altura - tamanho, 10)
			CobraComp += 1
			
			for genoma in lista_genomas:
				genoma.fitness += 1
				pontuacao += 1

		if pos_x > largura:
			pos_x = 0
		if pos_x < 0:
			pos_x = largura - tamanho
		if pos_y > altura:
			pos_y = 0
		if pos_y < 0:
			pos_y = altura - tamanho

		CobraInicio = []
		CobraInicio.append(pos_x)  
		CobraInicio.append(pos_y)
		CobraXY.append(CobraInicio)
		if len (CobraXY) > CobraComp:
			del CobraXY[0]
			lista_genomas[i].fitness -= 1

		if any (Bloco == CobraInicio for Bloco in CobraXY[: -1]):
			jogar = False

			
		texto(f"Geração: {geracao}", azul)
		texto2(f"Pontuação: {pontuacao}", azul)
		Cobra(CobraXY)
		Maca(maca_x, maca_y)
		pygame.display.update()
		relogio.tick(100)
		
def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    populacao.run(main,3)

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    rodar(caminho_config)
