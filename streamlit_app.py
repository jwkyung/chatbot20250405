import streamlit as st
from openai import OpenAI

st.title("🧠 시사 사설 분석 챗봇")
st.write("고등학생이 이해할 수 있도록 시사 사설을 분석해주는 챗봇입니다.")

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("API 키를 입력해야 분석이 가능합니다.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    article = st.text_area("📰 사설 전문을 여기에 붙여넣으세요.", height=300)

    if st.button("분석 시작하기") and article:
        analysis_prompt = f"""
        다음은 고등학교 국어 수업에서 활용하기 위한 시사 사설입니다. 이 사설을 분석해줘:

        사설 전문:
        {article}

        요청하는 분석 항목은 다음과 같아:
        1. 핵심 주제 요약 (3줄 이내)
        2. 글의 주장과 근거 정리 (논리 흐름 포함)
        3. 문체적 특징 (어휘, 어투, 글의 분위기 등)
        4. 배경지식이 부족한 고등학생을 위한 해설
        5. 생각을 확장할 수 있는 질문 2개

        분석은 고등학생이 이해할 수 있는 수준으로 써줘.
        """

        st.session_state.messages.append({"role": "user", "content": analysis_prompt})
        with st.chat_message("user"):
            st.markdown("사설 분석을 요청합니다...")

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 이전 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
