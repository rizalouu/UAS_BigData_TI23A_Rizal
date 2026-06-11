import pandas as pd
import random
from datetime import datetime, timedelta

zones = [
    "FoodCourt",
    "FashionArea",
    "Cinema"
]

start_time = datetime.now().replace(
    minute=0,
    second=0,
    microsecond=0
)

data = []

for i in range(180):

    timestamp = start_time + timedelta(minutes=i)

    for zone in zones:

        visitor_count = random.randint(10, 500)

        data.append([
            timestamp,
            zone,
            visitor_count
        ])

df = pd.DataFrame(
    data,
    columns=[
        "timestamp",
        "zone",
        "visitor_count"
    ]
)

df.to_csv(
    "data/raw/visitor_data.csv",
    index=False
)

print("visitor_data.csv berhasil dibuat")