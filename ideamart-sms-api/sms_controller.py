from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import json
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):

    def get(self):
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Accept'] = 'application/json'
        self.response.out.write('Hello, Telco App Runs on this Space')

    def post(self):

        logging.info(self.request.body)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Accept'] = 'application/json'
           
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        requestMessage = decoded_json["message"]
        
        logging.info("???????????")
        logging.info(requestMessage)
        logging.info("$$$$$$$$$$$")
        
#        self.response.headers['Content-Type'] = "text/plain"
#        self.response.out.write(self.request.body)
    
        url='http://localhost:7000/sms/send'
        
        replyMessage = "Hello : ", requestMessage;
        destinationAddrs = ["tel:94771122336"];
        appPasswordCode = "password";
        applicationId = "APP_000001";
        
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
            logging.info(result.content)

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":

    main()
