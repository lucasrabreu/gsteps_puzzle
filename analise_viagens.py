import pandas as pd
import streamlit as st
import os
from test_arepl import simulate

puzzle_text = """
Pedro deseja encher 3 canecas de 500 mL de uma mesa com chopp usando um balde de 5L. 
Para fazer isso, ele enche o balde com 5L de chopp em um barril e leva até a mesa, enchendo as canecas. 
Porém, Pedro está bêbado e, sempre que volta do barril até sua mesa, 
perde uma quantidade aleatória de chopp com distribuição uniforme sobre a capacidade do balde. 
Ele, então, preenche as canecas com o que houver de chopp no balde (pode preencher mais de uma caneca com o chopp do balde). 
Por isso, pode ser necessário que Pedro faça mais de uma viagem até ter todas as canecas cheias.

a) Qual a probabilidade de Pedro encher as canecas em sua N-ésima viagem?
b) Em média, quantas viagens Pedro deve fazer para encher as 3 canecas?
c) Quantas viagens Pedro deveria fazer, em média, para encher N canecas de chopp, sendo N um número natural qualquer?
"""


st.title('Puzzle - GS')
st.text(puzzle_text)

st.subheader('Amostra dos dados simulados')
st.text('Foram realizadas simulações da situação descrita e gerados os dados abaixo para 3 canecas.')
simulate(canecas=3)
df = pd.read_pickle('dados_viagens.pkl')
st.table(df.head(10))

st.subheader('Distribuição da quantidade derramada')
st.text('A distribuição é uniforme entre a quantidade mínima e máxima do balde [0, 5L].')
f = df.LiqDerramado.hist()
f.figure

st.subheader('Análise das viagens')
viagens = df.groupby('n_simul').n_viagem.max()\
    .value_counts()\
    .to_frame('qtd_viagens_simuladas')\
    .assign(PctViagens=lambda x: x.qtd_viagens_simuladas/x.qtd_viagens_simuladas.sum())\
    .assign(PctViagensAcum=lambda x: x.PctViagens.cumsum())\
    .reset_index()\
    .rename(columns={'index': 'Quantidade de viagens'})

st.text('A probabilidade de encher as canecas na N-ésima viagem foram simuladas e \n podem ser aproximadas pela porcentagem histórica representadas pela coluna PctViagens.')
st.table(viagens)

df_max_viagens = df.groupby('n_simul').n_viagem.max()
desc = df_max_viagens.describe()

st.subheader('Estatísticas sobre a quantidade de viagens')
st.text('Média de {} +- {} viagens para 3 canecas.'.format(desc['mean'], desc['std']))
st.table(desc)
f = df_max_viagens.hist()
f.set_title('Histograma da quantidade de viagens para encher 3 canecas')
f.figure

st.subheader('Estatísticas sobre a quantidade de canecas')
sim = []
for n_canecas in range(2, 50+1):
    simulate(canecas=n_canecas)
    df = pd.read_pickle('dados_viagens.pkl')
    df_max_viagens = df.groupby('n_simul').n_viagem.max()
    sim.append((n_canecas, df_max_viagens.mean()))

sim2 = pd.DataFrame(sim, columns=['Canecas', 'MediaViagens'])
sim2['Incremento'] = sim2.MediaViagens.diff()
st.table(sim2.head().append(sim2.tail()))

tmp = sim2.Incremento.describe()
st.text('Incremento médio de aproximadamente {} +- {} no número de viagens para \n cada caneca a mais.'.format(tmp['mean'], tmp['std']))
st.table(tmp)

import matplotlib.pyplot as plt
f = sim2.Incremento.plot(grid=True)
f.set_xlabel('#Canecas')
f.set_ylabel('Incremento médio na quantidade de viagens')
f.figure
