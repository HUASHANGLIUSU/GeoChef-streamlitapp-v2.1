import streamlit as st
from datetime import datetime
from views.result_card import render_result_card
from views.leakage_graph import render_leakage_graph
from views.export_utils import (
    leak_to_excel, leak_to_csv, leak_to_word, leak_to_bibtex, leak_to_markdown,
)

PAGE_SIZE = 10

_LEAK_FORMATS = [
    ("Excel",    "📊", "xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    ("CSV",      "📄", "csv",  "text/csv"),
    ("Word",     "📝", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("BibTeX",   "📚", "bib",  "text/plain"),
    ("Markdown", "🗒️", "md",   "text/markdown"),
]
_LEAK_GENERATORS = {
    "Excel":    leak_to_excel,
    "CSV":      leak_to_csv,
    "Word":     leak_to_word,
    "BibTeX":   leak_to_bibtex,
    "Markdown": leak_to_markdown,
}


def _render_leak_export(entries: list[dict], source_label: str,
                        lang: str, cache_suffix: str):
    """泄露检测结果导出面板，复用于单源和批量模式。"""
    if not entries:
        return
    is_cn = lang == "cn"
    label = (
        f"📤 {'导出检测结果' if is_cn else 'Export Results'}"
        f" ({len(entries)} {'条' if is_cn else 'items'})"
    )
    with st.expander(label, expanded=False):
        hint = (
            "导出包含原始数据集来源（LeakSource / IncludedSources）字段，导出全量结果。"
            if is_cn else
            "Export includes LeakSource and IncludedSources fields. All results exported."
        )
        st.caption(hint)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        cols = st.columns(len(_LEAK_FORMATS), gap="small")
        for col, (fmt_name, icon, ext, mime) in zip(cols, _LEAK_FORMATS):
            with col:
                if fmt_name == "Word":
                    try:
                        import docx  # noqa: F401
                    except ImportError:
                        st.button(f"{icon} {fmt_name}",
                                  key=f"leak_exp_{fmt_name}_{cache_suffix}_dis",
                                  use_container_width=True, disabled=True,
                                  help="需要安装 python-docx")
                        continue

                cache_key = f"_leak_export_{fmt_name}_{cache_suffix}_{len(entries)}"
                if cache_key not in st.session_state:
                    try:
                        st.session_state[cache_key] = _LEAK_GENERATORS[fmt_name](
                            entries, source_label
                        )
                    except Exception as e:
                        st.error(f"{fmt_name} 生成失败: {e}")
                        continue

                st.download_button(
                    label=f"{icon} {fmt_name}",
                    data=st.session_state[cache_key],
                    file_name=f"leak_{ts}.{ext}",
                    mime=mime,
                    key=f"leak_dl_{fmt_name}_{cache_suffix}_{len(entries)}",
                    use_container_width=True,
                    type="secondary",
                )


def _render_chat_hint(lang: str):
    """标题下方的 ChatECNU 跳转提示条。"""
    is_cn = lang == "cn"
    hint_text = "💡 不确定该查哪个数据集？问问 ChatECNU 助手，它了解数据泄露检测的完整流程。"
    hint_en   = "💡 Not sure which dataset to check? Ask the ChatECNU Assistant — it knows the full leakage detection workflow."
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
        if st.button(btn_text, key="leakage_to_chat_btn", use_container_width=True, type="secondary"):
            st.session_state.page = "chat"
            st.rerun()
    st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)


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
            st.rerun()


def render_leakage(i18n: dict, lang: str, chef):
    _render_chat_hint(lang)
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
                render_leakage_graph(selected_label, results, i18n, chart_key="single")
                _render_leak_export(results, selected_label, lang, cache_suffix="single")
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
            batch_source_label = " ∩ ".join(st.session_state.get("leak_batch_selected", []))
            _render_leak_export(common_entries, batch_source_label, lang, cache_suffix="batch_common")
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
                    render_leakage_graph(src, entries, i18n, chart_key=f"bsrc{src_idx}")
                    _render_leak_export(entries, src, lang, cache_suffix=f"bsrc{src_idx}")
                    for idx, entry in enumerate(entries):
                        render_result_card(entry["item"], f"{safe_key}_{idx}", i18n, lang)
