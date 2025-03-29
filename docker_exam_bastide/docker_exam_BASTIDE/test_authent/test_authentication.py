import os
import requests

# définition de l'adresse de l'API
api_address = 'fastapi-api'
# port de l'API
api_port = 8000

# credentials to test
user_credentials = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

for username, password in user_credentials.items():

    # requête
    r = requests.get(
        url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
        params= {
            'username': '{username_}'.format(username_=username),
            'password': '{password_}'.format(password_=password)
        }
    )

    output = '''
    ============================
        Authentication test
    ============================

    request done at "/permissions"
    | username={username_}
    | password={password_}

    Expected result = 200; 
    actual restult = {status_code}

    ==>  {test_status}

    '''


    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    output_formatted = output.format(username_=username, password_=password, status_code=status_code, test_status=test_status)
    print(output_formatted)

    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('/home/test/logs/api_test.log', 'a') as file:
            file.write(output_formatted)