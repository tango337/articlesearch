import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="Market Manager", 
    page_icon="📊",
    layout = "wide")

st.title("Market Manager 📈")
st.header("This is Header")
st.subheader("This Sub Header")

# 버튼 생성 및 로직
if st.button("클릭하세요"):
    st.success("버튼이 클릭되었습니다! 🎉")
else:
    st.info("버튼을 눌러보세요.")
