from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class RegressionMetrics:
    r2: float
    mae: float  # Mean Absolute Error
    rmse: float  # Root Mean Squared Error


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
    clusters_size: dict[int, int]  # Ex: {0: 150, 1: 340}


@dataclass(frozen=True)
class ModelResult:
    model_id: str  # Nome do modelo para controle de versão
    model_name: str  # Ex: K-Means, Logistic Regression, XGBoost Regressor
    model_type: Literal["regression", "classification", "cluster"]
    minimum_threshold: float  # Limite para guardrail aceitar o modelo
    pass_guardrail: bool  # Calculado pelo backend
    trained_model: Any  # O objeto do modelo (Booster, Sklearn)
    metrics: RegressionMetrics | ClassificationMetrics | ClusterMetrics
    # Metadados opcionais
    features: list[str] = field(default_factory=list)
    hyperparameters: dict[str, Any] = field(default_factory=dict)
