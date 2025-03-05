
import pandas as pd

df = pd.read_csv('factory1.csv')

print(str(df.loc[df.index.min() ,'timestamp']))