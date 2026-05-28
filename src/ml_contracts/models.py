from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class RegressionMetrics:
    r2: float
    mae: float
    rmse: float


@dataclass(frozen=True)
class ClassificationMetrics:
    accuracy: float
    f1_score: float
    auc_roc: float
    precision: float
    recall: float


@dataclass(frozen=True)
class ClusterMetrics:
    silhouette: float
    num_clusters: int
    clusters_size: dict[int, int]


MetricPayload = RegressionMetrics | ClassificationMetrics | ClusterMetrics
ModelType = Literal["regression", "classification", "cluster"]


@dataclass(frozen=True)
class ModelResult[T: MetricPayload]:
    model_id: str
    model_name: str
    model_type: ModelType
    minimum_threshold: float
    pass_guardrail: bool
    trained_model: Any
    metrics: T
    features: list[str] = field(default_factory=list)
    hyperparameters: dict[str, Any] = field(default_factory=dict)
