import streamlit as st

st.set_page_config( #페이지 설정
 page_title="하교수의 Streamlit", #페이지 Tab의 타이틀
 page_icon="", #페이지 Tab의 아이콘
 layout="wide", #페이지 레이아웃: centered, wide
 #사이드바 초기 상태 : auto, collapsed, expanded
 initial_sidebar_state="expanded",
 #페이지 오른쪽 상부의 메뉴에 추가할 메뉴 항목: Get help, Report a bug, About
 menu_items={
  'Get help': "https://docs.streamlit.io", # URL만
  'Report a bug': "https://streamlit.io", #URL만
  'About': "## 하정훈 교수 \n -[https://ie.hongik.ac.kr/ie/0201.do?mode=view&deptCd=AAB530&S1=2006&S2=10077]"
 }
)
