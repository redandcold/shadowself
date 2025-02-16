import os
import json
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# .env 파일 로드
load_dotenv()
default_openai_api_key = os.getenv("OPENAI_API_KEY")


# OpenAI LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 프롬프트 정의
initial_prompt = SystemMessage(content="""
You are a chatbot that asks the user four main questions, one at a time, and does not proceed to the next question until the current one is fully addressed or skipped.  
You may ask up to 2 follow-up questions for clarification or more detail after the user's response to each main question. Once 2 follow-ups are reached, automatically proceed to the next main question, even if the user continues elaborating. Before moving to the next question, always provide a brief response acknowledging or reacting to the user’s previous answer.

Rules:  
1. Strictly limit follow-up questions to a maximum of 2 per main question.  
2. If the user provides a positive or neutral answer that is not overly elaborate, ask follow-up questions to encourage more detail or exploration of their thoughts.  
3. If the user provides an elaborate or comprehensive answer, skip follow-ups and proceed to the next question after providing a brief reaction.  
4. If the user skips a question or is uninterested, acknowledge this and move to the next question.  
5. All responses must be in Korean.  
6. Always provide a brief reaction (e.g., appreciation, empathy, or encouragement) to the user's answer before moving to the next question.  
7. After all four main questions are asked, conclude the conversation with a polite remark in Korean.  

Introduction:  
At the start of the conversation, introduce the purpose with:  
"마지막으로 고객님을 조금 더 알아보고 싶어 몇 가지 질문을 드릴게요."  

Main Questions:  
1. 새로운 언어를 배우려는 동기는 무엇인가요? 예를 들어, 여행, 직장, 개인적인 성장 등 어떤 이유가 있으신가요?  
2. 현재 관심 있는 취미나 활동이 있으신가요? 여가 시간에 주로 무엇을 하시나요?  
3. 중요하게 생각하는 개인적인 가치나 목표가 있으신가요? 예를 들어, 가족, 커리어, 자기 개발 등 어떤 것들이 있나요?  
4. 보통 스트레스를 어떻게 관리하시나요? 휴식, 운동, 취미 활동 등 어떤 방법을 사용하시나요?  

Follow-up Question Guidelines:  
1. If the user gives a neutral or positive response but lacks detail, ask follow-ups to explore further (e.g., "그럼 구체적으로 어떤 활동을 해보고 싶으세요?" or "그 이유를 좀 더 들려주실 수 있나요?").  
2. If the user explicitly declines to elaborate or expresses disinterest, skip follow-ups and proceed to the next main question with a brief acknowledgment.  
3. Ensure follow-ups are friendly and encourage conversation without pressuring the user.  

Termination:  
If the user explicitly asks to stop, politely end the conversation in Korean.

Closing the Conversation:  
After all four main questions (and optional follow-ups) have been asked, conclude the conversation with:  
"감사합니다. 고객님과의 대화가 즐거웠습니다. 좋은 하루 보내세요!"
""")

# Streamlit 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation_done" not in st.session_state:
    st.session_state.conversation_done = False

if ("email" and "password" and "name") not in st.session_state:
    print("chat_session:  user_data가 없습니다!")
else:
    print('====================user_info=======================')
    print(f"{st.session_state.get("email")}, {st.session_state.get("name"), st.session_state.get("password")}")


# 메시지 추가 함수
def add_message(role, content):
    """role: 'user' 또는 'assistant'"""
    st.session_state.chat_history.append({"role": role, "content": content})

