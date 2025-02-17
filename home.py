import streamlit as st
import base64

# 로컬 MP4 파일 경로 설정
video_path = "./data/shadowself_background.mp4"

# MP4 비디오 파일을 Base64로 인코딩하는 함수
def video_to_base64(video_path):
    with open(video_path, "rb") as file_:
        video_contents = file_.read()
        video_base64 = base64.b64encode(video_contents).decode("utf-8")
    return video_base64

# Base64로 인코딩된 비디오 데이터 가져오기
video_base64 = video_to_base64(video_path)

# HTML 및 CSS 코드
video_html = f"""
    <style>
    #myVideo {{
      position: fixed;
      top: 50%;   /* 화면의 세로 중앙에 위치 */
      left: 50%;  /* 화면의 가로 중앙에 위치 */
      transform: translate(-50%, -50%);  /* 정확히 중앙에 맞추기 */
      min-width: 100%;
      min-height: 100%;
    }}
    </style>  
    <video autoplay muted loop id="myVideo">
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      Your browser does not support HTML5 video.
    </video>
"""


# HTML 마크업 렌더링
st.markdown(video_html, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>Shadow Self👥</h1>", unsafe_allow_html=True)

# "Get Started" 버튼을 Streamlit 기본 버튼으로 추가
# CSS 스타일 적용
st.markdown(
    """
    <style>
    button[data-testid="stBaseButton-secondary"] {
        position: fixed;           /* 버튼을 화면에 고정 */
        bottom: 140px;              /* 화면 하단에서 위 */
        right: 55px;               /* 화면 오른쪽에서 20px 왼쪽 */
        background-color: #003366; /* 버튼 배경색 */
        color: white;              /* 텍스트 색상 */
        font-size: 100px;           /* 글자 크기 */
        padding: 35px 55px;        /* 버튼 크기 (패딩) */
        border: none;              /* 테두리 제거 */
        border-radius: 10px;       /* 둥근 모서리 */
        cursor: pointer;           /* 마우스 커서 */
        z-index: 10;               /* 다른 요소 위에 표시 */
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #002244; /* 호버 시 배경색 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# 로그인 상태 확인
if not st.session_state["logged_in"]:
    
  # Streamlit 버튼으로 페이지 이동 처리
  if st.button("Get Started"):
      st.switch_page("pages/login.py")
else:
   # CSS를 사용해 텍스트를 오른쪽으로 정렬
    st.markdown(
        f"""
        <style>
        .welcome-message {{
        position: fixed; /* 화면에 고정된 위치로 설정 */
        top: 140px; /* 화면 상단에서 80px 아래 */
        right: 80px; /* 화면 오른쪽에서 80px 왼쪽 */
        color: white; /* 텍스트 색상 */
        font-size: 20px; /* 글자 크기 */
        background-color: rgba(0, 0, 0, 0.3); /* 배경색 (투명도 50%) */
        padding: 10px; /* 텍스트 주변 여백 */
        border-radius: 5px; /* 모서리 둥글게 */
        }}
        </style>
        <div class="welcome-message">
            {st.session_state["name"]}님 환영합니다!
        </div>
        """,
        unsafe_allow_html=True,
    )

    # List of pages
    pages = {
        "🎡 choose the page": None,
        "🔎 search people": "./pages/people_list.py",
        "🧑👧 friends": "./pages/friends_list.py",
        "🚧 logout": "pages/logout.py",
        "🗑 delete account":"pages/delete.py"
    }

    # Dropdown to select the page
    selected_page = st.selectbox("Select a page:", list(pages.keys()))
    
     # 페이지 이동 처리
    if pages[selected_page]:  # 선택된 페이지가 None이 아닐 경우
        st.switch_page(pages[selected_page])  # switch_page로 이동