import streamlit as st
from views.result_card import render_result_card
from views.leakage_graph import render_leakage_graph

PAGE_SIZE = 10


def _render_result_list(results: list, key_prefix: str, page_key: str,
                        i18n: dict, lang: str):
    """渲染带翻页+收起的结果列表，复用于单选和批量模式。"""
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    page = st.session_state[page_key]
    total_pages = max(1, (len(results) + PAGE_SIZE - 1) // PAGE_SIZE)
    page_items = results[page * PAGE_SIZE: (page + 1) * PAGE_SIZE]

    for idx, entry in enumerate(page_items):
        render_result_card(entry["item"], f"{key_prefix}_{page * PAGE_SIZE + idx}", i18n, lang)

    nav_cols = st.columns([1, 2, 1, 1], gap="medium")
    with nav_cols[0]:
        if total_pages > 1:
            if st.button("◀ " + ("上一页" if lang == "cn" else "Prev"),
                         key=f"{key_prefix}_prev", disabled=page == 0, use_container_width=True):
                st.session_state[page_key] -= 1
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
            if st.button(("下一页" if lang == "cn" else "Next") + " ▶",
                         key=f"{key_prefix}_next", disabled=page >= total_pages - 1, use_container_width=True):
                st.session_state[page_key] += 1
                st.rerun()
    with nav_cols[3]:
        if st.button(i18n["collapse_btn"], key=f"{key_prefix}_collapse",
                     use_container_width=True, type="secondary"):
            if key_prefix.startswith("batch"):
                st.session_state.leak_batch_results = None
                st.session_state["batch_common_page"] = 0
            else:
                st.session_state.leak_results = None
                st.session_state.leak_page = 0
            st.session_state[page_key] = 0
            st.rerun()


def render_leakage(i18n: dict, lang: str, chef):
    all_sources = chef.get_all_sources()

    tab_single, tab_batch = st.tabs([
        "🔍 " + ("单源查询" if lang == "cn" else "Single Source"),
        "📦 " + ("批量检测" if lang == "cn" else "Batch Detection"),
    ])

    # ── 单源查询 ──────────────────────────────────────────
    with tab_single:
        col1, col2 = st.columns([3, 1], gap="medium")
        with col1:
            selected = st.selectbox(i18n["leak_select_train"], all_sources, key="leak_source_select")
        with col2:
            st.markdown('<div class="leak-button-wrapper">', unsafe_allow_html=True)
            detect = st.button(i18n["leak_detect_btn"], key="leak_detect_btn",
                               use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

        if detect and selected:
            with st.spinner(i18n["leak_detecting"]):
                st.session_state.leak_results = chef.query_by_source(selected)
                st.session_state.leak_selected = selected
                st.session_state.leak_page = 0

        results = st.session_state.get("leak_results")
        if results is not None:
            selected_label = st.session_state.get("leak_selected", "")
            st.markdown(f"<p><strong>{i18n['leak_source_label']}</strong>{selected_label}</p>",
                        unsafe_allow_html=True)
            if not results:
                st.markdown(f"<div class='no-result'><h4>{i18n['leak_no_result']}</h4></div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<h5>{i18n['leak_used_by'].format(count=len(results))}</h5>",
                            unsafe_allow_html=True)
                render_leakage_graph(selected_label, results, i18n)
                _render_result_list(results, "leak", "leak_page", i18n, lang)

    # ── 批量检测 ──────────────────────────────────────────
    with tab_batch:
        selected_multi = st.multiselect(
            i18n["leak_batch_mode"],
            all_sources,
            key="leak_batch_select",
            placeholder=("请选择多个原始数据集..." if lang == "cn" else "Select multiple source datasets..."),
        )
        col1, col2 = st.columns([3, 1], gap="medium")
        with col2:
            batch_detect = st.button(
                i18n["leak_detect_btn"], key="leak_batch_detect_btn",
                use_container_width=True, type="primary",
                disabled=len(selected_multi) < 2
            )

        if batch_detect and len(selected_multi) >= 2:
            with st.spinner(i18n["leak_detecting"]):
                st.session_state.leak_batch_results = chef.query_by_multiple_sources(selected_multi)
                st.session_state.leak_batch_selected = selected_multi

        batch_data = st.session_state.get("leak_batch_results")
        if batch_data is None:
            if len(selected_multi) < 2:
                st.caption("请至少选择 2 个原始数据集" if lang == "cn" else "Please select at least 2 source datasets")
            return

        per_source: dict = batch_data["per_source"]
        common_names: set = batch_data["common_names"]

        # 交集结果
        if common_names:
            st.markdown(
                f"<h5>{i18n['leak_batch_common'].format(count=len(common_names))}</h5>",
                unsafe_allow_html=True
            )
            common_entries = [e for e in list(per_source.values())[0] if e["name"] in common_names]
            _render_result_list(common_entries, "batch_common", "batch_common_page", i18n, lang)
        else:
            st.markdown(f"<div class='no-result'><h4>{i18n['leak_batch_no_common']}</h4></div>",
                        unsafe_allow_html=True)

        # 每个源的独立结果
        st.divider()
        for src_idx, (src, entries) in enumerate(per_source.items()):
            safe_key = f"bsrc_{src_idx}"
            with st.expander(i18n["leak_batch_per"].format(src=src, count=len(entries)), expanded=False):
                if not entries:
                    st.caption(i18n["leak_no_result"])
                else:
                    render_leakage_graph(src, entries, i18n)
                    for idx, entry in enumerate(entries):
                        render_result_card(entry["item"], f"{safe_key}_{idx}", i18n, lang)
