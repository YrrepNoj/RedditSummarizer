#!/usr/bin/env python
"""Simple wrapper around the SMMRY_API. This allows us to get a Summarization from an article
given its URL """

import requests
from summarization import Summarization
from account_info import smmryApiKey

API_KEY = smmryApiKey
ENDPOINT = "http://api.smmry.com/"


def build_url(api_key, artical_url=None):
    """returns the endpoint to summarize a given article with the SMMRY_API"""
    post_url = ENDPOINT + "&SM_LENGTH=10&SM_API_KEY="
    post_url += api_key

    if artical_url:
        post_url += "&SM_WITH_BREAK&SM_URL="
        post_url += artical_url

    return post_url


def summerize_url(artical_url):
    """Returns the Summarization of an article via the SMMRY_API"""
    endpoint_url = build_url(API_KEY, artical_url)
    response = requests.post(endpoint_url)
    response.close()
    smmry_dict = response.json()

    if smmry_dict.get('sm_api_error'):
        return Summarization(smmry_dict)

    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].replace('[BREAK] ', '\n* ')
    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].replace('[BREAK]', '')
    smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

    return Summarization(smmry_dict)
