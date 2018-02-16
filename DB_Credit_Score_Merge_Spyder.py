# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 19:41:28 2018

@author: Chris.Cirelli
"""

# Import Libraries
import os
import pandas as pd



# Import Files

#File_universe_DB = r'C:\Users\Chris.Cirelli\Desktop\Capital IQ Match w Salesforce\Final Report\D&B Universe.csv'
#Renewal_Book_DB = r'C:\Users\Chris.Cirelli\Desktop\Capital IQ Match w Salesforce\Final Report\Renewal_book_w_DUNS.xlsx'

# Read Files

#File_universe_open = open(File_universe_DB)
#File_renewal_book = open(Renewal_Book_DB, 'rb')

# Create Dataframes

#df_DB_universe = pd.read_csv(File_universe_DB)
#df_renewal_book = pd.read_excel(File_renewal_book)


# Create a Unique Set for the DB Universe
def get_universe_set(df):
    df_DB_universe_set = df.drop_duplicates(subset = 'D-U-N-S Number')
    return df_DB_universe_set

#df_DB_universe_set = get_universe_set(df_DB_universe)



def return_DUNS_str(df): 
    if df == 'df_renewal_book':
        df_renewal_book['DUNS Number'] = [str(x) for x in df_renewal_book['DUNS Number']]
        df_renewal_book['DUNS Number'] = [x[:-2] for x in df_renewal_book['DUNS Number']]
        return df_renewal_book
    elif df == 'df_DB_universe_set':
        df_DB_universe_set['D-U-N-S Number'] = [str(x) for x in df_DB_universe_set['D-U-N-S Number']]   
        return df_DB_universe_set



#df_renewal_book_str = return_DUNS_str('df_renewal_book')
#df_universe_set_str = return_DUNS_str('df_DB_universe_set')
#
#DB_renewal_list = [x for x in df_renewal_book_str['DUNS Number']]
#DB_universe_list = [x for x in df_universe_set_str['D-U-N-S Number']]


def get_match_count():
    Count = 0

    for x in DB_renewal_list:
        if x in DB_universe_list:
            Count += 1
    return Count



# Create an enumerated list for the columns of each dataset. 

#print('Renewal Book Columns =>\n\n', list(enumerate(df_renewal_book.columns)))
#print('')
#print('')
#print('Universe List Columns =>\n\n', list(enumerate(df_DB_universe_set.columns)))



def get_DelinquencyScore_for_matching_records(df_renewal, df_universe):
    '''The purpose of this code is to identify matching records by using the DUNS numbers.
    Input  = Two dataframes 
    Output = A single list that includes all of the matchings and None values. The list must be 
             the same length as the other columns in the renewal dataframe. 
    '''
    
    # Create Tuples for each dataframe.     
    df_DB_renewal_tuple = [x for x in df_renewal.itertuples()]
    df_DB_universe_set_tuple = [x[9] for x in df_universe.itertuples()]

    # Create the List to catch the matches
    List_of_matching_records = []
    
    # Iterate over the rows in the universe dataset
    for ren_row in df_DB_renewal_tuple:
        # Identify the index value that pertaines to the DUNS Number and assign it to univ_DUNS
        ren_DUNS = ren_row[8]
        
        # Identify if the DUNS number from the universe list is in the renewal list
        if ren_DUNS in df_DB_universe_set_tuple:
            
            # Identify Delinquency Rating
            df_universe_matching_DUNS = df_universe['D-U-N-S Number'] == ren_DUNS
            df_universe_matching_record = df_universe[df_universe_matching_DUNS]
            df_universe_first_record = df_universe_matching_record.iloc[:1]
            
            # Append matching record to list
            List_of_matching_records.append(df_universe_first_record['Delinquency Risk'])

            # If there is no match, append a None value to the list. 
        else:
            List_of_matching_records.append('No Match Found')
    
    # Return to the user the list of Delinquincy scores for the matching records
    return List_of_matching_records

#List_delinquencyScore_matching_records = get_DelinquencyScore_for_matching_records(df_renewal_book_str, df_universe_set_str)



df_renewal_book_str['Delinquency Score'] = List_delinquencyScore_matching_records


                   
                   
                   
def write_to_excel(dataframe, filename):
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()
    
write_to_excel(df_renewal_book_str, 'Renewal_Book_w_Delinquency_Rates')
    

























    



