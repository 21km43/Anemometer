
import requests
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout


class ServerComm():
    def __init__(
            self,
            su='http://localhost:8000/',
            pd='data/create/',
            gd='data/list/',            
            ):
        self.Server_Url=su
        self.Post_Dir=pd
        self.Get_Dir=gd

    def post_data(self,body):
        try:
            response = requests.post(
                self.Server_Url+self.Post_Dir,
                body
            )
            response.raise_for_status()
            return response.text
        except ConnectionError as ce:
            return "Connection Error:"+str(ce)
        except HTTPError as he:
            return "HTTP Error:"+str(he)
        except Timeout as te:
            return "Timeout Error:"+str(te)
        except RequestException as re:
            return "Error:"+str(re)
    


    def get_data(self,query_set=''):
        try:
            response = requests.get(self.Server_Url+self.Get_Dir+query_set)
            return response.text
        except ConnectionError as ce:
            return "Connection Error:"+str(ce)
        except HTTPError as he:
            return "HTTP Error:"+str(he)
        except Timeout as te:
            return "Timeout Error:"+str(te)
        except RequestException as re:
            return "Error:"+str(re)