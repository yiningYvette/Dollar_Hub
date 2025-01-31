import census
import pandas as pd
import numpy as np
#from pathlib import Path

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format  # Avoid scientific notation

# Set API Key
key = '8e19fd877f583ed3a97c25036bb5dd39a65daf9f'
c = census.Census(key)

# Chicago-specific settings
city_name = 'Chicago'
state = '17'
FIPS = ['031', '043', '089', '093', '097', '111', '197']
sql_query = 'state:{} county:*'.format(state)

# Function to filter FIPS codes
def filter_FIPS(df):
    return df[df['county'].isin(FIPS)]

# Variables to fetch from ACS 2023
variables_2023 = ['B03002_001E', 'B03002_003E', 'B19001_001E', 'B19013_001E',
                  'B25077_001E', 'B25077_001M', 'B25064_001E', 'B25064_001M',
                  'B15003_001E', 'B15003_022E', 'B15003_023E', 'B15003_024E', 
                  'B15003_025E', 'B25034_001E', 'B25034_010E', 'B25034_011E',
                  'B25003_002E', 'B25003_003E', 'B25105_001E', 'B06011_001E']

# Income categories
income_vars = ['B19001_' + str(i).zfill(3) + 'E' for i in range(2, 18)]
variables_2023.extend(income_vars)

# Run API query
var_dict_acs5 = c.acs5.get(variables_2023, geo={'for': 'tract:*', 'in': sql_query}, year=2023)

# Convert to DataFrame and filter by FIPS
df_2023 = pd.DataFrame.from_dict(var_dict_acs5)
df_2023['FIPS'] = df_2023['state'] + df_2023['county'] + df_2023['tract']
df_2023 = filter_FIPS(df_2023)

# Rename columns
df_2023 = df_2023.rename(columns={  'B03002_001E': 'pop_23',
                                    'B03002_003E': 'white_23',
                                    'B19001_001E': 'hh_23',
                                    'B19013_001E': 'hinc_23',
                                    'B25077_001E': 'mhval_23',
                                    'B25077_001M': 'mhval_23_se',
                                    'B25064_001E': 'mrent_23',
                                    'B25064_001M': 'mrent_23_se',
                                    'B25003_002E': 'ohu_23',
                                    'B25003_003E': 'rhu_23',
                                    'B25105_001E': 'mmhcosts_23',
                                    'B15003_001E': 'total_25_23',
                                    'B15003_022E': 'total_25_col_bd_23',
                                    'B15003_023E': 'total_25_col_md_23',
                                    'B15003_024E': 'total_25_col_pd_23',
                                    'B15003_025E': 'total_25_col_phd_23',
                                    'B25034_001E': 'tot_units_built_23',
                                    'B25034_010E': 'units_40_49_built_23',
                                    'B25034_011E': 'units_39_early_built_23',
                                    'B07010_025E':'mov_wc_w_income_23',
                                    'B07010_026E':'mov_wc_9000_23',
                                    'B07010_027E':'mov_wc_15000_23',
                                    'B07010_028E':'mov_wc_25000_23',
                                    'B07010_029E':'mov_wc_35000_23',
                                    'B07010_030E':'mov_wc_50000_23',
                                    'B07010_031E':'mov_wc_65000_23',
                                    'B07010_032E':'mov_wc_75000_23',
                                    'B07010_033E':'mov_wc_76000_more_23',
                                    'B07010_036E':'mov_oc_w_income_23',
                                    'B07010_037E':'mov_oc_9000_23',
                                    'B07010_038E':'mov_oc_15000_23',
                                    'B07010_039E':'mov_oc_25000_23',
                                    'B07010_040E':'mov_oc_35000_23',
                                    'B07010_041E':'mov_oc_50000_23',
                                    'B07010_042E':'mov_oc_65000_23',
                                    'B07010_043E':'mov_oc_75000_23',
                                    'B07010_044E':'mov_oc_76000_more_23',
                                    'B07010_047E':'mov_os_w_income_23',
                                    'B07010_048E':'mov_os_9000_23',
                                    'B07010_049E':'mov_os_15000_23',
                                    'B07010_050E':'mov_os_25000_23',
                                    'B07010_051E':'mov_os_35000_23',
                                    'B07010_052E':'mov_os_50000_23',
                                    'B07010_053E':'mov_os_65000_23',
                                    'B07010_054E':'mov_os_75000_23',
                                    'B07010_055E':'mov_os_76000_more_23',
                                    'B07010_058E':'mov_fa_w_income_23',
                                    'B07010_059E':'mov_fa_9000_23',
                                    'B07010_060E':'mov_fa_15000_23',
                                    'B07010_061E':'mov_fa_25000_23',
                                    'B07010_062E':'mov_fa_35000_23',
                                    'B07010_063E':'mov_fa_50000_23',
                                    'B07010_064E':'mov_fa_65000_23',
                                    'B07010_065E':'mov_fa_75000_23',
                                    'B07010_066E':'mov_fa_76000_more_23',
                                    'B06011_001E':'iinc_23',
                                    'B19001_002E':'I_10000_23',
                                    'B19001_003E':'I_15000_23',
                                    'B19001_004E':'I_20000_23',
                                    'B19001_005E':'I_25000_23',
                                    'B19001_006E':'I_30000_23',
                                    'B19001_007E':'I_35000_23',
                                    'B19001_008E':'I_40000_23',
                                    'B19001_009E':'I_45000_23',
                                    'B19001_010E':'I_50000_23',
                                    'B19001_011E':'I_60000_23',
                                    'B19001_012E':'I_75000_23',
                                    'B19001_013E':'I_100000_23',
                                    'B19001_014E':'I_125000_23',
                                    'B19001_015E':'I_150000_23',
                                    'B19001_016E':'I_200000_23',
                                    'B19001_017E':'I_201000_23'})
    
