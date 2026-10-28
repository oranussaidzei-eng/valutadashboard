
import plotly.express as px

NAVY = "#172B45"
TEXT = "#30343A"
MUTED = "#7C8490"
GRID = "#F0F1F2"


def style_chart(fig):
    # Apply the same design to all charts
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color=TEXT
        ),
        margin=dict(l=35, r=25, t=25, b=40),
        hovermode="x unified",
        showlegend=False,
        height=390,
        bargap=0.45,
    )

    fig.update_xaxes(
        showgrid=False,
        showline=False,
        ticks="",
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
        automargin=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        showline=False,
        ticks="",
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
        automargin=True,
    )

    return fig


def create_history_chart(df):
    # Create historical exchange rate line chart
    fig = px.line(
        df,
        x="date",
        y="rate",
        labels={
            "date": "Date",
            "rate": "Exchange Rate",
        },
    )

    fig.update_traces(
        line=dict(color=NAVY, width=2.5),
        hovertemplate=(
            "%{x}<br>Rate: %{y:.5f}<extra></extra>"
        ),
    )

    style_chart(fig)

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "responsive": True,
            "displayModeBar": False,
        },
    )


def create_monthly_average_chart(monthly_data):
    # Create monthly average bar chart
    fig = px.bar(
        x=monthly_data.index,
        y=monthly_data.values,
        labels={
            "x": "Month",
            "y": "Average Exchange Rate",
        },
    )

    fig.update_traces(
        marker_color=NAVY,
        marker_line_width=0,
        opacity=0.9,
        hovertemplate=(
            "%{x}<br>Average: %{y:.5f}<extra></extra>"
        ),
    )

    style_chart(fig)

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "responsive": True,
            "displayModeBar": False,
        },
    )
