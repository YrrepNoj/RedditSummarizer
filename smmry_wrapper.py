import requests
import os

apiKey = os.environ['SMMRY_API_KEY']
endpoint = "http://api.smmry.com/"

def buildURL(apiKey, articalURL):
    postURL = endpoint+"&SM_LENGTH=10&SM_API_KEY="
    postURL += apiKey

    if articalURL:
        postURL += "&SM_WITH_BREAK&SM_URL="
        postURL += articalURL

    return postURL


def summerizeURL(articalURL):
    endpointURL = buildURL(apiKey, articalURL)
    response = requests.post(endpointURL)
    response.close()
    smmry_dict = response.json()

    if smmry_dict.get('sm_api_error'):
        print('Received api error: ' + smmry_dict.get('sm_api_error'))
        return

    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].replace('[BREAK]', '\n')
    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

    return smmry_dict


def summarizeText(text):
    endpointURL = buildURL(apiKey)
    text = text.encode("utf-8")

    response = requests.post(endpointURL, dict(sm_api_input=text))
    response.close()
    smmry_dict = response.json()

    if smmry_dict.get('sm_api_error'):
        print('Received api error: ' + smmry_dict.get('sm_api_error'))
        return

    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].replace('[BREAK]', '\n')
    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

    return smmry_dict

