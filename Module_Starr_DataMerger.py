'''This Module captures the functions to be used in the Salesforce / CIQ Data merger for Starr'''



def hello_word():
    
    print('Hello world! Today is a good day to code')

    
    
# CHECK FOR MISSING VALUES

def get_nanValues(Dataframe):
    '''The purpose of this function is to count nan values of a dataframe
    Input  = Dataframe.  Iterates over each column.
    Output = Dictionary with count of none values per column. 
    
    date:    02.10.2018
    author:  Chris Cirelli
    '''

    # Dict to catch values per column. 
    Dict = {}
    
    # Loop over columns. 
    for col in Dataframe:
        
        # Define dict keys. 
        Dict[col] = 0
        
        # Count none values. 
        Count = 0
        
        # Loop over values in each column
        for value in Dataframe[col]:
            #if value is none
            if value is None:
                Count += 1
                
            Dict[col] = Count
        
    # Return Dict with none values. 
    return Dict


# GET LIST OF FIRST COMPANY NAME (Column Slicer set at -7)

def get_company_name(Dataframe, Position):

    '''The purpose of this code is to obtain either the first or second company name from a either the SF or CIQ datasets. 
    
    Input  = a.) the target dataframe, b.) either 'First' or 'Second' position to indicate which part of the name to generate. 
    Output = A list of either the first or second name w/ ',' and '.' removed. 
    
    date:   02.10.2018
    author: Chris Cirelli
    '''
    
    # Obtain the column where the Company Names are located. 
    List_company_name = Dataframe['Company Name']
     
    # Clean Names
    
    # Convert all names to string 
    CIQ_string = [str(word) for word in List_company_name]
    # Replace comma with space
    CIQ_replace_comma = [word.replace(',', '') for word in CIQ_string]
    # Split on spaces
    CIQ_split_on_space = [word.split(' ' ) for word in List_company_name]    
    
    
    # Create a list to capture the first or second names generated from the below function
    List_name = []
    
    # Iterate over the CIQ dataframe. 
    for x in CIQ_split_on_space:
        
        # if Position == First, append the first name to List_name
        if Position == 'First':
            List_name.append(x[0])
    
        # Else Position == Second
        else:
            # If there are two names or more, append the second to List_name
            if len(x)>1:
                List_name.append(x[1])
            # Else, append a placeholder to the list and take the placeholder. 
            else:
                x.append('placeholder')
                List_name.append(x[1])
    
    # Replace any remaining commas with a space.  
    List_final = [x.replace(',','') for x in List_name]
    
    # Return the final list. 
    return List_final


def clean_zip_Code(Dataframe_str, Dataframe):
    '''The purpose of this code is to generate a zipCode with a single format for comparison purposes.  
    Input  = a.) a string version of the target dataframe. b.) The target dataframe. 
    Output = a list of zipCodes for each record with a standardized format. 
    
    date:   02.10.2018
    author: Chris Cirelli
    '''
    
    # Identify the target dataframe. 
    if Dataframe_str == 'DAT_SF':
        
        # Obtain the zipCode column of the SF dataframe 
        DAT_SF_ZIP = Dataframe['Billing Zip/Postal Code']
        
        # Create a list to capture the clean zipCode values. 
        DAT_SF_Zip_Code_Clean = []
        
        # Iterate over the zipCode column. 
        for x in DAT_SF_ZIP:
            # Conver int to string. 
            x_string = str(x)
            # Split any zipCodes on '-'
            x_split = x_string.split('-')
            # Take the part of the zipCode in position one. 
            DAT_SF_Zip_Code_Clean.append((x_split[0]))
            
        # Return a list of the zipCodes n the standardized format.  
        return DAT_SF_Zip_Code_Clean
    
    # Note:  the below code repeats the same proces, but for the CIQ dataframe. 
    
    elif Dataframe_str == 'DAT_CIQ':
        
        DAT_CIQ_ZIP = Dataframe['Primary Zip Code/Postal Code']
        DAT_CIQ_Zip_Code_Clean = []
    
        for x in DAT_CIQ_ZIP:
            x_string = str(x)
            x_split = x_string.split('-')
            DAT_CIQ_Zip_Code_Clean.append((x_split[0]))
            
        return DAT_CIQ_Zip_Code_Clean
    

def get_match_v2():
    '''The purpose of this code is to match records from the SF and CIQ dataframes. 
    Input  = The CIQ and SF Dataframes.  Requires that these dataframes were pre-cleaned by the codes included in the
             Module_Starr_Datamerge file. 
    Output = The DAT_CIQ Dataframe with the matching values appended to each row. 
    
    Date:    02.10.2018
    author:  Chris Cirelli
    '''
    
    # Create a tuple for each row in the dataframe. 
    CIQ = [x for x in CIQ_head.itertuples()]         # Rever back to DAT CIQ when finished testing. 
    SF = [x for x in DAT_SF.itertuples()]
    
    # Loop over each row of the CIQ Dataframe. 
    for row_CIQ in CIQ:
        
        # Get the index value for the target CIQ row.  Use this at end of code. 
        row_CIQ_index_value = row_CIQ.index
        
        # Loop over each row of the SF Dataframe. 
        for row_SF in SF:
            if row_CIQ[8] in row_SF[8]:
            
                # Limit SF dataframe to only those records that have the CIQ zip code
                SF_limit = DAT_SF['Zip Code Clean'] == row_CIQ[8]
                # Define new SF Dataframe
                SF_limited_zip = DAT_SF[SF_limit]
                # Create a new SF tupple object from the SF limited dataframe. 
                SF_2 = [x for x in SF_limited_zip.itertuples()]
                
                # Iterate over new SF dataframe
                for row_SF2 in SF_2:
                    # See if the first name of the same company in question is in the SF dataframe
                    if row_CIQ[6] in row_SF2[6]:
                        
                        # Limit the SF Dataframe to only those records that have the CIQ first company name
                        SF_limit = SF_limited_zip['Company First Name'] == row_SF2[6]
                        # Define new SF Dataframe
                        SF_limited_firstName = SF_limited_zip[SF_limit]
                        # Create a new SF tupple object from the SF limited dataframe. 
                        SF_3 = [x for x in SF_limited_firstName.itertuples()]
                        
                        
                        # Iterate over new SF dataframe
                        for row_SF3 in SF_3:
                            
                            # Check to see if there is a match with the second name from our original CIQ dataframe
                            if row_CIQ[7] in row_SF3[7]:
                            
                                # Limit the SF Dataframe to only those records that have the CIQ second company name
                                SF_limit = SF_limited_firstName['Company Second Name'] == row_SF3[7]
                                # Define Final SF Dataframe
                                SF_Final = SF_limited_firstName[SF_limit]
                        
                                return SF_Final
                        

            
def write_to_excel(dataframe, filename):
    '''The purpose of this code is to write a pandas dataframe to excel. 
    
    Input  = a.) Target dataframe, b.) String representing the resulting file name. 
    Output = an Excel spreadsheet with the data from the target dataframe. 
    '''
    # Ensure that pandas is imported. 
    import pandas as pd
    # Choose an Excel writer. 
    writer = pd.ExcelWriter(filename+'.xlsx')
    # Transfer the dataframe to Excel and name the sheet 'Data'
    dataframe.to_excel(writer, sheet_name = 'Data')
    # Save the Excel file. 
    writer.save()

    # return none as this function writes directly to the current directory. 
    return None


















