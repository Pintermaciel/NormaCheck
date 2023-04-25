import pandas as pd 

df = pd.DataFrame.from_dict(titulos, orient='index').reset_index().rename(columns={'index': 'chave', 0: 'descricao'})
df = df.explode('chave')
df = df.fillna('')
df[['ISO', 'VERSAO']] = df['chave'].str.split(':', expand=True)
df[['colunaex','IDIOMA']] = df['chave'].str.split('(', expand=True)
df['ISO'] = df['ISO'].str.split('(', n=1).str.get(0)
df['VERSAO'] = df['VERSAO'].str.split('(', n=1).str.get(0)
df['IDIOMA'] = df['IDIOMA'].str.split(')', n=1).str.get(0)
df = df.drop('chave', axis=1)
df = df.drop('colunaex', axis=1)
df
df.to_csv('iso.csv', index=False, sep=";")  