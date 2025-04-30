import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("allegations_202007271729.csv")


df_filtered = df[df["fado_type"].notna()].copy()
df_filtered["fado_type"] = df_filtered["fado_type"].str.strip()

complaint_counts = (
    df_filtered["fado_type"]
    .value_counts()
    .loc[["Discourtesy", "Force", "Abuse of Authority"]]
    .reset_index()
)
complaint_counts.columns = ["fado_type", "num_complaints"]

x_vals = complaint_counts["fado_type"]
y_vals = complaint_counts["num_complaints"]

hover_texts = [
    "<b>Discourtesy</b><br>4,677 reports<br><span style='color:#777;'>Often tone-related</span>",
    "<span style='background-color:rgba(243,156,18,0.9); padding:4px 8px; border-radius:4px; color:white; font-size:13px;'>"
    "<b>Only 7,636 reports</b><br>Rare and frequently dismissed</span>",
    "<b>Abuse of Authority</b><br>20,292 reports<br>"
]

colors = ["#c0c0c0", "#f39c12", "#c0c0c0"]


bars = go.Bar(
    x=x_vals,
    y=y_vals,
    marker_color=colors,
    hovertext=hover_texts,
    hoverinfo="text",
    name="Substantiation Rate" 
)

trend_line = go.Scatter(
    x=x_vals,
    y=[4600, 7200, 20292],
    mode="lines+markers",
    line=dict(color="black", dash="dot", shape="spline"),
    marker=dict(symbol="circle", size=6),
    hoverinfo="skip",
    name="Force Complaint Cliff" 
)



annotations = [
    dict(
        xref='paper', yref='paper',
        x=0.5, y=1.3,
        text="<b style='font-size:26px;'>🟠 Force Complaints: Not Evidence of a Crisis</b>",
        showarrow=False,
        font=dict(size=26),
        xanchor="center"
    ),
    dict(
        xref='paper', yref='paper',
        x=0.5, y=1.18,
        text="Force reports are too minimal and isolated to justify sweeping conclusions.",
        showarrow=False,
        font=dict(size=15, color="#444"),
        xanchor="center"
    ),
    dict(
        x="Force",
        y=8200,
        text="⬇ Force complaints are exceptionally low",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(size=14, color="#e67e22")
    ),
    dict(
        x="Abuse of Authority",
        y=21100,
        text="⬆ Highest complaint type",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(size=14, color="#444")
    ),
    dict(
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.75,
        text="<b>“Most cops I know never got a single Force complaint.”</b><br>— Anonymous NYPD Officer",
        showarrow=False,
        font=dict(size=13),
        align="center",
        bordercolor="#bbb",
        borderwidth=1,
        bgcolor="#f9f9f9",
        opacity=0.95,
        xanchor="center"
    )
    
]

layout = go.Layout(
    xaxis_title="Type of NYPD Complaint",
    yaxis_title="Number of Complaints Filed",
    yaxis=dict(range=[6000, 23000], gridcolor="#eee"),
    plot_bgcolor="#ffffff",
    annotations=annotations,
    showlegend=True, 
    legend=dict(
        orientation="h",
        x=0.65,
        y=1.15
    ),
    font=dict(family="Arial", size=13)
)

layout.update(annotations=annotations)
layout.update(
    legend=dict(
        orientation="h",
        x=1,
        xanchor="right",
        y=1.12,
        font=dict(size=12)
    )
)

fig = go.Figure(data=[bars, trend_line], layout=layout)
fig.write_html("prop1_opp_interactive.html")
