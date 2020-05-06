import pandas as pd
import pandas_profiling as pp

df = pd.read_csv('data_hot.csv')
profile = pp.ProfileReport(df, title='Pandas Profiling Report', html={'style':{'full_width':True}})
profile.to_notebook_iframe()
profile.to_file(output_file="data_hot_pdprofiler.html")
