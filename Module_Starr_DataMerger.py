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
    

    
def get_match(CIQ_Dataframe, SF_Dataframe):
       
    # Step 1:  Create a list of the col name in question. 
    List_CIQ_zip = [x for x in CIQ_Dataframe['Zip Code Clean']]
    List_SF_zip = [x for x in SF_Dataframe['Zip Code Clean']]
    
    # For each zip code in our CIQ dataframe
    for zipCode in List_CIQ_zip:
        
        # Check to see if there is a match in our List_SF_zip list
        if zipCode in List_SF_zip:
            
        
            # Step 2: For each match, we are going to narrow our two dataframes by the zipCode. 
            CIQ_limit_zip = CIQ_Dataframe['Zip Code Clean'] == zipCode
            CIQ_Dataframe_limit_by_zip = CIQ_Dataframe[CIQ_limit_zip]
            
            SF_limit_zip = SF_Dataframe['Zip Code Clean'] == zipCode
            SF_Dataframe_limit_by_zip = SF_Dataframe[SF_limit_zip]
            
            
            # Repeat Step1: Now that you have your new dataframes limited by the matching zip code, we need to repeat step 1 
            List_CIQ_coName = [x for x in CIQ_Dataframe_limit_by_zip['Company First Name']]
            List_SF_coName = [x for x in SF_Dataframe_limit_by_zip['Company First Name']]
            
            # Iterate over the List_CIQ_coName list 
            for coName in List_CIQ_coName:
                # Check to see if any of these names match the coNames in List_SF_coNames
                if coName in List_SF_coName:
                    
                    
                    # Repeat Step 2: For each match, we are going to narrow our two dataframes by the Company's First Name. 
                    CIQ_limit_coName = CIQ_Dataframe_limit_by_zip['Company First Name'] == coName
                    CIQ_Dataframe_limit_by_coName = CIQ_Dataframe_limit_by_zip[CIQ_limit_coName]
                    
                    SF_limit_coName = SF_Dataframe_limit_by_zip['Company First Name'] == coName
                    SF_Dataframe_limit_by_coName = SF_Dataframe_limit_by_zip[SF_limit_coName]
            
                    
                    # Repeat Step1:  Now that we have identified the matching coNames within the defined zipCode, 
                    #                we need to iterate over the lists using the sec_coName
                
                    List_CIQ_sec_coName = [x for x in CIQ_Dataframe_limit_by_coName['Company Second Name']]
                    List_SF_sec_coName = [x for x in SF_Dataframe_limit_by_coName['Company Second Name']]
            
            
                    # Iterate over CIQ sec_coName list:
                    for sec_coName in List_CIQ_sec_coName:
                        # Check if sec_coName in DF dataframe. 
                        if sec_coName in List_SF_sec_coName:
                            
                            CIQ_limit_sec_coName = CIQ_Dataframe_limit_by_coName['Company Second Name'] == sec_coName
                            CIQ_limit_by_sec_coName = CIQ_Dataframe_limit_by_coName[CIQ_limit_sec_coName]
                        
                            SF_limit_sec_coName = SF_Dataframe_limit_by_coName['Company Second Name'] == sec_coName
                            SF_limit_sec_coName = SF_Dataframe_limit_by_coName[SF_limit_sec_coName]
                            
                            Final_SF_Dataframe = SF_limit_sec_coName.append(CIQ_limit_by_sec_coName)
                            
        return Final_SF_Dataframe
            
def write_to_excel(dataframe, filename):
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()




















