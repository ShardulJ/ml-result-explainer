import pandas as pd 
import numpy as np 
from typing import Tuple, Optional, List, Dict
import os

class CSVValidator:

	def __init__(self, max_size_mb: int = 50):
		self.max_size_bytes = max_size_mb * 1024 * 1024

	def validate_file(self, filepath : str) -> Tuple[bool, Optional[str]]:
		if not os.path.exists(filepath):
			return False, "File not found"

		file_size = os.path.getsize(filepath)
		if file_size > self.max_size_bytes:
			return False, f"File Size too big. Max Size is {self.max_size_bytes/(1024*1024):.0f}MB"

		if file_size == 0:
			return False, "file is empty"

		try:
			df = pd.read_csv(filepath, nrows=5)
			if len(df.columns) == 0:
				return False, "file has no columns"
			if len(df) == 0:
				return False, "file is no rows"
			return True, None
		except Exception as e:
			return False, f"invalid CSV format: {str(e)}"

	def load_and_analyse(self, filepath: str) -> Tuple[pd.DataFrame, Dict]:
		df = pd.read_csv(filepath)

		metadata = {
			"row_data" : len(df),
			"column_data" : len(df.columns),
			"column_names" : df.columns.tolist(),
			"dtypes" : {col:str(dtype) for col, dtype in df.dtypes.items()},
			"has_ground_truth" : False,
			"has_timestamp" : False,
			"prediction_column" : None
		}


		prediction_candidates = ["prediction", "predicted", "pred", "score", "probability", "target"]
		for col in df.columns:
			if any(cand in col.lower() for cand in prediction_candidates):
				metadata["prediction_column"] = col
				break

		if metadata["prediction_column"] is None and len(df.columns)>0:
			metadata["prediction_column"] = df.columns[-1]

		label_candidates = ["label", "actual", "truth", "ground_truth", "true"]
		for col in df.columns:
			if any(cand in col.lower() for cand in label_candidates):
				metadata["has_ground_truth"] = True
				break

		label_candidates = ["timestamp", "date", "time", "datetime", "true"]
		for col in df.columns:
			if any(cand in col.lower() for cand in label_candidates):
				metadata["has_ground_truth"] = True
				break

		return df, metadata

	def identify_column_types(self, df: pd.DataFrame) -> Tuple[List[str], List[str]]:
		numeric_cols = df.select_dtypes(include=[np.number])
		categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
		return numeric_cols, categorical_cols
