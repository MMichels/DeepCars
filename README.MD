# DEEPCARS 
    Uma implementação em Python e C++

Este projeto baseou-se no código e projeto disponibilizados pelo desenvolvedor [Victor Dias](https://github.com/JVictorDias/DeepCars) \
Foi apresentado como um trabalho academico, no 8° periodo de engenharia da computação na [Uninter](uninter.com)


Alterações realizadas: \
    1 - Implementado em Python, com a biblioteca PyGame utilizando o paradigma POO; \
    2 - Implementados 4 Cerebros diferentes (Python, Cython, Keras e PyTorch) \
    3 - Alteração do algoritmo genético, adicionando favoritismo;
    
Melhorias necessariass:\
    1 - Adicionar [Recombinação](https://pt.wikipedia.org/wiki/Recombina%C3%A7%C3%A3o_(computa%C3%A7%C3%A3o_evolutiva) 
    (Crossover) no algoritmo genético dos individuos; \
    2 - Adicionar os obstaculos na pista; \
    3 - Adicionar melhores opções de iteração com os individuos e com o ambiente;

Para executar o projeto crie um novo ambiente virtual e instale os requisitos do arquivo "requirements.txt"

## Cyrebro
A implementação do cerebro em C++ foi realizada com a biblioteca Cython, ainda não possuimos uma versão distribuivel.\
Para instalar o Cyrebro siga os passos:\
    1 - Clonar o projeto [Cyrebro](https://github.com/MMichels/Cyrebro) ;\
    2 - Clonar o projeto [Cyrebro-Python](https://github.com/MMichels/Cyrebro-Python) ; \
    4 - Instale e teste a biblioteca [Cython](https://cython.org/) ; \
    3 - Alterar o diretorio do projeto Cyrebro no arquivo Cyrebro-Python\config.py; \
    4 - Abrir o CMD como administrador; \
    5 - Executar o arquivo setup.bat; \
    6 - Executar o comando "python setup.py install";
