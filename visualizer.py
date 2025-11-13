import plotly.graph_objects as go
import numpy as np
from typing import Tuple

def create_drift_visualization(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> go.Figure:
    """드리프트 데이터를 Plotly로 시각화"""

    fig = go.Figure()

    # incremental drift는 연속 값으로 처리
    if drift_type == "incremental":
        # 0-1 사이 값을 색상으로 매핑
        colors = []
        for val in y:
            # 파란색(0)에서 초록색(1)로 점진적 변화
            blue = int(255 * (1 - val))
            green = int(255 * val)
            colors.append(f'rgb({blue}, {green}, 150)')

        fig.add_trace(go.Bar(
            x=X,
            y=np.ones(len(X)),
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            showlegend=False,
            hovertemplate='Time: %{x}<br>Value: %{customdata:.2f}<extra></extra>',
            customdata=y
        ))
    else:
        # 이진 분류 (0: 파란색, 1: 초록색)
        class_0_indices = np.where(y == 0)[0]
        class_1_indices = np.where(y == 1)[0]

        # Class 0 (파란색)
        if len(class_0_indices) > 0:
            fig.add_trace(go.Bar(
                x=X[class_0_indices],
                y=np.ones(len(class_0_indices)),
                marker=dict(color='rgb(70, 130, 180)', line=dict(width=0)),
                name='Class 0',
                showlegend=True,
                hovertemplate='Time: %{x}<br>Class: 0<extra></extra>'
            ))

        # Class 1 (초록색)
        if len(class_1_indices) > 0:
            fig.add_trace(go.Bar(
                x=X[class_1_indices],
                y=np.ones(len(class_1_indices)),
                marker=dict(color='rgb(60, 179, 113)', line=dict(width=0)),
                name='Class 1',
                showlegend=True,
                hovertemplate='Time: %{x}<br>Class: 1<extra></extra>'
            ))

    # 레이아웃 설정
    title_map = {
        "sudden": "Sudden Drift",
        "gradual": "Gradual Drift",
        "incremental": "Incremental Drift",
        "recurring": "Reoccurring Concepts"
    }

    fig.update_layout(
        title=dict(
            text=title_map.get(drift_type, "Concept Drift"),
            x=0.5,
            xanchor='center',
            font=dict(size=20, weight='bold')
        ),
        xaxis_title="Time",
        yaxis_title="Data distribution",
        hovermode='closest',
        template='plotly_white',
        height=400,
        showlegend=(drift_type != "incremental"),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 1.2]
        ),
        plot_bgcolor='white',
        bargap=0
    )

    return fig


def create_comparison_visualization(drift_data_dict: dict) -> go.Figure:
    """여러 드리프트 유형을 한 번에 비교"""
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Sudden Drift", "Gradual Drift", "Incremental Drift", "Reoccurring Concepts"),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    drift_types = ["sudden", "gradual", "incremental", "recurring"]

    for (row, col), drift_type in zip(positions, drift_types):
        if drift_type in drift_data_dict:
            X, y, drift_points = drift_data_dict[drift_type]

            if drift_type == "incremental":
                # Incremental drift: 연속 색상 변화
                colors = []
                for val in y:
                    blue = int(255 * (1 - val))
                    green = int(255 * val)
                    colors.append(f'rgb({blue}, {green}, 150)')

                fig.add_trace(
                    go.Bar(
                        x=X,
                        y=np.ones(len(X)),
                        marker=dict(color=colors, line=dict(width=0)),
                        showlegend=False
                    ),
                    row=row, col=col
                )
            else:
                # 이진 분류
                class_0_indices = np.where(y == 0)[0]
                class_1_indices = np.where(y == 1)[0]

                if len(class_0_indices) > 0:
                    fig.add_trace(
                        go.Bar(
                            x=X[class_0_indices],
                            y=np.ones(len(class_0_indices)),
                            marker=dict(color='rgb(70, 130, 180)', line=dict(width=0)),
                            showlegend=False
                        ),
                        row=row, col=col
                    )

                if len(class_1_indices) > 0:
                    fig.add_trace(
                        go.Bar(
                            x=X[class_1_indices],
                            y=np.ones(len(class_1_indices)),
                            marker=dict(color='rgb(60, 179, 113)', line=dict(width=0)),
                            showlegend=False
                        ),
                        row=row, col=col
                    )

    # 레이아웃 설정
    fig.update_xaxes(title_text="Time", showgrid=False, showticklabels=False)
    fig.update_yaxes(title_text="Data distribution", showgrid=False, showticklabels=False, range=[0, 1.2])
    fig.update_layout(
        height=800,
        title_text="Concept Drift Types Comparison",
        showlegend=False,
        bargap=0,
        template='plotly_white'
    )

    return fig
