import pandas as pd
from pathlib import Path

def to_numeric_safe(series):
    # Convert strings with commas and spaces to numeric values
    return pd.to_numeric(series.astype(str).str.replace(',', '').str.replace(' ', ''), errors='coerce').fillna(0)

def sort_key(row):
    region_idx = region_order.index(row['Region']) if row['Region'] in region_order else 999
    if row['Region'] in pref_order:
        pref_idx = pref_order[row['Region']].index(row['Prefecture']) if row['Prefecture'] in pref_order[row['Region']] else 999
    else:
        pref_idx = 999 if row['Prefecture'] != 'Total' else 1000
    return (region_idx, pref_idx)

# Map prefectures to regions
# Handle both with and without "Prefecture" suffix
def normalize_prefecture_name(name):
    """Normalize prefecture name by removing common suffixes"""
    if pd.isna(name):
        return name
    name = str(name).strip()
    # Remove common suffixes (with hyphen)
    for suffix in ['-ken', '-to', '-fu', '-do', ' Prefecture', ' Pref.', ' To', ' Fu', ' Ken', ' Do']:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    # Handle special case: Gumma -> Gunma
    if name == 'Gumma':
        name = 'Gunma'
    return name

region_mapping = {
    'Hokkaido': 'Other', 'Aomori': 'Other', 'Iwate': 'Other', 'Miyagi': 'Other',
    'Akita': 'Other', 'Yamagata': 'Other', 'Fukushima': 'Other', 'Ibaraki': 'Other',
    'Tochigi': 'Other', 'Gunma': 'Other', 'Saitama': 'Tokyo', 'Chiba': 'Tokyo',
    'Tokyo': 'Tokyo', 'Kanagawa': 'Tokyo', 'Niigata': 'Other', 'Toyama': 'Other',
    'Ishikawa': 'Other', 'Fukui': 'Other', 'Yamanashi': 'Other', 'Nagano': 'Other',
    'Gifu': 'Nagoya', 'Shizuoka': 'Other', 'Aichi': 'Nagoya', 'Mie': 'Nagoya',
    'Shiga': 'Other', 'Kyoto': 'Osaka', 'Osaka': 'Osaka', 'Hyogo': 'Osaka',
    'Nara': 'Osaka', 'Wakayama': 'Other', 'Tottori': 'Other', 'Shimane': 'Other',
    'Okayama': 'Other', 'Hiroshima': 'Other', 'Yamaguchi': 'Other', 'Tokushima': 'Other',
    'Kagawa': 'Other', 'Ehime': 'Other', 'Kochi': 'Other', 'Fukuoka': 'Other',
    'Saga': 'Other', 'Nagasaki': 'Other', 'Kumamoto': 'Other', 'Oita': 'Other',
    'Miyazaki': 'Other', 'Kagoshima': 'Other', 'Okinawa': 'Other'
}

region_order = ['Tokyo', 'Nagoya', 'Osaka', 'Other', 'Unknown', '']
pref_order = {
    'Tokyo': ['Total', 'Tokyo', 'Saitama', 'Chiba', 'Kanagawa'],
    'Nagoya': ['Total', 'Aichi', 'Gifu', 'Mie'],
    'Osaka': ['Total', 'Osaka', 'Kyoto', 'Hyogo', 'Nara'],
    'Other': ['Total'], 'Unknown': ['Total']
}

region_data = {
    'Region': ['Tokyo', 'Tokyo', 'Tokyo', 'Tokyo', 'Tokyo', 'Nagoya', 'Nagoya', 'Nagoya', 'Nagoya', 'Osaka', 'Osaka', 'Osaka', 'Osaka', 'Osaka', 'Other', 'Unknown'],
    'Prefecture': ['Total', 'Tokyo', 'Saitama', 'Chiba', 'Kanagawa', 'Total', 'Aichi', 'Gifu', 'Mie', 'Total', 'Osaka', 'Kyoto', 'Hyogo', 'Nara', 'Total', 'Total'],
    'Number_of_Corporations': [18198, 13888, 1105, 1043, 2162, 1933, 1552, 238, 143, 5034, 2963, 831, 1051, 189, 10347, 443],
    'Percentage': [50.6, 38.6, 3.1, 2.9, 6.0, 5.4, 4.3, 0.7, 0.4, 14.0, 8.2, 2.3, 2.9, 0.5, 28.8, 1.2]
}
df_cloud = pd.DataFrame(region_data)

