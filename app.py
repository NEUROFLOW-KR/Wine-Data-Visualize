import streamlit as st
import pandas as pd
import altair as alt

# CSV 파일 경로 설정
csv_file_path = 'wine_result.csv'  # 여기에 실제 CSV 파일 경로를 지정하세요.

# CSV 파일 로드

def load_data():
    df = pd.read_csv(csv_file_path)
    return df

# Streamlit 앱 제목
st.title("와인 데이터 시각화")

# 데이터 로드
data = load_data()

# 와인 선택 드롭다운
selected_wine = st.selectbox('와인 선택', data['wine_name'].unique())

# 선택한 와인의 데이터 필터링
selected_data = data[data['wine_name'] == selected_wine]

# 선택한 와인의 지역 출력
selected_region = selected_data['region'].values[0]
st.subheader(f'와인 지역: {selected_region}')

# 데이터 재구성
score_data = selected_data.melt(id_vars=['vintage'], value_vars=['predict_score', 'target_score'], var_name='variable', value_name='value')

# '-' 값을 가진 행 제외하고 점수를 오름차순으로 정렬
score_data = score_data[score_data['value'] != '-']
score_data['value'] = score_data['value'].astype(float)  # 문자열을 실수로 변환
score_data = score_data.sort_values(by=['vintage', 'variable'], ascending=[True, True])

x_ticks = score_data['vintage'].unique().tolist()  # 모든 vintage 값

# X축 범위 설정
x_min = score_data['vintage'].min()  # X축 최솟값
x_max = score_data['vintage'].max()  # X축 최댓값

y_min = score_data['value'].min()-3  # X축 최솟값
y_max = score_data['value'].max()+3 # X축 최댓값

# 그래프 그리기
st.subheader('평론가 점수 예측 결과')
score_chart = alt.Chart(score_data).mark_line().encode(
    x=alt.X('vintage', scale=alt.Scale(domain=[x_min, x_max])),  # X축 범위 설정
    y=alt.Y('value', scale=alt.Scale(domain=[y_min,y_max]),title='Score'),
    color=alt.Color('variable:N', title='Predict Score'),
).properties(
    width=600,
    height=400,
)
st.altair_chart(score_chart)

# 데이터 재구성
price_data = selected_data.melt(id_vars=['vintage'], value_vars=['predict_price', 'target_price'], var_name='variable', value_name='value')

# '-' 값을 가진 행 제외하고 점수를 오름차순으로 정렬
price_data = price_data[price_data['value'] != '-']
price_data['value'] = price_data['value'].astype(float)  # 문자열을 실수로 변환
price_data = price_data.sort_values(by=['vintage', 'variable'], ascending=[True, True])

y_min = price_data['value'].min()-10.0  # X축 최솟값
y_max = price_data['value'].max()+10.0 # X축 최댓값

# 그래프 그리기
st.subheader('가격 예측 결과')
price_chart = alt.Chart(price_data).mark_line().encode(
    x=alt.X('vintage', scale=alt.Scale(domain=[x_min, x_max])),  # X축 범위 설정
    y=alt.Y('value', scale=alt.Scale(domain=[y_min, y_max]),title='Price(USD)'),
    color=alt.Color('variable:N', title='Predict Price'),
).properties(
    width=600,
    height=400,
)
st.altair_chart(price_chart)