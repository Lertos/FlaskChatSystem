import re
from modules import db_manager


#Validates the account creation info provided by the new player
def validateAccountInfo(username, displayName, password, passwordConfirm, season):
    #Check for tampering with the season value
    try:
        season = int(season)
    except ValueError:
        return 'Dont mess with form values...'

    #Check if the username/display name/password meets length requirements
    if(len(username) < 6 or len(displayName) < 6 or len(password) < 6):

        if(len(username) < 6):
            return 'Your username must be more than 6 characters'
        elif(len(displayName) < 6):
            return 'Your display name must be more than 6 characters'         
        else:
            return 'Your password must be more than 6 characters'

    #Check if there are any symbols in the players username
    if re.match('^[\w-]+$', username) is None:
        return 'Your username must not have symbols in it'

    #Check if there are any symbols in the players display name
    if re.match('^[\w-]+$', displayName) is None:
        return 'Your display name must not have symbols in it'

    #Check if passwords are the same
    if(password != passwordConfirm):
        return 'Passwords do not match'

    return ''