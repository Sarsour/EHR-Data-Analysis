import pandas as pd
import datetime as dt
import numpy as np
from pandas import ExcelWriter

'''Initialize global analysis excel sheet to be accessed in methods'''
writer = ExcelWriter('Analysis_Dataframes.xlsx')
	
def main():
	patient_df = pd.read_excel('Processed_Dataframes.xlsx', sheet_name='patient_df')
	encounter_df = pd.read_excel('Processed_Dataframes.xlsx', sheet_name='encounter_df')
	encounterdx_df = pd.read_excel('Processed_Dataframes.xlsx', sheet_name='encounterdx_df')
	
	print(patient_df.head())
	print('')
	print(encounter_df.head())
	print('')
	print(encounterdx_df.head())
	print('')
	

	
	basic_patient_analysis(patient_df)
	
	basic_encounter_analysis(encounter_df)
	
	basic_encounterdx_analysis(encounterdx_df)
	
	
	
'''Method created to calculate value counts of certain columns'''
def value_count_auto(df, og_col_name, new_col_name):
	analysis_df = pd.DataFrame(df[og_col_name].value_counts())
	analysis_df.columns = ['Number']
	analysis_df.index.name = new_col_name
	#print(analysis_df.head())
	#print('')
	export_dfs_to_excel(analysis_df, (new_col_name + ' Count'))
	#return analysis_df


'''Basic Analysis of patient_df'''
def basic_patient_analysis(patient_df):
	'''number of patients'''
	num_of_patients = patient_df.shape[0]
	print('num of patients: ', num_of_patients)
	print('')
	
	'''patients per state'''
	value_count_auto(patient_df, 'statedesc', 'State')
	
	'''patients per gender'''
	value_count_auto(patient_df, 'sexdesc', 'Sex')
	
	'''patients per race'''
	value_count_auto(patient_df, 'racedesc', 'Race')
	
	'''patients per age'''
	now = pd.Timestamp(dt.datetime.now())
	patient_df['dob'] = pd.to_datetime(patient_df['dob'], format='%Y-%m-%d')
	patient_df['dob'] = patient_df['dob'].where(patient_df['dob'] < now, patient_df['dob'] -  np.timedelta64(100, 'Y'))
	patient_df['age'] = (now - patient_df['dob']).astype('<m8[Y]')
	patient_df['age'] = patient_df['age'].astype(np.int64)
	patients_per_age_df = pd.DataFrame(patient_df['age'].value_counts())
	patients_per_age_df.columns = ['Number']
	patients_per_age_df.index.name = 'Age'
	#print(patients_per_age_df.head())
	#print('')
	export_dfs_to_excel(patients_per_age_df, ('Age Count'))

	'''patients per city'''
	value_count_auto(patient_df, 'city', 'City')
	
	'''patients per zip code'''
	value_count_auto(patient_df, 'zip', 'Zip Code')
	
	'''patients per address'''
	value_count_auto(patient_df, 'address', 'Address')
	

'''Basic Analysis of encounter_df'''	
def basic_encounter_analysis(encounter_df):
	'''number of encounters - not accurate, see count in basic_encounterdx_analysis'''
	num_of_encounters = encounter_df.shape[0]
	print('num of encounters: ', num_of_encounters)
	print('')
	
	'''encounters per patientid''' #issue with this one - looks like patient and encounterids are wrong
	value_count_auto(encounter_df, 'patientid', 'Patientid')
	
	'''encounters per hospital'''
	value_count_auto(encounter_df, 'hospitalname', 'Hospital')
	
	'''encounters per state'''
	value_count_auto(encounter_df, 'statedesc', 'State')
	
	'''encounters per date'''
	value_count_auto(encounter_df, 'adate', 'Date')
	
	'''encounters per issue'''
	value_count_auto(encounter_df, 'dispdesc', 'Issue')
	
	'''length of stay (average, long, most frequent)'''
	value_count_auto(encounter_df, 'los', 'Length of Stay')
	
	max_los = encounter_df['los'].max()
	print('Max Length of Stay: ', max_los)
	
	avg_los = encounter_df['los'].mean()
	print('Average Length of Stay: ', avg_los)


'''Basic Analysis of encounterdx_df'''	
def basic_encounterdx_analysis(encounterdx_df):
	'''number of encounters'''
	num_of_encounters = encounterdx_df.shape[0]
	print('Number of Encounters: ', num_of_encounters)
	print('')
	
	'''encounters per result'''
	value_count_auto(encounterdx_df, 'shorttitle', 'Result')
	
	
'''Export analysis dataframes to same excel file'''
def export_dfs_to_excel(df, sheet_name):
	df.to_excel(writer, sheet_name)
	writer.save()
	
	
if __name__ == "__main__":
		main()