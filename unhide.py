import requests
import json


#Crowdstrike login API 1
cloud = 'https://api.crowdstrike.com'
id = 'CLIENTID'
secret = 'CLIENTSECRET'


def TokenAuth():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'client_id': id,
        'client_secret': secret,
    }

   
    response = requests.post(cloud+'/oauth2/token', headers=headers, data=data)
    response = response.json()
    token_auth = response['access_token']
    return(token_auth)

def MaquinaOnlineLixeira():
    params = {
        'filter': "last_seen:>='now-1h'+last_seen:<'now'"
    }
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + TokenAuth(), 
    }
    response = requests.get(cloud+"/devices/queries/devices-hidden/v1", headers=headers, params=params)
    resources = response.json().get('resources', [])
    print("Maquinas online na lixeira: "+(str(resources)))
    return resources

def RemoverDaLixeira():
    headers = {
        'authorization': 'Bearer ' + TokenAuth(),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "ids": MaquinaOnlineLixeira()
    }
    response = requests.post(cloud+"/devices/entities/devices-actions/v2?action_name=unhide_host", headers=headers, json=payload)
    return response.json()


print(RemoverDaLixeira())