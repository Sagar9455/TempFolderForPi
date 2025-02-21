import pandas as pd

# Load the Excel file
file_path = 'uds_configuration.xlsx'  
df=pd.read_excel(file_path)


services=df[['Service ID','Service Name']].drop_duplicates()
print("Available Services:")

for index,row in services.iterrows():
	print(f"{index}: {row['Service Name']} (ID: {row['Service ID']})")
	

service_index=int(input("Select a service by index:"))
selected_service=services.iloc[service_index]

print(f"Selected services: {selected_service['Service Name'] }")	

subservices=df[(df['Service ID'] == selected_service['Service ID']) & (df['SubService ID'].notnull() )]

if not subservices.empty:
	print("Available Subservices:")
	for index, row in subservices.iterrows():
		print(f"{index}: {row['SubService Name'] } (ID: {row['SubService ID'] } )" )
		
	sub_index=int(input("Selet a Subservice by index: "))
	selected_subservice=subservices.loc[sub_index]
	print(f"U selected: {selected_subservice['SubService Name'] }")
else:
	print("No subservices available")
