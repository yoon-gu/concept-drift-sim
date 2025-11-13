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

    # incremental drift는 연속 값, 나머지는 이진 분류
    if drift_type == "incremental":
        # 연속 값 분석
        analysis["mean_y"] = float(np.mean(y))
        analysis["std_y"] = float(np.std(y))
        analysis["min_y"] = float(np.min(y))
        analysis["max_y"] = float(np.max(y))
    else:
        # 이진 분류 분석
        class_0_count = int(np.sum(y == 0))
        class_1_count = int(np.sum(y == 1))
        analysis["class_0_count"] = class_0_count
        analysis["class_1_count"] = class_1_count
        analysis["class_0_ratio"] = float(class_0_count / len(y))
        analysis["class_1_ratio"] = float(class_1_count / len(y))

    # 세그먼트별 분석
    segments = []
    segment_boundaries = [0] + drift_points.tolist() + [len(X)]

    for i in range(len(segment_boundaries) - 1):
        start = segment_boundaries[i]
        end = segment_boundaries[i + 1]

        segment_y = y[start:end]

        if drift_type == "incremental":
            # 연속 값 세그먼트 분석
            segments.append({
                "segment_id": i,
                "start_idx": int(start),
                "end_idx": int(end),
                "mean": float(np.mean(segment_y)),
                "std": float(np.std(segment_y))
            })
        else:
            # 이진 분류 세그먼트 분석
            class_0_count = int(np.sum(segment_y == 0))
            class_1_count = int(np.sum(segment_y == 1))
            total = len(segment_y)

            segments.append({
                "segment_id": i,
                "start_idx": int(start),
                "end_idx": int(end),
                "class_0_count": class_0_count,
                "class_1_count": class_1_count,
                "class_0_ratio": float(class_0_count / total) if total > 0 else 0.0,
                "class_1_ratio": float(class_1_count / total) if total > 0 else 0.0
            })

    analysis["segments"] = segments

    return analysis


def format_analysis_summary(analysis: Dict) -> str:
    """분석 결과를 사람이 읽기 쉬운 형식으로 포맷"""

    drift_type = analysis['drift_type']

    summary = f"""
## 드리프트 분석 결과

**드리프트 유형:** {drift_type.upper()}

**전체 데이터:**
- 총 샘플 수: {analysis['total_samples']}
- 드리프트 발생 횟수: {analysis['num_drift_points']}
"""

    if drift_type == "incremental":
        summary += f"""- 평균 값: {analysis['mean_y']:.2f}
- 표준편차: {analysis['std_y']:.2f}
- 범위: [{analysis['min_y']:.2f}, {analysis['max_y']:.2f}]
"""
    else:
        summary += f"""- Class 0 (파란색): {analysis['class_0_count']} 샘플 ({analysis['class_0_ratio']*100:.1f}%)
- Class 1 (초록색): {analysis['class_1_count']} 샘플 ({analysis['class_1_ratio']*100:.1f}%)
"""

    summary += "\n**세그먼트별 분석:**\n"

    for seg in analysis['segments']:
        if drift_type == "incremental":
            summary += f"""
**세그먼트 {seg['segment_id'] + 1}** (샘플 {seg['start_idx']}-{seg['end_idx']})
- 평균: {seg['mean']:.2f}
- 표준편차: {seg['std']:.2f}
"""
        else:
            summary += f"""
**세그먼트 {seg['segment_id'] + 1}** (샘플 {seg['start_idx']}-{seg['end_idx']})
- Class 0: {seg['class_0_count']} 샘플 ({seg['class_0_ratio']*100:.1f}%)
- Class 1: {seg['class_1_count']} 샘플 ({seg['class_1_ratio']*100:.1f}%)
"""

    return summary
