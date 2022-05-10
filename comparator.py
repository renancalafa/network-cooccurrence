import pandas as pd
import numpy as np
import networkx as nx
import os
import openpyxl as op
from openpyxl.styles import Border, Side

class Comparator:

    comorbidities = ['cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro ', 'paralysis', 'hypothyroid', 'rheum', 'coag', 'danemia ', 'dabuse', 'psychoses', 'depression']

    def create_main_sheet(self, Phi, t, race):
        # dataframe_phi = pd.read_csv('test/Phi.csv', header=None)
        # dataframe_t = pd.read_csv('test/t.csv', header=None)
        if(os.path.exists("sheets/Main.xlsx")):
            wb = op.load_workbook("sheets/Main.xlsx")
            ws = wb.active
            ws.move_range("A1:E233", cols=5 * race["number"])
        else:
            wb = op.Workbook()
            ws = wb.active


        phi_dict = self.get_data_dict(pd.DataFrame(Phi), "Phi", )
        t_dict = self.get_data_dict(pd.DataFrame(t), "t", )
        # merge t and phi
        for i, row in enumerate(t_dict):
            phi_dict[i]["t"] = row["t"]

        colour = self.get_cell_colour(race)
        ws.cell(row=1,column=2).value = race["race_full"]
        ws.cell(row=1,column=2).alignment = op.styles.Alignment(horizontal='center', vertical='center')
        ws.merge_cells('B1:E1')
        ws["B1"].fill = colour
        ws["B2"] = "Source"
        ws["C2"] = "Target"
        ws["D2"] = "Phi"
        ws["E2"] = "t"

        bd = Border(top = Side(border_style='thin', color='FF000000'),    
                              right = Side(border_style='thin', color='FF000000'), 
                              bottom = Side(border_style='thin', color='FF000000'),
                              left = Side(border_style='thin', color='FF000000'))

        ws["B1"].fill = colour

        for row, data in enumerate(phi_dict, start=3):
            ws[f"B{row}"] = data["Source"]
            ws[f"C{row}"] = data["Target"]
            ws[f"D{row}"] = data["Phi"]
            ws[f"E{row}"] = data["t"]

        for row in ws["B1:E233"]:
            for cell in row:
                cell.fill = colour
                cell.border = bd

        

        wb.save("sheets/Main.xlsx") 
        
    def get_data_dict(self, df, df_data):
        cmbdts = self.comorbidities
        race_data = []
        df_dict = df.to_dict('records')
        for i, data in enumerate(df_dict):
            for j, key in enumerate(data):
                if(j > i): #eliminates equals and duplicated
                    race_data.append({
                        "Source": cmbdts[i],
                        "Target": cmbdts[key],
                        df_data: data[key],
                    })
        return race_data

    def get_cell_colour(self, race):
        if(race["race_abv"] == "black"):
            colour = op.styles.PatternFill(start_color="f4cccc", fill_type="solid")
        elif(race["race_abv"] == "asian"):
            colour = op.styles.PatternFill(start_color="d9ead3", fill_type="solid")
        elif(race["race_abv"] == "white"):
            colour = op.styles.PatternFill(start_color="d9d2e9", fill_type="solid")
        elif(race["race_abv"] == "hisp"):
            colour = op.styles.PatternFill(start_color="c9daf8", fill_type="solid")
        else:
            colour = op.styles.PatternFill(start_color="fce5cd", fill_type="solid")
        return colour