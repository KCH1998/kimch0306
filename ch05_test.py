import streamlit as st
import openai
import os
from datetime import datetime

def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key = apikey)
    
    response = client.chat.completions.create(model=model, messages=prompt)
    
    gptResponse = response.choices[0].message.content
    return gptResponse

def main():
    st.set_page_config(
        page_title="중간고사 ",
        layout="wide")
    
    st.header("중간고사 ")

    st.markdown("---")

    with st.expander("중간고사 ",expanded=True):
        st.write(
            """
            문제: 다음에 유의해서 중간고사를 완성해보세요.

            1.기본적으로 교재 3장에 있는 코드를 참고하여 프로그램을 작성하시오.

            2.ChatGPT 질문과 답변을 (음성으로 재생하지 말고) 모두 문자로 (채팅 형식으로만) 제공하시오. 제출 코드에 음성 관련 코드가 있을 경우 감점함

            3.텍스트 입력 창: 기능구현영역 ‘질문하기’ 아래에 사용자가 질문을 입력하기 위한 텍스트 입력창을 배치하시오. (원한다면, 버튼을 추가적으로 배치해도 괜찮음)

            4.ChatGPT에 질문을 보내고 답변을 받아와서 오른쪽 ‘질문/답변’에 채팅 형식으로 표시하시오.
            """
        )
    if "chat" not in  st.session_state:
        st.session_state["chat"] = []

    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

        st.markdown("")
    #사이드바
    with st.sidebar:

        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")
            
        st.markdown("---")

        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        if st.button(label="초기화"):

            st.session_state["chat"]=[]
            st.session_state["messages"]=[{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True

    col1, col2 = st.columns(2)
    with col1:

        st.subheader("질문하기")
        question_text=st.text_input("텍스트 질문",placeholder="입력하세요.")
        btn=st.button("ask")
        if btn:
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+[("user", now, question_text)]
            st.session_state["messages"] = st.session_state["messages"]+[{"role": "user", "content": question_text}]
            st.session_state["q_type"]="text" 
  

    with col2:

        st.subheader("질문/답변")
        if btn :
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"])

            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "system", "content": response}]
            
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("bot",now, response)]
         
        for sender, time, message in st.session_state["chat"]:

            if sender == "user":

                st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                st.write("")

            else:

                st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                st.write("")
        

 
        

if __name__=="__main__":
    main()