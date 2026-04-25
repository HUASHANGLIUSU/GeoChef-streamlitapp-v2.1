import streamlit as st
from model import ECNUModel


def render_chat_history(history: list):
    """用 st.chat_message 渲染对话历史，支持 markdown。"""
    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])


def render_chat(i18n: dict):
    render_chat_history(st.session_state.chat_history)

    col1, col2, col3 = st.columns([4, 1, 1], gap="medium")
    with col1:
        chat_input = st.text_input(
            i18n["chat_input"],
            placeholder="问问我关于遥感数据集的问题",
            key="chat_text_input",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button(i18n["chat_send"], key="chat_send_btn", use_container_width=True, type="primary")
    with col3:
        clear_btn = st.button(i18n["chat_clear"], key="chat_clear_btn", use_container_width=True, type="secondary")

    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    if send_btn and chat_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.spinner(i18n["loading"]):
            response = ECNUModel.generate_response(chat_input, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
