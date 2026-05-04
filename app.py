import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="이미지 테스트", layout="centered")

st.title("📸 성심당 이미지 출력 테스트")

# 사용자님이 주신 마라미 고로케 주소
test_img_url = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FcnkONT%2FdJMcagekYkG%2FAAAAAAAAAAAAAAAAAAAAAOWcdHU52pYaOEaghnyOWE7a-HYlZchEEKlNFGyTpiBm%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1780239599%26allow_ip%3D%26allow_referer%3D%26signature%3DTWE0nI1OVhBOGA4PoJi2himNkuY%253D"

st.subheader("1. Streamlit 전용 함수로 출력")
st.image(test_img_url, caption="마라미 고로케 (st.image)", use_container_width=True)

st.divider()

st.subheader("2. HTML 태그로 출력")
st.markdown(f'<img src="{test_img_url}" width="100%">', unsafe_allow_html=True)
