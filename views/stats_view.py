import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def _chart_colors():
    dark = st.session_state.get("theme_mode", "dark") == "dark"
    return {
        "font_color": "#f9fafb" if dark else "#1e293b",
        "grid_color": "rgba(255,255,255,0.1)" if dark else "rgba(0,0,0,0.08)",
        "bg": "rgba(0,0,0,0)",
    }


def _base_layout(c: dict, height: int = 260, **kwargs) -> dict:
    return dict(
        margin=dict(l=0, r=0, t=10, b=0),
        height=height,
        paper_bgcolor=c["bg"],
        plot_bgcolor=c["bg"],
        font=dict(size=12, color=c["font_color"]),
        **kwargs,
    )


# ── 原有四张图 ────────────────────────────────────────────────────────────────

def _render_overview_charts(stats: dict, i18n: dict, c: dict):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"**{i18n['stats_by_year']}**")
        year_data = stats["year"]
        if year_data:
            fig = go.Figure(go.Bar(
                x=list(year_data.keys()),
                y=list(year_data.values()),
                marker_color="#2563eb",
                hovertemplate="%{x}: %{y} datasets<extra></extra>",
            ))
            fig.update_layout(
                **_base_layout(c),
                xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(color=c["font_color"])),
                yaxis=dict(showgrid=True, gridcolor=c["grid_color"], tickfont=dict(color=c["font_color"])),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="stats_year_bar")
        task_data = stats["task"]
        if task_data:
            fig = px.pie(
                names=list(task_data.keys()), values=list(task_data.values()),
                color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4,
            )
            fig.update_traces(
                textposition="inside", textinfo="percent+label",
                textfont=dict(color=c["font_color"]),
            )
            fig.update_layout(**_base_layout(c), showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="stats_task_pie")

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown(f"**{i18n['stats_by_modal']}**")
        modal_data = stats["modal"]
        if modal_data:
            sorted_modal = dict(sorted(modal_data.items(), key=lambda x: x[1], reverse=True))
            fig = go.Figure(go.Bar(
                x=list(sorted_modal.values()), y=list(sorted_modal.keys()),
                orientation="h", marker_color="#10b981",
                hovertemplate="%{y}: %{x} datasets<extra></extra>",
            ))
            fig.update_layout(
                **_base_layout(c, height=220),
                xaxis=dict(showgrid=True, gridcolor=c["grid_color"], tickfont=dict(color=c["font_color"])),
                yaxis=dict(showgrid=False, tickfont=dict(color=c["font_color"])),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="stats_modal_bar")

    with col4:
        st.markdown(f"**{i18n['stats_by_sheet']}**")
        sheet_data = {k: v for k, v in stats["sheet"].items()
                      if k not in ["统计期刊数量、国家数量、年份"]}
        if sheet_data:
            fig = px.pie(
                names=list(sheet_data.keys()), values=list(sheet_data.values()),
                color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4,
            )
            fig.update_traces(
                textposition="inside", textinfo="percent+label",
                textfont=dict(color=c["font_color"]),
            )
            fig.update_layout(**_base_layout(c, height=220), showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="stats_sheet_pie")


# ── 地理覆盖地图 ──────────────────────────────────────────────────────────────

# 国家名称 → (纬度, 经度, 显示名) 映射
# 台湾数据并入中国（坐标用北京），European Union 跳过
_NATION_TO_COORD = {
    "China":                 (35.86,  104.19, "中国 / China"),
    "United States":         (37.09,  -95.71, "美国 / United States"),
    "United Arab Emirates":  (23.42,   53.85, "阿联酋 / UAE"),
    "Saudi Arabia":          (23.89,   45.08, "沙特 / Saudi Arabia"),
    "Japan":                 (36.20,  138.25, "日本 / Japan"),
    "Germany":               (51.17,   10.45, "德国 / Germany"),
    "Australia":             (-25.27, 133.78, "澳大利亚 / Australia"),
    "Australian":            (-25.27, 133.78, "澳大利亚 / Australia"),
    "Italy":                 (41.87,   12.57, "意大利 / Italy"),
    "Greece":                (39.07,   21.82, "希腊 / Greece"),
    "Netherlands":           (52.13,    5.29, "荷兰 / Netherlands"),
    "France":                (46.23,    2.21, "法国 / France"),
    "Singapore":             (1.35,   103.82, "新加坡 / Singapore"),
    "European Union":        None,            # 跳过
    # 台湾数据并入中国
    "Taiwan":                (35.86,  104.19, "中国 / China"),
    "Taiwan, China":         (35.86,  104.19, "中国 / China"),
    "Chinese Taipei":        (35.86,  104.19, "中国 / China"),
}


