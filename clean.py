import pandas as pd
import numpy as np
import datetime as dt
import helpers as hp
import streamlit as st

dashboard = pd.read_csv(r"dashboard.csv", encoding= 'unicode_escape')
cols = ['unit','name','email','date_of_birth','phone number','next of kin','phone number.1','title','grade','started_at_ahc','qualification','english_level','residence',
        'old','housing','med.ins','allowance','gender','turnover','cause','ended_at_ahc','year']
dashboard = dashboard[cols] 
dashboard.rename(columns=hp.rename_cols, inplace=True)

dashboard.iloc[:, 13:19] = dashboard[dashboard.columns[13:19].tolist()].applymap(hp.replace_values)
dashboard.loc[:, ["date_of_birth", "started_at_ahc", "ended_at_ahc"]] = dashboard.loc[:, ["date_of_birth", "started_at_ahc", "ended_at_ahc"]].applymap(hp.to_datetime) 

dashboard["age"] = hp.subtract_from_current_date(dashboard["date_of_birth"])
dashboard["years_of_experience"] = dashboard.apply(hp.years_of_experience, axis=1)
dashboard["interval_experience"] = dashboard["years_of_experience"].apply(hp.intervals)

dashboard.to_csv("final_dataset.csv", index=False)