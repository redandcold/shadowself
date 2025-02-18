import streamlit as st
import os
import json

pages_dir = "pages"

if os.path.exists(pages_dir):
    pages = [
        file.replace(".py", "").replace("_", " ").title()
        for file in os.listdir(pages_dir)
        if file.endswith(".py")
    ]
    print("등록된 페이지들:", pages)
else:
    print("`pages/` 디렉토리를 찾을 수 없습니다.")

# List of pages
pages = {
    "🎡 choose the page": None,
    "🏠 home": "home.py",
}

# Dropdown to select the page
selected_page = st.selectbox("Select a page:", list(pages.keys()))

    # 페이지 이동 처리
if pages[selected_page]:  # 선택된 페이지가 None이 아닐 경우
    st.switch_page(pages[selected_page])  # switch_page로 이동

# 사용자 데이터베이스 JSON 파일 경로
USER_DATA_FILE = "user_data.json"
# 사용자 데이터베이스(간단히 딕셔너리로 구현)
user_db = []
# 사용자 데이터를 JSON 파일에서 불러오는 함수
def load_user_data_from_json(file_path=USER_DATA_FILE):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 사용자 데이터베이스 초기화
user_db = load_user_data_from_json()
print("="*30)
# print("user DB :", user_db)
print("="*30)
# 로그인 상태 관리
def authenticate(email, password):
    # user_db가 리스트인지 확인
    if isinstance(user_db, list):
        # 리스트에서 이메일이 일치하는 사용자 검색
        for user in user_db:
            if user["email"] == email and user["password"] == password:
                return user['name'], True
            else:
                st.error("이메일 또는 비밀번호가 잘못되었습니다.")
                print("user_data에 입력한 데이터가 없는경우")
    return False

# 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# 메인 페이지: 로그인과 회원가입 분리
if st.session_state["page"] == "login":
    st.title("로그인")

    login_tab, signup_tab = st.tabs(["로그인", "회원가입"])

    with login_tab:
        email = st.text_input("이메일", key="login_email")
        password = st.text_input("비밀번호", type="password", key="login_password")
        if st.button("로그인"):
            name, logged=authenticate(email, password)
            print("login 성공한 유저 이름:",name)
            if logged:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.session_state['name'] = name
                st.success("로그인 성공!")
                st.switch_page("home.py")
                
            else:
                st.error("이메일 또는 비밀번호가 잘못되었습니다.")

    with signup_tab:
        new_email = st.text_input("이메일", key="signup_email")
        if new_email:
            if any(user["email"] == new_email for user in user_db):  # 리스트 내부에서 이메일 중복 체크
                st.error("이미 존재하는 이메일입니다.")
            else:
                st.success("사용 가능한 이메일입니다.")

        new_password = st.text_input("비밀번호", type="password", key="signup_password")
        confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
        if new_password and confirm_password:
            if new_password == confirm_password:
                st.success("비밀번호가 일치합니다.")
            else:
                st.error("비밀번호가 일치하지 않습니다.")
        new_name = st.text_input("이름", key="signup_name")

        if st.button("다음"):
            if new_email and new_password and confirm_password and new_name:
                if any(user["email"] == new_email for user in user_db):  # 리스트 내부에서 이메일 중복 체크
                    st.error("이미 존재하는 이메일입니다.")
                elif new_password != confirm_password:
                    st.error("비밀번호가 일치하지 않습니다.")
                else:
                    st.session_state["page"] = "chat_session"
                    st.session_state["password"]=new_password
                    st.session_state['email']=new_email
                    st.session_state['name']=new_name
                    print(new_password, new_email, new_name)
                    st.switch_page("pages/chat_session.py")
            else:
                st.error("모든 필드를 입력해주세요.")

elif st.session_state["page"] == "chat_session":
    st.switch_page("pages/chat_session.py")   

