import plotly.graph_objects as go
import numpy as np
from typing import Tuple
from plotly.subplots import make_subplots

def create_drift_visualization(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> go.Figure:
    """드리프트 데이터를 Plotly로 시각화"""

    # 2개의 row로 subplot 생성
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.1,
        subplot_titles=("Time Series Data", "Drift Detection (20-sample windows)")
    )

    # Y축 범위 계산
    y_min, y_max = y.min(), y.max()
    y_range = y_max - y_min
    y_plot_min = y_min - y_range * 0.1
    y_plot_max = y_max + y_range * 0.1

    # === 첫 번째 row: 시계열 데이터 ===
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
        ), row=1, col=1)

    # 메인 라인 그래프
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name='Data',
        line=dict(color='rgb(50, 100, 180)', width=2),
        marker=dict(size=4, color='rgb(50, 100, 180)'),
        hovertemplate='Time: %{x}<br>Value: %{y:.2f}<extra></extra>'
    ), row=1, col=1)

    # 드리프트 발생 지점 표시
    for i, drift_point in enumerate(drift_points):
        fig.add_vline(
            x=X[drift_point],
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"Drift {i+1}",
            annotation_position="top",
            row=1, col=1
        )

    # === 두 번째 row: Drift Classification ===
    window_size = 20
    n_windows = len(X) // window_size
    window_centers = []
    drift_detected = []

    for i in range(n_windows):
        start_idx = i * window_size
        end_idx = (i + 1) * window_size
        window_center = (start_idx + end_idx) / 2

        # 이 window에 drift point가 포함되어 있는지 확인
        has_drift = any(start_idx <= dp < end_idx for dp in drift_points)

        window_centers.append(window_center)
        drift_detected.append(1 if has_drift else 0)

    # Drift detection bar graph
    bar_colors = ['rgba(255, 80, 80, 0.7)' if d == 1 else 'rgba(100, 200, 100, 0.7)'
                  for d in drift_detected]

    fig.add_trace(go.Bar(
        x=window_centers,
        y=drift_detected,
        marker=dict(color=bar_colors, line=dict(width=0)),
        name='Drift Detected',
        showlegend=False,
        hovertemplate='Window: %{x:.0f}<br>Drift: %{y}<extra></extra>',
        width=window_size * 0.9
    ), row=2, col=1)

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
        hovermode='closest',
        template='plotly_white',
        height=700,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        barmode='overlay',
        bargap=0
    )

    # 첫 번째 subplot 축 설정
    fig.update_xaxes(title_text="Time", showgrid=True, gridwidth=1, gridcolor='LightGray', row=1, col=1)
    fig.update_yaxes(title_text="Value", showgrid=True, gridwidth=1, gridcolor='LightGray',
                     range=[y_plot_min, y_plot_max], row=1, col=1)

    # 두 번째 subplot 축 설정
    fig.update_xaxes(title_text="Time", showgrid=True, gridwidth=1, gridcolor='LightGray', row=2, col=1)
    fig.update_yaxes(title_text="Drift", showgrid=True, gridwidth=1, gridcolor='LightGray',
                     range=[-0.2, 1.5], tickvals=[0, 1], ticktext=['No Drift', 'Drift'], row=2, col=1)

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
