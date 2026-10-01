from dash import Dash, Input, Output, dcc, html
import pandas as pd
import plotly.express as px

# 1. Leitura do arquivo de dados
df = pd.read_csv("ecommerce_estatistica (2).csv")

# Inicialização do aplicativo Dash
app = Dash(__name__)
server = app.server

# Layout da Aplicação
app.layout = html.Div(
    [
        html.H1(
            "Dashboard de E-commerce - Análise Estatística",
            style={"textAlign": "center", "color": "#333"},
        ),
        html.P(
            "Utilize o filtro abaixo para atualizar dinamicamente os gráficos do painel:",
            style={"textAlign": "center"},
        ),
        # Componente Interativo: Dropdown para filtrar por Gênero
        html.Div(
            [
                html.Label("Selecione o Gênero:"),
                dcc.Dropdown(
                    id="filtro-genero",
                    options=[
                        {"label": genero, "value": genero}
                        for genero in df["Gênero"].unique()
                    ],
                    value=df["Gênero"].unique()[
                        0
                    ],  # Valor padrão selecionado
                    clearable=False,
                ),
            ],
            style={"width": "50%", "margin": "0 auto", "paddingBottom": "20px"},
        ),
        # Gráficos
        html.Div(
            [
                dcc.Graph(id="grafico-histograma"),
                dcc.Graph(id="grafico-dispersao"),
                dcc.Graph(id="grafico-marcas"),
            ]
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
)


# Callback para atualizar os gráficos com base no Gênero selecionado
@app.callback(
    [
        Output("grafico-histograma", "figure"),
        Output("grafico-dispersao", "figure"),
        Output("grafico-marcas", "figure"),
    ],
    [Input("filtro-genero", "value")],
)
update_graphs(genero_selecionado):
  # Filtrar o DataFrame com base na seleção do usuário
  df_filtrado = df[df["Gênero"] == genero_selecionado]

  # 1. Histograma de Preços
  fig_hist = px.histogram(
      df_filtrado,
      x="Preço",
      nbins=30,
      title=f"Distribuição de Preços - {genero_selecionado}",
      color_discrete_sequence=["#1f77b4"],
  )

  # 2. Gráfico de Dispersão (Preço vs Nota)
  fig_disp = px.scatter(
      df_filtrado,
      x="Preço",
      y="Nota",
      size="N_Avaliações",
      color="Marca",
      title=f"Relação entre Preço e Nota - {genero_selecionado}",
  )

  # 3. Ranking das Principais Marcas (Top 10)
  top_marcas = (
      df_filtrado["Marca"].value_counts().reset_index().head(10)
  )  # Corrigido para compatibilidade com versões recentes do pandas
  top_marcas.columns = ["Marca", "Contagem"]
  fig_marcas = px.bar(
      top_marcas,
      x="Marca",
      y="Contagem",
      title=f"Top 10 Marcas Mais Frequentes - {genero_selecionado}",
      color="Contagem",
      color_continuous_scale="Viridis",
  )

  return fig_hist, fig_disp, fig_marcas


if __name__ == "__main__":
  app.run(debug=True)