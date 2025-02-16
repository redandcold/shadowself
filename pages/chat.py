import os
import json
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


# List of pages
pages = {
    "🎡 choose the page": None,
    "🏠 home": "home.py",
    "🔎 search people" : "pages/people_list.py",
    "🧑👧 friends": "./pages/friends_list.py",
    "🚧 logout": "pages/logout.py",
}

# Dropdown to select the page
selected_page = st.selectbox("Select a page:", list(pages.keys()))

    # 페이지 이동 처리
if pages[selected_page]:  # 선택된 페이지가 None이 아닐 경우
    st.session_state.friend_chat_history = []
    st.switch_page(pages[selected_page])  # switch_page로 이동

# 사용자 데이터베이스 JSON 파일 경로
USER_DATA_FILE = "user_data.json"
def load_user_data_from_json(file_path=USER_DATA_FILE):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

selected_person_name=st.session_state["selected_person_name"]
selected_person_email=st.session_state["selected_person_email"]
print(f"현재 선택한 사람 메일: {selected_person_email}")
user_chat_history={}
user_db=load_user_data_from_json(file_path=USER_DATA_FILE)
for user in user_db:
    if user["email"] == selected_person_email:
        user_chat_history=user["chat_history"]
    else:
        print(f"해당 유저를 찾지 못했습니다.")
# .env 파일 로드
load_dotenv()
default_openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI LLM 초기화
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# user_chat_history에서 'role': 'system'인 항목을 제거
filtered_history = [entry for entry in user_chat_history if entry['role'] != 'system']

# 결과 출력
print("filtered_history", filtered_history)

# 프롬프트 정의
initial_prompt = SystemMessage(content=f"""
You are an AI conversational assistant tasked with perfectly mirroring the User's tone, style, and interests as demonstrated in the example below. Your primary goal is to craft responses that closely replicate the User's tone and word choice, ensuring the use of key phrases, terms, and expressions found in the User's dialogue (role: "user"). If the User introduces a topic that does not align with the example, you must infer an appropriate response while maintaining the overall tone and style.

Key Instructions:
1. Tone and Style
   - replicate the User’s tone, speech patterns, and phrasing as shown in the example's User dialogue (role: "user").
   - Use the same key terms, vivid expressions, and sentence structure as demonstrated in the User's dialogue.
   - Avoid overgeneralizing or neutralizing your tone. Responses must feel intense, dramatic, or symbolic to match the example.

2. Contextual Engagement
   - Respond directly to the User’s input by using the style and vocabulary from the example dialogues.
   - If the User introduces a question or topic that completely deviates from the example, infer an appropriate response while maintaining the tone, structure, and word choice that align with the example dialogue.
   - For unfamiliar topics, adapt the response creatively to preserve the example tone and ensure logical flow.

3. Exact Replication with Flexibility for New Topics
   - For topics aligned with the example dialogue, prioritize replicating the User’s expressions, tone, and structure precisely.
   - When new or unexpected topics arise, answer them flexibly while ensuring stylistic consistency with the User's tone and speech patterns.

4. Relevance and Creativity
   - Ensure responses remain relevant to the User's input and are anchored in the example style and tone.
   - Avoid repetitive phrases by varying wording while staying consistent with the User's dialogue mannerisms.

5. Natural Dialogue Flow
   - Maintain logical flow in the conversation, ensuring transitions between topics are seamless and stylistically coherent.
   - Even when inferring answers for unfamiliar topics, responses must feel natural and aligned with the User’s tone and mannerisms.

6. Termination and Boundaries
   - If the User explicitly asks you to stop, immediately end the conversation in Korean without further prompts.
   - Once the conversation is complete, naturally conclude with the following phrase:
     "감사합니다. 고객님과의 대화가 즐거웠습니다. 좋은 하루 보내세요!"

### Starting the Conversation
Begin the conversation by asking the User what they want to discuss, using the tone and style of the User dialogue (role: "user") in the example provided. For instance:
"대화를 시작해보세요. (예시: 언어 공부의 이유, 최근 관심사, 스트레스 푸는 법 등)"

### Example Interaction:
{filtered_history}

Emphasis:
Your task is to prioritize the User's tone, expressions, and style in every response, mirroring the example dialogue provided. Use the specific language, structure, and emotional intensity found in the User’s input as your primary guide. For topics that deviate from the example, infer a response while maintaining stylistic consistency.
""")

