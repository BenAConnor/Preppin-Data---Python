import pandas as pd
import numpy as np

# Input the data
df_transactions = pd.read_csv('..\\Unprepped Data\PD 2023 Wk 1 Input.csv')
df_targets = pd.read_csv('..\\Unprepped Data\Targets.csv')

# For the transactions file:
# Filter the transactions to just look at DSB
df_transactions['Bank'] = df_transactions['Transaction Code'].str.split('-',expand=True)[0]

df_transactions = df_transactions.loc[df_transactions['Bank']=='DSB']

# Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
df_transactions['Online or In-Person']= np.where(df_transactions['Online or In-Person']==1,'Online','In-Person')

# Change the date to be the quarter - Be careful with date conversion, make sure to specify the format or can lead to errors!!!

df_transactions['Transaction Date'] = pd.to_datetime(df_transactions['Transaction Date'], format= '%d/%m/%Y %H:%M:%S')
df_transactions['Quarter'] = df_transactions['Transaction Date'].dt.quarter
print(df_transactions)

# Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person)
df_quarterly_data = df_transactions.groupby(['Quarter','Online or In-Person'],as_index=False)['Value'].sum()
print(df_quarterly_data)

# For the targets file:
# Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter
df_targets = pd.melt(df_targets,['Online or In-Person'],['Q1','Q2','Q3','Q4'])
#  Rename the fields
df_targets.columns = ['Online or In-Person','Quarter','Quarterly Targets']
# Remove the 'Q' from the quarter field and make the data type numeric
df_targets['Quarter'] = df_targets['Quarter'].str.replace('Q','').astype(int)

# Join the two datasets together
df_output = df_quarterly_data.merge(df_targets, how = 'inner', on = ['Online or In-Person','Quarter'])

# Calculate the Variance to Target for each row
df_output['Variance to Target'] = df_output['Value'] - df_output['Quarterly Targets']

#Output the data
df_output.to_csv('..\\Outputs\\Week3_Output.csv')

print('Data Prepped!')