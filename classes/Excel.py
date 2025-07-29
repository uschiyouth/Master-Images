from pathlib import Path

import numpy as np
import pandas as pd

class Excel:
    def __init__(self):
        file_path = Path("data/Soilcover.xlsx")

        if file_path.exists():
            df = pd.read_excel(file_path)
        else:
            df = pd.DataFrame({
                "plot": range(1, 101),
                "rock": np.nan,
                "dirt": np.nan,
                "native vegetation": np.nan,
                "Phalaris": np.nan
            })
            file_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_excel(file_path, index=False)
