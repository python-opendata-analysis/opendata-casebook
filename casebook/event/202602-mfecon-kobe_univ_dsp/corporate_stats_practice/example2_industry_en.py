import pandas as pd
from pathlib import Path

def to_numeric_safe(series):
    # Convert strings with commas, spaces, and hyphens to numeric values
    return pd.to_numeric(series.astype(str).str.replace(',', '').str.replace(' ', '').str.replace('-', '0'), errors='coerce').fillna(0)

# Map census industry classifications to cloud accounting industry classifications
industry_mapping = {
    'Construction': 'Construction',
    'Manufacturing': 'Manufacturing',
    'Information and Communications': 'Information and Communications',
    'Transport and Postal Activities': 'Transportation',
    'Wholesale and Retail Trade': 'Wholesale',  # Will be split later
    'Finance and Insurance': 'Finance and Insurance',
    'Real Estate and Goods Rental and Leasing': 'Real Estate',  # Includes rental services
    'Accommodations, Eating and Drinking Services': 'Food Service',
    'Education, Learning Support': 'Education',
    'Medical, Health Care and Welfare': 'Medical/Welfare',
    'Scientific Research, Professional and Technical Services': 'Services',
    'Living-Related and Personal Services and Amusement Services': 'Services',
    'Compound Services': 'Services',
    'Services, n.e.c.': 'Services',
    'Agriculture and Forestry': 'Other', 
    'Fisheries': 'Other', 
    'Mining and Quarrying of Stone and Gravel': 'Other',
    'Electricity, Gas, Heat Supply and Water': 'Other'
}

industry_order = ['Construction', 'Manufacturing', 'Information and Communications', 'Transportation', 'Wholesale', 'Retail', 'Finance and Insurance', 'Real Estate', 'Food Service', 'Education', 'Medical/Welfare', 'Services', 'Other', 'Unknown', 'Total']

industry_data = {
    'Industry': ['Construction', 'Manufacturing', 'Information and Communications', 'Transportation', 'Wholesale', 'Retail', 'Finance and Insurance', 'Real Estate', 'Food Service', 'Education', 'Medical/Welfare', 'Services', 'Other', 'Unknown'],
    'Number_of_Corporations': [2362, 1836, 3252, 413, 1709, 2806, 325, 2288, 1378, 587, 2061, 11878, 4723, 337],
    'Percentage': [6.6, 5.1, 9.0, 1.1, 4.8, 7.8, 0.9, 6.4, 3.8, 1.6, 5.7, 33.0, 13.1, 0.9]
}
df_cloud = pd.DataFrame(industry_data)

# Read CSV from Downloads
csv_path = Path.home() / "Downloads" / "estat_census_industry_en.csv"
df_census = pd.read_csv(csv_path, encoding='shift_jis')

df_census.columns = df_census.columns.str.strip()
cond = df_census['Area'].str.contains('Japan', na=False)
df_census_filtered = df_census.loc[cond].copy()

# Number of corporations = Companies + Corporations other than companies
df_census_filtered['Number_of_Corporations'] = to_numeric_safe(df_census_filtered['Companies']) + to_numeric_safe(df_census_filtered['Corporations other than companies'])
df_census_filtered['Industry'] = df_census_filtered['Industry groups of enterprises'].str.strip()

# Get total from "All industries" row
census_total_row = df_census_filtered[df_census_filtered['Industry groups of enterprises'].str.contains('All industries', na=False)].copy()
total_census = census_total_row['Number_of_Corporations'].iloc[0] if len(census_total_row) > 0 else df_census_filtered['Number_of_Corporations'].sum()

# Apply industry mapping (exclude industries not in mapping)
df_census_filtered['Industry_Mapped'] = df_census_filtered['Industry'].map(industry_mapping)

# Handle "Wholesale and Retail Trade" - split into Wholesale and Retail
wholesale_retail = df_census_filtered[df_census_filtered['Industry'] == 'Wholesale and Retail Trade'].copy()
if len(wholesale_retail) > 0:
    # Split 50/50 (or use actual ratio if available)
    wholesale_row = wholesale_retail.copy()
    wholesale_row['Industry_Mapped'] = 'Wholesale'
    wholesale_row['Number_of_Corporations'] = wholesale_row['Number_of_Corporations'] * 0.5
    
    retail_row = wholesale_retail.copy()
    retail_row['Industry_Mapped'] = 'Retail'
    retail_row['Number_of_Corporations'] = retail_row['Number_of_Corporations'] * 0.5
    
    # Remove original and add split rows
    df_census_filtered = df_census_filtered[df_census_filtered['Industry'] != 'Wholesale and Retail Trade'].copy()
    df_census_filtered = pd.concat([df_census_filtered, wholesale_row, retail_row], ignore_index=True)

df_census_filtered = df_census_filtered[df_census_filtered['Industry_Mapped'].notna()].copy()

# Aggregate by industry
census_industry = df_census_filtered.groupby('Industry_Mapped')['Number_of_Corporations'].sum().reset_index()
census_industry = census_industry.rename(columns={'Industry_Mapped': 'Industry'})
census_industry['Percentage'] = (census_industry['Number_of_Corporations'] / total_census * 100).round(1)

# Merge cloud accounting data and census data
result = df_cloud.merge(census_industry, on='Industry', how='left', suffixes=('_cloud', '_census'))
result = result.rename(columns={
    'Number_of_Corporations_cloud': 'Cloud_Accounting_Number',
    'Percentage_cloud': 'Cloud_Accounting_Percentage',
    'Number_of_Corporations_census': 'Census_Number',
    'Percentage_census': 'Census_Percentage'
})
# Fill missing census values with 0 before calculating difference
result['Census_Number'] = result['Census_Number'].fillna(0)
result['Census_Percentage'] = result['Census_Percentage'].fillna(0.0)
result['Difference_pp'] = (result['Cloud_Accounting_Percentage'] - result['Census_Percentage']).round(1)

total_row = pd.DataFrame({
    'Industry': ['Total'],
    'Cloud_Accounting_Number': [df_cloud['Number_of_Corporations'].sum()],
    'Cloud_Accounting_Percentage': [100.0],
    'Census_Number': [total_census],
    'Census_Percentage': [100.0],
    'Difference_pp': [0.0]
})
result = pd.concat([result, total_row], ignore_index=True)

result['_sort_key'] = result['Industry'].apply(lambda x: industry_order.index(x) if x in industry_order else 999)
result_final = result.sort_values('_sort_key').drop('_sort_key', axis=1).reset_index(drop=True)

print(result_final)

# Output CSV to Downloads
output_csv_path = Path.home() / "Downloads" / "industry_comparison_en.csv"
result_final.to_csv(output_csv_path, index=False, encoding='utf-8')
