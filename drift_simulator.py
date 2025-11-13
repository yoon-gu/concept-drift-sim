import numpy as np
from typing import Tuple

def generate_sudden_drift(n_samples: int = 1000, drift_point: int = 500) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """급격한 드리프트: t 시점에서 갑자기 데이터 분포 변경"""
    X = np.arange(n_samples)
    y = np.zeros(n_samples)

    # Before drift: y = 2 + sin(X/50) + noise
    y[:drift_point] = 2 + np.sin(X[:drift_point] / 50) + np.random.normal(0, 0.3, drift_point)

    # After drift: y = 5 - sin(X/50) + noise (완전히 다른 패턴)
    y[drift_point:] = 5 - np.sin(X[drift_point:] / 50) + np.random.normal(0, 0.3, n_samples - drift_point)

    drift_points = np.array([drift_point])
    return X, y, drift_points


def generate_gradual_drift(n_samples: int = 1000, drift_start: int = 300, drift_end: int = 700) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """점진적 드리프트: 두 분포가 섞이며 천천히 전환"""
    X = np.arange(n_samples)
    y = np.zeros(n_samples)

    # Before drift: y = 2 + sin(X/50) + noise
    y[:drift_start] = 2 + np.sin(X[:drift_start] / 50) + np.random.normal(0, 0.3, drift_start)

    # Gradual transition: 점진적으로 변환
    transition_length = drift_end - drift_start
    for i in range(drift_start, drift_end):
        weight = (i - drift_start) / transition_length
        old_concept = 2 + np.sin(X[i] / 50) + np.random.normal(0, 0.3)
        new_concept = 5 - np.sin(X[i] / 50) + np.random.normal(0, 0.3)
        y[i] = (1 - weight) * old_concept + weight * new_concept

    # After drift: y = 5 - sin(X/50) + noise
    y[drift_end:] = 5 - np.sin(X[drift_end:] / 50) + np.random.normal(0, 0.3, n_samples - drift_end)

    drift_points = np.array([drift_start, drift_end])
    return X, y, drift_points


def generate_incremental_drift(n_samples: int = 1000, n_steps: int = 5) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """증분적 드리프트: 계단식으로 작은 변화가 누적"""
    X = np.arange(n_samples)
    y = np.zeros(n_samples)

    step_size = n_samples // (n_steps + 1)
    drift_points = []

    for step in range(n_steps + 1):
        start_idx = step * step_size
        end_idx = (step + 1) * step_size if step < n_steps else n_samples

        # 각 단계마다 평균이 조금씩 변화
        mean_shift = 2 + (step / n_steps) * 3  # 2에서 5로 점진적 변화
        y[start_idx:end_idx] = mean_shift + np.sin(X[start_idx:end_idx] / 50) + np.random.normal(0, 0.3, end_idx - start_idx)

        if step > 0:
            drift_points.append(start_idx)

    return X, y, np.array(drift_points)


def generate_recurring_drift(n_samples: int = 1000, cycle_length: int = 250) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """반복적 드리프트: 이전 분포가 주기적으로 재등장"""
    X = np.arange(n_samples)
    y = np.zeros(n_samples)

    drift_points = []

    for i in range(n_samples):
        cycle_pos = i % cycle_length

        if cycle_pos < cycle_length // 2:
            # Concept A: y = 2 + sin(X/50) + noise
            y[i] = 2 + np.sin(X[i] / 50) + np.random.normal(0, 0.3)
        else:
            # Concept B: y = 5 - sin(X/50) + noise
            y[i] = 5 - np.sin(X[i] / 50) + np.random.normal(0, 0.3)

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
