# =====================================
# STREAMING LAYER (SPARK STRUCTURED STREAMING)
# =====================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

print("========================================")
print("        STREAMING LAYER STARTED         ")
print("========================================")

# ============================
# INIT SPARK
# ============================
spark = SparkSession.builder \
    .appName("StreamingLayer") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ============================
# SCHEMA (HARUS SESUAI GENERATOR)
# ============================
schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("product", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# ============================
# READ STREAM
# ============================
df_stream = spark.readStream \
    .schema(schema) \
    .json("stream_data")

# ============================
# TRANSFORMASI
# ============================
df_processed = df_stream.withColumn(
    "total_amount", col("quantity") * col("price")
)

# ============================
# WRITE TO PARQUET (SERVING)
# ============================
query = df_processed.writeStream \
    .format("parquet") \
    .option("path", "data/serving/stream") \
    .option("checkpointLocation", "data/checkpoint") \
    .outputMode("append") \
    .start()

print("Streaming is running...")

query.awaitTermination()