# Streamlit 상태 초기화
if "friend_chat_history" not in st.session_state:
    st.session_state.friend_chat_history = []
    

if "friend_conversation_done" not in st.session_state:
    st.session_state.friend_conversation_done = False

# 메시지 추가 함수
def add_message(role, content):
    """role: 'user' 또는 'assistant'"""
    st.session_state.friend_chat_history.append({"role": role, "content": content})

# 대화 기록을 JSON 파일로 저장하는 함수
def save_chat_history_to_json(file_path="friend_chat_history.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(st.session_state.friend_chat_history, f, ensure_ascii=False, indent=4)

# Streamlit UI 구성
st.title(f"💬 {selected_person_name}님께 말을 걸어보세요.")
st.caption("🚀 총 5번 발화할 수 있습니다.")


# 초기 메시지 처리
if not st.session_state.friend_chat_history:
    add_message("system", initial_prompt.content)
    try:
        # 초기 메시지에 대한 LLM 응답 생성
        llm_response = llm([SystemMessage(content=initial_prompt.content)])
        add_message("assistant", llm_response.content)
    except Exception as e:
        add_message("assistant", f"오류가 발생했습니다: {e}")

# 기존 메시지 렌더링
for msg in st.session_state.friend_chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# 사용자 입력을 세션 상태에 저장
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if not st.session_state.friend_conversation_done:  # 대화 종료 상태가 아닐 때만 입력 허용
    # 사용자 입력 처리
    if user_input := st.chat_input("메시지를 입력하세요:", max_chars=300 ):
        add_message("user", user_input)
        st.chat_message("user").write(user_input)

        try:
            # 대화 내역을 기반으로 메시지 생성
            messages = [
                SystemMessage(content=initial_prompt.content)
            ] + [
                HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
                for msg in st.session_state.friend_chat_history if msg["role"] != "system"
            ]

            # LLM 호출
            llm_response = llm(messages)
            response_content = llm_response.content

            # 모델 응답 추가
            add_message("assistant", response_content)
            st.chat_message("assistant").write(response_content)

            if "user_input_count" not in st.session_state:
                st.session_state.user_input_count=1
                print("input_count: ",st.session_state.user_input_count)
            else:
                st.session_state.user_input_count+=1
                print("input_count: ",st.session_state.user_input_count)

            # 대화 종료 메시지 확인
            if "즐거웠습니다" in response_content:
                st.session_state.friend_conversation_done = True
            if st.session_state.user_input_count>=5:
                st.session_state.friend_conversation_done = True
                st.info("5회의 크레딧을 모두 사용하였습니다")
            save_chat_history_to_json()
            print("대화 기록이 friend_chat_history.json 파일로 저장되었습니다.")


        except Exception as e:
            response_content = f"오류가 발생했습니다: {e}"
            add_message("assistant", response_content)
            st.chat_message("assistant").write(response_content)

# 디버깅: 상태 출력
print("=======회원가입 최종 대화 기록 =======")
for message in st.session_state.friend_chat_history:
    print(f"{message['role']}: {message['content']}")
print("=========================")

user_data_path="user_data.json"
# 대화 종료 후 회원가입 완료 버튼 표시
if st.session_state.friend_conversation_done:
    
    st.success("대화가 종료되었습니다. 친구 목록에 추가하시겠습니까?")
    if st.button("친구 추가"):
        # 파일 읽기
        with open(user_data_path, "r") as file:
            user_data = json.load(file)

        # 이메일과 일치하는 사용자 찾기
        for user in user_data:
                # 선택된 친구 추가
            if "friends" not in user:
                user["friends"] = {}  # friends 키가 없으면 딕셔너리로 생성

            selected_person_email = st.session_state.get("selected_person_email")
            selected_person_name = st.session_state.get("selected_person_name")

            # 친구 추가 조건 확인
            if selected_person_email and selected_person_email not in user["friends"]:
                user["friends"][selected_person_email] = selected_person_name


        # 파일 저장
        with open(user_data_path, "w") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)

        print(f"{selected_person_name}님이 친구 목록에 추가되었습니다.")
        st.session_state.friend_conversation_done=False
        st.session_state.friend_chat_history = []
        st.session_state.user_input_count=0
        st.switch_page("pages/friends_list.py")
    if st.button("목록 돌아가기"):
        st.session_state.friend_chat_history = []
        st.session_state.friend_conversation_done=False
        st.session_state.user_input_count=0
        st.switch_page("pages/people_list.py")
