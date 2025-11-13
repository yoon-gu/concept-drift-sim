import gradio as gr
from drift_simulator import (
    generate_sudden_drift,
    generate_gradual_drift,
    generate_incremental_drift,
    generate_recurring_drift,
    get_drift_description
)
from visualizer import create_drift_visualization
from analyzer import analyze_drift, format_analysis_summary

def simulate_and_visualize(drift_type: str):
    """드리프트 시뮬레이션 + 시각화 + 분석"""

    # 드리프트 타입에 따라 데이터 생성
    if drift_type == "Sudden (급격한 드리프트)":
        X, y, drift_points = generate_sudden_drift(n_samples=1000, drift_point=500)
        drift_key = "sudden"
    elif drift_type == "Gradual (점진적 드리프트)":
        X, y, drift_points = generate_gradual_drift(n_samples=1000, drift_start=300, drift_end=700)
        drift_key = "gradual"
    elif drift_type == "Incremental (증분적 드리프트)":
        X, y, drift_points = generate_incremental_drift(n_samples=1000, n_steps=5)
        drift_key = "incremental"
    elif drift_type == "Recurring (반복적 드리프트)":
        X, y, drift_points = generate_recurring_drift(n_samples=1000, cycle_length=250)
        drift_key = "recurring"
    else:
        return None, "올바른 드리프트 타입을 선택해주세요."

    # 시각화
    fig = create_drift_visualization(X, y, drift_points, drift_key)

    # 분석
    analysis = analyze_drift(X, y, drift_points, drift_key)
    summary = format_analysis_summary(analysis)

    # 설명 추가
    description = get_drift_description(drift_key)
    full_summary = f"### {description}\n\n{summary}"

    return fig, full_summary


# Gradio 인터페이스
with gr.Blocks(title="Concept Drift Simulator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Concept Drift Simulator

        컨셉 드리프트(Concept Drift)의 4가지 유형을 시뮬레이션하고 시각화합니다.

        드리프트 유형을 선택하면 자동으로 데이터를 생성하고 인터랙티브 차트를 표시합니다.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            drift_type_radio = gr.Radio(
                choices=[
                    "Sudden (급격한 드리프트)",
                    "Gradual (점진적 드리프트)",
                    "Incremental (증분적 드리프트)",
                    "Recurring (반복적 드리프트)"
                ],
                label="드리프트 유형 선택",
                value="Sudden (급격한 드리프트)"
            )

            simulate_btn = gr.Button("시뮬레이션 실행", variant="primary")

        with gr.Column(scale=2):
            plot_output = gr.Plot(label="드리프트 시각화")

    analysis_output = gr.Markdown(label="분석 결과")

    # 이벤트 핸들러
    simulate_btn.click(
        fn=simulate_and_visualize,
        inputs=drift_type_radio,
        outputs=[plot_output, analysis_output]
    )

    # 초기 로드
    demo.load(
        fn=simulate_and_visualize,
        inputs=drift_type_radio,
        outputs=[plot_output, analysis_output]
    )

if __name__ == "__main__":
    demo.launch()
