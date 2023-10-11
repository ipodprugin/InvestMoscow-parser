import pandas as pd
from contextlib import suppress


def merge_data_to_sheet(left, right, on, columns_order=None):
    updated_df = pd.merge(left, right, on=on, how='outer')

    columns_to_delete = []
    columns_to_rename = {}

    for column in list(right.columns)[1:]:
        with suppress(KeyError):
            updated_df[f'{column}_y'] = updated_df[f'{column}_y'].fillna(updated_df[f'{column}_x'], inplace=False)
            columns_to_delete.append(f'{column}_x')
            columns_to_rename[f'{column}_y'] = column

    updated_df.drop(columns=columns_to_delete, inplace=True)
    updated_df.rename(columns=columns_to_rename, inplace=True)

    if columns_order:
        updated_df = updated_df.reindex(columns=columns_order)

    return updated_df
