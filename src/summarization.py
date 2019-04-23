#!/usr/bin/env python
"""Summarization is an object that holds a map of the result of a summarization"""


class Summarization:
    """Summarization is an object that holds a map of the result of a summarization"""

    def __init__(self, summarization_map):
        if summarization_map is None:
            raise Exception("summarization_map is not properly initialized")
        self.summarization_map = summarization_map

    def get_summarized_text(self):
        """Gets the keyword array if it exists within the summarization map"""
        if 'sm_api_content' in self.summarization_map.keys():
            return self.summarization_map['sm_api_content']
        return None

    def get_title(self):
        """Gets the keyword array if it exists within the summarization map"""
        if 'sm_api_title' in self.summarization_map.keys():
            return self.summarization_map['sm_api_title']
        return None

    def get_api_requests_remaining(self):
        """Gets the keyword array if it exists within the summarization map"""

        # 'sm_api_limitation': 'Waited 0 extra seconds due to API Free mode, 94
        # requests left to make for today.'
        if 'sm_api_limitation' in self.summarization_map.keys():
            split_string = self.summarization_map['sm_api_limitation'].split(',')
            split_string = split_string[1].split(' ')
            return split_string[1]
        return None

    def get_percentage_reduced(self):
        """Gets the percentage reduced if it exists within the summarization map"""
        if 'sm_api_content_reduced' in self.summarization_map.keys():
            return self.summarization_map['sm_api_content_reduced']
        return None

    def get_api_message(self):
        """Gets the api message if it exists within the summarization map"""
        if 'sm_api_message' in self.summarization_map.keys():
            return self.summarization_map['sm_api_message']
        return None

    def get_summarized_character_count(self):
        """Gets the summarized character count if it exists within the summarization map"""
        return self.summarization_map['sm_api_character_count']

    def get_error_code(self):
        """Gets the error code if it exists within the summarization map"""
        if 'sm_api_error' in self.summarization_map.keys():
            return self.summarization_map['sm_api_error']
        return None

    def get_keyword_array(self):
        """Gets the keyword array if it exists within the summarization map"""
        if 'sm_api_keyword_array' in self.summarization_map.keys():
            return self.summarization_map['sm_api_keyword_array']
        return None
