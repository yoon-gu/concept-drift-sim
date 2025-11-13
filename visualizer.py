import plotly.graph_objects as go
import numpy as np
from typing import Tuple

def create_drift_visualization(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> go.Figure:
    """드리프트 데이터를 Plotly로 시각화"""

    fig = go.Figure()

    # 메인 데이터 scatter plot
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='markers',
        name='Data Points',
        marker=dict(
            size=4,
            color=np.arange(len(X)),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Time")
        ),
        hovertemplate='X: %{x:.2f}<br>y: %{y:.2f}<extra></extra>'
    ))

    # 드리프트 발생 지점 표시
    y_min, y_max = y.min(), y.max()
    y_range = y_max - y_min

    for i, drift_point in enumerate(drift_points):
        fig.add_vline(
            x=X[drift_point],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Drift {i+1}",
            annotation_position="top"
        )

    # 레이아웃 설정
    title_map = {
        "sudden": "Sudden (Abrupt) Drift - 급격한 드리프트",
        "gradual": "Gradual Drift - 점진적 드리프트",
        "incremental": "Incremental Drift - 증분적 드리프트",
        "recurring": "Recurring Drift - 반복적 드리프트"
    }

    fig.update_layout(
        title=dict(
            text=title_map.get(drift_type, "Concept Drift"),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Feature (X)",
        yaxis_title="Target (y)",
        hovermode='closest',
        template='plotly_white',
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig


def create_comparison_visualization(drift_data_dict: dict) -> go.Figure:
    """여러 드리프트 유형을 한 번에 비교"""
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Sudden Drift", "Gradual Drift", "Incremental Drift", "Recurring Drift")
    )

    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    drift_types = ["sudden", "gradual", "incremental", "recurring"]

    for (row, col), drift_type in zip(positions, drift_types):
        if drift_type in drift_data_dict:
            X, y, drift_points = drift_data_dict[drift_type]

            fig.add_trace(
                go.Scatter(
                    x=X,
                    y=y,
                    mode='markers',
                    marker=dict(size=3, color=np.arange(len(X)), colorscale='Viridis'),
                    showlegend=False
                ),
                row=row, col=col
            )

            # 드리프트 지점 표시
            for drift_point in drift_points:
                fig.add_vline(
                    x=X[drift_point],
                    line_dash="dash",
                    line_color="red",
                    row=row, col=col
                )

    fig.update_xaxes(title_text="X")
    fig.update_yaxes(title_text="y")
    fig.update_layout(height=800, title_text="Concept Drift Types Comparison", showlegend=False)

    return fig
