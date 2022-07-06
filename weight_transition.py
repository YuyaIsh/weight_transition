import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(layout="wide")

    st.subheader("体重推移")

    df = select_daily()


    fig = go.Figure(data=[
        go.Scatter(x=df["date"],y=df["weight"]),
        go.Scatter(x=df["date"],y=df["weight_avg"])
    ])
    fig.update_layout(height=800,
                      width=1500,
                      margin={'l': 20, 'r': 60, 't': 30, 'b': 0})

    st.plotly_chart(fig)

#                          ########        ########
#                          ###    ###      ###    ###
#                          ###      ###    ###    ###
#                          ###      ###    ########
#                          ###      ###    ###    ###
#                          ###    ###      ###    ###
#                          #######         ########

#dbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdb デイリーデータ取得 dbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbddd
def select_daily():
    sql = """select date,weight from daily
    ORDER BY date DESC"""
    df = connect_db(sql)

    df_avg = select_moving_avg()
    df = pd.merge(df,df_avg)  # 平均列を結合

    return df

#dbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdb 体重移動平均取得 dbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbdbddd
def select_moving_avg():
    sql = """select * from weight_weekly_moving_avg
    ORDER BY date DESC"""
    df = connect_db(sql)

    return df

def connect_db(sql):
    dbname = "bodymake"
    user = "postgres"
    pw = "a"
    db = f"dbname={dbname} user={user} password={pw}"

    # SELECT文ならデータ取得しdf化
    if sql[:6] == "select":
        with psycopg2.connect(db) as conn: # ローカル
            with conn.cursor() as cur:
                cur.execute(sql)
                data = list(cur.fetchall())  # 一行1タプルとしてリスト化
                colnames = [col.name for col in cur.description]  # 列名をリストで取得
        df = pd.DataFrame(data,columns=colnames)  # データをデータフレーム化
        return df
    # SELECT文以外なら実行のみ
    else:
        with psycopg2.connect(db) as conn: # ローカル
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()

main()