# Read CSV from Downloads
csv_path = Path.home() / "Downloads" / "estat_census_region_en.csv"
df_census = pd.read_csv(csv_path, encoding='shift_jis')

df_census.columns = df_census.columns.str.strip()
cond = df_census['Industry divisions of enterprises'].str.contains('All industries', na=False) & df_census['Industry divisions of enterprises'].str.contains('excluding', na=False)
df_census_filtered = df_census.loc[cond].copy()

# Number of corporations = Companies + Corporations other than companies
df_census_filtered['Number_of_Corporations'] = to_numeric_safe(df_census_filtered['Companies']) + to_numeric_safe(df_census_filtered['Corporations other than companies'])
df_census_filtered['Prefecture'] = df_census_filtered['Area'].str.strip()

# Get total from "Japan" row (for nationwide data)
census_total_row = df_census_filtered[df_census_filtered['Prefecture'] == 'Japan'].copy()
total_census = census_total_row['Number_of_Corporations'].iloc[0] if len(census_total_row) > 0 else df_census_filtered[df_census_filtered['Prefecture'] != 'Japan']['Number_of_Corporations'].sum()

# Exclude "Japan" and aggregate by prefecture and region
df_census_filtered = df_census_filtered[df_census_filtered['Prefecture'] != 'Japan'].copy()
# Normalize prefecture names before mapping
df_census_filtered['Prefecture_Normalized'] = df_census_filtered['Prefecture'].apply(normalize_prefecture_name)
df_census_filtered['Region'] = df_census_filtered['Prefecture_Normalized'].map(region_mapping)

census_pref = df_census_filtered[df_census_filtered['Prefecture_Normalized'].notna() & (df_census_filtered['Prefecture_Normalized'] != '')].groupby(['Region', 'Prefecture_Normalized'])['Number_of_Corporations'].sum().reset_index()
census_pref = census_pref.rename(columns={'Prefecture_Normalized': 'Prefecture'})
census_region = df_census_filtered.groupby('Region')['Number_of_Corporations'].sum().reset_index()
census_region['Prefecture'] = 'Total'

census_pref['Percentage'] = (census_pref['Number_of_Corporations'] / total_census * 100).round(1)
census_region['Percentage'] = (census_region['Number_of_Corporations'] / total_census * 100).round(1)
census_combined = pd.concat([census_region, census_pref], ignore_index=True)

# Merge cloud accounting data and census data
result = df_cloud.merge(census_combined, on=['Region', 'Prefecture'], how='left', suffixes=('_cloud', '_census'))
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
    'Region': [''], 'Prefecture': ['Total'],
    'Cloud_Accounting_Number': [df_cloud['Number_of_Corporations'].sum()], 'Cloud_Accounting_Percentage': [100.0],
    'Census_Number': [total_census], 'Census_Percentage': [100.0],
    'Difference_pp': [0.0]
})
result = pd.concat([result, total_row], ignore_index=True)

result_sorted = result[result['Prefecture'] != 'Total'].copy()
result_sorted['_sort_key'] = result_sorted.apply(sort_key, axis=1)
result_sorted = result_sorted.sort_values('_sort_key').drop('_sort_key', axis=1)
result_final = pd.concat([result_sorted, result[result['Prefecture'] == 'Total']], ignore_index=True)

print(result_final)

# Output CSV to Downloads
output_csv_path = Path.home() / "Downloads" / "region_comparison_en.csv"
result_final.to_csv(output_csv_path, index=False, encoding='utf-8')
