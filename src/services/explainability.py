import pandas as pd
import numpy as np
from typing import List, Dict

class FeatureImportanceCalculator:
    
    def __init__(self, max_features: int = 10):
        self.max_features = max_features
    
    def calculate_importance(self, df: pd.DataFrame, prediction_column: str, method: str = "correlation") -> List[Dict]:
        return self._correlation_importance(df, prediction_column)
    
    def _correlation_importance(self, df: pd.DataFrame, prediction_column: str) -> List[Dict]:
        if prediction_column not in df.columns:
            return []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        feature_cols = [col for col in numeric_cols if col != prediction_column]
        
        if not feature_cols:
            return []
        
        importances = []
        for col in feature_cols:
            try:
                corr = abs(df[col].corr(df[prediction_column]))
                if not np.isnan(corr):
                    importances.append({"feature": col, "importance": round(float(corr), 4)})
            except:
                pass
        
        importances.sort(key=lambda x: x["importance"], reverse=True)
        
        for idx, item in enumerate(importances[:self.max_features], 1):
            item["rank"] = idx
        
        return importances[:self.max_features]
    
    def generate_insights(self, importances: List[Dict], top_n: int = 3) -> List[str]:
        if not importances:
            return ["No significant features detected in the data."]
        
        insights = []
        
        if len(importances) > 0:
            top = importances[0]
            insights.append(
                f"The most influential feature is '{top['feature']}' with an importance score of {top['importance']:.3f}."
            )
        
        if len(importances) > 1:
            secondary = [imp['feature'] for imp in importances[1:min(4, len(importances))]]
            insights.append(f"Other important features include: {', '.join(secondary)}.")
        
        return insights