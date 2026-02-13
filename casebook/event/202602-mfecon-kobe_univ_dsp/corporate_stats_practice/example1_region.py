import pandas as pd
from pathlib import Path

def to_numeric_safe(series):
    # カンマ区切りや空白を含む文字列を数値に変換
    return pd.to_numeric(series.astype(str).str.replace(',', '').str.replace(' ', ''), errors='coerce').fillna(0)

def sort_key(row):
    region_idx = region_order.index(row['地域圏']) if row['地域圏'] in region_order else 999
    if row['地域圏'] in pref_order:
        pref_idx = pref_order[row['地域圏']].index(row['都道府県']) if row['都道府県'] in pref_order[row['地域圏']] else 999
    else:
        pref_idx = 999 if row['都道府県'] != '合計' else 1000
    return (region_idx, pref_idx)

# 都道府県を地域圏にマッピング
region_mapping = {
    '北海道': '三大都市圏以外', '青森県': '三大都市圏以外', '岩手県': '三大都市圏以外', '宮城県': '三大都市圏以外',
    '秋田県': '三大都市圏以外', '山形県': '三大都市圏以外', '福島県': '三大都市圏以外', '茨城県': '三大都市圏以外',
    '栃木県': '三大都市圏以外', '群馬県': '三大都市圏以外', '埼玉県': '東京圏', '千葉県': '東京圏',
    '東京都': '東京圏', '神奈川県': '東京圏', '新潟県': '三大都市圏以外', '富山県': '三大都市圏以外',
    '石川県': '三大都市圏以外', '福井県': '三大都市圏以外', '山梨県': '三大都市圏以外', '長野県': '三大都市圏以外',
    '岐阜県': '名古屋圏', '静岡県': '三大都市圏以外', '愛知県': '名古屋圏', '三重県': '名古屋圏',
    '滋賀県': '三大都市圏以外', '京都府': '大阪圏', '大阪府': '大阪圏', '兵庫県': '大阪圏',
    '奈良県': '大阪圏', '和歌山県': '三大都市圏以外', '鳥取県': '三大都市圏以外', '島根県': '三大都市圏以外',
    '岡山県': '三大都市圏以外', '広島県': '三大都市圏以外', '山口県': '三大都市圏以外', '徳島県': '三大都市圏以外',
    '香川県': '三大都市圏以外', '愛媛県': '三大都市圏以外', '高知県': '三大都市圏以外', '福岡県': '三大都市圏以外',
    '佐賀県': '三大都市圏以外', '長崎県': '三大都市圏以外', '熊本県': '三大都市圏以外', '大分県': '三大都市圏以外',
    '宮崎県': '三大都市圏以外', '鹿児島県': '三大都市圏以外', '沖縄県': '三大都市圏以外'
}

region_order = ['東京圏', '名古屋圏', '大阪圏', '三大都市圏以外', '不明', '']
pref_order = {
    '東京圏': ['計', '東京都', '埼玉県', '千葉県', '神奈川県'],
    '名古屋圏': ['計', '愛知県', '岐阜県', '三重県'],
    '大阪圏': ['計', '大阪府', '京都府', '兵庫県', '奈良県'],
    '三大都市圏以外': ['計'], '不明': ['計']
}

region_data = {
    '地域圏': ['東京圏', '東京圏', '東京圏', '東京圏', '東京圏', '名古屋圏', '名古屋圏', '名古屋圏', '名古屋圏', '大阪圏', '大阪圏', '大阪圏', '大阪圏', '大阪圏', '三大都市圏以外', '不明'],
    '都道府県': ['計', '東京都', '埼玉県', '千葉県', '神奈川県', '計', '愛知県', '岐阜県', '三重県', '計', '大阪府', '京都府', '兵庫県', '奈良県', '計', '計'],
    '法人数': [18198, 13888, 1105, 1043, 2162, 1933, 1552, 238, 143, 5034, 2963, 831, 1051, 189, 10347, 443],
    '比率（％）': [50.6, 38.6, 3.1, 2.9, 6.0, 5.4, 4.3, 0.7, 0.4, 14.0, 8.2, 2.3, 2.9, 0.5, 28.8, 1.2]
}
df_cloud = pd.DataFrame(region_data)

