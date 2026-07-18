"""Prediction model trainer."""

from __future__ import annotations

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from src.ml.prediction.schemas import PredictionType
from src.ml.prediction.target_builder import (
    PredictionTargetBuilder,
)


class PredictionTrainer:
    """ML training pipeline."""

    def __init__(self) -> None:
        self.targets = PredictionTargetBuilder()

    def train(
        self,
        data: pd.DataFrame,
        prediction_type: PredictionType,
    ):
        print("=" * 80)
        print("TRAINER INPUT")
        print(data.columns.tolist())
        print(data.shape)
        print("=" * 80)

        features = self.prepare_features(data, prediction_type)

        target = self.targets.build(
            data,
            prediction_type,
        )

        print(target.value_counts())
        print(target.value_counts(normalize=True))

        X_train, X_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=0.2,
            random_state=42,
            stratify=target,
        )

        model = RandomForestClassifier(
            n_estimators=120,
            random_state=42,
            class_weight="balanced",
        )
        print(features.columns.tolist())
        model.fit(
            X_train,
            y_train,
        )
        importance = (
            pd.DataFrame(
                {
                    "feature": X_train.columns,
                    "importance": model.feature_importances_,
                }
            )
            .sort_values(
                "importance",
                ascending=False,
            )
        )

        print(importance.head(15))

        prediction = model.predict(X_test)

        probability = model.predict_proba(X_test)[:, 1]

        try:
            roc_auc = round(
                float(
                    roc_auc_score(
                        y_test,
                        probability,
                    )
                ),
                3,
            )
        except ValueError:
            roc_auc = None

        metrics = {
            "accuracy": round(
                float(
                    accuracy_score(
                        y_test,
                        prediction,
                    )
                ),
                3,
            ),
            "precision": round(
                float(
                    precision_score(
                        y_test,
                        prediction,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "recall": round(
                float(
                    recall_score(
                        y_test,
                        prediction,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "f1_score": round(
                float(
                    f1_score(
                        y_test,
                        prediction,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "roc_auc": roc_auc,
            
        }

        print("=" * 80)
        print("MODEL EVALUATION")
        for k, v in metrics.items():
            print(f"{k}: {v}")
        print("=" * 80)

        importance = (
            pd.DataFrame(
                {
                    "feature": X_train.columns,
                    "importance": model.feature_importances_,
                }
            )
            .sort_values("importance", ascending=False)
        )

        return (
            model,
            {
                "metrics": metrics,
                "feature_importance": (
                    importance.head(10)
                    .round(4)
                    .to_dict(orient="records")
                ),
            },
        )

    def prepare_features(
        self,
        data: pd.DataFrame,
        prediction_type: PredictionType,
    ):
        """
        Prepare model features while preventing
        target leakage.
        """

        drop = [
            "customer_id",
        ]

        if prediction_type == PredictionType.CUSTOMER_CHURN:
            drop.extend(
                [
                    "customer_id",
                    "last_order_date",
                ]
            )

        elif prediction_type == PredictionType.DELIVERY_DELAY:
            drop.extend(
                [
                    # IDs
                    "order_id",
                    "customer_id",

                    # Target
                    "delivery_delay_days",

                    # Post-delivery
                    "delivery_days",
                    "delivery_date",
                    "order_delivered_customer_date",
                    "actual_delivery_days",
                    "is_delayed",

                    # Estimated target helpers
                    "order_estimated_delivery_date",

                    # Reviews
                    "review_score",
                    "positive_review",
                    "negative_review",

                    # Existing ML outputs
                    "risk_score",
                    "risk_level",
                    "risk_reason",
                    "ml_target_delivery_risk",
                    "ml_target_customer_satisfaction",
                ]
            )

        return (
            data.drop(
                columns=[
                    c
                    for c in drop
                    if c in data.columns
                ],
                errors="ignore",
            )
            .select_dtypes(
                include=[
                    "number",
                    "bool",
                ]
            )
            .fillna(0)
        )