# uloz CSV pomoci pandas
import pandas as pd

def uloz_dataframe_do_csv(df, nazev_souboru):
    """Tato funkce vezme tabulku a ulozi ji do CSV."""
    df.to_csv(nazev_souboru, index=False, encoding='utf-8')
    print(f" Hotovo! Data jsou v souboru: {nazev_souboru}")
