import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from model import ECNUModel

COMPARE_FIELDS = [
    "Name", "Year", "Publisher", "#Samples", "Modality",
    "GSD", "Ann. Methed", "Ann. Method", "Method", "Type", "Data Pipeline",
    "Avg. Len.", "标注比例", "新标注比例", "包含数据集", "数据集备注",
]
SKIP_FIELDS = {"_sheet", "_text", "_years", "_leak_originals"}

# 可用于雷达图的数值字段
NUMERIC_FIELDS = ["Year", "#Samples", "Avg. Len."]


def _get_display_value(item: dict, field: str) -> str:
    val = item.get(field, "")
    if val == "" or str(val).strip().lower() in ("nan", "none"):
        return "—"
    return str(val).strip()


def _try_numeric(val: str) -> float | None:
    try:
        return float(str(val).replace(",", "").replace("，", ""))
    except Exception:
        return None


def _render_radar(items: list, i18n: dict):
    """雷达图：对比各数据集的数值型字段（归一化到 0-1）"""
    dark = st.session_state.get("theme_mode", "dark") == "dark"
    font_color = "#f9fafb" if dark else "#1e293b"

    # 收集有效数值字段
    radar_fields = []
    for f in NUMERIC_FIELDS:
        vals = [_try_numeric(_get_display_value(it, f)) for it in items]
        if any(v is not None for v in vals):
            radar_fields.append(f)

    if len(radar_fields) < 2:
        return  # 数值字段不足，不画雷达图

    st.markdown(f"**{i18n.get('compare_radar_title', '📡 数值指标雷达图')}**")

    # 归一化
    field_ranges = {}
    for f in radar_fields:
        vals = [_try_numeric(_get_display_value(it, f)) for it in items]
        valid = [v for v in vals if v is not None]
        mn, mx = min(valid), max(valid)
        field_ranges[f] = (mn, mx)

    colors = ["#2563eb", "#ef4444", "#10b981", "#f59e0b"]
    fig = go.Figure()

    for i, item in enumerate(items):
        name = str(item.get("Name", item.get("name", f"Dataset {i+1}"))).strip()
        r_vals = []
        for f in radar_fields:
            raw = _try_numeric(_get_display_value(item, f))
            mn, mx = field_ranges[f]
            if raw is None:
                r_vals.append(0.0)
            elif mx == mn:
                r_vals.append(1.0)
            else:
                r_vals.append((raw - mn) / (mx - mn))

        fig.add_trace(go.Scatterpolar(
            r=r_vals + [r_vals[0]],
            theta=radar_fields + [radar_fields[0]],
            fill="toself",
            name=name,
            line=dict(color=colors[i % len(colors)]),
            opacity=0.6,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color=font_color)),
            angularaxis=dict(tickfont=dict(color=font_color)),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color),
        showlegend=True,
        legend=dict(font=dict(color=font_color)),
        margin=dict(l=40, r=40, t=40, b=40),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="compare_radar")


