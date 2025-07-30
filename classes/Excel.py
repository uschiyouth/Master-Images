from pathlib import Path

import numpy as np
import pandas as pd

class Excel:
    def __init__(self):
        self.file_path = Path("data/Soilcover.xlsx")
        self.to_fill = 1

        if self.file_path.exists():
            self.file = pd.read_excel(self.file_path)
        else:
            self.file = pd.DataFrame({
                "ID": range(1, 101),
                "plot": np.nan,
                "rock": np.nan,
                "dirt": np.nan,
                "native vegetation": np.nan,
                "Phalaris": np.nan
            })
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file.to_excel(self.file_path, index=False)

        if self.file["plot"].notna().any():
            self.to_fill = int(self.file["plot"].dropna().max() + 1)

    def save_row(self, plot, row):
        # Write values from row to the corresponding excel row (only if the column exists)
        for key, value in row.items():
            if key in self.file.columns:
                self.file.at[plot-1, key] = value

        self.file.at[plot-1, 'plot'] = plot
        self.file.to_excel(self.file_path, index=False)

    def get_to_fill(self):
        return self.to_fill


