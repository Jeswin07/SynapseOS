"""Feature builder registry."""

from src.models.dataset_enums import (
    BusinessDomain,
)

from src.ml.features.base import (
    BaseFeatureBuilder,
)

from src.ml.features.commerce import (
    CommerceFeatureBuilder,
)

from src.ml.features.generic import (
    GenericFeatureBuilder,
)


class FeatureBuilderRegistry:
    """
    Selects feature builder by domain.
    """


    BUILDERS = {

        BusinessDomain.ECOMMERCE:
            CommerceFeatureBuilder,

        BusinessDomain.RETAIL:
            CommerceFeatureBuilder,

    }


    @classmethod
    def get_builder(
        cls,
        domain: BusinessDomain,
    ) -> BaseFeatureBuilder:


        builder = (
            cls.BUILDERS
            .get(
                domain,
                GenericFeatureBuilder,
            )
        )


        return builder()