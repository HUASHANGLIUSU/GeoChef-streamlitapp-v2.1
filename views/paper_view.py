import streamlit as st
from model import ECNUModel
from github_parser import get_paper_link_by_name
from paper_explainer import explain_paper_by_link
from views.chat_view import render_chat_history


def _run_explain(link: str, name: str, lang: str, i18n: dict):
    """调用讲解 + 按需翻译，结果存入 paper_chat_history。"""
    full_text = ""
    for chunk in explain_paper_by_link(link, name):
        full_text += chunk

    if lang == "en":
        with st.spinner(i18n["paper_translating"]):
            full_text = ECNUModel.translate_line(full_text)

    st.session_state.paper_chat_history.append({"role": "assistant", "content": full_text})


def _run_followup(question: str, history: list, i18n: dict):
    system = (
        "你是一位遥感领域的论文助手。用户已经获得了一篇论文的讲解，"
        "请根据对话历史回答用户的追问，保持专业、简洁。"
    )
    trimmed_history = history[-10:] if len(history) > 10 else history
    messages = [{"role": "system", "content": system}] + trimmed_history
    response = ECNUModel.multi_chat(messages)
    st.session_state.paper_chat_history.append({"role": "assistant", "content": response})


def render_paper_chat(i18n: dict, lang: str):
    if st.session_state.pending_explain_link:
        link = st.session_state.pending_explain_link
        name = st.session_state.pending_explain_name or ""
        st.session_state.pending_explain_link = None
        st.session_state.pending_explain_name = None
        label = f"{name}（{link}）" if name else link
        st.session_state.paper_chat_history.append({"role": "user", "content": label})
        with st.spinner(i18n["explain_loading"]):
            _run_explain(link, name, lang, i18n)
        st.rerun()

    # 对话历史
    has_history = bool(st.session_state.paper_chat_history)
    if has_history:
        render_chat_history(st.session_state.paper_chat_history)

    # 输入区：有历史时显示追问框，无历史时显示链接/名称输入框
    col1, col2, col3 = st.columns([4, 1, 1], gap="medium")
    with col1:
        if has_history:
            placeholder = i18n.get("paper_followup_placeholder", "继续追问这篇论文...")
            user_input = st.text_input(
                i18n.get("paper_followup_input", "追问"),
                placeholder=placeholder,
                key="paper_followup_input",
                label_visibility="collapsed"
            )
        else:
            placeholder = (
                "输入数据集名称（如 OSVQA）或论文链接（如 https://arxiv.org/abs/xxx）"
                if lang == "cn" else
                "Enter dataset name (e.g. OSVQA) or paper URL (e.g. https://arxiv.org/abs/xxx)"
            )
            user_input = st.text_input(
                i18n["paper_chat_input"],
                placeholder=placeholder,
                key="paper_link_input",
                label_visibility="collapsed"
            )
    with col2:
        btn_label = i18n.get("paper_followup_send", "📤 追问") if has_history else i18n["paper_chat_send"]
        send_btn = st.button(btn_label, key="paper_send_btn", use_container_width=True, type="primary")
    with col3:
        clear_btn = st.button(i18n["paper_chat_clear"], key="paper_clear_btn", use_container_width=True, type="secondary")

    if clear_btn:
        st.session_state.paper_chat_history = []
        st.rerun()

    if send_btn and user_input.strip():
        text = user_input.strip()
        st.session_state.paper_chat_history.append({"role": "user", "content": text})

        if has_history:
            with st.spinner(i18n.get("loading", "加载中...")):
                _run_followup(text, st.session_state.paper_chat_history[:-1], i18n)
        else:
            if text.startswith("http://") or text.startswith("https://"):
                link = text
                name = ""
            else:
                link = get_paper_link_by_name(text)
                name = text
                if not link:
                    msg = (
                        f"❌ Could not find a paper link for **{text}**. Please enter the URL directly."
                        if lang == "en" else
                        f"❌ 未找到数据集 **{text}** 对应的论文链接，请尝试直接输入论文 URL。"
                    )
                    st.session_state.paper_chat_history.append({"role": "assistant", "content": msg})
                    st.rerun()

            with st.spinner(i18n["explain_loading"]):
                _run_explain(link, name, lang, i18n)
        st.rerun()
