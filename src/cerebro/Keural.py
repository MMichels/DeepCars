import numpy as np
import time
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense


class Keural:
    def __init__(self, qtdNeuroniosEntrada, qtdCamadas, profundidade, qtdNeuroniosSaida):
        self.model = Sequential()
        self.model.add(Dense(profundidade, activation='relu', input_dim=qtdNeuroniosEntrada))
        self.model.add(Dense(qtdNeuroniosSaida, activation='relu'))
        self.model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
        self.entrada = [0] * qtdNeuroniosEntrada
        self.saida = [0] * qtdNeuroniosSaida

    def aplicarEntrada(self, entrada):
        self.entrada = np.array(entrada)
        self.entrada = self.entrada.reshape((1, 18))

    def calculaSaida(self):
        self.saida = self.model.predict(self.entrada)

    def obterSaida(self):
        return self.saida[0]





if __name__ == '__main__':
    import time
    medias = []
    model = Keural(18, 1, 6, 4)
    entrada = np.random.randint(0, 101, 18)
    for i in range(10):
        ini = time.time()
        model.aplicarEntrada(entrada)
        model.calculaSaida()
        model.obterSaida()
        end = time.time()
        medias.append(end - ini)
    print(sum(medias) / len(medias))
    print(model.model.weights)
