import gspread
import os
from google.oauth2.service_account import Credentials

current_directory = os.path.dirname(os.path.abspath(__file__))
credential = os.path.join(current_directory, "credentials.json")

class GoogleSheet:
    def __init__(self):
        # Define the scope of access
        self.scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
        
    
    def create_sheet(self,spreadsheet_id,sheet_name):
        credentials = Credentials.from_service_account_file(credential)
        scoped_credentials = credentials.with_scopes(self.scope)
        client = gspread.authorize(scoped_credentials)
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        return sheet
    
    
    def convert_to_column_number(self,col_literal):
        column_number = 0
        for char in col_literal.upper():
            digit = ord(char) - ord('A') + 1
            column_number = column_number * 26 + digit
        return column_number
        
        
    def add_row(self, sheet, data):
        last_row = len(sheet.get_all_values())
        print(data)
        for column, value in data.items():
            column_index=self.convert_to_column_number(column)
            if column_index:
                sheet.update_cell(last_row + 1, column_index, value)
            else:
                # Handle case where column is not found in the mapping (optional)
                print(f"Warning: Column '{column}' not found in mapping.")


    def get_row_number_by_cell_content(self, sheet, search_content, column):
        column_index = self.convert_to_column_number(column)
        if column_index:
            column_values = sheet.col_values(column_index)
            try:
                cell_index = column_values.index(search_content) + 1  # Adjust to 1-based index
                return cell_index
            except ValueError:
                print(f"Content '{search_content}' not found in column '{column}'.")
                return False
        else:
            print(f"Invalid column: '{column}'.")
            return False

    
    
    def append_to_cell(self, sheet, value, column, row_number):
        column_index = self.convert_to_column_number(column)
        if column_index:
                try:
                    # Get the current content of the cell
                    current_content = sheet.cell(row_number, column_index).value
                    if current_content:
                        new_content = f"{current_content}, {value}"
                    else:
                        new_content = value
                    # Update the cell with the new content
                    sheet.update_cell(row_number, column_index, new_content)
                    return True
                except Exception as e:
                    print(f"Error occurred while appending value: {e}")
                    return False
        else:
                print(f"Invalid column: '{column}'.")
                return False