# Downloads から CSV を読み込む
#  「令和3年経済センサス-活動調査 / 企業等に関する集計 / 産業横断的集計 / 経理事項等（表番号：7）」
#  （総務省統計局）（https://www.e-stat.go.jp/dbview?sid=0004006333）を加工して作成
csv_path = Path.home() / "Downloads" / "estat_census_region.csv"
df_census = pd.read_csv(csv_path, encoding='shift_jis')

df_census.columns = df_census.columns.str.strip()
cond = df_census['企業産業大分類'].str.contains('全産業', na=False) & df_census['企業産業大分類'].str.contains('公務を除く', na=False)
df_census_filtered = df_census.loc[cond].copy()

# 法人数 = 会社企業 + 会社以外の法人
df_census_filtered['法人数'] = to_numeric_safe(df_census_filtered['会社企業']) + to_numeric_safe(df_census_filtered['会社以外の法人'])
df_census_filtered['都道府県'] = df_census_filtered['地域'].str.strip()

# 「全国」の行から合計を取得
census_total_row = df_census_filtered[df_census_filtered['都道府県'] == '全国'].copy()
total_census = census_total_row['法人数'].iloc[0] if len(census_total_row) > 0 else df_census_filtered[df_census_filtered['都道府県'] != '全国']['法人数'].sum()

# 「全国」を除いて都道府県別・地域圏別に集計
df_census_filtered = df_census_filtered[df_census_filtered['都道府県'] != '全国'].copy()
df_census_filtered['地域圏'] = df_census_filtered['都道府県'].map(region_mapping)

census_pref = df_census_filtered[df_census_filtered['都道府県'].notna() & (df_census_filtered['都道府県'] != '')].groupby(['地域圏', '都道府県'])['法人数'].sum().reset_index()
census_region = df_census_filtered.groupby('地域圏')['法人数'].sum().reset_index()
census_region['都道府県'] = '計'

census_pref['比率（％）'] = (census_pref['法人数'] / total_census * 100).round(1)
census_region['比率（％）'] = (census_region['法人数'] / total_census * 100).round(1)
census_combined = pd.concat([census_region, census_pref], ignore_index=True)

# クラウド会計データと経済センサスデータを結合
result = df_cloud.merge(census_combined, on=['地域圏', '都道府県'], how='left', suffixes=('_cloud', '_census'))
result = result.rename(columns={
    '法人数_cloud': 'クラウド会計_法人数',
    '比率（％）_cloud': 'クラウド会計_比率（％）',
    '法人数_census': '経済センサス_法人数',
    '比率（％）_census': '経済センサス_比率（％）'
})
# 経済センサスの値を0で埋めてから差分を計算
result['経済センサス_法人数'] = result['経済センサス_法人数'].fillna(0)
result['経済センサス_比率（％）'] = result['経済センサス_比率（％）'].fillna(0.0)
result['差分（％pt）'] = (result['クラウド会計_比率（％）'] - result['経済センサス_比率（％）']).round(1)

total_row = pd.DataFrame({
    '地域圏': [''], '都道府県': ['合計'],
    'クラウド会計_法人数': [df_cloud['法人数'].sum()], 'クラウド会計_比率（％）': [100.0],
    '経済センサス_法人数': [total_census], '経済センサス_比率（％）': [100.0],
    '差分（％pt）': [0.0]
})
result = pd.concat([result, total_row], ignore_index=True)

result_sorted = result[result['都道府県'] != '合計'].copy()
result_sorted['_sort_key'] = result_sorted.apply(sort_key, axis=1)
result_sorted = result_sorted.sort_values('_sort_key').drop('_sort_key', axis=1)
result_final = pd.concat([result_sorted, result[result['都道府県'] == '合計']], ignore_index=True)

print(result_final)

# Downloads に CSV を出力
output_csv_path = Path.home() / "Downloads" / "region_comparison.csv"
result_final.to_csv(output_csv_path, index=False, encoding='shift_jis')

