# Olist ML Dataset

File

olist_ml_dataset.csv

Rows

95,831

Columns

25

Purpose

This dataset is a cleaned and feature-engineered version of the original Olist data.

It is specifically prepared for:

- Regression
- Forecasting
- Explainable AI
- AutoML
- Enterprise Analytics
- AI Decision Support

---

## Features

### Order

order_id

Unique order identifier.

---

### Time

order_purchase_timestamp

Timestamp when purchase occurred.

purchase_year

purchase_month

purchase_weekday

purchase_hour

weekend_purchase

---

### Customer

customer_state

Brazilian state.

---

### Product

product_category_name_english

Product category.

product_weight_g

product_length_cm

product_height_cm

product_width_cm

product_volume_cm3

---

### Financial

price

freight_value

payment_value

payment_installments

payment_type

freight_ratio

price_per_kg

---

### Delivery

delivery_days

estimated_delivery_days

delivery_delay

---

### Customer Satisfaction

review_score

---

## Typical Prediction Targets

payment_value

review_score

delivery_delay

price

delivery_days

---

## Common Features

customer_state

payment_type

purchase_month

purchase_hour

product_category_name_english

price

freight_value

review_score

delivery_days

---

## Machine Learning Tasks

Regression

Forecasting

AutoML

Feature Importance

SHAP

Anomaly Detection

Clustering