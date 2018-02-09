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




















