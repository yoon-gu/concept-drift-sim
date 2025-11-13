import numpy as np
from typing import Dict, Tuple

def analyze_drift(X: np.ndarray, y: np.ndarray, drift_points: np.ndarray, drift_type: str) -> Dict[str, any]:
    """드리프트 데이터 분석"""

    analysis = {
        "drift_type": drift_type,
        "total_samples": len(X),
        "num_drift_points": len(drift_points),
        "drift_locations": drift_points.tolist() if len(drift_points) > 0 else [],
    }

    # 전체 통계
    analysis["mean_y"] = float(np.mean(y))
    analysis["std_y"] = float(np.std(y))
    analysis["min_y"] = float(np.min(y))
    analysis["max_y"] = float(np.max(y))

    # 세그먼트별 분석
    segments = []
    segment_boundaries = [0] + drift_points.tolist() + [len(X)]

    for i in range(len(segment_boundaries) - 1):
        start = segment_boundaries[i]
        end = segment_boundaries[i + 1]

        segment_y = y[start:end]
        segment_X = X[start:end]

        # 선형 회귀 계수 계산 (기울기)
        if len(segment_X) > 1:
            coeffs = np.polyfit(segment_X, segment_y, 1)
            slope = float(coeffs[0])
            intercept = float(coeffs[1])
        else:
            slope = 0.0
            intercept = float(segment_y[0]) if len(segment_y) > 0 else 0.0

        segments.append({
            "segment_id": i,
            "start_idx": int(start),
            "end_idx": int(end),
            "mean": float(np.mean(segment_y)),
            "std": float(np.std(segment_y)),
            "slope": slope,
            "intercept": intercept
        })

    analysis["segments"] = segments

    return analysis


def format_analysis_summary(analysis: Dict) -> str:
    """분석 결과를 사람이 읽기 쉬운 형식으로 포맷"""

    summary = f"""
## 드리프트 분석 결과

**드리프트 유형:** {analysis['drift_type'].upper()}

**전체 데이터:**
- 총 샘플 수: {analysis['total_samples']}
- 드리프트 발생 횟수: {analysis['num_drift_points']}
- 평균: {analysis['mean_y']:.2f}
- 표준편차: {analysis['std_y']:.2f}
- 범위: [{analysis['min_y']:.2f}, {analysis['max_y']:.2f}]

**세그먼트별 분석:**
"""

    for seg in analysis['segments']:
        summary += f"""
**세그먼트 {seg['segment_id'] + 1}** (샘플 {seg['start_idx']}-{seg['end_idx']})
- 평균: {seg['mean']:.2f}
- 표준편차: {seg['std']:.2f}
- 관계식: y = {seg['slope']:.2f}x + {seg['intercept']:.2f}
"""

    return summary
