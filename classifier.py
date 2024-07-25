import sys

import pandas as pd
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report

# death_path = './death.csv'
# accident_path = './accident.csv'

# death_df = pd.read_csv(death_path)
# accident_df = pd.read_csv(accident_path)
# df = pd.merge(death_df, accident_df, on=['대업종', '중업종', '규모'])

# 데이터 전처리 
# ## '소계' 항목만 남김
# cond_df = df[df['중업종'].str.endswith('소계')]
# ## '중업종' 컬럼 제거 
# cond_df = cond_df.drop(columns=['중업종'])
# cond_df.to_csv('./total.csv', index=False)

path = '/home/ny/Safety_Hub/data/total.csv'
df = pd.read_csv(path)

X = df[['대업종', '규모']]
y = df.drop(columns=['대업종', '규모'])

# 범주형 변수 인코딩
categorical_features = ['대업종', '규모']
categorical_transformer = OneHotEncoder()

# 피처 스케일링
numeric_features = y.columns
numeric_transformer = StandardScaler()

# 전처리 파이프라인 설정
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)])

# 범주형 변수만 변환
X_transformed = preprocessor.fit_transform(X)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.1, random_state=42)

# 수치형 피처 스케일링
scaler = StandardScaler()
y_train_scaled = scaler.fit_transform(y_train)
y_test_scaled = scaler.transform(y_test)

# 로지스틱 회귀 모델 설정
multi_output_model = MultiOutputClassifier(LogisticRegression(max_iter=1000))

# model = LogisticRegression(max_iter=1000)

# 모델 학습
multi_output_model.fit(X_train, y_train_scaled)

# 테스트 데이터로 평가
y_pred = multi_output_model.predict(X_test)
print(classification_report(y_test_scaled, y_pred, target_names=y.columns))