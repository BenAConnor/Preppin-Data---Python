import pandas as pd
import numpy as np

# Input the data
transactions_df = pd.read_csv('..\\Unprepped Data\Transactions.csv')
swift_df = pd.read_csv('..\\Unprepped Data\Swift Codes.csv')

# In the Transactions table, there is a Sort Code field which contains dashes. We need to remove these so just have a 6 digit string
transactions_df['Sort Code'] = transactions_df['Sort Code'].str.replace('-','')

# Use the SWIFT Bank Code lookup table to bring in additional information about the SWIFT code and Check Digits of the receiving bank account
df = transactions_df.merge(swift_df, how= 'inner', on = 'Bank')

# Add a field for the Country Code
df['Country Code'] = 'GB'

# Create the IBAN as above - change data types
df['IBAN'] = df['Country Code']+df['Check Digits'].astype(str)+df['SWIFT code'].astype(str)+df['Account Number'].astype(str)

#Keep Relevant Columns
df = df[['Transaction ID','IBAN']]

# Output the Data
df.to_csv('..\\Outputs\Week2_Output.csv')

print('Data Prepped!')