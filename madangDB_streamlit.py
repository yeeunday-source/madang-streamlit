import psycopg2 
import pandas as pd
import streamlit as st

st.title('도서 검색')
name = st.text_input('작가 이름', '한강')

if st.button('Search'):
    try:
        dbConn = psycopg2.connect(
            host='ep-calm-wildflower-b4l7kkg9-pooler.c-6.us-east-2.aws.neon.tech',
            database='neondb',
            user='neondb_owner',
            password=st.secrets['DB_PASSWORD'],
            sslmode='require',
            channel_binding='require'
        )

        sql = '''SELECT bookname, author
                 FROM Book
                  WHERE author=%s
                  ORDER BY bookid'''

        with dbConn.cursor() as cursor:
            cursor.execute(sql, (name,))
            result = pd.DataFrame(
                cursor.fetchall(),
                columns=['도서명', '작가']
            )

        dbConn.close()
        st.dataframe(result, hide_index=True)

    except psycopg2.Error as e:
        st.error(f'DB 연결 또는 조회 오류: {e}')
