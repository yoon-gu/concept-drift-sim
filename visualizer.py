import plotly.graph_objects as go
import numpy as np
from typing import Tuple

def create_drift_visualization(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> go.Figure:
    """드리프트 데이터를 Plotly로 시각화"""

    fig = go.Figure()

    # incremental drift는 연속 값으로 처리
    if drift_type == "incremental":
        # 색상 리스트 생성
        colors = []
        for val in y:
            # 파란색(0)에서 초록색(1)로 점진적 변화
            r = int(50 + 50 * val)
            g = int(100 + 79 * val)
            b = int(200 - 87 * val)
            colors.append(f'rgb({r}, {g}, {b})')

        # Scatter로 표현 (색상 영역)
        fig.add_trace(go.Scatter(
            x=X,
            y=np.ones(len(X)),
            mode='markers',
            marker=dict(
                color=colors,
                size=10,
                symbol='square',
                line=dict(width=0)
            ),
            showlegend=False,
            hovertemplate='Time: %{x}<br>Value: %{customdata:.2f}<extra></extra>',
            customdata=y
        ))
    else:
        # 이진 분류 (0: 파란색, 1: 초록색)
        # Class 0 (파란색)
        class_0_mask = y == 0
        if np.any(class_0_mask):
            fig.add_trace(go.Scatter(
                x=X[class_0_mask],
                y=np.ones(np.sum(class_0_mask)),
                mode='markers',
                marker=dict(color='rgb(65, 105, 225)', size=10, symbol='square', line=dict(width=0)),
                name='Class 0',
                showlegend=True,
                hovertemplate='Time: %{x}<br>Class: 0<extra></extra>'
            ))

        # Class 1 (초록색)
        class_1_mask = y == 1
        if np.any(class_1_mask):
            fig.add_trace(go.Scatter(
                x=X[class_1_mask],
                y=np.ones(np.sum(class_1_mask)),
                mode='markers',
                marker=dict(color='rgb(50, 205, 50)', size=10, symbol='square', line=dict(width=0)),
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
            font=dict(size=20)
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
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0.5, 1.5]
        ),
        plot_bgcolor='white'
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
                    r = int(50 + 50 * val)
                    g = int(100 + 79 * val)
                    b = int(200 - 87 * val)
                    colors.append(f'rgb({r}, {g}, {b})')

                fig.add_trace(
                    go.Scatter(
                        x=X,
                        y=np.ones(len(X)),
                        mode='markers',
                        marker=dict(color=colors, size=5, symbol='square', line=dict(width=0)),
                        showlegend=False
                    ),
                    row=row, col=col
                )
            else:
                # 이진 분류
                class_0_mask = y == 0
                class_1_mask = y == 1

                if np.any(class_0_mask):
                    fig.add_trace(
                        go.Scatter(
                            x=X[class_0_mask],
                            y=np.ones(np.sum(class_0_mask)),
                            mode='markers',
                            marker=dict(color='rgb(65, 105, 225)', size=5, symbol='square', line=dict(width=0)),
                            showlegend=False
                        ),
                        row=row, col=col
                    )

                if np.any(class_1_mask):
                    fig.add_trace(
                        go.Scatter(
                            x=X[class_1_mask],
                            y=np.ones(np.sum(class_1_mask)),
                            mode='markers',
                            marker=dict(color='rgb(50, 205, 50)', size=5, symbol='square', line=dict(width=0)),
                            showlegend=False
                        ),
                        row=row, col=col
                    )

    # 레이아웃 설정
    fig.update_xaxes(title_text="Time", showgrid=False, showticklabels=False)
    fig.update_yaxes(title_text="Data distribution", showgrid=False, showticklabels=False, range=[0.5, 1.5])
    fig.update_layout(
        height=800,
        title_text="Concept Drift Types Comparison",
        showlegend=False,
        template='plotly_white'
    )

    return fig
