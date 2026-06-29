"""Domain-specific business entities for GraphRAG."""

BUSINESS_ENTITIES: set[str] = {

    # Core Business
    "customer",
    "seller",
    "order",
    "product",
    "payment",
    "review",
    "category",
    "delivery",
    "marketplace",
    "dataset",

    # Olist datasets
    "olist_orders_dataset",
    "olist_order_items_dataset",
    "olist_order_reviews_dataset",
    "olist_order_payments_dataset",
    "olist_products_dataset",
    "olist_customers_dataset",
    "olist_sellers_dataset",
    "olist_geolocation_dataset",
    "olist_category_name_translation",
    "olist_ml_dataset",

    # Analytics
    "review_score",
    "payment_type",
    "payment_installments",
    "order_status",
    "freight_value",
    "price",
    "delivery_time",
    "estimated_delivery_date",

    # Business
    "logistics",
    "inventory",
    "fulfillment",
    "shipment",
    "warehouse",

    # Legal
    "consumer",
    "consumer protection code",
    "article 39",
    "article 6",
    "article 18",
}