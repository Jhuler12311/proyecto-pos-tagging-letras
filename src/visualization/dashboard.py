import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import os

# ────────────────────────────────────────────────
# Cargar datos
# ────────────────────────────────────────────────
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta = os.path.join(base_dir, 'data', 'processed', 'dataset_master.csv')

if not os.path.exists(ruta):
    print(f"❌ No se encuentra {ruta}")
    exit(1)

df = pd.read_csv(ruta)

# Limpieza suave
df['decade'] = df['decade'].astype(str).fillna('Unknown')
df['artist'] = df['artist'].astype(str).str.strip()
df['genre'] = df['genre'].astype(str).str.strip().fillna('Desconocido')

print(f"Datos cargados: {len(df)} filas, {df['artist'].nunique()} artistas únicos")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis Morfosintáctico de Letras Musicales",
            style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px 0'}),

    html.Div([
        html.Div([
            html.Label("🎵 Género:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{'label': g, 'value': g} for g in sorted(df['genre'].unique())],
                value=None,
                placeholder="Todos los géneros"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("🎤 Artista:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='artist-dropdown')
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("📊 Métrica:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'Densidad léxica', 'value': 'densidad_lexica'},
                    {'label': 'Pronombres', 'value': 'pronombres_count'},
                    {'label': 'Ratio Sust/Verb', 'value': 'ratio_sust_verb'},
                    {'label': 'Valence', 'value': 'valence'},
                    {'label': 'Sadness', 'value': 'sadness'},
                    {'label': 'Romantic', 'value': 'romantic'},
                ],
                value='densidad_lexica'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'}),

    html.Div(id='adn-box', style={
        'margin': '20px', 'padding': '20px',
        'backgroundColor': '#f1f4f6', 'borderLeft': '5px solid #34495e',
        'borderRadius': '6px', 'fontSize': '17px', 'minHeight': '140px'
    }),

    html.Div([
        dcc.Graph(id='graph-temporal'),
        dcc.Graph(id='graph-top'),
        dcc.Graph(id='graph-pos'),
        dcc.Graph(id='graph-corr')
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(550px, 1fr))', 'gap': '20px', 'padding': '20px'})
])

# ────────────────────────────────────────────────
# Callbacks
# ────────────────────────────────────────────────
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
     Output('graph-corr', 'figure')],
    [Input('genre-dropdown', 'value'),
     Input('artist-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_all(genre, artist, metric):
    dff = df if genre is None else df[df['genre'] == genre].copy()

    if dff.empty:
        empty = px.line(title="Sin datos")
        return "No hay datos para este filtro", empty, empty, empty, empty

    # Seleccionar fila del artista (robustamente)
    if artist:
        artist_clean = str(artist).strip()
        matching = dff[dff['artist'].str.strip() == artist_clean]
        if matching.empty:
            matching = dff[dff['artist'].str.strip().str.lower() == artist_clean.lower()]
        if matching.empty:
            return f"Artista '{artist}' no encontrado en este filtro", px.line(), px.bar(), px.pie(), px.scatter()
        row = matching.iloc[0]
    else:
        row = dff.iloc[0]

    # ADN (limpio, sin duplicados)
    adn = [
        html.Strong(f"ADN Gramatical – {row['artist']} ({row.get('genre', '—')})"),
        html.Br(), html.Br(),
        f"• Lemas clave: {row.get('palabras_clave', '—')}",
        html.Br(),
        f"• Adjetivos representativos: {row.get('adjetivos_ejemplo', '—')}",
        html.Br(), html.Br(),
        html.Strong("Emocionalidad detectada:"),
        html.Br(),
        f"Valence: {row.get('valence', '—'):.3f} | Sadness: {row.get('sadness', '—'):.3f} | Romantic: {row.get('romantic', '—'):.3f}"
    ]

    # Temporal
    decades = dff['decade'].unique()
    if len(decades) <= 1:
        fig_t = px.bar(x=[decades[0] if decades.size > 0 else 'Ninguna'],
                       y=[dff[metric].mean()],
                       title=f"Solo década disponible: {decades[0] if decades.size > 0 else 'Ninguna'} – Promedio {metric}: {dff[metric].mean():.3f}")
    else:
        temp = dff.groupby('decade')[metric].mean().reset_index()
        fig_t = px.line(temp, x='decade', y=metric, markers=True, title=f"Evolución {metric}")

    # Top artistas
    top = dff.groupby('artist')[metric].mean().nlargest(10).reset_index()
    fig_top = px.bar(top, x='artist', y=metric, color='artist', title=f"Top 10 – {metric}")

    # POS por género
    pos_cols = ['verbos', 'sustantivos', 'adjetivos', 'pronombres_count']
    if genre:
        vals = dff[pos_cols].mean()
        fig_pos = px.pie(vals, names=vals.index, title=f"Distribución POS – {genre}", hole=0.4)
    else:
        fig_pos = px.bar(df.groupby('genre')[pos_cols].mean().reset_index(), x='genre', y=pos_cols,
                         barmode='group', title="POS promedio por Género")

    # Correlación (título corregido)
    fig_corr = px.scatter(dff, x=metric, y='valence', color='genre' if genre is None else None,
                          size='sadness', hover_data=['artist'],
                          title=f"{metric.capitalize()} vs Valence (tamaño = tristeza)")

    return adn, fig_t, fig_top, fig_pos, fig_corr


if __name__ == '__main__':
    app.run(debug=True, port=8050)