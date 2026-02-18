import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import os

# =========================
# CARGA DE DATOS
# =========================
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta = os.path.join(base_dir, 'data', 'processed', 'dataset_master.csv')

if not os.path.exists(ruta):
    print(f"No se encuentra {ruta}")
    exit(1)

df = pd.read_csv(ruta)

df['decade'] = df['decade'].astype(str).fillna('Unknown')
df['artist'] = df['artist'].astype(str).str.strip()
df['genre'] = df['genre'].astype(str).str.strip().fillna('Desconocido')

if 'source' in df.columns:
    df['source'] = df['source'].fillna('corpus')
else:
    df['source'] = 'corpus'

print(f"Datos cargados: {len(df)} filas, {df['artist'].nunique()} artistas únicos")

# =========================
# APP
# =========================
app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        "Dashboard de Analisis Morfosintactico (POS Tagging) en Letras Musicales",
        style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px 0'}
    ),

    html.Div([
        html.Div([
            html.Label("Genero"),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': g, 'value': g} for g in sorted(df['genre'].unique())],
                value=None,
                placeholder="Todos"
            )
        ], style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Artista"),
            dcc.Dropdown(id='artist-dropdown')
        ], style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Metrica"),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'Densidad Lexica', 'value': 'densidad_lexica'},
                    {'label': 'Pronombres', 'value': 'pronombres_count'},
                    {'label': 'Ratio Sust/Verb', 'value': 'ratio_sust_verb'},
                    {'label': 'Valence', 'value': 'valence'},
                    {'label': 'Sadness', 'value': 'sadness'},
                    {'label': 'Romantic', 'value': 'romantic'}
                ],
                value='densidad_lexica'
            )
        ], style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Fuente"),
            dcc.Dropdown(
                id='source-dropdown',
                options=[
                    {'label': 'Todos', 'value': None},
                    {'label': 'Mis Artistas', 'value': 'my_artists'},
                    {'label': 'Corpus Historico', 'value': 'corpus'}
                ],
                value=None
            )
        ], style={'width': '25%', 'display': 'inline-block'})
    ], style={'padding': '10px'}),

    html.Div(id='adn-box', style={
        'margin': '20px',
        'padding': '20px',
        'backgroundColor': '#f1f4f6',
        'borderLeft': '5px solid #34495e'
    }),

    html.Div(id='interpretacion-box', style={
        'margin': '20px',
        'padding': '20px',
        'backgroundColor': '#f9fbfc',
        'borderLeft': '5px solid #7f8c8d'
    }),

    html.Div([
        dcc.Graph(id='graph-temporal'),
        dcc.Graph(id='graph-top'),
        dcc.Graph(id='graph-pos'),
        dcc.Graph(id='graph-corr'),
        dcc.Graph(id='graph-verbos-genero'),
        dcc.Graph(id='graph-ratios')
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(550px, 1fr))',
        'gap': '20px',
        'padding': '20px'
    })
])

# =========================
# CALLBACKS
# =========================
@app.callback(
    Output('artist-dropdown', 'options'),
    Output('artist-dropdown', 'value'),
    Input('genre-dropdown', 'value')
)
def update_artist_options(genre):
    dff = df if genre is None else df[df['genre'] == genre]
    artists = sorted(dff['artist'].unique())
    return [{'label': a, 'value': a} for a in artists], (artists[0] if artists else None)


@app.callback(
    [
        Output('adn-box', 'children'),
        Output('graph-temporal', 'figure'),
        Output('graph-top', 'figure'),
        Output('graph-pos', 'figure'),
        Output('graph-corr', 'figure'),
        Output('graph-verbos-genero', 'figure'),
        Output('graph-ratios', 'figure'),
        Output('interpretacion-box', 'children')
    ],
    [
        Input('genre-dropdown', 'value'),
        Input('artist-dropdown', 'value'),
        Input('metric-dropdown', 'value'),
        Input('source-dropdown', 'value')
    ]
)
def update_all(genre, artist, metric, source):

    dff = df.copy()

    if source == 'my_artists':
        dff = dff[dff['source'] == 'my_artists']
    elif source == 'corpus':
        dff = dff[dff['source'] != 'my_artists']

    if genre:
        dff = dff[dff['genre'] == genre]

    if dff.empty:
        empty = px.line(title="Sin datos")
        return "Sin datos", empty, empty, empty, empty, empty, empty, "Sin interpretacion"

    row = dff.iloc[0]

    adn = [
        html.Strong(f"ADN Gramatical – {row['artist']} ({row['genre']})"),
        html.Br(),
        f"Palabras clave: {row.get('palabras_clave', '')}",
        html.Br(),
        f"Adjetivos representativos: {row.get('adjetivos_ejemplo', '')}"
    ]

    temp = dff.groupby('decade')[metric].mean().reset_index()
    fig_t = px.line(temp, x='decade', y=metric, title=f"Evolucion temporal de {metric}")

    top = dff.groupby('artist')[metric].mean().nlargest(10).reset_index()
    fig_top = px.bar(top, x='artist', y=metric, title=f"Top 10 artistas por {metric}")

    pos_cols = ['verbos', 'sustantivos', 'adjetivos', 'pronombres_count']
    fig_pos = px.bar(
        dff.groupby('genre')[pos_cols].mean().reset_index(),
        x='genre',
        y=pos_cols,
        barmode='group',
        title="Distribucion POS promedio por genero"
    )

    fig_corr = px.scatter(
        dff,
        x=metric,
        y='valence',
        size='sadness',
        hover_data=['artist'],
        title=f"{metric} vs Valence"
    )

    fig_verbos = px.bar(
        df.groupby('genre')['verbos'].mean().reset_index(),
        x='genre',
        y='verbos',
        title="Promedio de verbos por genero"
    )

    ratio_cols = ['ratio_sust_verb', 'ratio_adjetivos', 'densidad_lexica']
    fig_ratios = px.bar(
        df.groupby('genre')[ratio_cols].mean().reset_index(),
        x='genre',
        y=ratio_cols,
        barmode='group',
        title="Ratios morfologicos derivados del POS Tagging"
    )

    interpretacion = [
        html.Strong("Interpretacion"),
        html.Br(),
        "Las metricas presentadas se derivan del POS Tagging aplicado a las letras musicales, "
        "permitiendo analizar patrones gramaticales como densidad lexica, balance sustantivo-verbo "
        "y uso de verbos de accion por genero y periodo."
    ]

    return adn, fig_t, fig_top, fig_pos, fig_corr, fig_verbos, fig_ratios, interpretacion


if __name__ == '__main__':
    app.run(debug=True, port=8050)
