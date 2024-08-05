import pandas as pd
import sys

# 유해 위험 요인 추출
path = './KRA_20910.xls'
df = pd.read_excel(path, sheet_name='3-3 위험성평가(4)')
df_cleaned = df.dropna(subset=['Unnamed: 1', 'Unnamed: 3'])

matches = {}
results = []
current_factor = None

for _, row in df_cleaned.iterrows():
    factor = row['Unnamed: 1']
    description = row['Unnamed: 3']
    
    if pd.notna(factor) and '요인' in factor:
        current_factor = factor
        if current_factor not in matches:
            matches[current_factor] = []
    if pd.notna(description) and current_factor:
        matches[current_factor].append(description)

for factor, descriptions in matches.items():
    print(f"{factor}:")
    for description in descriptions:
        results.append((factor, description))

results_df = pd.DataFrame(results)
results_df.to_csv('./extracted_factor.csv', index=False, header=['factor', 'descriptions'])
