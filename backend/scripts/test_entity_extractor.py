from src.ml.knowledge.graph.entity_extractor import EntityExtractor

extractor = EntityExtractor()

text = """
The olist_orders_dataset.csv joins with
olist_order_reviews_dataset.csv.

The delivery_time can be analysed
using order_status.
"""

print(extractor.extract(text))