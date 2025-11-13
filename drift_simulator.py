import numpy as np
from typing import Tuple

def generate_sudden_drift(n_samples: int = 1000, drift_point: int = 500) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """급격한 드리프트: t 시점에서 갑자기 데이터 분포 변경"""
    X = np.arange(n_samples)  # 시간 인덱스
    y = np.zeros(n_samples, dtype=int)

    # Before drift: class 0 (파란색)
    y[:drift_point] = 0

    # After drift: class 1 (초록색)
    y[drift_point:] = 1

    drift_points = np.array([drift_point])
    return X, y, drift_points


def generate_gradual_drift(n_samples: int = 1000, drift_start: int = 300, drift_end: int = 700) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """점진적 드리프트: 두 분포가 섞이며 천천히 전환"""
    X = np.arange(n_samples)  # 시간 인덱스
    y = np.zeros(n_samples, dtype=int)

    # Before drift: class 0 (파란색)
    y[:drift_start] = 0

    # Gradual transition: class 0과 class 1이 섞임
    transition_length = drift_end - drift_start
    for i in range(drift_start, drift_end):
        # 점진적으로 class 1의 비율 증가
        weight = (i - drift_start) / transition_length
        y[i] = 1 if np.random.random() < weight else 0

    # After drift: class 1 (초록색)
    y[drift_end:] = 1

    drift_points = np.array([drift_start, drift_end])
    return X, y, drift_points


def generate_incremental_drift(n_samples: int = 1000, n_steps: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """증분적 드리프트: 계단식으로 작은 변화가 누적"""
    X = np.arange(n_samples)  # 시간 인덱스
    y = np.zeros(n_samples)  # 연속 값 (시각화를 위해)

    step_size = n_samples // n_steps
    drift_points = []

    for step in range(n_steps):
        start_idx = step * step_size
        end_idx = (step + 1) * step_size if step < n_steps - 1 else n_samples

        # 각 단계마다 0에서 1로 점진적 변화
        value = step / (n_steps - 1)
        y[start_idx:end_idx] = value

        if step > 0:
            drift_points.append(start_idx)

    return X, y, np.array(drift_points)


def generate_recurring_drift(n_samples: int = 1000, cycle_length: int = 250) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """반복적 드리프트: 이전 분포가 주기적으로 재등장"""
    X = np.arange(n_samples)  # 시간 인덱스
    y = np.zeros(n_samples, dtype=int)

    drift_points = []

    for i in range(n_samples):
        cycle_pos = i % cycle_length

        if cycle_pos < cycle_length // 2:
            # Concept A: class 0 (파란색)
            y[i] = 0
        else:
            # Concept B: class 1 (초록색)
            y[i] = 1

        if cycle_pos == cycle_length // 2:
            drift_points.append(i)

    return X, y, np.array(drift_points)


def get_drift_description(drift_type: str) -> str:
    """드리프트 유형별 설명 반환"""
    descriptions = {
        "sudden": "급격한 드리프트: 특정 시점에서 데이터 분포가 갑자기 변경됩니다. 예: 팬데믹, 정책 변경 등",
        "gradual": "점진적 드리프트: 이전 분포와 새 분포가 섞이며 천천히 전환됩니다. 전환 기간 동안 두 컨셉이 공존합니다.",
        "incremental": "증분적 드리프트: 작은 단계로 변화가 발생하여 계단식 패턴을 형성합니다.",
        "recurring": "반복적 드리프트: 이전 분포가 주기적으로 다시 나타납니다. 계절성이나 주기적 패턴에서 발생합니다."
    }
    return descriptions.get(drift_type, "알 수 없는 드리프트 유형")
