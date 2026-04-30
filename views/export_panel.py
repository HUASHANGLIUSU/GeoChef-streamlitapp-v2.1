"""
导出面板：在筛选结果下方渲染一个可折叠的导出区域。
支持 Excel / CSV / Word / BibTeX / Markdown 五种格式。
"""
import streamlit as st
from datetime import datetime
from views.export_utils import to_excel, to_csv, to_word, to_bibtex, to_markdown


_FORMATS = [
    ("Excel",    "📊", "xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    ("CSV",      "📄", "csv",  "text/csv"),
    ("Word",     "📝", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("BibTeX",   "📚", "bib",  "text/plain"),
    ("Markdown", "🗒️", "md",   "text/markdown"),
]

_GENERATORS = {
    "Excel":    to_excel,
    "CSV":      to_csv,
    "Word":     to_word,
    "BibTeX":   to_bibtex,
    "Markdown": to_markdown,
}


def render_export_panel(items: list[dict], i18n: dict, lang: str):
    """
    在筛选结果区域底部渲染导出面板。
    items: 当前全部筛选结果（非分页，导出全量）。
    """
    if not items:
        return

    label_cn = f"📤 导出全部结果（{len(items)} 条）"
    label_en = f"📤 Export All Results ({len(items)} items)"
    label = label_cn if lang == "cn" else label_en

    with st.expander(label, expanded=False):
        hint_cn = "选择格式后点击按钮即可下载，导出的是**全部筛选结果**，不受分页影响。"
        hint_en = "Click a button to download **all filtered results** (not just the current page)."
        st.caption(hint_cn if lang == "cn" else hint_en)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"rs_vlm_datasets_{ts}"

        cols = st.columns(len(_FORMATS), gap="small")
        for col, (fmt_name, icon, ext, mime) in zip(cols, _FORMATS):
            with col:
                # Word 需要 python-docx，做一个友好的错误提示
                if fmt_name == "Word":
                    try:
                        import docx  # noqa: F401
                        _word_ok = True
                    except ImportError:
                        _word_ok = False
                    if not _word_ok:
                        st.button(
                            f"{icon} {fmt_name}",
                            key=f"export_{fmt_name}_disabled",
                            use_container_width=True,
                            disabled=True,
                            help="需要安装 python-docx：pip install python-docx",
                        )
                        continue

                # 生成文件内容（缓存在 session_state，避免每次重渲染都重新生成）
                import hashlib
                _content_hash = hashlib.md5(str([i.get("Name", i.get("name","")) for i in items]).encode()).hexdigest()[:8]
                cache_key = f"_export_{fmt_name}_{len(items)}_{_content_hash}"
                if cache_key not in st.session_state:
                    try:
                        st.session_state[cache_key] = _GENERATORS[fmt_name](items)
                    except Exception as e:
                        st.error(f"{fmt_name} 生成失败: {e}")
                        continue

                file_bytes = st.session_state[cache_key]
                st.download_button(
                    label=f"{icon} {fmt_name}",
                    data=file_bytes,
                    file_name=f"{base_name}.{ext}",
                    mime=mime,
                    key=f"export_dl_{fmt_name}_{len(items)}_{_content_hash}",
                    use_container_width=True,
                    type="secondary",
                )
