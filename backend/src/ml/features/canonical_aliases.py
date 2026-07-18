"""
Enterprise canonical column registry.

Each canonical field maps to an ordered list of possible
column names.

IMPORTANT:
The order matters.

The first matching column becomes the canonical field.
"""

from __future__ import annotations

CANONICAL_ALIASES = {

    # ==========================
    # Revenue
    # ==========================

    "revenue": [

        # Olist
        "payment_value",

        # Flipkart
        "selling_price",

        "sale_price",

        "sellingprice",
        "order_total_inr",

        # Generic
        "revenue",
        "sales",
        "amount",
        "paid_amount",
        "gross_amount",
        "total_order_value",
        "selling_price",
        "discounted_price_inr",
        "sale_price",
        "invoice_amount",
        "order_total",
        "total_amount",
        "gross_sales",
        "net_sales",
        "subtotal",
        "final_amount",
        "price",

    ],

    # ==========================
    # Customer
    # ==========================

    "customer_id": [

        # Olist (MOST IMPORTANT)
        "customer_unique_id",

        "buyer_id",
        "client_id",
        "consumer_id",
        "user_id",

        # LAST
        "customer_id",

    ],

    # ==========================
    # Seller
    # ==========================

    "seller_id": [

        "seller_id",

        "merchant_id",

        "vendor_id",

        "supplier_id",

        "store_id",

        "partner_id",

    ],

    # ==========================
    # Product
    # ==========================

    "product_id": [

        "product_id",

        "sku",

        "item_id",

        "product",

    ],

    # ==========================
    # Category
    # ==========================

    "category": [

        # Olist
        "product_category_name",

        # Generic
        "category",

        "product_category",

        "product_type",

        "vertical",

        "department",

        "segment",

        "category_name",

        "category_id",

    ],

    # ==========================
    # Brand
    # ==========================

    "brand": [

        "brand",

        "manufacturer",

        "company",

    ],

    # ==========================
    # Quantity
    # ==========================

    "quantity": [

        "quantity",

        "qty",

        "units",

    ],

    # ==========================
    # Discount
    # ==========================

    "discount": [

        "discount",

        "discount_amount",

        "discount_value",

        "coupon_discount",

        "discount_percent",

    ],

    # ==========================
    # Rating
    # ==========================

    "review_score": [

        # Olist
        "review_score",

        # Generic
        "product_rating",
        "seller_rating",
        "rating",

        "stars",

        "customer_rating",

        "feedback_score",

        "score",

    ],

    # ==========================
    # Order Date
    # ==========================

    "order_date": [

        # Olist
        "order_purchase_timestamp",

        # Generic
        "purchase_date",

        "order_date",

        "transaction_date",

        "invoice_date",

        "created_at",

        "date",

    ],

    # ==========================
    # Delivery Date
    # ==========================

    "delivery_date": [

        # Olist
        "order_delivered_customer_date",

        # Generic
        "delivery_date",

        "delivered_date",

        "ship_date",

        "dispatch_date",

    ],

    # ==========================
    # Estimated Delivery
    # ==========================

    "estimated_delivery_date": [

        "order_estimated_delivery_date",

        "estimated_delivery_date",

    ],

    # ==========================
    # State
    # ==========================

    "state": [

        # Olist
        "customer_state",

        # Generic
        "state",

        "state_x",

        "seller_state",

        "province",

        "region",

    ],

    # ==========================
    # City
    # ==========================

    "city": [

        # Olist
        "customer_city",

        # Generic
        "city",

        "town",

        "city_x",

        "seller_city",


    ],

}