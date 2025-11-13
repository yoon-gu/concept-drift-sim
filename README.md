---
title: Concept Drift Simulator
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: mit
---

# Concept Drift Simulator

컨셉 드리프트(Concept Drift)의 4가지 주요 유형을 시뮬레이션하고 시각화하는 인터랙티브 웹 애플리케이션입니다.

**🚀 Live Demo:** [https://huggingface.co/spaces/yoon-gu/concept-drift-simulator](https://huggingface.co/spaces/yoon-gu/concept-drift-simulator)

## 주요 기능

4가지 컨셉 드리프트 유형 시뮬레이션:

1. **Sudden (급격한 드리프트)**: 특정 시점에서 데이터 분포가 갑자기 변경
2. **Gradual (점진적 드리프트)**: 이전 분포와 새 분포가 섞이며 천천히 전환
3. **Incremental (증분적 드리프트)**: 작은 단계로 변화가 발생하여 계단식 패턴 형성
4. **Recurring (반복적 드리프트)**: 이전 분포가 주기적으로 다시 나타남

## 기술 스택

- **Gradio**: 인터랙티브 UI 구성
- **Plotly**: 동적 시각화
- **NumPy**: 데이터 생성 및 분석

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
python app.py
```

브라우저에서 `http://localhost:7860` 접속

## 사용 방법

1. 왼쪽 패널에서 드리프트 유형 선택
2. "시뮬레이션 실행" 버튼 클릭
3. 오른쪽에 인터랙티브 Plotly 차트와 분석 결과 확인

## 프로젝트 구조

```
concept-drift/
├── app.py              # Gradio 애플리케이션
├── drift_simulator.py  # 드리프트 데이터 생성
├── visualizer.py       # Plotly 시각화
├── analyzer.py         # 드리프트 분석
├── requirements.txt    # 패키지 의존성
└── README.md
```

## Hugging Face Spaces

배포된 앱: https://huggingface.co/spaces/yoon-gu/concept-drift-simulator

## 라이선스

MIT License
