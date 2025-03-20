""" 
code for exploring the claims dataset
for Healthfirst interview
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

### EDA ##
sample_data = pd.read_csv('synthetic_claims2024.csv' )
print(sample_data.shape)
print(sample_data.columns)
print(sample_data.dtypes)
sample_data.CLM_FROM_DT.max()
print(sample_data.BENE_ID.unique().shape)
sample_data.isna().sum()
# about 3k code descriptions are na
missing_decr=sample_data.loc[sample_data.ICD_DGNS_CD1_DESC.isna()]
missing_decr.ICD_DGNS_CD1.value_counts()

# examine payment mount
sample_data.CLM_PMT_AMT.describe()
sample_data.CLM_PMT_AMT.plot.hist()
plt.show()

## DATES CLEAN UP AND EDA ##
# convert date columns to datetime
target_date_columns = [x for x in sample_data.columns if x.__contains__("_DT")]
sample_data[target_date_columns] = sample_data[target_date_columns].apply(
    pd.to_datetime,
    format="%m/%d/%y")
ym_dates = [x + '_YM' for x in target_date_columns]

# year-month
ym_dates = [x + '_YM' for x in target_date_columns]
sample_data[ym_dates] = sample_data[target_date_columns].apply(lambda x: x.dt.strftime('%Y-%m'))

# length of stay (approx)
sample_data['claim_days'] = sample_data['CLM_THRU_DT'] - sample_data['CLM_FROM_DT']
sample_data['claim_days'] = sample_data['claim_days'].dt.days
sample_data.claim_days.plot(kind='bar')
plt.show()

## PRNCPAL_DGNS_CD exploration ##
# total top codes overall
# very naive way
top_codes = sample_data.PRNCPAL_DGNS_CD.value_counts()[:10].index.to_list()

# subset
top_codes_df = sample_data.loc[sample_data['PRNCPAL_DGNS_CD'].isin(top_codes),
                                ['CLM_FROM_DT_YM'
                                 'PRNCPAL_DGNS_CD',
                                 'CLM_PMT_AMT']]   
# group by for aggregate
code_costs_over_time = top_codes_df.groupby(by=["CLM_FROM_DT_YM",
                                                'PRNCPAL_DGNS_CD']).sum().reset_index()
code_costs_over_time.plot(x ='CLM_FROM_DT_YM', y='CLM_PMT_AMT', legend='PRNCPAL_DGNS_CD')
# pandas.plot doesn't seam to work in vscode without plt.show()

# change from long to wide for matplotlib
formatted_for_graph = code_costs_over_time.pivot(index='CLM_FROM_DT_YM',
                                                 columns='PRNCPAL_DGNS_CD',
                                                 values='CLM_PMT_AMT')

############

## FIG 1 ##
# raw codes
fig, ax = plt.subplots(figsize=(10, 5))
x_axis = np.asarray(formatted_for_graph.index, dtype='datetime64[s]')
for code in top_codes:
    ax.plot(x_axis, formatted_for_graph[code], label=code)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.set_title('Sum of claims over time by ICD')
ax.set_ylabel('monthly claims(USD)')
ax.yaxis.set_major_formatter('${x:,.0f}')
ax.set_xlabel('year-month')
ax.set_xticklabels(formatted_for_graph.index, rotation=45, ha='right')
plt.show()
plt.savefig('claim_over_time.png')

## ROOT ICD Code

# take only first section of codes
sample_data["PRNC_ICD_RT"]= sample_data.PRNCPAL_DGNS_CD.apply(lambda x: x.split('.')[0])
print(sample_data.PRNC_ICD_RT.value_counts()[:10])

ICD_desc = {'I35':'Other forms of heart disease',
 'M7':'Other soft tissue disorders',
 'Z73':'Problems related to life management difficulty',
 'Z60': 'Problems related to social environment',
 'T74': 'Adult and child abuse, neglect and other maltreatment, confirmed',
 'I25': 'Chronic ischemic heart disease',
 'N18': 'Chronic kidney disease'}

root_code_sample = sample_data[ ['PRNC_ICD_RT','CLM_PMT_AMT']]
root_grouped = root_code_sample.groupby(by=[ 'PRNC_ICD_RT']).sum()
root_grouped['percent_of_Claims'] = root_grouped.CLM_PMT_AMT.apply(lambda x:
                                 x/float(root_grouped.CLM_PMT_AMT.sum()))
root_grouped['percent_of_Claims'].head()
root_code_sample.PRNC_ICD_RT.value_counts(normalize=True)
claim_ratios = pd.concat([root_grouped,
                          (root_code_sample
                           .PRNC_ICD_RT
                           .value_counts()
                           .rename('claims_submitted')),
                          (root_code_sample
                           .PRNC_ICD_RT
                           .value_counts(normalize=True)
                           .rename('percent of submitted'))
                           ],
                          axis=1)

new_columns = ['percent of submitted', 'percent_of_Claims']
claim_ratios[new_columns].plot(kind='scatter')
claim_ratios[new_columns].plot.scatter('percent of submitted',
                                       'percent_of_Claims',)
plt.show()
plt.savefig('scatter.png')

## FIG 2 ##
#### Scatter Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(claim_ratios['percent of submitted'], claim_ratios['percent_of_Claims'])
for i, txt in enumerate(claim_ratios.index):
    ax.annotate(txt, (claim_ratios['percent of submitted'][i],
                      claim_ratios['percent_of_Claims'][i]))
ax.xaxis.set_major_formatter(PercentFormatter())
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_ylabel('Percent of Total Claims Dollars')
ax.set_xlabel('percent of Total Claim Count')
# slope = 1
# intercept = 0
# line = slope * x + intercept
# ax.add_line(line=line)
ax.set_title("Comparing percent of claims in dollars vs count")
plt.show()


## MEMBER EXPLORATION

memb_sample=sample_data.loc[sample_data["BENE_ID"] == 10000010270727]
memb_sample.RFR_PHYSN_NPI.value_counts()
memb_sample.PRNC_ICD_RT.value_counts()
memb_sample.shape()

mental_health_claims = sample_data.loc[sample_data["PRNC_ICD_RT" ]== 'Z73',:]
mental_health_claims.CLM_PMT_AMT.describe()
mental_health_claims.CLM_PMT_AMT.plot(kind='hist')
plt.show()
