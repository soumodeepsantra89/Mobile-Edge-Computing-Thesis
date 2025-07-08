import pandas as pd
import os

# Step 1: Set the path
base_path = r'E:\dataset\thesis'
input_file = os.path.join(base_path, 'Mobile Edge computing dataset.csv')  # Replace with your actual CSV filename

# Step 2: Read the CSV file
df = pd.read_csv(input_file)

# Step 3: Define year ranges and output CSV file names
year_ranges = {
    '2011_2013.csv': (2011, 2013),
    '2014_2016.csv': (2014, 2016),
    '2017_2019.csv': (2017, 2019),
    '2020_2022.csv': (2020, 2022),
    '2023_2024.csv': (2023, 2024)
}

# Step 4: Filter and save each range as CSV
for filename, (start_year, end_year) in year_ranges.items():
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    output_path = os.path.join(base_path, filename)
    filtered_df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} ({len(filtered_df)} rows)")
