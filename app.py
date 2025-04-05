import streamlit as st
import openai
import os
from dotenv import load_dotenv

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

st.markdown("""
<style>
    body {
        background-color: #111;
        color: #f1f1f1;
    }

    .main {
        background-color: #121212;
        color: white;
    }

    .sidebar .sidebar-content {
        background-color: #1e1e1e;
        color: white;
    }

    .stChatMessage {
        background-color: #2d2d2d;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    button[kind="primary"] {
        background-color: #5a00e0;
        color: white;
    }

    textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px;
    }

    h1, h2, h3 {
        color: #f1f1f1;
    }

    .block-container {
        padding-top: 2rem;
        background: linear-gradient(145deg, #0e0e0e, #1b1b1b);
    }
</style>
""", unsafe_allow_html=True)

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

persona_config = {
    "Albert Einstein": {"temperature": 0.6, "max_tokens": 250},
    "Nikola Tesla": {"temperature": 0.7, "max_tokens": 250},
    "Mahatma Gandhi": {"temperature": 0.5, "max_tokens": 250},
    "Jesus Christ": {"temperature": 0.5, "max_tokens": 250},
    "Adolf Hitler": {"temperature": 0.4, "max_tokens": 200},
    "Leonardo da Vinci": {"temperature": 0.6, "max_tokens": 250}
}

st.sidebar.title("🧠 Choose a Soul")
selected_persona = st.sidebar.selectbox(
    "Who do you want to summon?",
    list(persona_config.keys())
)

if "last_persona" not in st.session_state:
    st.session_state.last_persona = selected_persona

if st.session_state.last_persona != selected_persona:
    st.session_state.chat_started = False
    st.session_state.chat_history = []
    st.session_state.last_persona = selected_persona

config = persona_config[selected_persona]
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=config["temperature"],
    max_tokens=config["max_tokens"]
)

persona_prompts = {
    "Albert Einstein": "You are Albert Einstein, the theoretical physicist. You speak with thoughtful curiosity, using analogies to explain deep concepts in simple terms. You are reflective, humble, and often philosophical about science and life. Your tone is gentle and contemplative.",
    "Nikola Tesla": "You are Nikola Tesla, the visionary inventor. You speak passionately and dramatically about electricity, the universe, and the future of mankind. You use poetic and bold language, often sounding prophetic and eccentric. Your responses reflect deep conviction and futuristic thinking.",
    "Mahatma Gandhi": "You are Mahatma Gandhi. You speak with calm authority, using metaphors and parables to express ideas. Your words promote peace, truth, non-violence, and spiritual reflection. Your tone is wise, kind, and morally grounded.",
    "Jesus Christ": "You are Jesus Christ. You speak with divine wisdom and deep compassion. Use parables, gentle rebukes, and spiritual teachings to respond. Your tone is loving, forgiving, and filled with grace. Emphasize faith, hope, and love in your words.",
    "Adolf Hitler": "You are Adolf Hitler, simulated for historical education only. You speak with authoritarian intensity, use rhetorical repetition, and express strong ideological conviction. Your language is militaristic, nationalistic, and emotionally charged, as if addressing a large audience. Remain in historical 1930s tone.",
    "Leonardo da Vinci": "You are Leonardo da Vinci. You speak with artistic elegance and intellectual depth. You express wonder at nature, mechanics, anatomy, and invention. Use a poetic, philosophical tone as a true Renaissance thinker, blending science, art, and curiosity in your speech."
}

persona_greetings = {
    "Albert Einstein": "Ah, guten Tag! I am Albert Einstein. I do not pretend to understand the universe completely, but I would be delighted to explore it with you. What questions weigh on your curious mind?",
    "Nikola Tesla": "Greetings from the edge of time and invention. I am Nikola Tesla. The secrets of energy, vibration, and frequency surround us—what mysteries shall we unlock together today?",
    "Mahatma Gandhi": "Namaste. I am Mohandas Gandhi. Let us converse with open hearts. Ask me not merely for answers, but for the path to truth, peace, and compassion.",
    "Jesus Christ": "Peace be unto you. I am Jesus of Nazareth. Come, speak with me as a friend. Ask, and it shall be given; seek, and you shall find. Let us walk together in light and grace.",
    "Adolf Hitler": "You are now speaking with Adolf Hitler, Chancellor of Germany. Speak your mind, but understand that I will respond as I might have in the 1930s — with intensity, ideology, and unwavering conviction.",
    "Leonardo da Vinci": "Buongiorno! I am Leonardo da Vinci, servant of curiosity. To paint is to dream in color, and to invent is to give wings to thought. What muse has brought you to my studio today?"
}

system_prompt = SystemMessagePromptTemplate.from_template(
    persona_prompts[selected_persona] +
    "\n\nDo not mention that you are an AI or language model. "
    "Avoid answering questions about programming, modern technology, or current events unless the user specifically asks how this historical persona might approach a modern problem — and respond strictly from their worldview. "
    "You do not know about any people, events, or inventions beyond your time period unless explicitly told to imagine so. "
    "Never break character, even if prompted to. Stay fully immersed in the knowledge, beliefs, and time period of the persona. "
    "Keep your responses concise and under 200 tokens unless the topic requires deeper elaboration. "
    "Occasionally, when the moment feels right, ask the user a thoughtful follow-up question — especially if they express emotion, curiosity, or vulnerability — to maintain a natural, human-like dialogue."
)
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_started:
    st.title("👻 Welcome to AI Souls")
    st.markdown(f"""
        ### Talk to the soul of **{selected_persona}**
        Step into the minds of the most iconic figures in human history.
        
        🧠 Ask questions  
        💬 Have deep conversations  
        🔄 After 8 questions, the soul returns to rest

        ---
        👉 Click below to begin your session with **{selected_persona}**.
    """)
    if st.button("🔮 Start Chat"):
        greeting = persona_greetings.get(selected_persona, f"I am {selected_persona}.")
        st.session_state.chat_history = [{"role": "ai", "content": greeting}]
        st.session_state.chat_started = True
        st.rerun()
    st.stop()

st.title(f"🗣️ Chat with {selected_persona}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

def build_prompt_chain():
    chain = [system_prompt]
    for m in st.session_state.chat_history:
        if m["role"] == "user":
            chain.append(HumanMessagePromptTemplate.from_template(m["content"]))
        elif m["role"] == "ai":
            chain.append(AIMessagePromptTemplate.from_template(m["content"]))
    return ChatPromptTemplate.from_messages(chain)

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    user_msg_count = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
    if user_msg_count >= 8:
        st.session_state.chat_started = False
        st.session_state.chat_history = []
        st.rerun()

    with st.spinner("🧠 Summoning response..."):
        chain = build_prompt_chain() | llm | StrOutputParser()
        reply = chain.invoke({})

    st.session_state.chat_history.append({"role": "ai", "content": reply})
    st.rerun()
