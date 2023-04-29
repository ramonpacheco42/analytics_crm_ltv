# Infoormações sobre o projeto
# O conjunto de dados inclui vendas entre 01/12/2009 - 09/12/2011.
# Nesse projeto analisaremos somente dados entre os anos 2010-2011
# O catalogo de produtos dessa empresa contém recordações
# A grande maioria dos clientes dessa empresa são B2B
# ----------------------------------------------------------------
# Informações sobre as variáveis do dataset
# invoice - Número da fatura da compra ou número do pedido. Caso começe com a letra C é porque a compra foi cancelada.
# StockCode - Código único do produto, ou seja existe somente um código desse por produto.
# Description - Nome do Produto.
# Quantity - Quantidade de produto vendido na fatura.
# InvoiceDate - Data e hora da compra.
# UnitPrice - Preço unitário do produto (GBP).
# CustomerID - Número único do cliente.
# Country - País onde o cliente mora.
# %%
import pandas as pd
import numpy as np
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sklearn.preprocessing import MinMaxScaler
from lifetimes.plotting import plot_probability_alive_matrix, plot_frequency_recency_matrix
from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases, plot_period_transactions, plot_history_alive
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#pd.set_option('display.float_format', lambda x: '%5f' % x)
# %%
df = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2010-2011')
# %%
df
# %%
def check_df(dataframe):
    print("######################    Shape    ############################")
    print(dataframe.shape)
    print("######################    Columns  ############################")
    print(dataframe.columns)
    print("######################    Types    ############################")
    print(dataframe.dtypes)
    print("######################    Head     ############################")
    print(dataframe.head())
    print("######################    Tail     ############################")
    print(dataframe.tail())
    print("######################    Describe ############################")
    print(dataframe.describe().T)
# %%
# Check nos principais números do dataset
check_df(df)
# %%
# Verificando a existencia de valores nulos
df.isnull().sum()
# %%
# Removendo os valores nulos
df.dropna(inplace=True)
df.isnull().sum()
# %%
# Criando função para remover outliers
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit
# %%
# Criando uma função para remover os outliers dentro do dataframe
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
# %%
# Criando novo dataframe com os parametros abaixo
df_uk = df[df['Country'] == 'United Kingdom']
# %%
# Removendo os pedidos que tem C de cancelados
df_uk = df_uk[~df_uk['Invoice'].str.contains('C', na=False)]
# %%
# Removendo valores negativos do modelo
df_uk = df_uk[df_uk['Price'] > 0]
# %%
# Removendo os outliers nas variáveis Price e Quantity e relocando na variável df_uk
replace_with_thresholds(df_uk, 'Price')
replace_with_thresholds(df_uk, 'Quantity')
# %%
# Check no dataframe
df_uk
# %%
# Criando coluna com valor total da compra
df_uk['TotalPrice'] = df_uk['Quantity'] * df_uk['Price']
# %%
# Check no invoice 536365 para conferir total do preço
df_uk[df_uk['Invoice'] == 536365]
# %%
# Check no período máximo da análise
df_uk['InvoiceDate'].max()
# %%
# Criando variável do dia da análise para calcular recencia
today_date = dt.datetime(2011,12,11)
# %%
# Fazendo um agrupamento dos valores total de gasto do cliente, recencia , coluna T auxiliar de recencia e frequencia
df_uk = df_uk.groupby('Customer ID').agg({'TotalPrice':'sum',
                                  'InvoiceDate': [lambda date: (date.max()-date.min()).days,
                                                  lambda date: (today_date - date.min()).days],
                                                  'Invoice' : lambda Invoice: Invoice.nunique()})
# %%
df_uk.columns.droplevel(0)
# %%
# Renomeando as colunas do group by
df_uk.columns = ['monetary', 'recency', 'T', 'frequency']
# %%
# check nos valores
df_uk.head()
# %%
# Calculando o ticket médio
df_uk['monetary'] = df_uk['monetary'] / df_uk['frequency']
# %%
# Filtrando somente frequencia maior que 1
df_uk = df_uk[df_uk['frequency'] > 1]
# %%
# Passando a recencia para semanas
df_uk['recency'] = df_uk['recency'] / 7
# %%
# Passamdo a coluna auxiliar de recencia para semanas
df_uk['T'] = df_uk['T'] / 7
# %%
# Preparando o ambiente estatistico
bgf = BetaGeoFitter()
# %%
# Criando o modelo Gama
bgf.fit(df_uk['frequency'], df_uk['recency'], df_uk['T'])
# %%
# Verificando os indicadores estatístico para o modelo estimado
bgf.summary
# %%
# Plotando um gráfico comparando o valor atual com valor estimado do modelo
plot_period_transactions(bgf)
# %%
# Anexando o valor estimado a um dataframe
bgf.conditional_expected_number_of_purchases_up_to_time(1, df_uk['frequency'], df_uk['recency'], df_uk['T']).sort_values(ascending=False).head(10)
# %%
df_uk['expected_purch_6month'] = bgf.predict(4*6, df_uk['frequency'], df_uk['recency'], df_uk['T'])
# %%
# Expectativa de compra por customer nos próximos 6 meses.
df_uk.sort_values(by='expected_purch_6month', ascending= False).head()
# %%
ggf = GammaGammaFitter(penalizer_coef=0.01)
# %%
ggf.fit(df_uk['frequency'], df_uk['monetary'])
# %%
ggf.summary
# %%
ggf.conditional_expected_average_profit(df_uk['frequency'], df_uk['monetary']).sort_values(ascending=False).head(10)
# %%
df_uk['expected_average_profit'] = ggf.conditional_expected_average_profit(df_uk['frequency'], df_uk['monetary'])
# %%
cltv = ggf.customer_lifetime_value(bgf, df_uk['frequency'], df_uk['recency'], df_uk['T'], df_uk['monetary'], time=6, freq='W')
# %%
cltv = cltv.reset_index()
# %%
cltv_final = df_uk.merge(cltv, on='Customer ID', how='left')
# %%
# Publicando a expectativa de compra, média de lucro e clv nos próximos 6 meses
cltv_final.sort_values(by='clv', ascending=False).head()
# %%
scaler = MinMaxScaler(feature_range=(0, 1))
# %%
# Publicando modelo Final
cltv_final.head()
# %%
scaler.fit(cltv_final[['clv']])
# %%
cltv_final['scaled_cltv'] = scaler.transform(cltv_final[['clv']])
# %%
cltv_final.sort_values(by='scaled_cltv', ascending=False).head()

# %%
cltv_final.sort_values(by='scaled_cltv', ascending=False).tail()