import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import os

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

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Analisis Morfosintactico de Letras Musicales",
            style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px 0'}),

    html.Div([
        html.Div([
            html.Label("Genero:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': g, 'value': g} for g in sorted(df['genre'].unique())],
                value=None,
                placeholder="Todos los generos"
            )
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Artista:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='artist-dropdown')
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Metica:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'Densidad lexica', 'value': 'densidad_lexica'},
                    {'label': 'Pronombres', 'value': 'pronombres_count'},
                    {'label': 'Ratio Sust/Verb', 'value': 'ratio_sust_verb'},
                    {'label': 'Valence', 'value': 'valence'},
                    {'label': 'Sadness', 'value': 'sadness'},
                    {'label': 'Romantic', 'value': 'romantic'},
                ],
                value='densidad_lexica'
            )
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Tipo de datos:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='source-dropdown',
                options=[
                    {'label': 'Todos', 'value': None},
                    {'label': 'Mis Artistas', 'value': 'my_artists'},
                    {'label': 'Corpus Historico', 'value': 'corpus'}
                ],
                value=None,
                placeholder="Todos"
            )
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'}),

    html.Div(id='adn-box', style={
        'margin': '20px', 'padding': '20px',
        'backgroundColor': '#f1f4f6', 'borderLeft': '5px solid #34495e',
        'borderRadius': '6px', 'fontSize': '17px', 'minHeight': '140px'
    }),

    html.Div(id='interpretacion-box', style={
        'margin': '20px', 'padding': '20px',
        'backgroundColor': '#f9fbfc', 'borderLeft': '5px solid #7f8c8d',
        'borderRadius': '6px', 'fontSize': '16px'
    }),

    html.Div([
        dcc.Graph(id='graph-temporal'),
        dcc.Graph(id='graph-top'),
        dcc.Graph(id='graph-pos'),
        dcc.Graph(id='graph-corr'),
        dcc.Graph(id='graph-verbos-genero')
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(550px, 1fr))', 'gap': '20px', 'padding': '20px'})
])

@app.callback(
    Output('artist-dropdown', 'options'),
    Output('artist-dropdown', 'value'),
    Input('genre-dropdown', 'value')
)
def update_artist_options(genre):
    dff = df if genre is None else df[df['genre'] == genre]
    artists = sorted(dff['artist'].unique())
    options = [{'label': a, 'value': a} for a in artists]
    default = artists[0] if artists else None
    return options, default

