import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, 
                               FormatStrFormatter, 
                               FuncFormatter,
                               AutoMinorLocator) 

sample_data = pd.read_csv('synthetic_claims2024.csv' )

# convert date columns to datetime
target_date_columns = [x for x in sample_data.columns if x.__contains__("_DT")]
sample_data[target_date_columns] = sample_data[target_date_columns].apply(pd.to_datetime, format="%m/%d/%y")

ym_dates = [x + '_YM' for x in target_date_columns] 
# check missing data
sample_data.isna().sum()
sample_data.shape
missing_decr=sample_data.loc[sample_data.ICD_DGNS_CD1_DESC.isna()]

sample_data.CLM_FROM_DT.max()
missing_decr.ICD_DGNS_CD1.value_counts()

# create new variables

# year-month
ym_dates = [x + '_YM' for x in target_date_columns] 
sample_data[ym_dates] = sample_data[target_date_columns].apply(lambda x: x.dt.strftime('%Y-%m'))

# length of stay (approx)
sample_data['claim_days'] = sample_data['CLM_THRU_DT'] - sample_data['CLM_FROM_DT'] 
sample_data['claim_days'] = sample_data['claim_days'].dt.days

top_codes = sample_data.PRNCPAL_DGNS_CD.value_counts()[:10].index.to_list()
top_codes_df = sample_data.loc[sample_data['PRNCPAL_DGNS_CD'].isin(top_codes), ['CLM_FROM_DT_YM','PRNCPAL_DGNS_CD','CLM_PMT_AMT']]   
code_costs_over_time = top_codes_df.groupby(by=["CLM_FROM_DT_YM", 'PRNCPAL_DGNS_CD']).sum().reset_index()

code_costs_over_time.plot(x ='CLM_FROM_DT_YM', y='CLM_PMT_AMT', legend='PRNCPAL_DGNS_CD')

formatted_for_graph = code_costs_over_time.pivot(index='CLM_FROM_DT_YM', columns='PRNCPAL_DGNS_CD', values='CLM_PMT_AMT')

############

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, 
                               FormatStrFormatter, 
                               FuncFormatter,
                               AutoMinorLocator,
                               PercentFormatter) 

fig, ax = plt.subplots(figsize=(10, 5))
x_axis = np.asarray(formatted_for_graph.index, dtype='datetime64[s]')
for code in top_codes:
    ax.plot(x_axis, formatted_for_graph[code], label=code)

ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.set_title('Sum of claims over time by ICD') 
  
### label x-axis and y-axis 
# currency_format = lambda x, pos: '${:,.0f}K'.format(x/1000)
ax.set_ylabel('monthly claims(USD)')
ax.yaxis.set_major_formatter('${x:,.0f}')
ax.set_xlabel('year-month') 
ax.set_xticklabels(formatted_for_graph.index, rotation=45, ha='right')
plt.show()

### Code clean up

# take only first section of codes
sample_data["PRNC_ICD_RT"]= sample_data.PRNCPAL_DGNS_CD.apply(lambda x: x.split('.')[0])
sample_data.PRNC_ICD_RT.value_counts()[:10]
# remove X from codes (it means multiple times)

ICD_desc = {'I35':'Other forms of heart disease',
 'M7':'Other soft tissue disorders',
 'Z73':'Problems related to life management difficulty',
 'Z60': 'Problems related to social environment',
 'T74': 'Adult and child abuse, neglect and other maltreatment, confirmed',
 'I25': 'Chronic ischemic heart disease',
 'N18': 'Chronic kidney disease'}

root_code_sample = sample_data[ ['PRNC_ICD_RT','CLM_PMT_AMT']]
root_grouped = root_code_sample.groupby(by=[ 'PRNC_ICD_RT']).sum()
root_grouped['percent_of_Claims'] = root_grouped.CLM_PMT_AMT.apply(lambda x: x/float(root_grouped.CLM_PMT_AMT.sum()))
root_grouped['percent_of_Claims'].head()
root_code_sample.PRNC_ICD_RT.value_counts(normalize=True)
claim_ratios = pd.concat([root_grouped,root_code_sample.PRNC_ICD_RT.value_counts().rename('claims_submitted'), root_code_sample.PRNC_ICD_RT.value_counts(normalize=True).rename('percent of submitted')], axis=1)

new_columns = ['percent of submitted', 'percent_of_Claims']
claim_ratios[new_columns].plot(kind='scatter')

claim_ratios[new_columns].plot.scatter('percent of submitted', 'percent_of_Claims',)
plt.show()
#### Scatter Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(claim_ratios['percent of submitted'], claim_ratios['percent_of_Claims'])
for i, txt in enumerate(claim_ratios.index):
    ax.annotate(txt, (claim_ratios['percent of submitted'][i], claim_ratios['percent_of_Claims'][i]))
ax.xaxis.set_major_formatter(PercentFormatter())
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_ylabel('Percent of Total Claims Dollars') 
ax.set_xlabel('percent of Total Claim Count') 
slope = 1
intercept = 0
line = slope * x + intercept
ax.add_line(line=line)
ax.set_title("Comparing percent of claims in dollars vs count")



plt.show()

sample_data.BENE_ID.unique().shape

memb_sample=sample_data.loc[sample_data["BENE_ID"] == 10000010270727]
memb_sample.RFR_PHYSN_NPI.value_counts()
memb_sample.shape()

mental_health_claims = sample_data.loc[sample_data["PRNC_ICD_RT" ]== 'Z73',:] 
mental_health_claims.CLM_PMT_AMT.plot(kind='hist')
plt.show()

mental_health_claims.columns