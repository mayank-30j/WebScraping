import pandas as pd

df = pd.DataFrame({'Name': ['Maa', 'adk', 'adf'],'Class': ['45', '343', '334']})
df2 = pd.DataFrame({'Name': ['Maa', 'adk', 'adf'],'Class': ['45', '343', '334']})

df_temp = df.append(df2,ignore_index=True)
print(df_temp)
# df.to_excel(r'C:\Users\mayan\OneDrive\Desktop\Fiverr\Demo2.xlsx', index=False, sheet_name='Sheet1')
# df2.to_excel(r'C:\Users\mayan\OneDrive\Desktop\Fiverr\Demo2.xlsx', index=False, sheet_name='Sheet1')
