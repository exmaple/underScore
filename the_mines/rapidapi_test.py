'''
rapidapi requires credit card data even for free acount.
free account gives you 50 free api calls per month and $0.25 for each call after that.
NO THANKS!

'''
import requests

url = "https://heisenbug-bundesliga-live-scores-v1.p.rapidapi.com/api/bundesliga"

querystring = {"matchday":"1"}

headers = {
    'x-rapidapi-host': "heisenbug-bundesliga-live-scores-v1.p.rapidapi.com",
    'x-rapidapi-key': "f62b37deecmsh70ff9936f552727p12e33fjsna71d32d2130d"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
