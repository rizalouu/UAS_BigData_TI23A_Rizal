import pandas as pd
import os

# ==========================================
# LOAD DATA
# ==========================================
def load_data(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    # Mencari file parquet di folder utama maupun subfolder (Spark sering membuat subfolder)
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".parquet") and not f.startswith("."):
                files.append(os.path.join(root, f))
    
    if not files:
        return pd.DataFrame()
    
    try:
        df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        return df
    except Exception:
        return pd.DataFrame()

# ==========================================
# PREPROCESS
# ==========================================
def preprocess(df):
    if df.empty:
        return df
    # Memastikan kolom timestamp benar-to-datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # Menghapus data yang gagal konversi waktu
    df = df.dropna(subset=["timestamp"])
    # Memastikan kolom fare adalah angka
    df["fare"] = pd.to_numeric(df["fare"], errors='coerce').fillna(0)
    return df

# ==========================================
# METRICS
# ==========================================
def compute_metrics(df):
    if df.empty or len(df) == 0:
        return {"total_trips": 0, "total_fare": 0, "top_location": "-"}
    
    return {
        "total_trips": len(df),
        "total_fare": df["fare"].sum(),
        "top_location": df.groupby("location")["fare"].sum().idxmax()
    }

# ==========================================
# PEAK HOUR
# ==========================================
def detect_peak_hour(df):
    if df.empty:
        return None
    df["hour"] = df["timestamp"].dt.hour
    return df.groupby("hour").size().idxmax()

# ==========================================
# VISUALIZATION DATA
# ==========================================
def fare_per_location(df):
    if df.empty:
        return pd.Series()
    return df.groupby("location")["fare"].sum().sort_values(ascending=False)

def vehicle_distribution(df):
    if df.empty:
        return pd.Series()
    return df.groupby("vehicle_type").size().sort_values(ascending=False)

def mobility_trend(df):
    """
    Fungsi ini diperbaiki untuk menangani error frequency 'S' vs 's'
    dan memastikan index adalah datetime.
    """
    if df.empty:
        return pd.Series()
    
    # Buat copy agar tidak merusak dataframe asli
    df_trend = df.copy()
    df_trend = df_trend.set_index("timestamp")
    
    # Gunakan '10s' (huruf kecil) agar kompatibel dengan Pandas versi baru
    # Jika masih error '10s', ganti menjadi '10S'
    try:
        return df_trend["fare"].resample("10s").sum()
    except ValueError:
        return df_trend["fare"].resample("10S").sum()

# ==========================================
# ANOMALY DETECTION
# ==========================================
def detect_anomaly(df):
    if df.empty:
        return pd.DataFrame()
    return df[df["fare"] > 80000]