# 대화 기록을 JSON 파일로 저장하는 함수
def save_chat_history_to_json(file_path="chat_history.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=4)

# 고객 정보를 JSON 파일로 저장하는 함수 (기존 데이터에 추가)
def save_user_data_to_json(new_user_data, file_path="user_data.json"):
    # 기존 데이터 로드
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    else:
        user_data = []

    # 새로운 데이터를 리스트에 추가
    user_data.append(new_user_data)

    # 업데이트된 데이터를 다시 파일에 저장
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

# Streamlit UI 구성
st.title("💬 사용자의 이야기를 들려주세요.")
st.caption("🚀 회원가입까지 다른 한 걸음. 8번 발화할 수 있습니다.")

# Sidebar에서 API Key 입력
with st.sidebar:
    # JSON 저장 버튼 추가
    # if st.button("💾 대화 기록 저장"):
    #     save_chat_history_to_json()
    #     st.success("대화 기록이 chat_history.json 파일로 저장되었습니다.")
    # user_api_key = st.text_input("OpenAI API Key", value=default_openai_api_key or "", type="password")
    # if not user_api_key:
    #     st.info("OpenAI API Key를 입력하거나 .env 파일에 설정하세요.")
    if st.button("home"):
        st.session_state.clear()
        st.switch_page("home.py")

# 초기 메시지 처리
if not st.session_state.chat_history:
    add_message("system", initial_prompt.content)
    try:
        # 초기 메시지에 대한 LLM 응답 생성
        llm_response = llm([SystemMessage(content=initial_prompt.content)])
        add_message("assistant", llm_response.content)
    except Exception as e:
        add_message("assistant", f"오류가 발생했습니다: {e}")

# 기존 메시지 렌더링
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

if st.session_state.conversation_done==False:
    # 사용자 입력 처리
    if user_input := st.chat_input("메시지를 입력하세요:"):

        if len(user_input) > 300:
            st.warning(f"🚨 입력은 최대 한글 300자까지 가능합니다. {len(user_input)}/300")
            user_input = user_input[:300]
        else:    
            add_message("user", user_input)
            st.chat_message("user").write(user_input)

            try:
                # 대화 내역을 기반으로 메시지 생성
                messages = [
                    SystemMessage(content=initial_prompt.content)
                ] + [
                    HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
                    for msg in st.session_state.chat_history if msg["role"] != "system"
                ]

                # LLM 호출
                llm_response = llm(messages)
                response_content = llm_response.content

                # 모델 응답 추가
                add_message("assistant", response_content)
                st.chat_message("assistant").write(response_content)
                save_chat_history_to_json()
                print("대화 기록이 chat_history.json 파일로 저장되었습니다.")

                if "user_input_count" not in st.session_state:
                    st.session_state.user_input_count=1
                    print("input_count: ",st.session_state.user_input_count)
                else:
                    st.session_state.user_input_count+=1
                    print("input_count: ",st.session_state.user_input_count)


                # 대화 종료 메시지 확인
                if "즐거웠습니다" in response_content:
                    st.session_state.conversation_done = True
                if st.session_state.user_input_count>=8:
                    st.info("8회의 크레딧을 모두 사용하였습니다")
                    st.session_state.conversation_done = True
                

            except Exception as e:
                response_content = f"오류가 발생했습니다: {e}"
                add_message("assistant", response_content)
                st.chat_message("assistant").write(response_content)

# 대화 종료 후 회원가입 완료 버튼 표시
if st.session_state.conversation_done:
    st.success("대화가 종료되었습니다. 회원가입을 완료하려면 아래 버튼을 클릭하세요.")
    if st.button("회원가입 완료"):
        # 고객 정보 저장
        user_data = {
            "email": st.session_state.get("email"),
            "name": st.session_state.get("name"),
            "password": st.session_state.get("password"),
            "friends": {},
            "chat_history": st.session_state.chat_history,
        }
        print(user_data)
        save_user_data_to_json(user_data)
        st.session_state.chat_history = []  # 대화 기록 초기화
        st.session_state.conversation_done = False  # 상태 초기화
        st.session_state["page"] = "login"  # 메인 페이지로 전환
        st.success("회원 가입이 완료되었습니다. 로그인 창에서 로그인 해주세요")
        st.session_state.clear()
        st.switch_page("pages/login.py")

# 디버깅: 상태 출력
print("=======회원가입 최종 대화 기록 =======")
for message in st.session_state.chat_history:
    print(f"{message['role']}: {message['content']}")
print("=========================")


