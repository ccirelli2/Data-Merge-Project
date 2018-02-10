'''This Module captures the functions to be used in the Salesforce / CIQ Data merger for Starr'''



def hello_word():
    
    print('Hello world! Today is a good day to code')

    
    
# CHECK FOR MISSING VALUES

def get_nanValues(Dataframe):
    '''The purpose of this function is to count nan values of a dataframe
    Input  = Dataframe.  Iterates over each column.
    Output = Dictionary with count of none values per column. '''

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

    '''The purpose of this code is to clean the comapny name 
    1.) Remove comma
    2.) Split on space
    3.) Create a list for the first and second words of the company name. '''

    # Get List of Company names
    List_company_name = Dataframe['Company Name']
     
    # Clean Lists - Remove Commas / Split on spaces
    
    CIQ_string = [str(word) for word in List_company_name]
    CIQ_replace_comma = [word.replace(',', '') for word in CIQ_string] 
    CIQ_split_on_space = [word.split(' ' ) for word in List_company_name]    
    
    List_name = []
    
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
    
    List_final = [x.replace(',','') for x in List_name]
    
    
    return List_final


def clean_zip_code(String, Dataframe):
    
    if String == 'DAT_SF':
        
        DAT_SF_ZIP = Dataframe['Billing Zip/Postal Code']
        DAT_SF_Zip_Code_Clean = []
    
        for x in DAT_SF_ZIP:
            x_string = str(x)
            x_split = x_string.split('-')
            DAT_SF_Zip_Code_Clean.append((x_split[0]))
    
        return DAT_SF_Zip_Code_Clean
    
    elif String == 'DAT_CIQ':
        
        DAT_CIQ_ZIP = Dataframe['Primary Zip Code/Postal Code']
        DAT_CIQ_Zip_Code_Clean = []
    
        for x in DAT_CIQ_ZIP:
            x_string = str(x)
            x_split = x_string.split('-')
            DAT_CIQ_Zip_Code_Clean.append((x_split[0]))
    
        return DAT_CIQ_Zip_Code_Clean
    

def get_match_v2():

    CIQ = [x for x in DAT_head.itertuples()]
    SF = [x for x in DAT_SF.itertuples()]

    for row_CIQ in CIQ:
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
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()




















