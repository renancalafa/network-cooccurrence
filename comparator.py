from hamcrest import none
import pandas as pd
import numpy as np
import networkx as nx
import os
import openpyxl as op
from openpyxl.styles import Border, Side, Font

class Comparator:

    comorbidities = ['cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro ', 'paralysis', 'hypothyroid', 'rheum', 'coag', 'danemia ', 'dabuse', 'psychoses', 'depression']
    pathfile = "sheets/Main.xlsx"

    def create_main_sheet(self, race):

        wb, ws = self.initialize_workbook(race)

        # phi_dict = self.get_data_dict(pd.DataFrame(Phi), "Phi", )
        # t_dict = self.get_data_dict(pd.DataFrame(t), "t", )

        phi_df = pd.read_csv('test/' + race["race_abv"] + '/' + race["race_abv"] + '_all_Phi.csv', header=None)
        t_df = pd.read_csv('test/' + race["race_abv"] + '/' + race["race_abv"] + '_all_t.csv', header=None)
        print(phi_df)
        print(t_df)
        phi_dict = self.get_data_dict(pd.DataFrame(phi_df), "Phi", )
        t_dict = self.get_data_dict(pd.DataFrame(t_df), "t", )

        # merge t and phi
        for i, row in enumerate(t_dict):
            phi_dict[i]["t"] = row["t"]

        phi_dict_sorted = sorted(phi_dict, key=lambda d: d['Phi'], reverse=True) 

        for row, data in enumerate(phi_dict_sorted, start=3):
            ws[f"B{row}"] = data["Source"]
            ws[f"C{row}"] = data["Target"]
            ws[f"D{row}"] = data["Phi"]
            ws[f"E{row}"] = data["t"]
            # if (-1.96 < data["t"] < 1.96):
            #     ws[f"E{row}"].font = Font(bold=True)
            #     ws[f"D{row}"].font = Font(bold=True)

        wb.save(self.pathfile) 
        
    def initialize_workbook(self, race):

        if(os.path.exists(self.pathfile)):
            wb = op.load_workbook(self.pathfile)
            ws = wb.active
            ws.move_range("A1:E233", cols=5 * race["number"])
        else:
            wb = op.Workbook()
            ws = wb.active

        colour = self.get_cell_colour(race)
        ws.cell(row=1,column=2).value = race["race_full"]
        ws.cell(row=1,column=2).alignment = op.styles.Alignment(horizontal='center', vertical='center')
        ws.merge_cells('B1:E1')
        ws.merge_cells('G1:J1')
        ws.merge_cells('L1:O1')
        ws.merge_cells('Q1:T1')
        ws["B1"].fill = colour
        ws["B2"] = "Source"
        ws["C2"] = "Target"
        ws["D2"] = "Phi"
        ws["E2"] = "t"
        ws.column_dimensions['F'].width = 1
        ws.column_dimensions['K'].width = 1
        ws.column_dimensions['P'].width = 1

        bd = Border(top = Side(border_style='thin', color='FF000000'),    
                              right = Side(border_style='thin', color='FF000000'), 
                              bottom = Side(border_style='thin', color='FF000000'),
                              left = Side(border_style='thin', color='FF000000')) 

        for row in ws["B1:E233"]:
            for cell in row:
                cell.fill = colour
                cell.border = bd

        return wb, ws

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