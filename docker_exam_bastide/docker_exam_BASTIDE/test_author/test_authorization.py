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
}

for username, password in user_credentials.items():
    for version in [1,2]:

        # requête
        r = requests.get(
            url=f"http://{api_address}:{api_port}/v{version}/sentiment",
            params= {
                'username': username,
                'password': password,
                'sentence': 'hello%20world'
            }
        )

        output = '''
        ============================
            Authorization test
        ============================

        request done at "/v{version_}/sentiment"
        | username={username_}
        | password={password_}

        Expected result = 200; 
        actual restult = {status_code}

        ==>  {test_status}
        ==>  {output}

        '''

        status_code = r.status_code
        output_text = r.text

        # affichage des résultats
        if status_code == 200:
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'
        output_formatted = output.format(version_=version, username_=username, password_=password, status_code=status_code, test_status=test_status, output=output_text)
        print(output_formatted)

        # impression dans un fichier
        if os.environ.get('LOG') == "1":
            with open('/home/test/logs/api_test.log', 'a') as file:
                file.write(output_formatted)