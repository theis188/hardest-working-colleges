import pandas as pd
import numpy as np

class AcsCodes(object):
	def __init__(self):
		self.code_file_path = 'ACSPUMS2015CodeLists.xls'
		self.load_values()
	def descriptive_call_fun(self,fun,s):
		print('running {}...'.format(s))
		fun()
		print('complete!')
	def load_values(self):
		self.descriptive_call_fun(self.load_colmaj_dict,'college major codes')
		self.descriptive_call_fun(self.load_occupation_codes,'occupation codes')
	def load_colmaj_dict(self):
		colmaj_code=pd.read_excel(self.code_file_path,sheet_name='Field of Degree', skiprows=2)
		self.colmaj_code_dict = {code:degree for code,degree in
					zip(colmaj_code['2015 PUMS code'],
						colmaj_code['2015 PUMS Field of Degree Description'])}
	def load_occupation_codes(self):
		occ_code = pd.read_excel('ACSPUMS2015CodeLists.xls',sheet_name='Occupation', skiprows=14)
		occ_code = occ_code.dropna(axis=0,how='all').reset_index()
		del occ_code['index']
		occ_code_short = occ_code.ix[:,[0,1]].dropna(axis=0,how='all').reset_index()
		del occ_code_short['index']
		two_cols = occ_code_short.ix
		self.occ_name_dict = {str(code):name for code,name in
								zip(occ_code['2010 Census Occupation Code'],
									occ_code['Unnamed: 2']) }
		self.occ_code_dict = {}
		for i in range( occ_code_short.shape[0] ):
			cen_code,soc_code = two_cols[i,:]
			if len(str(cen_code))>4:	
				continue
			if 'XX' in str(soc_code):
				last_cen_code = cen_code
				continue
			if not (isinstance(cen_code,str)):
				if np.isnan(cen_code):
					if (soc_code) == "Combines:":		
						continue
					if not (isinstance(soc_code,str)):
						continue
					self.occ_code_dict[str( soc_code ).strip() ] = str(last_cen_code).strip()
					continue
			last_cen_code = cen_code
			self.occ_code_dict[str( soc_code).strip() ] = str( cen_code ).strip()


columns = {
	"PERNP":"Total income laste 12 months",
	"AGEP":"Age",
	"OCCP":"Occupation",
	"FOD1P":"Bachelors Degree Field",
	"WKHP":"Hours per week worked",
	"INDP":"Industry",
	"ST":"State",
	"SCHL":"Eduction Level"
}

NONCOMP_indu = {
	'9160',
	'9170',
	'9180',
	'9190',
	'9370',
	'9380',
	'9390',
	'9470',
	'9480',
	'9490',
	'9570',
	'9590',
	'7860',
	'7870',
	'7880',
	'7890',
	'7970',
	'7980',
	'7990',
	'8070',
	'8080',
	'8090',
	'8170',
	'8180',
	'8190',
	'8270',
	'8290',
	'8370',
	'8380',
	'8390',
	'8470',
}

rev_occ_grps_append = {
	'25-1000':'Postsecondary Teachers',
	'41-1011':'Sales Managers',
	'41-1012':'Sales Managers',
	'29-9000':'Healthcare Support Occupations',
	'15-113X':'Software Developers',
	'11-9199':'Other'
}

acs_state_codes={
int('01'):'Alabama',
int('02'):'Alaska',
int('04'):'Arizona',
int('05'):'Arkansas',
int('06'):'California',
int('08'):'Colorado',
int('09'):'Connecticut',
int('10'):'Delaware',
int('11'):'District of Columbia',
int('12'):'Florida',
int('13'):'Georgia',
int('15'):'Hawaii',
int('16'):'Idaho',
int('17'):'Illinois',
int('18'):'Indiana',
int('19'):'Iowa',
int('20'):'Kansas',
int('21'):'Kentucky',
int('22'):'Louisiana',
int('23'):'Maine',
int('24'):'Maryland',
int('25'):'Massachusetts',
int('26'):'Michigan',
int('27'):'Minnesota',
int('28'):'Mississippi',
int('29'):'Missouri',
int('30'):'Montana',
int('31'):'Nebraska',
int('32'):'Nevada',
int('33'):'New Hampshire',
int('34'):'New Jersey',
int('35'):'New Mexico',
int('36'):'New York',
int('37'):'North Carolina',
int('38'):'North Dakota',
int('39'):'Ohio',
int('40'):'Oklahoma',
int('41'):'Oregon',
int('42'):'Pennsylvania',
int('44'):'Rhode Island',
int('45'):'South Carolina',
int('46'):'South Dakota',
int('47'):'Tennessee',
int('48'):'Texas',
int('49'):'Utah',
int('50'):'Vermont',
int('51'):'Virginia',
int('53'):'Washington',
int('54'):'West Virginia',
int('55'):'Wisconsin',
int('56'):'Wyoming',
int('72'):'Puerto Rico',
}