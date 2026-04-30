import streamlit as st
from views.result_card import render_result_card
from views.export_panel import render_export_panel

PAGE_SIZE = 10


def _render_chat_hint(lang: str):
    """标题下方的 ChatECNU 跳转提示条。"""
    is_cn = lang == "cn"
    hint_text = "💡 不知道怎么搜？问问 ChatECNU 助手吧，它能帮你分析需求、推荐筛选条件。"
    hint_en   = "💡 Not sure how to search? Ask the ChatECNU Assistant — it can help you find the right filters."
    btn_text  = "去问问 →" if is_cn else "Ask Now →"

    col_hint, col_btn = st.columns([5, 1], gap="small")
    with col_hint:
        st.markdown(
            f"<div style='padding:0.55rem 0.9rem;border-radius:8px;"
            f"border:1px solid rgba(37,99,235,0.35);"
            f"background:rgba(37,99,235,0.08);"
            f"font-size:0.88rem;line-height:1.5'>"
            f"{hint_text if is_cn else hint_en}</div>",
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button(btn_text, key="filter_to_chat_btn", use_container_width=True, type="secondary"):
            st.session_state.page = "chat"
            st.rerun()
    st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)


def render_filter(i18n: dict, lang: str, chef):
    _render_chat_hint(lang)
    # 关键词搜索框
    search_query = st.text_input(
        i18n["search_placeholder"],
        placeholder=i18n["search_placeholder"],
        key="filter_search_input",
        label_visibility="collapsed"
    )

    cols = st.columns(5, gap="medium")
    with cols[0]:
        modals = st.multiselect(i18n["modal"], chef.modalities, key="filter_modals", placeholder="请选择..." if lang == "cn" else "Select...")
    with cols[1]:
        tasks = st.multiselect(i18n["task"], chef.tasks, key="filter_tasks", placeholder="请选择..." if lang == "cn" else "Select...")
    with cols[2]:
        years = st.multiselect(i18n["year"], chef.years, key="filter_years", placeholder="请选择..." if lang == "cn" else "Select...")
    with cols[3]:
        publishers = st.multiselect(i18n["publisher"], chef.publishers, key="filter_publishers", placeholder="请选择..." if lang == "cn" else "Select...")
    with cols[4]:
        methods = st.multiselect(i18n["method"], chef.methods, key="filter_methods", placeholder="请选择..." if lang == "cn" else "Select...")

    btn_cols = st.columns([7, 3], gap="medium")
    with btn_cols[0]:
        go = st.button(i18n["search_btn"], key="filter_go_btn", use_container_width=True)
    with btn_cols[1]:
        rand = st.button(i18n["random"], key="filter_rand_btn", use_container_width=True, type="secondary")

    if rand:
        st.session_state.search_results = [chef.random_one()] if chef.random_one() else []
        st.session_state.result_page = 0
    elif go:
        kws = [w.strip() for w in search_query.split() if w.strip()]
        st.session_state.search_results = chef.filter(modals, tasks, years, publishers, methods, kws)
        st.session_state.result_page = 0

    res = st.session_state.search_results
    if res is None:
        return

    st.caption(f"📊 {i18n['result']}: {len(res)}")
    if not res:
        st.markdown(
            f"<div class='no-result'><h4>😶 {i18n['no_result']}</h4>"
            f"<p>{'建议调整筛选条件后重试' if lang == 'cn' else 'Try adjusting the filters'}</p></div>",
            unsafe_allow_html=True
        )
        return

    # 导出面板（全量结果，不受分页影响）
    render_export_panel(res, i18n, lang)

    if "result_page" not in st.session_state:
        st.session_state.result_page = 0
    page = st.session_state.result_page
    total_pages = max(1, (len(res) + PAGE_SIZE - 1) // PAGE_SIZE)
    page_items = res[page * PAGE_SIZE: (page + 1) * PAGE_SIZE]

    _render_items(page_items, page, i18n, lang)

    nav_cols = st.columns([1, 2, 1, 1], gap="medium")
    with nav_cols[0]:
        if total_pages > 1:
            if st.button("◀ " + ("上一页" if lang == "cn" else "Prev"), key="page_prev_btn", disabled=page == 0, use_container_width=True):
                st.session_state.result_page -= 1
                st.rerun()
    with nav_cols[1]:
        if total_pages > 1:
            st.markdown(
                f"<p style='text-align:center;margin-top:8px'>"
                f"{'第' if lang == 'cn' else 'Page '} {page + 1} / {total_pages}</p>",
                unsafe_allow_html=True
            )
    with nav_cols[2]:
        if total_pages > 1:
            if st.button(("下一页" if lang == "cn" else "Next") + " ▶", key="page_next_btn", disabled=page >= total_pages - 1, use_container_width=True):
                st.session_state.result_page += 1
                st.rerun()
    with nav_cols[3]:
        if st.button(i18n["collapse_btn"], key="filter_collapse_btn", use_container_width=True, type="secondary"):
            st.session_state.search_results = None
            st.session_state.result_page = 0
            st.rerun()


def _render_items(items, page_offset, i18n, lang):
    for idx, item in enumerate(items):
        global_idx = page_offset * PAGE_SIZE + idx
        render_result_card(item, str(global_idx), i18n, lang)
