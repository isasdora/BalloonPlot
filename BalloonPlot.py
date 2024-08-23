import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o dataset mpg da biblioteca seaborn
df = sns.load_dataset('mpg')

# Definir as variáveis para serem exibidas em colunas
vars = ['mpg', 'horsepower', 'weight']

# Preparar os dados: selecionar apenas as colunas necessárias e remover linhas com NA
df = df.dropna(subset=['origin'])[vars + ['name', 'origin']]

# Agrupar por 'origin' e amostrar 5 linhas aleatórias de cada grupo
df_sampled = df.groupby('origin').apply(lambda x: x.sample(5)).reset_index(drop=True)

# Converter os dados para formato longo usando a função melt do pandas
df_long = df_sampled.melt(id_vars=['name', 'origin'], value_vars=vars, var_name='variable', value_name='value')

# Filtrar linhas onde 'value' não é NA
df_long = df_long.dropna(subset=['value'])

# Ordenar os dados
df_long = df_long.sort_values(by=['origin', 'name'])

# Criar uma coluna 'row' que será a posição y no gráfico
df_long['row'] = pd.factorize(df_long[['origin', 'name']].apply(tuple, axis=1))[0] + 1

# Criar uma coluna 'col' que será a posição x no gráfico
df_long['col'] = pd.factorize(df_long['variable'])[0] + 1

# Ajustar o espaçamento entre as colunas
df_long['col'] = df_long['col'] * 0.9

# Obter o vetor de nomes das variáveis para o eixo x
vars_x_axis = df_long['variable'].unique()

# Obter o vetor de nomes das observações para o eixo y
names_y_axis = df_long.drop_duplicates(subset=['row'])['name'].values

# Plotagem
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(data=df_long, x='col', y='row', hue='origin', size='value', sizes=(100, 500), alpha=0.6)

# Adicionar rótulos de texto
for i, row in df_long.iterrows():
    plt.text(row['col'] + 0.1, row['row'], round(row['value'], 2), color='black', ha="left", va="center", fontsize=8)

# Ajustar as legendas
h, l = ax.get_legend_handles_labels()
# Legenda para as cores
l1 = plt.legend(h[1:4], l[1:4], title="origin", bbox_to_anchor=(1.05, 0.5), loc="center left")
ax.add_artist(l1)

# Legenda para os tamanhos
l2 = plt.legend(h[4:], l[4:], title="value", bbox_to_anchor=(1.05, 0.8), loc="center left")
ax.add_artist(l2)

# Configurar os rótulos dos eixos x e y
plt.xticks(ticks=df_long['col'].unique(), labels=vars_x_axis)
plt.yticks(ticks=range(1, len(names_y_axis) + 1), labels=names_y_axis)

# Personalizar o gráfico semelhante ao theme_bw() no R
plt.grid(False)
plt.xlabel('')
plt.ylabel('')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Mover os rótulos do eixo x para o topo do gráfico
ax.xaxis.tick_top()

plt.show()