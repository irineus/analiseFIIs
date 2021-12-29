from buscaFIIs import busca_funds_explorer
from statistics import harmonic_mean
import time
import calculos as calc
import pandas as pd
import database


def main():
    print('Buscando dados em https://www.fundsexplorer.com.br/', end='...')
    temporizador = time.time()
    df = busca_funds_explorer()
    temporizador = calcula_tempo(temporizador)
    # A ideia do programa é realizar um cálculo de pontuação para cada item do FII considerado no cálculo.
    # Para cada item, a média confere um score de 500 pontos.
    # Para cada desvio padrão acima ou abaixo, adiciona-se ou subtrai-se (respectivamente) 100 pontos.

    print('Calculando pontuações dos FIIs', end='...')
    itens_diretos = ['Liquidez', 'DividendYield%', 'DY12MAcum%', 'DY12MMedia%', 'DY+VarAnoAtual%', 'PatrimonioLiq']
    itens_inversos = ['P/VPA']
    pesos = [1, 2, 2, 3, 1, 2, 2]
    for item in itens_diretos:
        df = calc.calcula_pontuacao_direta(item, df)
    for item in itens_inversos:
        df = calc.calcula_pontuacao_inversa(item, df)
    df['FINAL_SCORE'] = df.apply(lambda x: harmonic_mean([x['Liquidez_SCORE'],
                                                          x['DividendYield%_SCORE'],
                                                          x['DY12MAcum%_SCORE'],
                                                          x['DY12MMedia%_SCORE'],
                                                          x['DY+VarAnoAtual%_SCORE'],
                                                          x['PatrimonioLiq_SCORE'],
                                                          x['P/VPA_SCORE']],
                                                         pesos), axis=1)
    df['Data'] = pd.to_datetime("today")
    temporizador = calcula_tempo(temporizador)
    # print(df.sort_values(by=['FINAL_SCORE'], ascending=False))

    print('Conectando à base de dados analiseFIIs', end='...')
    db = database.conecta_usuario_senha('analiseFIIs')
    # db = database.conecta_certificado('analiseFIIs')
    colecao = database.acessa_colecao('FIIScore', db)
    temporizador = calcula_tempo(temporizador)

    print(f'Existem {colecao.count_documents({})} documentos na coleção {colecao.name}')

    # print(f'Inserindo dados na coleção {colecao.name}', end='...')
    # database.inserir_df(colecao, df)
    # temporizador = calcula_tempo(temporizador)
    #
    # print(f'Existem agora {colecao.count_documents({})} documentos na coleção {colecao.name}')

    # print(f'Limpando dados da coleção {colecao.name}', end='...')
    # database.limpar_colecao(colecao)
    # temporizador = calcula_tempo(temporizador)

    # df.to_excel(f'analiseFIIs_{time.strftime("%Y%m%d")}.xlsx', engine='xlsxwriter')


def calcula_tempo(tempo_inicial):
    tempo_final = time.time()
    tempo_total = (tempo_final - tempo_inicial) * 1000
    print(f' ({tempo_total:.2f}ms)')
    return tempo_final


main()
