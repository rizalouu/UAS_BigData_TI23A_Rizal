# =====================================
# TRANSACTION GENERATOR
# =====================================

import json
import time
import random
import os
from datetime import datetime

# Create folder if not exists
if not os.path.exists("stream_data"):
    os.makedirs("stream_data")

products = ["Laptop", "Phone", "Tablet", "Headphones", "Monitor"]
cities = ["Jakarta", "Bandung", "Surabaya", "Medan", "Yogyakarta"]

counter = 1

print("========================================")
print("     TRANSACTION GENERATOR STARTED     ")
print("========================================")

while True:
    transaction = {
        "transaction_id": counter,
        "product": random.choice(products),
        "quantity": random.randint(1, 5),
        "price": random.randint(100, 1000) * 1000,
        "city": random.choice(cities),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    filename = f"stream_data/transaction_{counter}.json"

    with open(filename, "w") as f:
        json.dump(transaction, f)

    print(f"Generated: {filename}")

    counter += 1
    time.sleep(3)