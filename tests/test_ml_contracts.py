from src.ml_contracts import (
    ClassificationMetrics,
    ClusterMetrics,
    ModelResult,
    RegressionMetrics,
)


def test_model_result_with_regression_metrics() -> None:
    metrics = RegressionMetrics(r2=0.92, mae=0.10, rmse=0.15)
    result = ModelResult(
        model_id="reg-001",
        model_name="LinearRegression",
        model_type="regression",
        minimum_threshold=0.8,
        pass_guardrail=True,
        trained_model=object(),
        metrics=metrics,
        features=["x1", "x2"],
    )
    assert result.metrics.r2 == 0.92
    assert result.pass_guardrail is True


def test_model_result_with_classification_metrics() -> None:
    metrics = ClassificationMetrics(
        accuracy=0.89,
        f1_score=0.88,
        auc_roc=0.90,
        precision=0.87,
        recall=0.89,
    )
    result = ModelResult(
        model_id="clf-001",
        model_name="LogisticRegression",
        model_type="classification",
        minimum_threshold=0.75,
        pass_guardrail=True,
        trained_model=object(),
        metrics=metrics,
    )
    assert result.model_type == "classification"
    assert result.metrics.accuracy == 0.89


def test_model_result_with_cluster_metrics() -> None:
    metrics = ClusterMetrics(
        silhouette=0.45,
        num_clusters=3,
        clusters_size={0: 10, 1: 20, 2: 30},
    )
    result = ModelResult(
        model_id="clu-001",
        model_name="KMeans",
        model_type="cluster",
        minimum_threshold=0.40,
        pass_guardrail=True,
        trained_model=object(),
        metrics=metrics,
    )
    assert result.metrics.num_clusters == 3
