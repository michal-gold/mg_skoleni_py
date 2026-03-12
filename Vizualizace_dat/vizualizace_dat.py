import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import os


# Trochu jsem si tento ukol upravil, aby pozdeji po upravach vyhovoval mym potrebam k logovani stavu PLC.
# Co je ale asi problem, je generovani kodu pres AI. Takto chapu, ze se to nenaucim poradne. 
# Predpokladam ze v manualech k jednotlivym knihovnam, lze pri hlubsim studiu najit, jak se co pouziva.
# Na co se chci ale zeptat je strukturovani programu, neco jako je  IEC 61131-3 pro PLC. 
# Existuji nejake postupy ci standardy pro programovani obecne? Pokud je obecne prijmano, ze lze pouzit kod 
# generovany AI, jak takovy kod zpracovat aby byl dobre citelny a srozumitelny? V TIA Portal jsem nijak 
# zvlast aktivne AI nevyuzival, tudiz je to pro me neprobadane uzemi.
# Pokusil jsem se skryt zkratky.md pres .gitignore, ale jsou tam. Co jsem udelal spatne?

# --- 1. NACETNI DAT ---
# Cesta k souboru musi odpovidat slozce.
path = "Data/R1.csv"
df = pd.read_csv(path)

# --- 2. KONSTRUKCE GRAFU (SUBPLOTS) ---
# rows=2 vytvori dve patra, shared_xaxes=True zajisti synchronizaci zoomu.
fig = make_subplots(
    rows=2, cols=1,     
    shared_xaxes=True, 
    vertical_spacing=0.08, # Mezera mezi hornim a dolnim grafem
    subplot_titles=("RYCHLOST", "POZICE ROBOTA (X, Y, Z)")
)

# --- HORNI GRAF: Rychlost ---
fig.add_trace(
    go.Scatter(x=df['Time'], y=df['Speed In Current Wobj'], 
               name="Rychlost [mm/s]", line=dict(color='#00ced1', width=2)),
    row=1, col=1
)

# --- DOLNI GRAF: Pozice ---
# Seznam dvojic (nazev sloupce v CSV, nazev v legende, barva cary).
osi_nastaveni = [
    ('Position\\X Position In Current Wobj', 'Osa X [mm]', '#ff4500'),
    ('Position\\Y Position In Current Wobj', 'Osa Y [mm]', '#32cd32'),
    ('Position\\Z Position In Current Wobj', 'Osa Z [mm]', '#1e90ff')
]

# Cyklus projde seznam a pro kazdou osu prida do dolniho grafu (row=2) jednu krivku.
for col, name, color in osi_nastaveni:
    fig.add_trace(
        go.Scatter(x=df['Time'], y=df[col], name=name, line=dict(color=color)),
        row=2, col=1
    )

# --- 3. INTERAKTIVITA A SYNCHRONIZACE ---
# DULEZITE: Sjednoceni detekce dat pro vsechna patra.
fig.update_traces(xaxis='x')

fig.update_layout(
    height=850,
    title_text="Detailni analyza pohybu (Interactive PLC Log)",
    template="plotly_dark",      
    hovermode="x unified",       # Sjednoti hodnoty k svisle care pod kurzorem
    spikedistance=-1,            # Zajisti, ze svisla cara nezmizi
    hoverdistance=-1,            
    
    # Nastaveni "Spikes" (vodicu) pro ob? osy X.
    xaxis=dict(showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=1, spikecolor="white", spikedash="solid"),
    xaxis2=dict(showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=1, spikecolor="white", spikedash="solid"),
    
    # Umisteni legendy pod graf vodorovne.
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
)

# Popisek spodni casove osy.
fig.update_xaxes(title_text="Cas [s]", row=2, col=1)

# Formatovani zobrazeni cisel v tooltipu.
fig.update_traces(hovertemplate="<b>%{y:.2f}</b>")

# --- 4. ULOZENI A DOPLNENI O JAVASCRIPT ---
output_file = "analyza_robota_final.html"
fig.write_html(output_file)

# JS pro zachyceni Ctrl+Mezernik a vypis dat
custom_js = """
<div id="snapshot-container" style="background-color: #111; color: #00ced1; font-family: 'Consolas', monospace; padding: 15px; margin-top: 10px; border: 2px solid #00ced1; border-radius: 5px; width: fit-content;">
    <h3 style="margin-top: 0; font-size: 14px; color: #aaa;">AKTUALNI BOD (Ctrl + Mezernik):</h3>
    <div id="display-area" style="font-size: 18px; font-weight: bold; color: white;">
        Zatim nebyl vybran zadny bod...
    </div>
</div>

<script>
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.code === 'Space') {
        event.preventDefault(); 
        
        var gd = document.getElementsByClassName('plotly-graph-div')[0];
        var d = gd._hoverdata;

        if (d && d.length > 0) {
            var time = d[0].x; 
            var values = {};
            
            d.forEach(function(point) {
                values[point.fullData.name] = point.y.toFixed(2);
            });

            var output = `Cas: <span style="color: #00ced1">${time}s</span> | `;
            output += `Rychlost: <span style="color: #00ced1">${values['Rychlost [mm/s]'] || '-'}</span> | `;
            output += `X: <span style="color: #ff4500">${values['Osa X [mm]'] || '-'}</span> | `;
            output += `Y: <span style="color: #32cd32">${values['Osa Y [mm]'] || '-'}</span> | `;
            output += `Z: <span style="color: #1e90ff">${values['Osa Z [mm]'] || '-'}</span>`;
            
            document.getElementById('display-area').innerHTML = output;
        }
    }
});
</script>
"""

with open(output_file, 'a', encoding='utf-8') as f:
    f.write(custom_js)

file_path = os.path.abspath(output_file)
print(f"Hotovo! Display aktivni: {file_path}")
webbrowser.open(f"file://{file_path}")