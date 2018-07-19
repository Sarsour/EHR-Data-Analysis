import pandas as pd
import os
import glob
from pandas import ExcelWriter

'''
This script imports the data and reformats it to make it easier for analysis then exports it back out to excel

Cleaning Data:
	Oregon was spelled wrong, fixed in file before running script
'''

	
def main():
	path = "C:\\Users\\NSarsour\\Documents\\EHR Data\\Sample_EHR_Data-master\\data backup"
	os.chdir(path)

	files_list = get_files(path)
	#print(files_list)
	
	df_dict = import_tables(files_list)

	patient_df, encounter_df, encounterdx_df = join_main_dfs_with_lookup_dfs(df_dict)
	print(patient_df.head())
	print('')
	print(encounter_df.head())
	print('')
	print(encounterdx_df.head())
	print('')
	
	export_dfs_to_excel(patient_df, encounter_df, encounterdx_df)
	

'''Find all files in folder and add to files dict'''
def get_files(path):
	dirs = os.listdir(path)
	files_list = []

	for file in dirs:
		files_list.append(file)
	
	return files_list
	

'''Create dict of dataframes from imported files in get_files method'''
def import_tables(files):
	df_dict = dict()
	
	for file in files:
		df = pd.read_csv(file)
		df_dict[str(file)[:-4]] = df
	
	return df_dict

	
'''Switching out the abbreviated values in the 3 main dfs for their values in the lookup tables'''
def join_main_dfs_with_lookup_dfs(df_dict):
	'''Patient dataframe'''
	df_dict['patient'] = pd.merge(df_dict['patient'], df_dict['lookupsex'], on='sex', how='left')
	del df_dict['patient']['sex']
	
	df_dict['patient'] = pd.merge(df_dict['patient'], df_dict['lookupstate'], on='st', how='left')
	del df_dict['patient']['st']
	
	df_dict['patient'] = pd.merge(df_dict['patient'], df_dict['lookuprace'], on='raceid', how='left')
	del df_dict['patient']['raceid']
	
	patient_df = df_dict['patient']
	
	cols = list(patient_df.columns.values)
	cols.pop(cols.index('city'))
	cols.pop(cols.index('statedesc'))
	patient_df = patient_df[cols+['city','statedesc']]
	
	'''Encounter dataframe'''
	df_dict['encounter'] = pd.merge(df_dict['encounter'], df_dict['lookuphospital'], on='hospid', how='left')
	del df_dict['encounter']['hospid']
	
	df_dict['encounter'] = pd.merge(df_dict['encounter'], df_dict['lookupadmitsource'], on='asourceid', how='left')
	del df_dict['encounter']['asourceid']
	
	df_dict['encounter'] = pd.merge(df_dict['encounter'], df_dict['lookupdisposition'], on='dispid', how='left')
	del df_dict['encounter']['dispid']
	
	encounter_df = df_dict['encounter']
	
	'''Encounterdx dataframe'''
	df_dict['encounterdx'] = pd.merge(df_dict['encounterdx'], df_dict['lookupdiagnosis'], on='dxcode', how='left')
	del df_dict['encounterdx']['dxcode']
	del df_dict['encounterdx']['longtitle']
	
	encounterdx_df = df_dict['encounterdx']
	
	return patient_df, encounter_df, encounterdx_df


'''Export all dataframes to same excel file'''
def export_dfs_to_excel(patient_df, encounter_df, encounterdx_df):
	path = "C:\\Users\\NSarsour\\Documents\\EHR Data"
	os.chdir(path)
	
	writer = ExcelWriter('Processed_Dataframes.xlsx')
	patient_df.to_excel(writer,'patient_df')
	encounter_df.to_excel(writer,'encounter_df')
	encounterdx_df.to_excel(writer,'encounterdx_df')
	writer.save()


if __name__ == "__main__":
		main()