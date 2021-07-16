import pandas as pd

class PickleIO:
    def get_field_from_pickle(filename: str, field: str) -> tuple:
        data  = pd.read_pickle(filename)
        dates = data.index
        res = data[field].to_numpy()

        return (dates, res)