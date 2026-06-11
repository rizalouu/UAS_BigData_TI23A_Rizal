from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import random
from datetime import datetime, timedelta
import pandas as pd
import os

print("====================================")
print(" SMART HOSPITAL MONITORING SYSTEM ")
print("====================================")

spark = SparkSession.builder \
    .appName("UTSBigData") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# =========================
# GENERATE DUMMY DATA
# =========================

rooms = ["ICU", "Emergency", "Pharmacy"]

data = []

start_time = datetime.now()

for i in range(120):

    current_time = start_time + timedelta(minutes=i)

    for room in rooms:

        patient_count = random.randint(5, 80)

        data.append((
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            room,
            patient_count
        ))

columns = ["timestamp", "room", "patient_count"]

df = spark.createDataFrame(data, columns)

df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

df.show(5)

# =========================
# TOTAL PATIENT PER ROOM
# =========================

patient_total = df.groupBy("room") \
    .agg(sum("patient_count").alias("total_patient"))

patient_total.show()

# =========================
# PATIENT TREND PER 15 MIN
# =========================

patient_time = df.groupBy(
    window(col("timestamp"), "15 minutes"),
    col("room")
).agg(
    sum("patient_count").alias("patient_trend")
)

patient_time.show()

# =========================
# ML DATASET
# =========================

ml_data = df.withColumn(
    "hour",
    hour(col("timestamp"))
).select(
    "hour",
    "patient_count"
)

ml_data.show()

# =========================
# CREATE OUTPUT FOLDER
# =========================

base_path = os.path.abspath("output")

# =========================
# SAVE PARQUET
# =========================

patient_total.write.mode("overwrite") \
    .parquet(f"{base_path}/patient_total")

patient_time.write.mode("overwrite") \
    .parquet(f"{base_path}/patient_time")

ml_data.write.mode("overwrite") \
    .parquet(f"{base_path}/ml_data")

print("====================================")
print(" PARQUET SUCCESSFULLY SAVED ")
print("====================================")

spark.stop()