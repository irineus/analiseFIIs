# calcula pontuação de forma diretamente proporcional ao aumento do valor
def calcula_pontuacao_direta(chave, df):
    media, desvio_padrao = calcula_medias(chave, df)
    df[chave + '_SCORE'] = df[chave].apply(lambda x: round((500 + (((x - media) / desvio_padrao) * 100)), 2))
    return df


# calcula pontuação de forma inversamente proporcional ao aumento do valor
def calcula_pontuacao_inversa(chave, df):
    media, desvio_padrao = calcula_medias(chave, df)
    df[chave + '_SCORE'] = df[chave].apply(lambda x: round((500 + (((media - x) / desvio_padrao) * 100)), 2))
    return df


def calcula_medias(chave, df):
    media = df[chave].mean(skipna=True)
    # print(f'{chave} (media): {media}')
    desvio_padrao = df[chave].std(skipna=True)
    # print(f'{chave} (std): {desvio_padrao}')
    return media, desvio_padrao
