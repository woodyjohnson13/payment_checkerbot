import gspread
import os
from google.oauth2.service_account import Credentials

current_directory = os.path.dirname(os.path.abspath(__file__))
credential = os.path.join(current_directory, "testing_creds.json")

class GoogleSheet:
    def __init__(self):
        # Define the scope of access
        self.scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
        
    
    def create_sheet(self,credentials_file,spreadsheet_id,sheet_name):
        credentials = Credentials.from_service_account_file(credentials_file)
        scoped_credentials = credentials.with_scopes(self.scope)
        client = gspread.authorize(scoped_credentials)
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        return sheet
            
        
    def add_row(self, row_data, column_mapping,sheet):
        try:
            # Find the next available row
            next_row = len(sheet.get_all_values()) + 1
            
            # Initialize a list to hold the values for the row
            row_values = []
            
            # Iterate over the column mapping to construct the row values
            for column_name, value in row_data.items():
                # Add the value to the list of row values
                row_values.append(value)
            
            # Update the values within the specified row
            sheet.insert_row(row_values, index=next_row)
            
            print("Row added successfully!")
        except Exception as e:
            print("Error adding row:", e)

    def read_data(self):
        # Read data from the sheet
        data = self.sheet.get_all_values()
        return data


column_mapping = {'Name': 'A', 'Age': 'C', 'Location': 'B'}
row_data = {'Name': 'John', 'Age': 30, 'Location': 'New York'}

google=GoogleSheet()
my_sheet=google.create_sheet(credential,"154wOj16F5j_YvMRcw0rRE6_u_Hi4qBZCwdejWD_bWMU","test1")
google.add_row(row_data,column_mapping,my_sheet)

