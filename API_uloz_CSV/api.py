# plotly express - umoznuje rychlou vizualizaci dat (px)
# plotly.graf_object - umoznuje vetsi kontrolu nad grafem (go)

import plotly.graph_objects as go
import os
import time
from lib.api_pocasi import stahni_pocasi
from lib.file_handling import uloz_dataframe_do_csv

# popuzij API a stahni data o pocasi
df = stahni_pocasi()

# cesta ke složce, kde leží tento skript api.py
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "Data")

# vytvor slozku Data, pokud tam neni
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# definice cest k souborum
csv_cesta = os.path.join(data_dir, "pocasi_morkov.csv")
html_cesta = os.path.join(data_dir, "graf_pocasi.html")

# pandas pro ulozeni do CSV
uloz_dataframe_do_csv(df, csv_cesta)

# plotly zobrazi graf pocasi
# vytvoreni grafu
fig = go.Figure()

# Teplota 
fig.add_trace(go.Scatter(
    x=df['Datum'], 
    y=df['Teplota'],
    name='Teplota (°C)',
    line=dict(color='red', width=3)
))

# Vitr
fig.add_trace(go.Scatter(
    x=df['Datum'], 
    y=df['Vitr'],
    name='Vítr (km/h)',
    line=dict(color='blue', width=2, dash='dot') # dash='dot' udělá tečkovanou čáru
))

# Srazky
fig.add_trace(go.Bar(
    x=df['Datum'], 
    y=df['Dest'],
    name='Srážky (mm)',
    marker_color='lightblue',
    opacity=0.6 # pruhlednost barvy
))

# nastaveni cele vrstvy
fig.update_layout(
    title='Kompletní předpověď: Mořkov',
    xaxis_title='Čas',
    yaxis_title='Hodnoty',
    legend_title='Veličiny',
    hovermode='x unified', # ukazuje hodnoty pri najeti mysi
    template='plotly_white'
)
# protoze mi to nejde pres fig - ulozim do data a zobrazim
fig.write_html(html_cesta)
time.sleep(1)
if os.path.exists(html_cesta):
    os.startfile(html_cesta)
    print("Graf byl úspěšně vytvořen a otevřen.")
else:
    print(f"Chyba: Soubor {html_cesta} nebyl nalezen ani po krátkém čekání.")
# at se to hned nezavre
input("Stiskni Enter pro ukonceni...")