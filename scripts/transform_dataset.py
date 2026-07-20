"""
GlobalMart Dataset Transformation

Transforms the original Olist dataset into a modern GlobalMart
Enterprise Commerce Dataset.

Features
--------
1. Shift dates to 2024–2025
2. Globalize customer & seller locations
3. Translate product categories
4. Validate transformed data
5. Export cleaned datasets

Author: SynapseOS
"""

from pathlib import Path
import logging
import pandas as pd
import hashlib
import json
from datetime import datetime
from pandas.tseries.offsets import DateOffset

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "datasets" / "raw" 
OUTPUT_DIR = BASE_DIR / "datasets" / "globalmart"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Dataset filenames
# ---------------------------------------------------------------------

FILES = {
    "customers": "olist/olist_customers_dataset.csv",
    "orders": "olist/olist_orders_dataset.csv",
    "order_items": "olist/olist_order_items_dataset.csv",
    "order_payments": "olist/olist_order_payments_dataset.csv",
    "order_reviews": "olist/olist_order_reviews_dataset.csv",
    "products": "olist/olist_products_dataset.csv",
    "sellers": "olist/olist_sellers_dataset.csv",
    "translations": "olist/product_category_name_translation.csv",
}

# ---------------------------------------------------------------------
# Date Configuration
# ---------------------------------------------------------------------

TARGET_YEAR = 2024


# ---------------------------------------------------------------------
# Deterministic Weighted City Mapper
# ---------------------------------------------------------------------

CITY_POOL = (
    [("New York", "US")] * 14 +
    [("London", "UK")] * 12 +
    [("Singapore", "SG")] * 10 +
    [("Dubai", "UAE")] * 10 +
    [("Toronto", "CA")] * 8 +
    [("Sydney", "AU")] * 7 +
    [("Tokyo", "JP")] * 6 +
    [("Berlin", "DE")] * 6 +
    [("Mumbai", "IN")] * 6 +
    [("Amsterdam", "NL")] * 5 +
    [("Paris", "FR")] * 5 +
    [("Chicago", "US")] * 5 +
    [("San Francisco", "US")] * 5 +
    [("Melbourne", "AU")] * 4 +
    [("Munich", "DE")] * 4 +
    [("Seoul", "KR")] * 4 +
    [("Madrid", "ES")] * 3 +
    [("Milan", "IT")] * 3 +
    [("Doha", "QA")] * 2 +
    [("Manama", "BH")] * 2 +
    [("Riyadh", "SA")] * 2 +
    [("Jeddah", "SA")] * 2 +
    [("Dublin", "IE")] * 2 +
    [("Copenhagen", "DK")] * 2 +
    [("Zurich", "CH")] * 2 +
    [("Vienna", "AT")] * 2 +
    [("Auckland", "NZ")] * 1
)


CITY_MAPPING = {}


def map_city(city: str):
    """
    Deterministically map every Brazilian city
    to one realistic global business city.
    """

    if pd.isna(city):
        return city, None

    city = str(city).strip().lower()

    if city in CITY_MAPPING:
        return CITY_MAPPING[city]

    index = int(
        hashlib.md5(city.encode("utf-8")).hexdigest(),
        16
    ) % len(CITY_POOL)

    mapped = CITY_POOL[index]

    CITY_MAPPING[city] = mapped

    return mapped

# ---------------------------------------------------------------------
# Load datasets
# ---------------------------------------------------------------------

def load_datasets():

    logger.info("Loading datasets...")

    datasets = {}

    for name, filename in FILES.items():

        path = RAW_DIR / filename

        if not path.exists():
            raise FileNotFoundError(path)

        datasets[name] = pd.read_csv(path)

        logger.info(
            f"✓ {filename:<40}"
            f"{len(datasets[name]):>8,} rows"
        )

    return datasets

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate(datasets):

    logger.info("\nValidating datasets...")

    for name, df in datasets.items():

        if df.empty:
            raise ValueError(f"{name} is empty")

        logger.info(
            f"✓ {name:<18}"
            f"{len(df.columns)} columns"
        )

# ---------------------------------------------------------------------
# Shift Dates
# ---------------------------------------------------------------------