# Download ACS 2018 5-Year Estimates
# --------------------------------------------------------------------------

df_vars_18=['B03002_001E',
            'B03002_003E',
            'B19001_001E',
            'B19013_001E',
            'B25077_001E',
            'B25077_001M',
            'B25064_001E',
            'B25064_001M',
            'B15003_001E',
            'B15003_022E',
            'B15003_023E',
            'B15003_024E',
            'B15003_025E',
            'B25034_001E',
            'B25034_010E',
            'B25034_011E',
            'B25003_002E',
            'B25003_003E',
            'B25105_001E',
            'B06011_001E']

# Income categories - see notes
var_str = 'B19001'
var_list = []
for i in range (1, 18):
    var_list.append(var_str+'_'+str(i).zfill(3)+'E')
df_vars_18 = df_vars_18 + var_list

# Migration - see notes
var_str = 'B07010'
var_list = []
for i in list(range(25,34))+list(range(36, 45))+list(range(47, 56))+list(range(58, 67)):
    var_list.append(var_str+'_'+str(i).zfill(3)+'E')
df_vars_18 = df_vars_18 + var_list


# Run API query
# --------------------------------------------------------------------------
# NOTE: Memphis is located in two states so the query looks different
# same for Boston


var_dict_acs5 = c.acs5.get(df_vars_18, geo = {'for': 'tract:*',
                                 'in': sql_query}, year=2018)

# Convert and Rename Variables
# --------------------------------------------------------------------------

### Converts variables into dataframe and filters only FIPS of interest

df_vars_18 = pd.DataFrame.from_dict(var_dict_acs5)
df_vars_18['FIPS']=df_vars_18['state']+df_vars_18['county']+df_vars_18['tract']
df_vars_18 = filter_FIPS(df_vars_18)

### Renames variables

