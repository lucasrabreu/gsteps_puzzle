import numpy as np
import pandas as pd

# Pedro deseja encher 3 canecas de 500 mL de uma mesa com chopp usando um balde de 5L. 
# Para fazer isso, ele enche o balde com 5L de chopp em um barril e leva até a mesa, enchendo as canecas. 
# Porém, Pedro está bêbado e, sempre que volta do barril até sua mesa, 
# perde uma quantidade aleatória de chopp com distribuição uniforme sobre a capacidade do balde. 
# Ele, então, preenche as canecas com o que houver de chopp no balde (pode preencher mais de uma caneca com o chopp do balde). 
# Por isso, pode ser necessário que Pedro faça mais de uma viagem até ter todas as canecas cheias.

# a) Qual a probabilidade de Pedro encher as canecas em sua N-ésima viagem?
# b) Em média, quantas viagens Pedro deve fazer para encher as 3 canecas?
# c) Quantas viagens Pedro deveria fazer, em média, para encher N canecas de chopp, sendo N um número natural qualquer?

def get_uniform_random_spill(high, low=0, size=1):
    return np.random.uniform(low, high, size)

def simulate(
    canecas = 3,
    cap_caneca = 500, 
    max_liq_balde = 5000,  
    max_viagens = 50,
    max_simulacoes = 50000,):

    dados = []
    # simula diversas situacoes para servir o chopp
    for n_simul in range(1, max_simulacoes+1):

        # inicializa quantidade de liquido (chopp) a ser servido
        liq_para_encher = canecas*cap_caneca

        # inicia viagens
        for n_viagem in range(1, max_viagens):
            # enche balde
            liq_balde = max_liq_balde  #ml

            # anda e derrama
            liq_derramado = get_uniform_random_spill(0, liq_balde)[0]
            liq_balde -= liq_derramado
            liq_para_encher = 0 if liq_balde >= liq_para_encher else liq_para_encher - liq_balde

            # chega na mesa
            # se tem liq suficiente, enche e termina
            if liq_para_encher == 0:
                dados.append((n_simul, n_viagem, liq_balde, liq_derramado, liq_para_encher, 1))
                break
            # se nao tem liq suficiente, enche e volta pra pegar mais
            else:
                dados.append((n_simul, n_viagem, liq_balde, liq_derramado, liq_para_encher, 0))

    df = pd.DataFrame(dados, columns=['n_simul','n_viagem','LiqBalde', 'LiqDerramado', 'AindaFaltaML', 'Fim'])
    df.to_pickle('dados_viagens.pkl')