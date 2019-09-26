import pandas as pd

'''Data cleaning helper funcs'''

def strip_extra(df, col):
    for val in df[col]:
        new_val = val.strip()
        df.replace(val, new_val)
    return df

def clean_line_breaks(df, col):
    for val in df[col]:
        val_l = val.split('\n  ')
        new_val = ' '.join(val_l)
        df.replace(val, new_val, inplace=True)
    
    return df

def remove_paren(df, col):
    for val in df[col]:
        new_val = val.strip(')')
        df.replace(val, new_val, inplace=True)
