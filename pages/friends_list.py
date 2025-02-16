import streamlit as st
import json

st.title("🧑👧 친구 목록 게시판")

# List of pages
pages = {
    "🎡 choose the page": None,
    "🏠 home": "home.py",
    "🔎 search people": "./pages/people_list.py",
    "🚧 logout": "pages/logout.py",
}

# Dropdown to select the page
selected_page = st.selectbox("Select a page:", list(pages.keys()))

    # 페이지 이동 처리
if pages[selected_page]:  # 선택된 페이지가 None이 아닐 경우
    st.switch_page(pages[selected_page])  # switch_page로 이동


# 사용자 데이터 로딩
with open("user_data.json", "r", encoding="utf-8") as file:
    users = json.load(file)

# 현재 사용자의 이메일
current_user_email = st.session_state.get("email")

# 현재 사용자 데이터 찾기
current_user = None
for user in users:
    if user["email"] == current_user_email:
        current_user = user
        break

# 친구 목록 가져오기
if current_user and "friends" in current_user:
    friends = current_user["friends"]  # friends는 딕셔너리로 저장됨 (email: name)
else:
    friends = {}

# 친구 목록이 없을 경우 메시지 표시
if not friends:
    st.info("친구 목록이 비어 있습니다. 사람 목록에서 친구를 추가해보세요!")
else:
    # 친구 목록 출력
    for idx, (friend_email, friend_name) in enumerate(friends.items()):
        st.subheader(friend_name)  # 친구 이름 표시
        print(friend_email, friend_name)
        col1, col2, col3 = st.columns(3)

        with col1:
            # 대화하기 버튼
            if st.button(f"💬 대화하기", key=f"chat_{friend_email}"):
                st.session_state["selected_person_name"] = friend_name
                st.session_state["selected_person_email"] = friend_email
                st.switch_page("pages/chat.py")

        with col2:
            # 프로필 보기 버튼
            friend_data = next((user for user in users if user["email"] == friend_email), None)
            if friend_data:
                if st.button(f"📖 프로필 보기", key=f"profile_{friend_email}"):
                    st.info(f"**자기소개:** {friend_data.get('bio', '자기소개가 없습니다.')}")

        with col3:
            # 친구 삭제 버튼
            if st.session_state.get(f"confirm_delete_{friend_email}") == "pending":
                # 확인 버튼 및 취소 버튼 표시
                st.warning(f"정말로 {friend_name}님을\n삭제하시겠습니까?")
                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button("확인", key=f"confirm_{friend_email}"):
                        del friends[friend_email]  # 딕셔너리에서 친구 삭제

                        # 사용자 데이터 파일 업데이트
                        with open("user_data.json", "w", encoding="utf-8") as file:
                            json.dump(users, file, ensure_ascii=False, indent=4)

                        st.success(f"{friend_name}님이 친구 목록에서 삭제되었습니다.")
                        st.rerun()

                with cancel_col:
                    if st.button("취소", key=f"cancel_{friend_email}"):
                        st.session_state[f"confirm_delete_{friend_email}"] = None
                        st.info("삭제가 취소되었습니다.")
            else:
                if st.button(f"❌ 친구 삭제", key=f"delete_{friend_email}"):
                    st.session_state[f"confirm_delete_{friend_email}"] = "pending"


        # 연한 실선 추가 (HTML 사용)
        st.markdown(
            """
            <hr style="border: 1px solid #ddd; margin: 10px 0;">
            """,
            unsafe_allow_html=True,
        )
