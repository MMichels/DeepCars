"""
Exemplo para demonstrar 'como' uma imagem é manipulada na tela de um jogo
"""
#%%
# Inicie-mos utilizando apenas um simples vetor de 1 dimensão preenchido de 1's e 2's
# Imagine isso como um lindo cenário extremamente simplificado
screen = [1, 1, 2, 2, 2, 1]
# O player do jogo, será representado pelo numero 8
player = 8
screen
#%%
# Vamos colocar o player no meio do nosso cenário
# nesse ponto, existe um cenário e um player dentro do cenário, porem tudo está estatico
playerposition = 3
screen[playerposition] = player
screen


#%%
# Para movimentar o personagem pela tela, basta mover ele para frente ou para trás
playerposition -= 1
screen[playerposition] = player
screen

#%%
#Oops, algo deu errado, agora, ao inves de termos um cenário com um personagem
# existem 2 players em 2 lugares diferentes no cenário.
# Para evitar esse tipo de impessilio, é necessario manter uma 'copia' da paisagem original
# chamada 'background'
background = [1, 1, 2, 2, 2, 1]
# E a tela, sera limpa, ou seja, uma tela vazia
screen = [0] * 6
screen
#%%
# Agora que temos um background e uma tela, vamos preencher a tela com o background
# Isso seria como 'pintar a tela com o cenario'
for i in range(6):
    screen[i] = background[i]

screen

#%%
# Apos preencher a tela com o background, � possivel come�ar a colocar o personagem na tela
screen[playerposition] = player
screen

#%%
# Nesse ponto, � possivel movimentar o player pela tela, sem se preocupar em com
# o que estava atras do personagem antes de ele ocupar aquele espa�o na tela

# EXECUTE A CELULA DE PREENCHIMENTO DO BACKGROUND ANTES DE EXECUTAR ESSA CELULA

playerposition -= 1
screen[playerposition] = player
screen
