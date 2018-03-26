import pandas as pd
from config import columns, AcsCodes, rev_occ_grps_append, NONCOMP_indu, acs_state_codes
from collections import defaultdict
import json
import re
import numpy as np
import os

######## Initialize and load ACS data

acs_path = ## insert path here

usa = pd.read_csv( os.path.join(acs_path,'ss15pusa.csv') )
print('loaded A')
usb = pd.read_csv( os.path.join(acs_path,'ss15pusb.csv') )
print('loaded B')
us = pd.concat([usa,usb])
print('Concatenated')
del usa
del usb
us_sel = us[[col for col in columns]]
print('Columns selected')
us_sel_col = us_sel[ (us_sel['SCHL']>=21) ].dropna(axis=0) ### only bachelors degreeand higher
us_sel_col_ft = us_sel_col[ (us_sel_col['PERNP']>10000) ] ### earnings > $10000/yr
codes = AcsCodes()

################ College Work Hours

col_work = us_sel_col.groupby(['FOD1P']).mean().WKHP.reset_index()
col_work['maj_name']=col_work.FOD1P.apply( lambda x: codes.colmaj_code_dict[x])
col_work_dict = {maj:hrs for maj,hrs in zip(col_work.maj_name,col_work.WKHP)}

################ Load College Data (downloaded from NCES)

static_cols = {'Institution Name'}

df1 = pd.read_csv('college_data_1.csv')
df1 = df1.set_index('UnitID')

df2 = pd.read_csv('college_data_2.csv')
df2 = df2.set_index('UnitID')

df3 = pd.read_csv('college_data_3_websites.csv')
df3 = df3.set_index('UnitID')

def check_colname(s):
	if s in static_cols:
		return True
	elif 'CIPCODE' in s:
		return True
	else:
		return False

def clean_colname(col):
	if col in static_cols:
		return col
	else:
		return re.search(r' CIPCODE=([^ ]+) ',col).groups(1)[0]

def clean_df(df):
	for col in df.columns:
		if not check_colname(col):
			del df[col]
	df.columns = [clean_colname(col) for col in df.columns]
	return df

df1c = clean_df(df1)
df2c = clean_df(df2)
del df2c['Institution Name']
del df3['Institution Name']
df = df1c.join(df2c)
df = df.join(df3)
df = df[ ~df['99'].isnull() ]
df_large = df[ df['99']>100 ] ### colleges with >100 graduates
df_large = df_large[ ~df_large['WEBADDR (HD2014)'].isnull() ] ## require web address

############### convert college majors between lists

def get_major_conversion_list():
	ret = defaultdict(list)
	with open('CIP_to_colmaj.txt') as f:
		for line in f:
			_,code,colmaj_title = line.strip().split('\t')
			ret[colmaj_title].append(code)
	return ret

major_conversion = get_major_conversion_list() ####### Load college major conversion list

for major in major_conversion:  #######
	in_maj = major_conversion[major]
	in_maj = [m for m in in_maj if m in df_large.columns]
	df_large[major] = df_large[in_maj].sum(axis=1)

df_large['Total'] = df_large[list(major_conversion)].sum(axis=1)

temp_col = pd.Series( [0]*df_large.shape[0],index=df_large.index )
for major in major_conversion:
	temp_col = temp_col + df_large[major]/df_large['Total']*col_work_dict[major]

college_work = pd.DataFrame( {'College':df_large['Institution Name'] , 'Hours':temp_col} )

######### Income Data

col_sal_count = us_sel_col_ft[ us_sel_col_ft['SCHL']==21 ].groupby(['FOD1P']).count().PERNP
col_sal_mean = us_sel_col_ft[ us_sel_col_ft['SCHL']==21 ].groupby(['FOD1P']).mean().PERNP
col_sal_median = us_sel_col_ft[ us_sel_col_ft['SCHL']==21 ].groupby(['FOD1P']).median().PERNP
col_majors = pd.Series(col_sal_mean.index, index = col_sal_mean.index).apply( lambda x: codes.colmaj_code_dict[x] )


bach_sal_info_df = pd.DataFrame({
			"count":col_sal_count,
			"mean":col_sal_mean,
			"median":col_sal_median,
			"major":col_majors,
	})

bach_sal_info_dict={
	major:{
	'count':int(count),
	'mean':int(mean),
	'median':int(median)
	}
	for major,count,mean,median in
	zip( bach_sal_info_df.major,
		bach_sal_info_df['count'],
		bach_sal_info_df['mean'],
		bach_sal_info_df['median'] )
}

median_col = pd.Series( [0]*df_large.shape[0],index=df_large.index )
mean_col = pd.Series( [0]*df_large.shape[0],index=df_large.index )
for major in major_conversion:
	median_col = median_col + df_large[major]/df_large['Total']*bach_sal_info_dict[major]['median']
	mean_col = mean_col + df_large[major]/df_large['Total']*bach_sal_info_dict[major]['mean']

college_sals_df = pd.DataFrame( {'College':df_large['Institution Name'] , 'UnitID':df_large.index,
							'Mean_Sal':mean_col, 'Median_Sal':median_col} )


######### final

addresses_df = pd.read_csv('college_addresses.csv')
college_info = addresses_df.join(college_work,on=['UnitID']).merge(college_sals_df,left_on=['UnitID'],right_on=['UnitID'])

def get_top_college_majors(college):
	maj_list = list(major_conversion)
	print(college)
	sub = df_large[ df_large.index==college ]
	major_counts = np.array(sub[maj_list]).reshape(-1)
	total = major_counts.sum()
	sorted_counts = pd.Series(  major_counts,index=maj_list).sort_values(ascending=False)
	ret = [
		{
			'major':major,
			'count':int(count),
			'total':int(total),
			'percent':'{:.1f}%'.format( 100.*count/total ),
			'hours':col_work_dict[major],
			'mean_sal':bach_sal_info_dict[major]['mean'],
			'median_sal':bach_sal_info_dict[major]['median'],
			'stat_count':bach_sal_info_dict[major]['count'],
		}
		for count,major,_ in zip( sorted_counts, sorted_counts.index, range(10) )
		if count>0
	]
	return ret

college_info = college_info.join( df_large[['WEBADDR (HD2014)']])
college_info = college_info.sort_values('Hours',ascending=False)

college_info.to_csv('output.csv')



