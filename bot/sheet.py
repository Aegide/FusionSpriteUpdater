import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


spreadsheet_name = "Pokemon IF Sprite Completion (main sheet)"


# white square before the data
row_fusion_init = 9
col_fusion_init = 8


pokemon_amount = 420


no_fusion = ""
valid_fusion = "x"
approved_fusion = "✓"


scope = None
creds = None
client = None
sheet = None
wks = None


# def create_json_token(token_data, keyfile):
#     with open(keyfile, "w") as json_file: 
#         json_file.write(token_data)


# def get_creds(scope):
#     try:
#         token_data = os.environ["GSHEET_KEY"]
#     except:
#         keyfile = "token/gsheet.json"
#         creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
#     else:
#         keyfile = "token/gsheet.json"
#         create_json_token(token_data, keyfile)
#         creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
#     return creds


# def init(worksheet_name):
#     successful_init = True
#     try:
#         global scope, creds, client, sheet, wks
#         scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
#         creds = get_creds(scope)
#         client = gspread.authorize(creds)
#         sheet = client.open(spreadsheet_name)
#         wks = sheet.worksheet(worksheet_name)
#     except Exception as e:
#         print("Exception :", e, "\n")
#         successful_init = False
#     return successful_init


# def get_fusion_data_by_fusion_id(fusion_id):
#     split_fusion_id = fusion_id.split(".")
#     if len(split_fusion_id) == 2:
#         head_id, body_id = int(split_fusion_id[0]), int(split_fusion_id[1])
#         return get_fusion_data(head_id, body_id)
#     else:
#         print("ERROR", "get_fusion_data_by_fusion_id", fusion_id)


# def get_valid_cell_by_fusion_id(fusion_id):
#     split_fusion_id = fusion_id.split(".")
#     if len(split_fusion_id) == 2:
#         head_id, body_id = int(split_fusion_id[0]), int(split_fusion_id[1])
#         return get_valid_cell(head_id, body_id)
#     else:
#         print("ERROR", "get_cell_by_fusion_id", fusion_id)


# def get_valid_cell(head_id, body_id):
#     row, col = row_fusion_init + body_id, col_fusion_init + head_id
#     try:
#         result = gspread.models.Cell(row, col, approved_fusion)
#     except Exception as e :
#         print(e)
#         result = "API ERROR"
#     return result


# def get_fusion_data(head_id, body_id):
#     row, col = row_fusion_init + body_id, col_fusion_init + head_id
#     try:
#         result = gspread.models.Worksheet.cell(wks, row, col).value
#     except Exception as e :
#         print(e)
#         result = "API ERROR"
#     return result


# def set_fusion_data(head_id, body_id, new_value):
#     head_id = int(head_id)
#     body_id = int(body_id)
#     row = row_fusion_init + body_id
#     col = col_fusion_init + head_id
#     if wks.col_count >= col and wks.row_count >= row: 
#         cell = gspread.utils.rowcol_to_a1(row, col)
#         wks.update_acell(cell, new_value)
#     else:
#         print("set_fusion_data", head_id, body_id)


# def set_fusion_data_from_list(list_cells):
#     wks.update_cells(list_cells)


# def validate_fusion(fusion_id, update_sheet=True):
#     split_fusion_id = fusion_id.split(".")
#     if len(split_fusion_id) == 2:
#         head_id, body_id= int(split_fusion_id[0]), int(split_fusion_id[1])
#         current_value = get_fusion_data(head_id, body_id)
#         if(current_value != approved_fusion and update_sheet):
#             set_fusion_data(head_id, body_id, valid_fusion)
#     else:
#         print("validate_fusion", fusion_id)


# def get_all_fusion_data():
#     first_cell = gspread.utils.rowcol_to_a1(row_fusion_init + 1, col_fusion_init + 1)
#     last_cell = gspread.utils.rowcol_to_a1(row_fusion_init + pokemon_amount, col_fusion_init + pokemon_amount)
#     all_range = first_cell + ":" + last_cell
#     all_data = wks.get(all_range)
#     return all_data


# if __name__ == "__main__":
#     scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
#     creds = get_creds(scope)
#     worksheet_name = "Full dex"

#     init(worksheet_name)
