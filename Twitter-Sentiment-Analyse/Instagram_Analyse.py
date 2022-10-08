import numpy as np
import pandas as pd

df_insta = pd.read_csv("instagram_global_top_1000.csv")

df_insta['Audience Country'].value_counts(normalize=True).round(2)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_insta)
df_insta.pivot_table(index="Category", values="Followers", aggfunc=['mean', 'sum', 'max', 'min'], sort=False)