def shift_dates(datasets):
    """
    Shift all timestamps using ONE global offset.

    This preserves the exact time differences between purchase,
    approval, shipping, delivery and review events.
    """

    logger.info("\nShifting timestamps...")

    orders = datasets["orders"]

    purchase_dates = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    if purchase_dates.dropna().empty:
        raise ValueError("No valid purchase timestamps found.")

    earliest_year = purchase_dates.min().year
    global_offset = TARGET_YEAR - earliest_year

    logger.info(
        f"Using global year offset: +{global_offset} years"
    )

    date_columns = {
        "orders": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        "order_reviews": [
            "review_creation_date",
            "review_answer_timestamp",
        ],
    }

    total_updated = 0

    for dataset_name, columns in date_columns.items():

        df = datasets[dataset_name]

        for column in columns:

            if column not in df.columns:
                continue

            logger.info(
                f"  Processing {dataset_name}.{column}"
            )

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            mask = df[column].notna()

            df.loc[mask, column] = (
                df.loc[mask, column]
                + DateOffset(years=global_offset)
            )

            total_updated += mask.sum()

    logger.info(
        f"✓ Updated {total_updated:,} timestamps"
    )

# ---------------------------------------------------------------------
# Validate Date Range
# ---------------------------------------------------------------------

def validate_date_range(datasets):

    logger.info("\nDate Range Validation")

    orders = datasets["orders"]

    purchase = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    logger.info(
        f"Purchase dates: "
        f"{purchase.min().date()} "
        f"→ "
        f"{purchase.max().date()}"
    )
        
# ---------------------------------------------------------------------
# Globalize Locations
# ---------------------------------------------------------------------

def globalize_locations(datasets):

    logger.info("\nGlobalizing customer locations...")

    customers = datasets["customers"]

    cities = []
    countries = []

    for city in customers["customer_city"]:

        new_city, new_country = map_city(city)

        cities.append(new_city)
        countries.append(new_country)

    customers["customer_city"] = cities
    customers["customer_state"] = countries

    logger.info(
        f"✓ Customers updated: {len(customers):,}"
    )

    logger.info("\nGlobalizing seller locations...")

    sellers = datasets["sellers"]

    cities = []
    countries = []

    for city in sellers["seller_city"]:

        new_city, new_country = map_city(city)

        cities.append(new_city)
        countries.append(new_country)

    sellers["seller_city"] = cities
    sellers["seller_state"] = countries

    logger.info(
        f"✓ Sellers updated: {len(sellers):,}"
    )

# ---------------------------------------------------------------------
# Enterprise Category Mapping
# ---------------------------------------------------------------------

CATEGORY_MAPPING = {
    "health_beauty": "Health & Beauty",
    "computers_accessories": "Computers & Accessories",
    "auto": "Automotive",
    "bed_bath_table": "Home & Living",
    "furniture_decor": "Furniture & Home Decor",
    "sports_leisure": "Sports & Outdoors",
    "perfumery": "Beauty & Fragrance",
    "housewares": "Home Essentials",
    "telephony": "Mobile & Accessories",
    "watches_gifts": "Watches & Gifts",
    "electronics": "Consumer Electronics",
    "garden_tools": "Garden & Outdoor",
    "toys": "Toys & Games",
    "cool_stuff": "Lifestyle Products",
    "fashion_bags_accessories": "Fashion Accessories",
    "fashion_shoes": "Footwear",
    "fashion_male_clothing": "Men's Fashion",
    "fashion_female_clothing": "Women's Fashion",
    "fashion_underwear_beach": "Beachwear & Underwear",
    "baby": "Baby Products",
    "pet_shop": "Pet Supplies",
    "stationery": "Office Supplies",
    "office_furniture": "Office Furniture",
    "books_general_interest": "Books",
    "books_imported": "Books",
    "books_technical": "Technical Books",
    "musical_instruments": "Musical Instruments",
    "small_appliances": "Small Appliances",
    "small_appliances_home_oven_and_coffee": "Kitchen Appliances",
    "kitchen_dining_laundry_garden_furniture": "Kitchen & Dining",
    "home_appliances": "Home Appliances",
    "home_appliances_2": "Home Appliances",
    "air_conditioning": "HVAC",
    "construction_tools_construction": "Construction Tools",
    "construction_tools_safety": "Safety Equipment",
    "construction_tools_lights": "Lighting",
    "construction_tools_garden": "Garden Equipment",
    "construction_tools_tools": "Power Tools",
    "construction_tools": "Construction Equipment",
    "industry_commerce_and_business": "Industrial Supplies",
    "agro_industry_and_commerce": "Agriculture & Industrial",
    "food": "Food",
    "food_drink": "Food & Beverage",
    "drinks": "Beverages",
    "la_cuisine": "Kitchen",
    "audio": "Audio",
    "cine_photo": "Cameras & Photography",
    "music": "Music",
    "dvds_blu_ray": "Movies & Entertainment",
    "cds_dvds_musicals": "Music & Movies",
    "gaming": "Gaming",
    "consoles_games": "Gaming",
    "pc_gamer": "Gaming PCs",
    "fixed_telephony": "Telecommunications",
    "tablets_printing_image": "Tablets & Printing",
    "signaling_and_security": "Security",
    "security_and_services": "Security",
    "art": "Art",
    "arts_and_craftmanship": "Arts & Crafts",
    "christmas_supplies": "Seasonal",
    "party_supplies": "Party Supplies",
    "flowers": "Flowers",
    "diapers_and_hygiene": "Personal Care",
}

