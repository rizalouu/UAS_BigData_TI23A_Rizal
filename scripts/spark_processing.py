from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# ==========================
# SPARK SESSION
# ==========================
spark = SparkSession.builder \
    .appName("VisitorPrediction") \
    .getOrCreate()

# ==========================
# READ CSV
# ==========================
df = spark.read.csv(
    "data/raw/visitor_data.csv",
    header=True,
    inferSchema=True
)

# ==========================
# UBAH TIMESTAMP
# ==========================
df = df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"))
)

# ==========================
# 1. TOTAL PENGUNJUNG TIAP ZONA
# ==========================
visitor_total = df.groupBy("zone") \
    .agg(
        sum("visitor_count")
        .alias("total_visitors")
    )

visitor_total.write \
    .mode("overwrite") \
    .parquet("data/serving/visitor_total")

# ==========================
# 2. TREN PENGUNJUNG TIAP 15 MENIT
# ==========================
visitor_time = df \
    .withColumn(
        "hour",
        hour("timestamp")
    ) \
    .withColumn(
        "minute_block",
        floor(minute("timestamp") / 15) * 15
    ) \
    .groupBy(
        "zone",
        "hour",
        "minute_block"
    ) \
    .agg(
        sum("visitor_count")
        .alias("visitor_count")
    )

visitor_time.write \
    .mode("overwrite") \
    .parquet("data/serving/visitor_time")

# ==========================
# 3. DATASET MACHINE LEARNING
# ==========================
ml_df = df.withColumn(
    "hour",
    hour("timestamp")
)

ml_df.select(
    "hour",
    "visitor_count",
    "zone"
).write \
 .mode("overwrite") \
 .parquet("data/serving/ml_visitor")

print("================================")
print("PARQUET BERHASIL DIBUAT")
print("================================")