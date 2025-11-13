import plotly.graph_objects as go
import numpy as np
from typing import Tuple

def create_drift_visualization(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> go.Figure:
    """드리프트 데이터를 Plotly로 시각화"""

    fig = go.Figure()

    # Y축 범위 계산
    y_min, y_max = y.min(), y.max()
    y_range = y_max - y_min
    y_plot_min = y_min - y_range * 0.1
    y_plot_max = y_max + y_range * 0.1

    # 배경: drift 구간을 bar graph로 표시
    segment_boundaries = [0] + drift_points.tolist() + [len(X)]
    colors = ['rgba(100, 150, 255, 0.15)', 'rgba(255, 150, 100, 0.15)', 'rgba(150, 255, 150, 0.15)',
              'rgba(255, 200, 100, 0.15)', 'rgba(200, 150, 255, 0.15)', 'rgba(150, 255, 200, 0.15)']

    for i in range(len(segment_boundaries) - 1):
        start_idx = segment_boundaries[i]
        end_idx = segment_boundaries[i + 1]

        # 각 segment를 bar로 표시
        fig.add_trace(go.Bar(
            x=X[start_idx:end_idx],
            y=[y_plot_max - y_plot_min] * (end_idx - start_idx),
            base=y_plot_min,
            marker=dict(
                color=colors[i % len(colors)],
                line=dict(width=0)
            ),
            name=f'Segment {i+1}',
            showlegend=False,
            hoverinfo='skip'
        ))

    # 메인 라인 그래프
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name='Data',
        line=dict(color='rgb(50, 100, 180)', width=2),
        marker=dict(size=4, color='rgb(50, 100, 180)'),
        hovertemplate='Time: %{x}<br>Value: %{y:.2f}<extra></extra>'
    ))

    # 드리프트 발생 지점 표시
    for i, drift_point in enumerate(drift_points):
        fig.add_vline(
            x=X[drift_point],
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"Drift {i+1}",
            annotation_position="top"
        )

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
        yaxis_title="Value",
        hovermode='closest',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            range=[y_plot_min, y_plot_max]
        ),
        plot_bgcolor='white',
        barmode='overlay',
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
    colors = ['rgba(100, 150, 255, 0.15)', 'rgba(255, 150, 100, 0.15)', 'rgba(150, 255, 150, 0.15)',
              'rgba(255, 200, 100, 0.15)', 'rgba(200, 150, 255, 0.15)', 'rgba(150, 255, 200, 0.15)']

    for (row, col), drift_type in zip(positions, drift_types):
        if drift_type in drift_data_dict:
            X, y, drift_points = drift_data_dict[drift_type]

            # Y축 범위 계산
            y_min, y_max = y.min(), y.max()
            y_range = y_max - y_min
            y_plot_min = y_min - y_range * 0.1
            y_plot_max = y_max + y_range * 0.1

            # 배경: drift 구간을 bar로 표시
            segment_boundaries = [0] + drift_points.tolist() + [len(X)]

            for i in range(len(segment_boundaries) - 1):
                start_idx = segment_boundaries[i]
                end_idx = segment_boundaries[i + 1]

                fig.add_trace(
                    go.Bar(
                        x=X[start_idx:end_idx],
                        y=[y_plot_max - y_plot_min] * (end_idx - start_idx),
                        base=y_plot_min,
                        marker=dict(
                            color=colors[i % len(colors)],
                            line=dict(width=0)
                        ),
                        showlegend=False,
                        hoverinfo='skip'
                    ),
                    row=row, col=col
                )

            # 라인 그래프 추가
            fig.add_trace(
                go.Scatter(
                    x=X,
                    y=y,
                    mode='lines',
                    line=dict(color='rgb(50, 100, 180)', width=1.5),
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
                    line_width=1,
                    row=row, col=col
                )

    # 레이아웃 설정
    fig.update_xaxes(title_text="Time", showgrid=True, gridcolor='LightGray')
    fig.update_yaxes(title_text="Value", showgrid=True, gridcolor='LightGray')
    fig.update_layout(
        height=800,
        title_text="Concept Drift Types Comparison",
        showlegend=False,
        template='plotly_white',
        barmode='overlay',
        bargap=0
    )

    return fig
