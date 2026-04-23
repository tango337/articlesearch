import streamlit as st
import google.generativeai as genai
import re
from urllib.parse import quote

# 페이지 기본 설정
st.set_page_config(
    page_title="AI Market Manager", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 - 설정
with st.sidebar:
    st.header("🎨 테마 설정")
    bg_color = st.color_picker("배경색 선택", "#FFC0CB") # 기본값 핑크
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
        }}
        </style>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.header("⚙️ AI 설정")
    gemini_api_key = st.text_input("Gemini API Key", type="password", help="Google AI Studio에서 발급받은 API 키를 입력하세요.")
    st.divider()
    st.info("API 키가 있으면 제미나이가 검색을 도와줍니다.")

st.title("AI Article Search Manager 📈")
st.divider()

# 검색 키워드 선택
st.subheader("검색 키워드 입력")
search_keywords = st.text_input("검색할 키워드를 입력하세요", placeholder="예: HBM, 전력 모듈, ESS")
st.divider()

# 검색 분야 선택
st.subheader("검색 분야 선택")
col1, col2, col3 = st.columns(3)
with col1:
    search_Fields_Company = st.pills("제조사",["LG전자","삼성전자","LS","SK하이닉스","한화","NVIDIA"], selection_mode="multi")
with col2:
    search_Fields_Tech = st.pills("기술분야",["AI","Power","Memory","ESS","PCS","Power Module","Data Center","Space"], selection_mode="multi")
with col3:
    search_Fields_Media = st.pills("검색 미디어",["조선일보","매일경제","네이버","블룸버그","로이터"], selection_mode="multi")

search_date = st.pills("검색 기간",["1주","1개월","3개월","6개월","1년이내","전체"])
st.divider()

# 선택된 항목들을 합쳐서 검색어 생성
combined_query = search_keywords
if search_Fields_Company:
    combined_query += " " + " ".join(search_Fields_Company)
if search_Fields_Tech:
    combined_query += " " + " ".join(search_Fields_Tech)
if search_Fields_Media:
    combined_query += " " + " ".join(search_Fields_Media)
combined_query = combined_query.strip()

# 구글 기간 설정 파라미터 매핑
date_mapping = {"1주": "w", "1개월": "m", "3개월": "m3", "6개월": "m6", "1년이내": "y"}
tbs_param = f"&tbs=qdr:{date_mapping[search_date]}" if search_date in date_mapping else ""

# 버튼 및 AI 로직
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("일반 구글 검색", use_container_width=True):
        if combined_query:
            # 안전하게 URL 인코딩 처리
            search_url = f"https://www.google.com/search?q={quote(combined_query)}{tbs_param}"
            st.components.v1.html(f"<script>window.open('{search_url}', '_blank');</script>", height=0)
        else:
            st.warning("검색어를 입력해주세요.")

with col_btn2:
    if st.button("🚀 제미나이 AI 검색 (URL 생성)", use_container_width=True):
        if not gemini_api_key:
            st.error("사이드바에 Gemini API Key를 입력해주세요.")
        elif not combined_query:
            st.warning("검색 항목을 하나 이상 선택하거나 키워드를 입력해주세요.")
        else:
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 리스트 항목을 쉼표로 연결된 문자열로 변환
                fields_company_str = ", ".join(search_Fields_Company) if search_Fields_Company else "없음"
                fields_tech_str = ", ".join(search_Fields_Tech) if search_Fields_Tech else "없음"
                fields_media_str = ", ".join(search_Fields_Media) if search_Fields_Media else "없음"
                
                prompt = f"""사용자가 다음 정보를 바탕으로 관련 기사를 찾고 싶어 합니다. 
                이 모든 조건을 만족하며 가장 정확한 최신 기사를 찾을 수 있는 '구글 검색 URL' 하나만 생성해서 답변해주세요. 
                반드시 'https://'로 시작하는 URL 하나만 출력하고, 다른 설명은 하지 마세요.
                
                - 기본 검색어: {search_keywords if search_keywords else "없음"}
                - 관련 기업: {fields_company_str}
                - 기술 분야: {fields_tech_str}
                - 선호 매체: {fields_media_str}
                - 기간 필터: {search_date if search_date else "전체"}
                """
                
                with st.spinner("제미나이가 최적의 검색 경로를 생성 중입니다..."):
                    response = model.generate_content(prompt)
                    ai_response = response.text.strip()
                
                # 정규표현식으로 URL만 추출 (import re는 상단에 있음)
                url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
                urls = re.findall(url_pattern, ai_response)
                
                if urls:
                    clean_url = urls[0].replace('`', '').replace(')', '').strip()
                    st.session_state.ai_url = clean_url
                    st.success("제미나이가 최적의 검색 URL을 생성했습니다!")
                else:
                    st.error(f"제미나이가 유효한 URL을 생성하지 못했습니다. 응답 내용: {ai_response[:100]}...")
            except Exception as e:
                if "404" in str(e):
                    st.error("모델을 찾을 수 없습니다. API 키 설정 또는 모델명을 확인해주세요.")
                else:
                    st.error(f"API 호출 중 오류 발생: {str(e)}")


st.divider()

# 결과 표시 섹션
st.subheader("검색 결과 확인")
if combined_query:
    st.info(f"현재 선택된 검색어: **{combined_query}**")
    
if "ai_url" in st.session_state:
    st.markdown(f"### 🤖 제미나이 추천 URL")
    st.code(st.session_state.ai_url)
    st.link_button("AI 추천 검색 결과 열기", st.session_state.ai_url, type="primary")

st.divider()
st.caption("Google AI Studio에서 무료 API 키를 발급받아 사용할 수 있습니다.")





