import json
from DecimalEncoder import DecimalEncoder
from urllib.parse import urlparse

class Validator:

    DEV_DOMAIN = "rll-dev.byu.edu"
    PRD_DOMAIN = "rll.byu.edu"
    allowedDomains = [DEV_DOMAIN, PRD_DOMAIN]

    def __init__(self, sub):
        self.subdomain = sub

    def validate(self, event):
        print('Event:', event)

        origin = self.getOrigin(event)
        domain = self.getDomain(origin)
        if (domain is None):
            raise Exception('Request does not come from an allowed domain:', origin)
        if (not self.validateRequest(origin, domain)):
            raise Exception('Request does not come from an allowed origin:', origin)
        return {'origin': origin, 'domain': domain}
    
    def getOrigin(self, event):
        caseInsensitiveEvent = dict((key.lower(), event[key]) for key in event)
        headers = caseInsensitiveEvent.get('headers',{})
        if headers is None:
            return None
        
        caseInsensitiveHeaders = dict((key.lower(), headers[key]) for key in headers)
        origin = caseInsensitiveHeaders.get('origin', None)
        return origin
    
    def getDomain(self, origin):
        if (origin is None):
            print('No origin provided in request. Origin is None.')
            return None
        
        hostname = urlparse(origin).hostname

        if (hostname.endswith(self.DEV_DOMAIN)):
            return self.DEV_DOMAIN
        elif (hostname.endswith(self.PRD_DOMAIN)):
            return self.PRD_DOMAIN
        else:
            return None

    def validateRequest(self, origin, domain):
        return origin == 'https://' + self.subdomain + '.' + domain
    
    def sendCorsResponse(self, response, origin):
        responseMsg = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': origin},
            'body': json.dumps(response, cls=DecimalEncoder)
        }
        print(responseMsg)
        return responseMsg
    