def render_compare(i18n: dict, lang: str, chef):
    all_names = chef.get_all_dataset_names()

    if st.session_state.get("_compare_clear_flag"):
       st.session_state["_compare_clear_flag"] = False
       st.session_state["_compare_data"] = []
       st.session_state["_compare_names"] = None

    # _compare_data 是唯一数据源，multiselect 不使用 key，用 default 初始化
    compare_data: list = st.session_state.get("_compare_data", [])

    sel_col, start_col, clear_col = st.columns([5, 1, 1], gap="medium")
    with sel_col:
        selected_names = st.multiselect(
            i18n.get("compare_select", "选择要对比的数据集（2~4个）"),
            all_names,
            default=compare_data,
            max_selections=4,
            placeholder=("请选择 2~4 个数据集..." if lang == "cn" else "Select 2–4 datasets..."),
        )
        # 用户操作 multiselect 后立即同步回 _compare_data
        st.session_state["_compare_data"] = selected_names
    with start_col:
        st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
        start_btn = st.button(
            i18n.get("compare_start", "🔀 开始对比"),
            key="compare_start_btn",
            use_container_width=True,
            type="primary",
            disabled=len(selected_names) < 2
        )
        if start_btn and len(selected_names) >= 2:
            st.session_state["_compare_names"] = selected_names
        st.markdown("</div>", unsafe_allow_html=True)
    with clear_col:
        st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
        if st.button(i18n.get("compare_clear", "🗑️ 清空"), key="compare_clear_btn",
                     use_container_width=True, type="secondary"):
            st.session_state["_compare_clear_flag"] = True
            st.session_state["_compare_names"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 只在点击"开始对比"后渲染结果
    compare_names = st.session_state.get("_compare_names")
    if not compare_names or len(compare_names) < 2:
        if len(selected_names) < 2:
            st.caption("请至少选择 2 个数据集" if lang == "cn" else "Please select at least 2 datasets")
        return

    items = [chef.get_item_by_name(n) for n in compare_names]
    items = [it for it in items if it is not None]
    if len(items) < 2:
        return
    # 雷达图
    _render_radar(items, i18n)

    # 收集字段
    all_keys = list(COMPARE_FIELDS)
    for item in items:
        for k in item.keys():
            if k not in SKIP_FIELDS and k not in all_keys:
                all_keys.append(k)

    active_keys = [
        k for k in all_keys
        if any(_get_display_value(it, k) != "—" for it in items)
    ]

    label_col = "字段" if lang == "cn" else "Field"

    if lang == "en":
        import hashlib
        cache_key = "_compare_trans_" + hashlib.md5(
            "||".join(sorted(compare_names)).encode()
        ).hexdigest()[:16]
        if cache_key not in st.session_state:
            field_pairs = [(k, "") for k in active_keys]
            translated_fields_raw = ECNUModel.translate_item_fields(field_pairs)
            translated_keys = []
            for line, orig in zip(translated_fields_raw, active_keys):
                try:
                    translated_keys.append(line.split("**")[1])
                except Exception:
                    translated_keys.append(orig)

            translated_values: dict[str, list[str]] = {}
            for item in items:
                name = str(item.get("Name", item.get("name", "?"))).strip()
                raw_vals = [_get_display_value(item, k) for k in active_keys]
                pairs = [(f"val_{i}", v) for i, v in enumerate(raw_vals) if v != "—" and _try_numeric(v) is None]
                if pairs:
                    trans_raw = ECNUModel.translate_item_fields(pairs)
                    trans_map = {}
                    for line, (orig_k, _) in zip(trans_raw, pairs):
                        try:
                            trans_map[orig_k] = line.split(": ", 1)[1] if ": " in line else line
                        except Exception:
                            trans_map[orig_k] = _
                    final_vals = []
                    for i, v in enumerate(raw_vals):
                        if v != "—" and _try_numeric(v) is None:
                            final_vals.append(trans_map.get(f"val_{i}", v))
                        else:
                            final_vals.append(v)
                    translated_values[name] = final_vals
                else:
                    translated_values[name] = raw_vals

            st.session_state[cache_key] = {"keys": translated_keys, "values": translated_values}

        cached = st.session_state[cache_key]
        display_keys = cached["keys"]
        table_data = {label_col: display_keys}
        for item in items:
            name = str(item.get("Name", item.get("name", "?"))).strip()
            table_data[name] = cached["values"].get(name, [_get_display_value(item, k) for k in active_keys])
    else:
        display_keys = active_keys
        table_data = {label_col: display_keys}
        for item in items:
            name = str(item.get("Name", item.get("name", "?"))).strip()
            table_data[name] = [_get_display_value(item, k) for k in active_keys]

    df = pd.DataFrame(table_data).set_index(label_col)

    def highlight_diff(row):
        vals = [v for v in row if v != "—"]
        if len(set(vals)) > 1:
            return ["background-color: rgba(239,68,68,0.15)"] * len(row)
        return [""] * len(row)

    styled = df.style.apply(highlight_diff, axis=1)
    st.dataframe(styled, use_container_width=True, height=min(60 + len(active_keys) * 35, 600))

    diff_fields = [
        k for k in active_keys
        if len(set(
            _get_display_value(it, k) for it in items
            if _get_display_value(it, k) != "—"
        )) > 1
    ]
    if diff_fields:
        sep = "、" if lang == "cn" else ", "
        label = f"📋 {'存在差异的字段' if lang == 'cn' else 'Fields with differences'} ({len(diff_fields)})"
        st.caption(label + ("：" if lang == "cn" else ": ") + sep.join(diff_fields))
