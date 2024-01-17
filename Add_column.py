import pandas as pd

# Load the CSV file
df = pd.read_csv("Restaurant_grubhub_data.csv")

# Extract the Restaurant ID and add it as a new column
df['Restaurant_id'] = df['Restaurant_Link'].apply(lambda x: x.split('/')[-1])

# Reorder columns to have Restaurant_id at the beginning
column_order = ['Restaurant_id', 'Restaurant_Link', 'Name', 'Ratings', 'Cuisine']
df = df[column_order]

# Save the updated DataFrame back to CSV
df.to_csv("Restaurant_grubhub_data_updated.csv", index=False, encoding='utf-8')
