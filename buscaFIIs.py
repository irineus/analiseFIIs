import requests
import pandas as pd
import re
import math


def busca_funds_explorer():
    # print('Buscando FIIs de FundsExplorer...')
    url = 'https://www.fundsexplorer.com.br/ranking'
    html = requests.get(url).content
    df_html = pd.read_html(html)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)
    # pd.set_option('display.max_columns', None)
    df = df_html[-1]
    # print(df)
    df.rename(
        columns={
            'CÃ³digodo fundo': 'CodigoFII',
            'Setor': 'Setor',
            'PreÃ§o Atual': 'Preco',
            'Liquidez DiÃ¡ria': 'Liquidez',
            'Dividendo': 'Dividendo',
            'DividendYield': 'DividendYield%',
            'DY (3M)Acumulado': 'DY3MAcum%',
            'DY (6M)Acumulado': 'DY6MAcum%',
            'DY (12M)Acumulado': 'DY12MAcum%',
            'DY (3M)MÃ©dia': 'DY3MMedia%',
            'DY (6M)MÃ©dia': 'DY6MMedia%',
            'DY (12M)MÃ©dia': 'DY12MMedia%',
            'DY Ano': 'DYAnoAtual%',
            'VariaÃ§Ã£o PreÃ§o': 'Variacao2M%',
            'Rentab.PerÃ­odo': 'DY+VarMes%',
            'Rentab.Acumulada': 'DY+VarAnoAtual%',
            'PatrimÃ´nioLÃ­q.': 'PatrimonioLiq',
            'VPA': 'VPA',
            'P/VPA': 'P/VPA',
            'DYPatrimonial': 'DYPatrimonial%',
            'VariaÃ§Ã£oPatrimonial': 'VarPatrimonial2M%',
            'Rentab. Patr.no PerÃ­odo': 'RentPatrimonial%',
            'Rentab. Patr.Acumulada': 'RentPatrimonialAnual%',
            'VacÃ¢nciaFÃ­sica': 'VacanciaFisica%',
            'VacÃ¢nciaFinanceira': 'VacanciaFinanceira%',
            'QuantidadeAtivos': 'QuantidadeAtivos',

        },
        inplace=True
    )
    df['Setor'] = df['Setor'].replace(['TÃ­tulos e Val. Mob.'], 'Titulos e Val. Mob.')
    df['Setor'] = df['Setor'].replace(['HÃ­brido'], 'Hibrido')
    df['Setor'] = df['Setor'].replace(['LogÃ­stica'], 'Logistica')
    #print(df)
    df['Preco'] = df['Preco'].map(converte_para_numero)
    df['Liquidez'] = df['Liquidez'].map(converte_para_numero)
    df['Dividendo'] = df['Dividendo'].map(converte_para_numero)
    df['DividendYield%'] = df['DividendYield%'].map(converte_para_numero)
    df['DY3MAcum%'] = df['DY3MAcum%'].map(converte_para_numero)
    df['DY6MAcum%'] = df['DY6MAcum%'].map(converte_para_numero)
    df['DY12MAcum%'] = df['DY12MAcum%'].map(converte_para_numero)
    df['DY3MMedia%'] = df['DY3MMedia%'].map(converte_para_numero)
    df['DY6MMedia%'] = df['DY6MMedia%'].map(converte_para_numero)
    df['DY12MMedia%'] = df['DY12MMedia%'].map(converte_para_numero)
    df['DYAnoAtual%'] = df['DYAnoAtual%'].map(converte_para_numero)
    df['Variacao2M%'] = df['Variacao2M%'].map(converte_para_numero)
    df['DY+VarMes%'] = df['DY+VarMes%'].map(converte_para_numero)
    df['DY+VarAnoAtual%'] = df['DY+VarAnoAtual%'].map(converte_para_numero)
    df['PatrimonioLiq'] = df['PatrimonioLiq'].map(converte_para_numero)
    # VPA = Patrimonio Liq. / Qtd. Cotas Fundo
    df['VPA'] = df['VPA'].map(converte_para_numero)
    df['P/VPA'] = df['P/VPA'].map(converte_para_numero)
    df['P/VPA'] = df['P/VPA'].map(lambda x: x/1000)
    df['DYPatrimonial%'] = df['DYPatrimonial%'].map(converte_para_numero)
    df['VarPatrimonial2M%'] = df['VarPatrimonial2M%'].map(converte_para_numero)
    # Retorno considerando o DY Patrimonial e Variação da Cota Patrimonial no mês
    df['RentPatrimonial%'] = df['RentPatrimonial%'].map(converte_para_numero)
    df['RentPatrimonialAnual%'] = df['RentPatrimonialAnual%'].map(converte_para_numero)
    df['VacanciaFisica%'] = df['VacanciaFisica%'].map(converte_para_numero)
    df['VacanciaFinanceira%'] = df['VacanciaFinanceira%'].map(converte_para_numero)
    df['QuantidadeAtivos'] = df['QuantidadeAtivos'].map(converte_para_numero)
    return df


def converte_para_numero(valor):
    try:
        try:
            if math.isnan(valor):
                return None
        except:
            pass
        string_valor = str(valor)
        # indica se deve ser retornado um valores referente a um percentual (dividir por 100)
        percentual = '%' in string_valor
        # retira todos os caracteres da string que não sejam '.', ',' ou um número
        numero_limpo = re.sub(r'[^0-9,-.]', '', string_valor)
        if not numero_limpo.isdigit():  # verifica se está formatado incorreto, indicando que deve estar no formato BR
            numero = str(numero_limpo).replace('.', '')
            numero = str(numero).replace(',', '.')
        else:
            numero = numero_limpo
        if percentual:
            return round(float(numero) / 100, 4)
        return float(numero)
    except ValueError:
        raise ValueError(f'Erro de conversão numérica do valor {valor}')
    except Exception as erro:
        raise ValueError(f'Erro de conversão numérica do valor {valor}: ** {erro} **')

# busca_funds_explorer()
