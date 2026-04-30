import streamlit as st
from model import ECNUModel
from views.export_utils import chat_to_txt, chat_to_markdown, chat_to_word
from datetime import datetime


def render_chat_history(history: list):
    """用 st.chat_message 渲染对话历史，支持 markdown。"""
    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])


def _render_chat_export(history: list, lang: str, key_prefix: str, title: str = ""):
    """在对话历史下方渲染导出面板（有历史时才显示）。"""
    if not history:
        return

    label = f"📤 {'导出对话记录' if lang == 'cn' else 'Export Chat'} ({len(history)} {'条' if lang == 'cn' else 'msgs'})"
    with st.expander(label, expanded=False):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_title = "ChatECNU 对话记录" if lang == "cn" else "ChatECNU Conversation"
        export_title = title or default_title

        cols = st.columns(3, gap="small")
        formats = [
            ("TXT",      "📄", "txt",  "text/plain"),
            ("Markdown", "🗒️", "md",   "text/markdown"),
            ("Word",     "📝", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ]
        generators = {
            "TXT":      lambda: chat_to_txt(history, export_title, lang),
            "Markdown": lambda: chat_to_markdown(history, export_title, lang),
            "Word":     lambda: chat_to_word(history, export_title, lang),
        }

        for col, (fmt_name, icon, ext, mime) in zip(cols, formats):
            with col:
                if fmt_name == "Word":
                    try:
                        import docx  # noqa: F401
                    except ImportError:
                        st.button(f"{icon} {fmt_name}", key=f"{key_prefix}_exp_{fmt_name}",
                                  use_container_width=True, disabled=True,
                                  help="需要安装 python-docx")
                        continue

                cache_key = f"_chat_export_{key_prefix}_{fmt_name}_{len(history)}"
                if cache_key not in st.session_state:
                    try:
                        st.session_state[cache_key] = generators[fmt_name]()
                    except Exception as e:
                        st.error(f"{fmt_name} 生成失败: {e}")
                        continue

                st.download_button(
                    label=f"{icon} {fmt_name}",
                    data=st.session_state[cache_key],
                    file_name=f"chat_{ts}.{ext}",
                    mime=mime,
                    key=f"{key_prefix}_dl_{fmt_name}_{len(history)}",
                    use_container_width=True,
                    type="secondary",
                )


def render_chat(i18n: dict):
    lang = st.session_state.get("lang", "cn")
    history = st.session_state.chat_history

    render_chat_history(history)

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

    # 导出面板（输入框下方）
    _render_chat_export(history, lang, key_prefix="chat")

    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    if send_btn and chat_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.spinner(i18n["loading"]):
            response = ECNUModel.generate_response(chat_input, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
