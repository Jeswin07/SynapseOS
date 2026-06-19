import numpy as np
import shap


class ModelExplainer:
    """
    Generates SHAP explanations for trained models.
    """

    def explain(
        self,
        *,
        model,
        preprocessor,
        dataframe,
        sample_index: int = 0,
        top_k: int = 10,
    ) -> dict:
        """
        Explain a single prediction.
        """

        # -------------------------
        # Transform input
        # -------------------------

        transformed = preprocessor.transform(
            dataframe,
        )

        if hasattr(
            transformed,
            "toarray",
        ):
            transformed = transformed.toarray()

        feature_names = list(
            preprocessor.get_feature_names_out()
        )

        # -------------------------
        # Select SHAP explainer
        # -------------------------

        if hasattr(
            model,
            "feature_importances_",
        ):

            explainer = shap.TreeExplainer(
                model,
            )

        else:

            explainer = shap.LinearExplainer(
                model,
                transformed,
            )

        # -------------------------
        # Compute SHAP values
        # -------------------------

        shap_values = explainer.shap_values(
            transformed,
        )

        prediction = float(
            model.predict(
                transformed[
                    sample_index:
                    sample_index + 1
                ]
            )[0]
        )

        # -------------------------
        # Base value
        # -------------------------

        base_value = explainer.expected_value

        if isinstance(
            base_value,
            np.ndarray,
        ):
            base_value = float(
                base_value[0]
            )

        # -------------------------
        # SHAP row
        # -------------------------

        row = shap_values[
            sample_index
        ]

        # -------------------------
        # Feature values
        # -------------------------

        raw_row = dataframe.row(
            sample_index,
            named=True,
        )

        feature_importance = []

        for index, value in enumerate(
            row,
        ):

            feature_name = (
                feature_names[index]
            )

            original_value = (
                raw_row.get(
                    feature_name,
                    None,
                )
            )

            feature_importance.append(
                {
                    "feature": feature_name,
                    "value": original_value,
                    "importance": float(value),
                    "absolute_importance": abs(
                        float(value)
                    ),
                }
            )

        feature_importance.sort(
            key=lambda item: item[
                "absolute_importance"
            ],
            reverse=True,
        )

        feature_importance = (
            feature_importance[
                :top_k
            ]
        )

        return {
            "prediction": prediction,
            "base_value": float(
                base_value,
            ),
            "features": feature_importance,
        }