import psycopg2
import pandas as pd
import streamlit as st

st.title('DB 연동')
name = st.text_input('고객 이름', '박지성')

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

        sql = '''SELECT o.orderid, c.name, b.bookname, o.saleprice, o.orderdate
                 FROM Customer c, Orders o, Book b
                 WHERE c.name=%s AND c.custid=o.custid AND b.bookid=o.bookid
                 ORDER BY o.orderid'''

        with dbConn.cursor() as cursor:
            cursor.execute(sql, (name,))
            result = pd.DataFrame(
                cursor.fetchall(),
                columns=['orderid', 'name', 'bookname', 'saleprice', 'orderdate']
            )

        dbConn.close()
        st.dataframe(result, hide_index=True)

    except psycopg2.Error as e:
        st.error(f'DB 연결 또는 조회 오류: {e}')