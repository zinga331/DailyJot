from Validator import Validator

# Replace with the Filename and function name
from Function import function

# Replace with the app name
SUBDOMAIN = 'appname'

validator = Validator(SUBDOMAIN)

def handle_function(event, context):
    results = validator.validate(event)
    # Replace 'function()' with the name of your lambda function
    return validator.sendCorsResponse(function(), results['origin'])
