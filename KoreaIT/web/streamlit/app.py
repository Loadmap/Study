import streamlit as st
import requests
import pandas as pd

st.title('광고 문구를 생성해주는 서비스앱')
url = 'http://127.0.0.1:8000/create_ad'

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고문구의 느낌',['기본', '재밌게', '차분하게', '과장스럽게', '참신하게',
                                     '고급스럽게', '센스있게', '아름답게'], default = ['기본'])

if st.button('광고 문구 생성하기') :
    try :
        response = requests.post(url,
                                 json = {
                                     "product_name" : product_name,
                                     "details" : details,
                                     "tone_and_manner" : ", ".join(options)
                                 })

        ad = response.json()['ad']
        datas = response.json()['datas']
        st.success(ad)

        st.subheader("Stored Data")
        st.table(datas)

    except :
        st.error('연결 실패!')