# ---------------------------------------------------------------------
# Translate Categories 
# ---------------------------------------------------------------------

def translate_categories(datasets):
    """
    Translate Portuguese product categories
    into standardized enterprise categories.
    """

    logger.info("\nTranslating product categories...")

    products = datasets["products"]
    translations = datasets["translations"]

    lookup = dict(
        zip(
            translations.iloc[:, 0].astype(str),
            translations.iloc[:, 1].astype(str)
        )
    )

    products["product_category_name"] = (
        products["product_category_name"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .map(lookup)
        .fillna(products["product_category_name"])
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    products["product_category_name"] = (
        products["product_category_name"]
        .replace(CATEGORY_MAPPING)
    )

    unknown_count = (
        products["product_category_name"]
        .eq("unknown")
        .sum()
    )

    logger.info(
        f"✓ Categories translated for {len(products):,} products"
    )

    logger.info(
        f"✓ Unknown categories: {unknown_count}"
    )

    logger.info(
        f"✓ Final enterprise categories: "
        f"{products['product_category_name'].nunique()}"
    )


# ---------------------------------------------------------------------
# Validate Transformation
# ---------------------------------------------------------------------

def validate_transformation(datasets):

    logger.info("\nRunning validation...")

    customers = datasets["customers"]
    sellers = datasets["sellers"]
    products = datasets["products"]
    orders = datasets["orders"]

    checks = [
        ("Customers", len(customers)),
        ("Sellers", len(sellers)),
        ("Products", len(products)),
        ("Orders", len(orders)),
    ]

    for name, count in checks:
        logger.info(f"✓ {name:<12}: {count:,} rows")

    # Missing city check
    customer_missing = customers["customer_city"].isna().sum()
    seller_missing = sellers["seller_city"].isna().sum()

    if customer_missing:
        logger.warning(f"Customers with missing city: {customer_missing}")

    if seller_missing:
        logger.warning(f"Sellers with missing city: {seller_missing}")

    logger.info("✓ Validation completed successfully")

# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------

def save_datasets(datasets):

    logger.info("\nSaving transformed datasets...")

    for name, df in datasets.items():

        if name == "translations":
            continue

        out = OUTPUT_DIR / f"{name}.csv"

        df.to_csv(out, index=False, encoding="utf-8-sig")

        logger.info(f"✓ {out.name}")


# ---------------------------------------------------------------------
# Dataset Summary
# ---------------------------------------------------------------------

def generate_summary(datasets):

    logger.info("\nGenerating dataset summary...")

    orders = datasets["orders"]
    customers = datasets["customers"]
    products = datasets["products"]

    purchase = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    summary = {

        "dataset_name": "GlobalMart Enterprise Commerce Dataset",

        "version": "1.0",

        "generated_by": "SynapseOS",

        "generated_at": datetime.now().isoformat(),

        "currency": "USD",

        "statistics": {

            "customers": len(customers),

            "orders": len(orders),

            "products": len(products),

            "cities": customers["customer_city"].nunique(),

            "countries": customers["customer_state"].nunique(),

            "categories":
                products["product_category_name"].nunique(),

            "date_range": {
                "start": str(purchase.min().date()),
                "end": str(purchase.max().date())
            }

        }

    }

    with open(
        OUTPUT_DIR / "dataset_summary.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(summary, f, indent=4)

    logger.info("✓ dataset_summary.json created")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 60)
    print("GlobalMart Dataset Transformation")
    print("=" * 60)

    datasets = load_datasets()

    validate(datasets)

    shift_dates(datasets)

    globalize_locations(datasets)

    translate_categories(datasets)

    validate_date_range(datasets)

    validate_transformation(datasets)

    generate_summary(datasets)

    save_datasets(datasets)

    print("\nTransformation Complete ✓")


if __name__ == "__main__":
    main()