def _render_geo_map(geo_stats: dict, i18n: dict, lang: str, c: dict):
    nation_data = geo_stats.get("nation", {})
    if not nation_data:
        st.caption("暂无地理数据" if lang == "cn" else "No geographic data available")
        return

    # 合并坐标相同的条目（台湾并入中国）
    coord_counts: dict[tuple, int] = {}
    coord_labels: dict[tuple, str] = {}
    for nation, cnt in nation_data.items():
        info = _NATION_TO_COORD.get(nation)
        if info is None:
            continue
        lat, lon, label = info
        key = (lat, lon)
        coord_counts[key] = coord_counts.get(key, 0) + int(cnt)
        # 中文模式显示中文名，英文模式显示英文名
        if lang == "cn":
            coord_labels[key] = label.split(" / ")[0]
        else:
            parts = label.split(" / ")
            coord_labels[key] = parts[1] if len(parts) > 1 else parts[0]

    if not coord_counts:
        st.caption("暂无地理数据" if lang == "cn" else "No geographic data available")
        return

    lats   = [k[0] for k in coord_counts]
    lons   = [k[1] for k in coord_counts]
    counts = list(coord_counts.values())
    labels = [coord_labels[k] for k in coord_counts]
    max_cnt = max(counts) if counts else 1

    # 气泡大小：对数缩放，最小 12，最大 55
    import math
    sizes = [max(12, int(12 + 43 * math.log1p(v) / math.log1p(max_cnt))) for v in counts]

    dark = st.session_state.get("theme_mode", "dark") == "dark"
    land_color  = st.session_state.get("_map_land",  "#0b1829" if dark else "#eef2f9")
    ocean_color = st.session_state.get("_map_ocean", "#040c17" if dark else "#dce4ef")
    bubble_color = "#02bfe7" if dark else "#0b3d91"
    coast_color  = "rgba(2,191,231,0.25)" if dark else "rgba(11,61,145,0.18)"

    title_cn = "论文来源国家 / 地区分布（气泡大小 = 论文数）"
    title_en = "Paper Origin by Country / Region (bubble size = paper count)"

    fig = go.Figure(go.Scattergeo(
        lat=lats,
        lon=lons,
        text=labels,
        customdata=counts,
        mode="markers",
        marker=dict(
            size=sizes,
            color=bubble_color,
            opacity=0.75,
            line=dict(width=1.5, color="white"),
            sizemode="diameter",
        ),
        hovertemplate=(
            "<b>%{text}</b><br>" +
            ("论文数" if lang == "cn" else "Papers") +
            ": %{customdata}<extra></extra>"
        ),
    ))

    fig.update_layout(
        title=dict(
            text=title_cn if lang == "cn" else title_en,
            font=dict(color=c["font_color"], size=12),
            x=0.5,
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor=coast_color,
            showland=True,
            landcolor=land_color,
            showocean=True,
            oceancolor=ocean_color,
            showlakes=False,
            showrivers=False,
            showcountries=True,
            countrycolor="rgba(100,130,160,0.15)" if dark else "rgba(11,61,145,0.10)",
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=c["font_color"]),
        margin=dict(l=0, r=0, t=36, b=0),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="stats_geo_map")

    # 排行榜
    display_data: dict[str, int] = {}
    for (lat, lon), cnt in coord_counts.items():
        name = coord_labels[(lat, lon)]
        display_data[name] = display_data.get(name, 0) + cnt

    sorted_nations = sorted(display_data.items(), key=lambda x: x[1], reverse=True)
    rank_label = "📊 国家排行" if lang == "cn" else "📊 Country Ranking"
    with st.expander(rank_label, expanded=False):
        cols = st.columns(3, gap="small")
        for i, (nation, cnt) in enumerate(sorted_nations):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            with cols[i % 3]:
                st.markdown(
                    f"<div style='padding:4px 0;font-size:0.88rem'>"
                    f"{medal} <b>{nation}</b> — {cnt}</div>",
                    unsafe_allow_html=True,
                )


# ── 增长趋势分析 ──────────────────────────────────────────────────────────────

