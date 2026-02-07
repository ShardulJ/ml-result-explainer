import pandas as pd
import numpy as np
from typing import Dict, Any
from scipy import stats

class DataProfiler:
    
    def __init__(self, anomaly_threshold: float = 3.0):
        self.anomaly_threshold = anomaly_threshold
    
    def profile_data(self, df: pd.DataFrame, prediction_column: str = None) -> Dict[str, Any]:
        profile = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": {},
            "missing_percentages": {},
            "numeric_columns": [],
            "categorical_columns": [],
            "prediction_summary": {}
        }
        
        for col in df.columns:
            missing_count = df[col].isna().sum()
            profile["missing_values"][col] = int(missing_count)
            profile["missing_percentages"][col] = round(missing_count / len(df) * 100, 2)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        profile["numeric_columns"] = numeric_cols
        profile["categorical_columns"] = categorical_cols
        
        if prediction_column and prediction_column in df.columns:
            pred_col = df[prediction_column]
            
            if prediction_column in numeric_cols:
                profile["prediction_summary"] = {
                    "type": "numeric",
                    "mean": float(pred_col.mean()),
                    "median": float(pred_col.median()),
                    "std": float(pred_col.std()),
                    "min": float(pred_col.min()),
                    "max": float(pred_col.max()),
                    "q25": float(pred_col.quantile(0.25)),
                    "q75": float(pred_col.quantile(0.75))
                }
            else:
                value_counts = pred_col.value_counts().to_dict()
                profile["prediction_summary"] = {
                    "type": "categorical",
                    "unique_values": int(pred_col.nunique()),
                    "most_common": str(pred_col.mode()[0]) if len(pred_col.mode()) > 0 else None,
                    "distribution": {str(k): int(v) for k, v in list(value_counts.items())[:10]}
                }
        
        return profile
    
    def detect_anomalies(self, df: pd.DataFrame, prediction_column: str = None) -> Dict[str, Any]:
        anomalies = {
            "total_anomalies": 0,
            "anomaly_indices": [],
            "anomaly_details": {}
        }
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        all_anomaly_indices = set()
        
        for col in numeric_cols:
            if df[col].notna().sum() > 0:
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                col_anomalies = np.where(z_scores > self.anomaly_threshold)[0]
                
                if len(col_anomalies) > 0:
                    anomalies["anomaly_details"][col] = {
                        "count": int(len(col_anomalies)),
                        "indices": col_anomalies.tolist()[:10]
                    }
                    all_anomaly_indices.update(df[df[col].notna()].iloc[col_anomalies].index.tolist())
        
        anomalies["total_anomalies"] = len(all_anomaly_indices)
        anomalies["anomaly_indices"] = sorted(list(all_anomaly_indices))[:50]
        
        return anomalies