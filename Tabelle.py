import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image as PILImage


def table_api():
    # Holt die Tabelle aus der API
    url = "https://api.openligadb.de/getbltable/bl1/2025"
    data = requests.get(url).json()

    table = []
    for team in data:
        wdl = f"{team['won']}-{team['draw']}-{team['lost']}"
        table.append([
            team["teamName"],
            team["matches"],
            wdl,
            f"{team['goals']}:{team['opponentGoals']}",
            team["points"]
        ])
    
    # 👉 HIER wird ein DataFrame (df) daraus
    df = pd.DataFrame(table, columns=[
        "Team", "Spiele", "S-U-N", "Torverhältnis", "Punkte"
    ])
    df["Rang"] = df.index + 1
    return df

def render_modern_png(df, logos_dict):
    # Figur & Achsen
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Kopf
    ax.text(0.5, 0.98, "Bundesliga – current standings",
            ha="center", va="center",
            fontsize=26, fontweight="bold", color="#000000")

    # Startposition (oben) und Zeilenabstand
    start_y = 0.90
    step = 0.045

    for idx, row in df.iterrows():
        y = start_y - idx * step

        platz = int(row['Rang'])

        if platz == 1:
            farbe = "#38B602"
        elif platz == 2 or platz == 3 or platz == 4:
            farbe = "#73FF28"
        elif platz == 5:
            farbe = "#00BEE4"
        elif platz == 6:
            farbe = "#57E6FF"
        elif platz == 16:
            farbe = "#FAAF00"
        elif platz == 17 or platz == 18:
            farbe = "#FF0101"
        else:
            farbe = "#AFAFAF"

        ax.add_patch(
        patches.Rectangle(
            (0.03, y - 0.021),   # (x, y) Startpunkt unten links
            0.008,               # Breite des Kastens
            0.036,               # Höhe des Kastens (gleiche Höhe wie das Logo)
            facecolor= farbe, # Farbe
            edgecolor="none",
            zorder=1)
        )
        # Rang
        ax.text(0.05, y, f"{int(row['Rang'])}.",
                fontsize=16, va="center", ha="left")

        # Logo (wenn vorhanden)
        team = row["Team"]
        if team in logos_dict and os.path.exists(logos_dict[team]):
            try:
                logo = PILImage.open(logos_dict[team]).convert("RGBA")
                # in numpy-array konvertieren und passende Extent setzen
                logo_arr = np.array(logo)
                # Extent: (left, right, bottom, top) in data coords (we work in 0..1)
                left, right = 0.10, 0.145
                bottom, top = y - 0.018, y + 0.018
                ax.imshow(logo_arr, extent=(left, right, bottom, top),
                          aspect='auto', zorder=2)
            except Exception as e:
                # Falls Logo fehlschlägt, weiter ohne Logo
                print(f"Logo konnte nicht geladen werden ({team}): {e}")

        # Teamname
        ax.text(0.16, y, team, fontsize=16, va="center", ha="left")

        # Werte rechts
        ax.text(0.55, y, str(row["Spiele"]), fontsize=16, ha="center", va="center")
        ax.text(0.65, y, row["S-U-N"], fontsize=16, ha="center", va="center")
        ax.text(0.75, y, str(row["Torverhältnis"]), fontsize=16, ha="center", va="center")
        ax.text(0.88, y, str(row["Punkte"]),
                fontsize=18, ha="center", va="center", fontweight="bold")

        # Trennlinie: y zweimal übergeben oder hlines verwenden
        ax.plot([0.03, 0.95], [y - 0.025, y - 0.025], color="#DDDDDD", linewidth=1, zorder=1)

    plt.tight_layout()

    os.makedirs("Screenshots_table", exist_ok=True)
    output_file = "Screenshots_table/table.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Modernes Bundesliga-Bild gespeichert unter: {output_file}")


def main():
    df = table_api()

    
    logos_dict = {
    "FC Bayern München" : "logos/Bayern.png",
    "RB Leipzig" : "logos/Leipzig.png",
    "Borussia Dortmund" : "logos/BVB.png",
    "VfB Stuttgart" : "logos/Stuttgart.png" ,
    "Bayer 04 Leverkusen" : "logos/Leverkusen.png",
    "TSG Hoffenheim" : "logos/Hoffenheim.png",
    "Eintracht Frankfurt" : "logos/Frankfurt.png",
    "SV Werder Bremen" : "logos/Bremen.png",
    "1. FC Köln" : "logos/Köln.png",
    "SC Freiburg" : "logos/Freiburg.png",
    "1. FC Union Berlin" : "logos/Union.png",
    "Borussia Mönchengladbach" : "logos/Gladbach.png",
    "Hamburger SV" : "logos/HSV.png",
    "VfL Wolfsburg" : "logos/Wolfsburg.png",
    "FC Augsburg" : "logos/Augsburg.png",
    "FC St. Pauli" : "logos/Pauli.png",
    "1. FSV Mainz 05" : "logos/Mainz.png",
    "1. FC Heidenheim 1846" : "logos/Heidenheim.png"
    }

    #
    render_modern_png(df, logos_dict)


main()