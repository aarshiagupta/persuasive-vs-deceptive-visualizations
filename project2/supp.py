import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("allegations_202007271729.csv")

df = df[df["fado_type"].notna() & df["board_disposition"].notna()]

types_of_interest = ["Abuse of Authority", "Discourtesy", "Offensive Language", "Force"]
df_filtered = df[df["fado_type"].isin(types_of_interest)]

df_filtered["substantiated"] = df_filtered["board_disposition"].str.contains("Substantiated")

substantiation_rates = (
    df_filtered.groupby("fado_type")["substantiated"]
    .mean().mul(100).round(1).reset_index()
    .rename(columns={"substantiated": "rate"})
)

substantiation_rates["fado_type"] = pd.Categorical(
    substantiation_rates["fado_type"],
    categories=["Abuse of Authority", "Discourtesy", "Offensive Language", "Force"],
    ordered=True
)
substantiation_rates = substantiation_rates.sort_values("fado_type")

x = substantiation_rates["fado_type"]
y = substantiation_rates["rate"]

colors = ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#d62728"]


bars = go.Bar(
    x=x,
    y=y,
    text=y.map(str),
    textposition="outside",
    marker=dict(
        color=colors,
        opacity=[1, 1, 1, 1.0] 
    ),
    name="Substantiation Rate",
    hovertemplate="%{x}: %{y:.1f}%<extra></extra>"

)

trend_line = go.Scatter(
    x=x,
    y=y,
    mode="lines+markers+text",
    line=dict(dash="dash", color="black"),
    name="Accountability Gap",
    text=["", "", "", ""],
    textposition="top center",
    hovertemplate="%{x}: %{y:.1f}%<extra></extra>"
)

annotations = [
    dict(
        x="Force", y=15,
        text="Only 12.8% of force complaints are sustained",
        font=dict(size=13, color="red"), showarrow=True, arrowhead=4
    ),
    dict(
        x="Abuse of Authority", y=32,
        text="Abuse of Authority: 30.4%",
        showarrow=True, arrowhead=3
    ),
    dict(
    x="Offensive Language", y=28,
    text="<b>⬇ Nearly 3× difference</b>",
    showarrow=False,
    font=dict(size=14, color="black")
)
]

annotations.append(dict(
    xref='paper', yref='paper',
    x=0.5, y=1.15,
    text="Despite serious allegations, force complaints are rarely upheld.",
    showarrow=False, font=dict(size=14, color="gray")
))

layout = go.Layout(
    title=dict(
        text="<b>❗Force Complaints Rarely Substantiated — A 3x Gap in NYPD Accountability</b>",
        font=dict(size=22),
        x=0.5
    ),
    xaxis_title="Type of NYPD Complaint",
    yaxis_title="Substantiation Rate (%)",
    yaxis=dict(range=[10, 35]),
    plot_bgcolor="#fafafa",
    annotations=annotations
)

fig = go.Figure(data=[bars, trend_line], layout=layout)

fig.write_html("prop1_support_interactive.html")