@app.callback(
    [Output('adn-box', 'children'),
     Output('graph-temporal', 'figure'),
     Output('graph-top', 'figure'),
     Output('graph-pos', 'figure'),
     Output('graph-corr', 'figure'),
     Output('graph-verbos-genero', 'figure'),
     Output('interpretacion-box', 'children')],
    [Input('genre-dropdown', 'value'),
     Input('artist-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('source-dropdown', 'value')]
)
def update_all(genre, artist, metric, source):
    dff = df.copy()

    if source == 'my_artists':
        dff = dff[dff.get('source', '') == 'my_artists']
    elif source == 'corpus':
        dff = dff[dff.get('source', '') != 'my_artists']

    if genre:
        dff = dff[dff['genre'] == genre]

    if dff.empty:
        empty = px.line(title="Sin datos")
        return "No hay datos para esta combinacion", empty, empty, empty, empty, empty, "No hay datos para mostrar interpretacion."

    if artist:
        artist_clean = str(artist).strip()
        matching = dff[dff['artist'].str.strip() == artist_clean]
        if matching.empty:
            matching = dff[dff['artist'].str.strip().str.lower() == artist_clean.lower()]
        if matching.empty:
            return f"Artista '{artist}' no encontrado", px.line(), px.bar(), px.pie(), px.scatter(), empty, "Artista no encontrado."
        row = matching.iloc[0]
    else:
        row = dff.iloc[0]

    adn = [
        html.Strong(f"ADN Gramatical – {row['artist']} ({row.get('genre', 'custom')})"),
        html.Br(), html.Br(),
        f"Lemas clave: {row.get('palabras_clave', '—')}",
        html.Br(),
        f"Adjetivos representativos: {row.get('adjetivos_ejemplo', '—')}",
        html.Br(), html.Br(),
        html.Strong("Emocionalidad detectada:"),
        html.Br(),
        f"Valence: {row.get('valence', '—'):.3f} | Sadness: {row.get('sadness', '—'):.3f} | Romantic: {row.get('romantic', '—'):.3f}"
    ]

    decades = dff['decade'].unique()
    if len(decades) <= 1:
        fig_t = px.bar(x=[decades[0] if decades.size > 0 else 'Ninguna'],
                       y=[dff[metric].mean()],
                       title=f"Solo decada disponible: {decades[0] if decades.size > 0 else 'Ninguna'} – Promedio {metric}: {dff[metric].mean():.3f}")
    else:
        temp = dff.groupby('decade')[metric].mean().reset_index()
        fig_t = px.line(temp, x='decade', y=metric, markers=True, title=f"Evolucion {metric}")

    top = dff.groupby('artist')[metric].mean().nlargest(10).reset_index()
    fig_top = px.bar(top, x='artist', y=metric, color='artist', title=f"Top 10 – {metric}")

    pos_cols = ['verbos', 'sustantivos', 'adjetivos', 'pronombres_count']
    if genre:
        vals = dff[pos_cols].mean()
        fig_pos = px.pie(vals, names=vals.index, title=f"Distribucion POS – {genre}", hole=0.4)
    else:
        fig_pos = px.bar(df.groupby('genre')[pos_cols].mean().reset_index(), x='genre', y=pos_cols,
                         barmode='group', title="POS promedio por Genero")

    fig_corr = px.scatter(dff, x=metric, y='valence', color='genre' if genre is None else None,
                          size='sadness', hover_data=['artist'],
                          title=f"{metric.capitalize()} vs Valence (tamano = tristeza)")

    verbos_por_genero = df.groupby('genre')['verbos'].mean().reset_index()
    fig_verbos = px.bar(verbos_por_genero, x='genre', y='verbos',
                        title="Promedio de Verbos por Genero",
                        color='genre',
                        labels={'verbos': 'Conteo promedio de verbos por cancion'})

    # Texto interpretativo dinámico (cambia segun genero, artista, metrica, source)
    interpretacion = []
    if source == 'my_artists':
        interpretacion.append(f"En tus artistas, {row['artist']} usa {row.get('verbos', 0)} verbos en promedio, con metrica {metric} de {row.get(metric, '—'):.3f}.")
    elif source == 'corpus':
        interpretacion.append("En el corpus historico, Hip-Hop muestra mayor promedio de verbos, frente a Baladas que usan mas estados emocionales.")
    else:
        interpretacion.append("En el conjunto completo, Hip-Hop destaca con mayor promedio de verbos, frente a Baladas que usan mas estados emocionales.")

    if genre:
        interpretacion.append(f"En {genre}, el promedio de verbos es {dff['verbos'].mean():.2f} por cancion.")
    if artist:
        interpretacion.append(f"El artista {artist} tiene {row.get('verbos', 0)} verbos, lo que indica una narrativa { 'activa' if row.get('verbos', 0) > dff['verbos'].mean() else 'reflexiva' }.")
    if metric == 'verbos':
        interpretacion.append(f"La metrica {metric} muestra variaciones por genero, con Hip-Hop liderando.")

    interpretacion_children = [
        html.Strong("Interpretacion rapida:"),
        html.Br(),
        html.Ul([html.Li(text) for text in interpretacion])
    ]

    return adn, fig_t, fig_top, fig_pos, fig_corr, fig_verbos, interpretacion_children

if __name__ == '__main__' :
    app.run(debug=True, port=8050)