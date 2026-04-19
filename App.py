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

# 검색 키워드 선택
st.subheader("검색 키워드 입력")
search_keywords = st.text_input("검색할 키워드를 입력하세요", placeholder="예: HBM, 전력 모듈, ESS")
st.divider()

# 검색 분야 선택
st.subheader("검색 분야 선택")
search_Fields_Company = st.pills("제조사",["LG전자","삼성전자","LS","SK하이닉스","한화","NVIDIA"], selection_mode="multi")
search_Fields_Tech = st.pills("기술분야",["AI","Power","Memory","ESS","PCS","Power Module","Data Center","Space"], selection_mode="multi")
search_Fields_Media = st.pills("검색 미디어",["조선일보","매일경제","네이버","ESS","PCS","Power Module","Data Center","Space"], selection_mode="multi")
st.divider()

## 검색 키워드 추가
#st.subheader("검색 키워드 추가. (콤마로 구분)")
#date = st.pills("",["1주 이내","1개월 이내","3개월 이내","6개월 이내","1년 이내","1년 이상"])
#st.divider()

# 버튼 생성 및 로직
st.button("검색 실행")

st.divider()

# 검색 결과 링크 생성
st.subheader("검색 결과 확인")
if search_keywords:
    # 네이버 검색 URL 생성
    search_url = f"https://search.naver.com/search.naver?query={search_keywords.replace(' ', '+')}"
    st.success(f"'{search_keywords}'에 대한 네이버 검색 준비가 되었습니다.")
    st.link_button("네이버에서 검색 결과 보기", search_url)
else:
    st.info("키워드를 입력하면 네이버 검색 링크가 생성됩니다.")

