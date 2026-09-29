#%%
import pandas as pd
a = pd.read_csv("C:/Users/Bruno/Desktop/CCOMP/TECHLAB/Analise_Stack_Overflow/dados/dados/2017.csv",encoding="latin-1")
#%%
a.shape
# %%
a.head()
# %%
a["What Country or Region do you live in?"].value_counts()
# %%
a.sample(5)
# %%
a.columns
# %%
a["Unnamed: 42"].value_counts()
# %%
a.head().T

# %%
pd.set_option('display.max_columns', None)
# %%
a["Country"].value_counts()
# %%
