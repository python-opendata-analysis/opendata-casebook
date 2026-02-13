#  ===============================================
#  e-Stat data loading
#  ===============================================
import pandas as pd
from pathlib import Path

# Read CSV from Downloads
#  Created by processing the data from the following source:
#  2021 Economic Census for Business Activity / Tabulation of Enterprises, etc. / Tabulation across Industries / Financial Items, etc.
#  Table number: 1（https://www.e-stat.go.jp/en/dbview?sid=0004006328）
csv_path = Path.home() / "Downloads" / "sample_estat_en.csv"

df = pd.read_csv(csv_path, encoding='shift_jis')
print(df)


#  ===============================================
#  MoneyForward cloud accounting statistics data (by region) reproduction
#  ===============================================

import pandas as pd

# Define region data in hierarchical structure (region and prefecture)
region_data = {
    'Region': ['Tokyo', 'Tokyo', 'Tokyo', 'Tokyo', 'Tokyo', 'Nagoya', 'Nagoya', 'Nagoya', 'Nagoya', 'Osaka', 'Osaka', 'Osaka', 'Osaka', 'Osaka', 'Other', 'Unknown'],
    'Prefecture': ['Total', 'Tokyo', 'Saitama', 'Chiba', 'Kanagawa', 'Total', 'Aichi', 'Gifu', 'Mie', 'Total', 'Osaka', 'Kyoto', 'Hyogo', 'Nara', 'Total', 'Total'],
    'Number_of_Corporations': [18198, 13888, 1105, 1043, 2162, 1933, 1552, 238, 143, 5034, 2963, 831, 1051, 189, 10347, 443],
    'Percentage': [50.6, 38.6, 3.1, 2.9, 6.0, 5.4, 4.3, 0.7, 0.4, 14.0, 8.2, 2.3, 2.9, 0.5, 28.8, 1.2]
}

# Create DataFrame
df = pd.DataFrame(region_data)

# Display DataFrame
print(df)

#  ===============================================
#  Region mapping
#  ===============================================

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

# Map prefectures to regions
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

#  ===============================================
#  MoneyForward cloud accounting statistics data (by industry) reproduction
#  ===============================================

# Define industry data
industry_data = {
    'Industry': ['Construction', 'Manufacturing', 'Information and Communications', 'Transportation', 'Wholesale', 'Retail', 'Finance and Insurance', 'Real Estate', 'Food Service', 'Education', 'Medical/Welfare', 'Services', 'Other', 'Unknown'],
    'Number_of_Corporations': [2362, 1836, 3252, 413, 1709, 2806, 325, 2288, 1378, 587, 2061, 11878, 4723, 337],
    'Percentage': [6.6, 5.1, 9.0, 1.1, 4.8, 7.8, 0.9, 6.4, 3.8, 1.6, 5.7, 33.0, 13.1, 0.9]
}

# Create industry DataFrame
df_industry = pd.DataFrame(industry_data)

# Display DataFrame
print(df_industry)


#  ===============================================
#  Industry mapping
#  ===============================================

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
