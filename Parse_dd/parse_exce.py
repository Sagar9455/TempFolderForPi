import pandas as pd

# Load the Excel file
file_path = 'uds_configuration.xlsx'  
xls=pd.ExcelFile(file_path)
# List all sheets
print("Sheets in the Excel file:", xls.sheet_names)

# Read each sheet into a DataFrame
services_df = pd.read_excel(xls, sheet_name='Services')
dtcs_df = pd.read_excel(xls, sheet_name='DTCs')
nrcs_df = pd.read_excel(xls, sheet_name='NRCs')
responses_df = pd.read_excel(xls, sheet_name='Responses')

# Display data
print("Services:\n", services_df.head())
print("\nDTCs:\n", dtcs_df.head())
print("\nNRCs:\n", nrcs_df.head())
print("\nResponses:\n", responses_df.head())

# Access specific data (e.g., all services)
all_services = services_df[['Service ID', 'Service Name']]
print("All Services:\n", all_services)
