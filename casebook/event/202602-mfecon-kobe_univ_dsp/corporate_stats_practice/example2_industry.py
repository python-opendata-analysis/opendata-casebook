import pandas as pd
from pathlib import Path

def to_numeric_safe(series):
    # カンマ区切りや空白、ハイフンを含む文字列を数値に変換
    return pd.to_numeric(series.astype(str).str.replace(',', '').str.replace(' ', '').str.replace('-', '0'), errors='coerce').fillna(0)

# 経済センサスの業種をクラウド会計の業種にマッピング
industry_mapping = {
    '建設業': '建設業',
    '製造業': '製造業',
    '情報通信業': '情報通信',
    '運輸業，郵便業': '運送業',
    '卸売業': '卸売業',
    '小売業': '小売業',
    '金融業，保険業': '金融保険業',
    '不動産業': '不動産業',
    '飲食店，持ち帰り・配達飲食サービス業': '飲食業',
    '教育，学習支援業': '教育業',
    '医療，福祉': '医療/福祉',
    '学術研究，専門・技術サービス業': 'サービス業',
    '生活関連サービス業，娯楽業': 'サービス業',
    '複合サービス事業': 'サービス業',
    'サービス業（他に分類されないもの）': 'サービス業',
    '宿泊業': 'サービス業',
    '農業，林業': 'その他', 
    '漁業': 'その他', 
    '鉱業，採石業，砂利採取業': 'その他',
    '電気・ガス・熱供給・水道業': 'その他',
    '物品賃貸業': 'その他'
}

industry_order = ['建設業', '製造業', '情報通信', '運送業', '卸売業', '小売業', '金融保険業', '不動産業', '飲食業', '教育業', '医療/福祉', 'サービス業', 'その他', '不明', '合計']

industry_data = {
    '業種': ['建設業', '製造業', '情報通信', '運送業', '卸売業', '小売業', '金融保険業', '不動産業', '飲食業', '教育業', '医療/福祉', 'サービス業', 'その他', '不明'],
    '法人数': [2362, 1836, 3252, 413, 1709, 2806, 325, 2288, 1378, 587, 2061, 11878, 4723, 337],
    '比率（％）': [6.6, 5.1, 9.0, 1.1, 4.8, 7.8, 0.9, 6.4, 3.8, 1.6, 5.7, 33.0, 13.1, 0.9]
}
df_cloud = pd.DataFrame(industry_data)

# Downloads から CSV を読み込む
#  「令和3年経済センサス-活動調査 / 企業等に関する集計 / 産業横断的集計 / 経理事項等（表番号：6）」
#  （総務省統計局）（https://www.e-stat.go.jp/dbview?sid=0004006361）を加工して作成
csv_path = Path.home() / "Downloads" / "estat_census_industry.csv"
df_census = pd.read_csv(csv_path, encoding='shift_jis')

df_census.columns = df_census.columns.str.strip()
cond = df_census['地域'].str.contains('全国', na=False)
df_census_filtered = df_census.loc[cond].copy()

# 法人数 = 会社企業 + 会社以外の法人
df_census_filtered['法人数'] = to_numeric_safe(df_census_filtered['会社企業']) + to_numeric_safe(df_census_filtered['会社以外の法人'])
df_census_filtered['業種'] = df_census_filtered['企業産業小分類'].str.strip()

# 「全産業」の行から合計を取得
census_total_row = df_census_filtered[df_census_filtered['企業産業小分類'].str.contains('全産業', na=False)].copy()
total_census = census_total_row['法人数'].iloc[0] if len(census_total_row) > 0 else df_census_filtered['法人数'].sum()

# 業種マッピングを適用（マッピングされていない業種は除外）
df_census_filtered['業種_マッピング'] = df_census_filtered['業種'].map(industry_mapping)
df_census_filtered = df_census_filtered[df_census_filtered['業種_マッピング'].notna()].copy()

# 業種別に集計
census_industry = df_census_filtered.groupby('業種_マッピング')['法人数'].sum().reset_index()
census_industry = census_industry.rename(columns={'業種_マッピング': '業種'})
census_industry['比率（％）'] = (census_industry['法人数'] / total_census * 100).round(1)

# クラウド会計データと経済センサスデータを結合
result = df_cloud.merge(census_industry, on='業種', how='left', suffixes=('_cloud', '_census'))
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
    '業種': ['合計'],
    'クラウド会計_法人数': [df_cloud['法人数'].sum()],
    'クラウド会計_比率（％）': [100.0],
    '経済センサス_法人数': [total_census],
    '経済センサス_比率（％）': [100.0],
    '差分（％pt）': [0.0]
})
result = pd.concat([result, total_row], ignore_index=True)

result['_sort_key'] = result['業種'].apply(lambda x: industry_order.index(x) if x in industry_order else 999)
result_final = result.sort_values('_sort_key').drop('_sort_key', axis=1).reset_index(drop=True)

print(result_final)

# Downloads に CSV を出力
output_csv_path = Path.home() / "Downloads" / "industry_comparison.csv"
result_final.to_csv(output_csv_path, index=False, encoding='shift_jis')