def _render_trend(trend_stats: dict, stats: dict, i18n: dict, lang: str, c: dict):
    # ── 折线图：各任务类型年度增长 ──
    title_line = "各任务类型年度数据集数量" if lang == "cn" else "Annual Dataset Count by Task Type"
    st.markdown(f"**{title_line}**")

    colors = {
        "VQA":            "#2563eb",
        "Caption":        "#10b981",
        "VG":             "#f59e0b",
        "Classification": "#ef4444",
        "Detection":      "#8b5cf6",
        "Segmentation":   "#06b6d4",
    }

    fig_line = go.Figure()
    for task, year_counts in trend_stats.items():
        if not year_counts:
            continue
        years  = list(year_counts.keys())
        counts = list(year_counts.values())
        fig_line.add_trace(go.Scatter(
            x=years, y=counts,
            mode="lines+markers",
            name=task,
            line=dict(color=colors.get(task, "#94a3b8"), width=2),
            marker=dict(size=7),
            hovertemplate=f"<b>{task}</b><br>%{{x}}: %{{y}} datasets<extra></extra>",
        ))

    fig_line.update_layout(
        **_base_layout(c, height=300),
        xaxis=dict(
            showgrid=False, tickangle=-30,
            tickfont=dict(color=c["font_color"]),
            title=dict(text="Year", font=dict(color=c["font_color"])),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=c["grid_color"],
            tickfont=dict(color=c["font_color"]),
            title=dict(text="Count", font=dict(color=c["font_color"])),
        ),
        legend=dict(
            font=dict(color=c["font_color"]),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False}, key="stats_trend_line")

    # ── 堆叠面积图：总体增长趋势 ──
    title_area = "数据集总量累计增长（堆叠面积）" if lang == "cn" else "Cumulative Dataset Growth (Stacked Area)"
    st.markdown(f"**{title_area}**")

    # 收集所有年份
    all_years: list[str] = sorted({y for yd in trend_stats.values() for y in yd})
    if not all_years:
        return

    fig_area = go.Figure()
    for task, year_counts in trend_stats.items():
        if not year_counts:
            continue
        y_vals = [year_counts.get(yr, 0) for yr in all_years]
        fig_area.add_trace(go.Scatter(
            x=all_years, y=y_vals,
            mode="lines",
            name=task,
            stackgroup="one",
            line=dict(color=colors.get(task, "#94a3b8"), width=0.5),
            fillcolor=colors.get(task, "#94a3b8"),
            opacity=0.75,
            hovertemplate=f"<b>{task}</b><br>%{{x}}: %{{y}}<extra></extra>",
        ))

    fig_area.update_layout(
        **_base_layout(c, height=280),
        xaxis=dict(
            showgrid=False, tickangle=-30,
            tickfont=dict(color=c["font_color"]),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=c["grid_color"],
            tickfont=dict(color=c["font_color"]),
            title=dict(text="Count", font=dict(color=c["font_color"])),
        ),
        legend=dict(
            font=dict(color=c["font_color"]),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False}, key="stats_trend_area")

    # ── 年度增速（同比增长率）──
    year_data = stats.get("year", {})
    if len(year_data) >= 2:
        title_growth = "年度数据集增速（同比）" if lang == "cn" else "Year-over-Year Growth Rate"
        st.markdown(f"**{title_growth}**")

        sorted_years = sorted(year_data.keys())
        growth_years, growth_rates = [], []
        for i in range(1, len(sorted_years)):
            prev = year_data[sorted_years[i - 1]]
            curr = year_data[sorted_years[i]]
            if prev > 0:
                rate = round((curr - prev) / prev * 100, 1)
                growth_years.append(sorted_years[i])
                growth_rates.append(rate)

        bar_colors = ["#10b981" if r >= 0 else "#ef4444" for r in growth_rates]
        fig_growth = go.Figure(go.Bar(
            x=growth_years, y=growth_rates,
            marker_color=bar_colors,
            hovertemplate="%{x}: %{y}%<extra></extra>",
            text=[f"{r:+.1f}%" for r in growth_rates],
            textposition="outside",
            textfont=dict(color=c["font_color"], size=10),
        ))
        fig_growth.add_hline(y=0, line_color="rgba(150,150,150,0.5)", line_width=1)
        fig_growth.update_layout(
            **_base_layout(c, height=240),
            xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(color=c["font_color"])),
            yaxis=dict(
                showgrid=True, gridcolor=c["grid_color"],
                tickfont=dict(color=c["font_color"]),
                ticksuffix="%",
            ),
        )
        st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False}, key="stats_trend_growth")


# ── 主入口 ────────────────────────────────────────────────────────────────────

def render_stats(i18n: dict, lang: str, chef):
    c = _chart_colors()
    stats      = chef.get_stats()
    geo_stats  = chef.get_geo_stats()
    trend_stats = chef.get_trend_stats()

    # Tab 布局：概览 / 地理分布 / 增长趋势
    tab_labels = (
        ["📊 概览", "🗺️ 地理分布", "📈 增长趋势"]
        if lang == "cn" else
        ["📊 Overview", "🗺️ Geographic", "📈 Trends"]
    )
    tab_overview, tab_geo, tab_trend = st.tabs(tab_labels)

    with tab_overview:
        _render_overview_charts(stats, i18n, c)

    with tab_geo:
        _render_geo_map(geo_stats, i18n, lang, c)

    with tab_trend:
        _render_trend(trend_stats, stats, i18n, lang, c)
