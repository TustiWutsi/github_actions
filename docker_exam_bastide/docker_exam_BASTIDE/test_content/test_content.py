import os
import requests
import json

# définition de l'adresse de l'API
api_address = 'fastapi-api'
# port de l'API
api_port = 8000

# sentences to test
sentences = ['life is beautiful', 'that sucks']

for i,sentence in enumerate(sentences):
    for version in [1,2]:

        # requête
        r = requests.get(
            url=f"http://{api_address}:{api_port}/v{version}/sentiment",
            params= {
                'username': 'alice',
                'password': 'wonderland',
                'sentence': sentence
            }
        )

        output = '''
        ============================
            Content test
        ============================

        request done at "/v{version_}/sentiment"
        | username='alice'
        | password='wonderland'
        | sentence={sentence_}

        Expected result : {expected_result}; 
        actual restult = {actual_result}

        ==>  {test_status}

        '''

        status_code = r.status_code
        output_dict = json.loads(r.text)
        output_score = output_dict['score']

        # affichage des résultats
        if i == 0:
            expected_result = 'positive score'
            if output_score > 0:
                test_status = 'SUCCESS'
            else:
                test_status = 'FAILURE'
        elif i == 1:
            expected_result = 'negative score'
            if output_score > 0:
                test_status = 'FAILURE'
            else:
                test_status = 'SUCCESS'
        output_formatted = output.format(version_=version, sentence_=sentence, expected_result=expected_result, actual_result=output_score, test_status=test_status)
        print(output_formatted)

        # impression dans un fichier
        if os.environ.get('LOG') == "1":
            with open('/home/test/logs/api_test.log', 'a') as file:
                file.write(output_formatted)