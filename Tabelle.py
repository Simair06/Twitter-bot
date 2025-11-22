import openpyxl
from openpyxl.drawing.image import Image
import os
import requests

# Beispiel-Dictionary, jetzt mit lokalem Pfad zum Logo
logos = {
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

def table_api():
    url = "https://api.openligadb.de/getbltable/bl1/2025"
    data = requests.get(url)
    data = data.json()
    table = []
    for team in data:
        info = []
        wdl = f"{team["won"]}-{team["draw"]}-{team["lost"]}"
        info = [team["teamName"], team["matches"], wdl, team["goalDiff"], team["points"]]
        table.append(info)
    return table 






def excel_writer(table):
    # Name der vorhandenen Excel-Datei
    excel_file = "table.xlsx"

    # Arbeitsmappe öffnen
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    # Startzeile = 4
    start_row = 4

    # Daten einfügen
    for i, team in enumerate(table, start=start_row):
        # Spalten H–L füllen
        ws[f"H{i}"] = team[0]
        ws[f"I{i}"] = team[1]
        ws[f"J{i}"] = team[2]
        ws[f"K{i}"] = team[3]
        ws[f"L{i}"] = team[4]

        # Logo aus lokalem Ordner einfügen
        logo_path = logos[team[0]]
        if os.path.exists(logo_path):
            img = Image(logo_path)
            img.width = 20
            img.height = 20
            cell_ref = f"G{i}"
            img.anchor = cell_ref
            
            # Offset in Punkten setzen (vertikal nach unten verschieben)
            from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
            from openpyxl.utils.units import pixels_to_emus
            
            # Erstelle einen OneCellAnchor mit Offset
            row_idx = i - 1  # 0-basierter Index
            col_idx = 6      # Spalte G ist Index 6 (0-basiert)
            
            # Offset in EMU (English Metric Units) - 8 Pixel ≈ 600000 EMU
            y_offset = 600000  # Experimentieren Sie mit diesem Wert
            
            marker = AnchorMarker(col=col_idx, colOff=0, row=row_idx, rowOff=y_offset)
            img.anchor = OneCellAnchor(_from=marker)

# Bild 8 Pixel nach unten verschieben (anpassen wie du willst)
            img.anchor.offset = (0, 8)
            ws.add_image(img)
        else:
            print(f"Logo nicht gefunden: {logo_path}")




    # Spaltenbreite anpassen
    ws.column_dimensions["G"].width = 10
    ws.column_dimensions["H"].width = 20

    # Speichern
    wb.save(excel_file)
    print(f"Excel-Datei '{excel_file}' erfolgreich aktualisiert ab Zeile 4!")



table = table_api()
excel_writer(table)