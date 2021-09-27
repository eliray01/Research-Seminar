import pandas as pd

df = pd.read_csv('appl.csv', delimiter= ';')

def time_to_num(time_str):
    hh, mm , ss = map(int, time_str.split(':'))
    return (mm + 60*hh)

for line in df['<TIME>']:
   print(time_to_num(line))


df['<TIME>'] = df['<TIME>'].apply(lambda x: time_to_num(x))
df.to_csv('df.csv')