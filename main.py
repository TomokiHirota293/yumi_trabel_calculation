import pandas as pd
import requests
import io
import streamlit as st

# 公開GoogleスプレッドシートのURL
sheet_id = '18wjkutmcPoYYfGKD1bz7Cd_VBxlwpQlwFXvjvvx-Rco'
spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'

# CSVデータの取得
response = requests.get(spreadsheet_url)
assert response.status_code == 200, 'Wrong status code'
data = response.content.decode('utf-8')

# データフレームの作成
gsheet = pd.read_csv(io.StringIO(data))
gsheet['一人当たり(自動入力)'] = gsheet['一人当たり(自動入力)'].replace({'¥': '', ',': '', '\.00': ''}, regex=True)
gsheet['一人当たり(自動入力)'] = pd.to_numeric(gsheet['一人当たり(自動入力)'], errors='coerce')


# 計算
def cal_from_to(gsheet,from_name,to_name):
    payment = gsheet[(gsheet['立替人']==to_name) & (gsheet[from_name]==1)]
    return payment['一人当たり(自動入力)'].sum()
    
# 表示するデータフレームの作成
names = ['亀井', '機田', '田中', '廣田', '中田', '中村','前中']

show_df = pd.DataFrame(columns=names, index=names)

for from_name in names:
    for to_name in names:
        show_df[to_name].loc[from_name] = cal_from_to(gsheet,from_name,to_name)


# Streamlitでデータを表示
st.markdown(
    '''
    # 2023年ゆみの会男子旅行立替等料金計算表
    https://docs.google.com/spreadsheets/d/18wjkutmcPoYYfGKD1bz7Cd_VBxlwpQlwFXvjvvx-Rco/edit#gid=0　
    このスプレッドシートに記載されたデータから，誰が誰にいくら払うべきかを算出します．
    ## 表の見方
    行(横列)の人が縦列の人に支払いをする必要があります．
    '''
            )
st.dataframe(show_df)

