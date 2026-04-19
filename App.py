import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="Power Packaging Solutiuon Task", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI Article Search Manager 📈")
#st.header("This is Header")
#st.subheader("This Sub Header")
st.divider()

# 검색 기간 선택
st.subheader("검색 기간 선택")
date = st.pills("",["1주 이내","1개월 이내","3개월 이내","6개월 이내","1년 이내","1년 이상"])
st.divider()

# 검색 분야 선택
st.subheader("검색 분야 선택")
#date = st.pills("",["1주 이내","1개월 이내","3개월 이내","6개월 이내","1년 이내","1년 이상"])
st.divider()


# 버튼 생성 및 로직