df_vars_18 = df_vars_18.rename(columns = {'B03002_001E':'pop_18',
                                          'B03002_003E':'white_18',
                                          'B19001_001E':'hh_18',
                                          'B19013_001E':'hinc_18',
                                          'B25077_001E':'mhval_18',
                                          'B25077_001M':'mhval_18_se',
                                          'B25064_001E':'mrent_18',
                                          'B25064_001M':'mrent_18_se',
                                          'B25003_002E':'ohu_18',
                                          'B25003_003E':'rhu_18',
                                          'B25105_001E':'mmhcosts_18',
                                          'B15003_001E':'total_25_18',
                                          'B15003_022E':'total_25_col_bd_18',
                                          'B15003_023E':'total_25_col_md_18',
                                          'B15003_024E':'total_25_col_pd_18',
                                          'B15003_025E':'total_25_col_phd_18',
                                          'B25034_001E':'tot_units_built_18',
                                          'B25034_010E':'units_40_49_built_18',
                                          'B25034_011E':'units_39_early_built_18',
                                          'B07010_025E':'mov_wc_w_income_18',
                                          'B07010_026E':'mov_wc_9000_18',
                                          'B07010_027E':'mov_wc_15000_18',
                                          'B07010_028E':'mov_wc_25000_18',
                                          'B07010_029E':'mov_wc_35000_18',
                                          'B07010_030E':'mov_wc_50000_18',
                                          'B07010_031E':'mov_wc_65000_18',
                                          'B07010_032E':'mov_wc_75000_18',
                                          'B07010_033E':'mov_wc_76000_more_18',
                                          'B07010_036E':'mov_oc_w_income_18',
                                          'B07010_037E':'mov_oc_9000_18',
                                          'B07010_038E':'mov_oc_15000_18',
                                          'B07010_039E':'mov_oc_25000_18',
                                          'B07010_040E':'mov_oc_35000_18',
                                          'B07010_041E':'mov_oc_50000_18',
                                          'B07010_042E':'mov_oc_65000_18',
                                          'B07010_043E':'mov_oc_75000_18',
                                          'B07010_044E':'mov_oc_76000_more_18',
                                          'B07010_047E':'mov_os_w_income_18',
                                          'B07010_048E':'mov_os_9000_18',
                                          'B07010_049E':'mov_os_15000_18',
                                          'B07010_050E':'mov_os_25000_18',
                                          'B07010_051E':'mov_os_35000_18',
                                          'B07010_052E':'mov_os_50000_18',
                                          'B07010_053E':'mov_os_65000_18',
                                          'B07010_054E':'mov_os_75000_18',
                                          'B07010_055E':'mov_os_76000_more_18',
                                          'B07010_058E':'mov_fa_w_income_18',
                                          'B07010_059E':'mov_fa_9000_18',
                                          'B07010_060E':'mov_fa_15000_18',
                                          'B07010_061E':'mov_fa_25000_18',
                                          'B07010_062E':'mov_fa_35000_18',
                                          'B07010_063E':'mov_fa_50000_18',
                                          'B07010_064E':'mov_fa_65000_18',
                                          'B07010_065E':'mov_fa_75000_18',
                                          'B07010_066E':'mov_fa_76000_more_18',
                                          'B06011_001E':'iinc_18',
                                          'B19001_002E':'I_10000_18',
                                          'B19001_003E':'I_15000_18',
                                          'B19001_004E':'I_20000_18',
                                          'B19001_005E':'I_25000_18',
                                          'B19001_006E':'I_30000_18',
                                          'B19001_007E':'I_35000_18',
                                          'B19001_008E':'I_40000_18',
                                          'B19001_009E':'I_45000_18',
                                          'B19001_010E':'I_50000_18',
                                          'B19001_011E':'I_60000_18',
                                          'B19001_012E':'I_75000_18',
                                          'B19001_013E':'I_100000_18',
                                          'B19001_014E':'I_125000_18',
                                          'B19001_015E':'I_150000_18',
                                          'B19001_016E':'I_200000_18',
                                          'B19001_017E':'I_201000_18'})

df_vars_summ = df_2023.merge(df_vars_18, on ='FIPS')
# Export the cleaned data
df_vars_summ.to_csv("data/census_summ_2023.csv", index=False)
