###################################
## @author:  harshadura, dewmal
## @contact: harshadura@gmail.com
## @license: GNU GPL v2
###################################

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import logging
import json
from random import randrange
from time import gmtime, strftime

class MainPage(webapp.RequestHandler):

    def get(self):
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Accept'] = 'application/json'
        self.response.out.write('Hello, Telco App Runs on this Space')

    def post(self):

        nowTime = strftime("%a, %d %b %Y %X +0000", gmtime())
        logging.info('\n\n\n>>>> SMS received on : ' + nowTime + ' <<<<')
        
        logging.info("\n\n**** HTTP Request:\n" + self.request.body + "****\n\n")
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Accept'] = 'application/json'
           
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        
        requestMessage = decoded_json["message"]
        requestTP = decoded_json["sourceAddress"]
        
        logging.info("*** Message: " + requestMessage + " | TP: " + requestTP + " ***")
        
        msgParts = requestMessage.split(' ')
        boy = msgParts[1]
        girl = msgParts[2]
        
        randomPercentage = randrange(30, 99)

        url='http://localhost:7000/sms/send'
        destinationAddrs = [requestTP];
        appPasswordCode = "password";
        applicationId = "APP_000001";
        
        replyMessage = 'Hello ' + boy + ' & ' + girl + ' You two got ' + str(randomPercentage) + '% of Love! Cheers!';
        
        res = { 'message': replyMessage,
                "destinationAddresses": destinationAddrs,
                "password": appPasswordCode,
                "applicationId": applicationId
        }

        logging.info(res)
        form_data = json.dumps(res)
        logging.info(form_data)
        result = urlfetch.fetch(url=url,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'application/json','Accept':'application/json'})

        logging.info(result.content)

        if result.status_code == 200:
            logging.info('*** Message delivered Successfully! ****')
        else:
            logging.info('*** Message was not delivered Successfully!! ERROR-CODE: ' + result.status_code + ' ****')

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
