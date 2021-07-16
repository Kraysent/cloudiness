import pandas as pd


def get_field_from_pickle(filename: str, field: str) -> tuple:
    data  = pd.read_pickle(filename)
    dates = data.index
    res = data[field].to_numpy()

    return (dates, res)

def dump_dict(filename: str, data: dict):
    res_df = pd.DataFrame.from_dict(data)
    res_df.to_pickle(filename)