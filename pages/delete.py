import streamlit as st
import json

# JSON 파일 로드
file_path = "user_data.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    # 이메일이 겹치지 않는 데이터만 필터링
    filtered_user_data = [user for user in user_data if user["email"] != st.session_state["email"]]

    # JSON 파일 다시 저장
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(filtered_user_data, f, ensure_ascii=False, indent=4)

    print("이메일 삭제 완료.")

except Exception as e:
    print(f"오류 발생: {e}")