import streamlit as st
import plotly.graph_objects as go
import math

MAX_NODES = 30


def render_leakage_graph(source_name: str, results: list, i18n: dict):
    if not results:
        return

    dark = st.session_state.get("theme_mode", "dark") == "dark"
    font_color = "#f9fafb" if dark else "#1e293b"
    edge_color = "rgba(200,200,200,0.3)" if dark else "rgba(100,100,100,0.3)"

    st.markdown(f"**{i18n.get('leak_graph_title', '🕸️ 关联关系图')}**")

    # 节点过多时截断并提示
    truncated = len(results) > MAX_NODES
    display_results = results[:MAX_NODES]
    if truncated:
        st.caption(
            f"节点过多，仅展示前 {MAX_NODES} 个（共 {len(results)} 个）"
            if i18n.get("lang", "cn") != "en" else
            f"Too many nodes, showing first {MAX_NODES} of {len(results)}"
        )

    nodes_x, nodes_y, nodes_text, nodes_color, nodes_size = [], [], [], [], []
    edge_x, edge_y = [], []

    center_x, center_y = 0.0, 0.0
    nodes_x.append(center_x)
    nodes_y.append(center_y)
    nodes_text.append(source_name)
    nodes_color.append("#ef4444")
    nodes_size.append(22)

    n = len(display_results)
    radius = 2.2 if n > 10 else 1.8
    for i, entry in enumerate(display_results):
        angle = 2 * math.pi * i / n
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        nodes_x.append(x)
        nodes_y.append(y)
        label = entry["name"] if len(entry["name"]) <= 18 else entry["name"][:16] + "…"
        nodes_text.append(label)
        nodes_color.append("#2563eb")
        nodes_size.append(14)
        edge_x += [center_x, x, None]
        edge_y += [center_y, y, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(width=1.2, color=edge_color),
        hoverinfo="none"
    )

    node_trace = go.Scatter(
        x=nodes_x, y=nodes_y,
        mode="markers+text",
        text=nodes_text,
        textposition="top center",
        textfont=dict(size=10, color=font_color),
        hovertext=[source_name] + [e["name"] for e in display_results],
        hoverinfo="text",
        marker=dict(
            color=nodes_color,
            size=nodes_size,
            line=dict(width=1.5, color="white")
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            hovermode="closest",
        )
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
