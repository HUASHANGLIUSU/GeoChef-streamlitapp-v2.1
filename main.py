import streamlit as st
from core import load_chef
from github_parser import load_github_paper_links
from theme import get_theme_css
from i18n import I18N
from views.chat_view import render_chat
from views.paper_view import render_paper_chat
from views.filter_view import render_filter
from views.leakage_view import render_leakage
from views.stats_view import render_stats
from views.compare_view import render_compare
from views.intro_view import render_intro

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

st.markdown(get_theme_css(), unsafe_allow_html=True)

PAGES = [
    ("intro",   "简介",         "Introduction",      "📖"),
    ("chat",    "ChatECNU 助手", "ChatECNU",          "💬"),
    ("paper",   "论文讲解助手",  "Paper Assistant",   "📚"),
    ("stats",   "数据集统计",    "Statistics",        "📊"),
    ("compare", "数据集对比",    "Compare",           "🔀"),
    ("filter",  "精准筛选",      "Search",            "🔍"),
    ("leakage", "数据泄露检测",  "Leakage Detection", "⚠️"),
]


def init_session():
    defaults = {
        "lang": "cn",
        "page": "intro",
        "chat_history": [],
        "paper_chat_history": [],
        "search_results": None,
        "result_page": 0,
        "leak_results": None,
        "leak_page": 0,
        "leak_selected": "",
        "leak_batch_results": None,
        "leak_batch_selected": [],
        "batch_common_page": 0,
        "pending_explain_link": None,
        "pending_explain_name": None,
        "_compare_names": None,
        "_compare_data": [],
        "chat_text_input": "",
        "paper_link_input": "",
        "paper_followup_input": "",
        "filter_search_input": "",
        "filter_modals": [],
        "filter_tasks": [],
        "filter_years": [],
        "filter_publishers": [],
        "filter_methods": [],
        "leak_source_select": None,
        "leak_batch_select": [],
        "compare_select": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def render_sidebar(i18n: dict, lang: str):
    with st.sidebar:
        st.markdown(
            f"<h1 style='font-size:1.8rem;margin:0 0 0.5rem 0'>{i18n['title']}</h1>",
            unsafe_allow_html=True
        )
        st.divider()

        for key, cn_name, en_name, icon in PAGES:
            label = f"{icon} {cn_name if lang == 'cn' else en_name}"
            btn_type = "primary" if st.session_state.page == key else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
                st.session_state.page = key
                st.rerun()

        st.divider()

        if st.button(i18n["switch_lang"], key="sidebar_lang_btn", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k.startswith("_trans_") or k.startswith("_compare_trans_"):
                    del st.session_state[k]
            st.session_state.lang = "en" if lang == "cn" else "cn"
            st.rerun()

        theme_text = "☀️ 浅色模式" if st.session_state.theme_mode == "dark" else "🌙 深色模式"
        if st.button(theme_text, key="sidebar_theme_btn", use_container_width=True, type="secondary"):
            st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
            st.rerun()

        st.divider()
        st.markdown(
            f'<a href="https://github.com/VisionXLab/Awesome-RS-VL-Data" target="_blank" '
            f'class="github-link" style="font-size:0.85rem">{i18n["github_link"]}</a>',
            unsafe_allow_html=True
        )


def render_topbar(i18n: dict, lang: str):
    page_info = next((p for p in PAGES if p[0] == st.session_state.page), PAGES[0])
    name = page_info[1] if lang == "cn" else page_info[2]
    st.markdown(
        f"<h2 style='margin:0 0 1.2rem 0;padding-bottom:0.6rem;"
        f"border-bottom:2px solid #2563eb'>{page_info[3]} {name}</h2>",
        unsafe_allow_html=True
    )


def main():
    st.set_page_config(
        page_title="GeoChef",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🌍"
    )

    init_session()

    if st.session_state.pending_explain_link and st.session_state.page != "paper":
        st.session_state.page = "paper"
        st.rerun()

    lang = st.session_state.lang
    i18n = I18N[lang]

    render_sidebar(i18n, lang)
    render_topbar(i18n, lang)

    page = st.session_state.page

    if page == "intro":
        render_intro(lang)
        return

    if "github_loaded" not in st.session_state:
        with st.spinner(i18n["loading"]):
            load_github_paper_links()
            st.session_state.github_loaded = True

    chef = load_chef()

    if page == "chat":
        render_chat(i18n)
    elif page == "paper":
        render_paper_chat(i18n, lang)
    elif page == "stats":
        render_stats(i18n, lang, chef)
    elif page == "compare":
        render_compare(i18n, lang, chef)
    elif page == "filter":
        render_filter(i18n, lang, chef)
    elif page == "leakage":
        render_leakage(i18n, lang, chef)


if __name__ == "__main__":
    main()
