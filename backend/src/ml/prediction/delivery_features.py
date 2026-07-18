"""Order-level features for delivery prediction."""

from __future__ import annotations

import pandas as pd


class DeliveryFeatureBuilder:
    """
    Delivery prediction works at ORDER level.

    One row = One order.
    """

    def build(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        frame = data.copy()

        return frame.fillna(0)