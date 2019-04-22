class Summarization:

    def __init__(self, summarizationMap):
        if summarizationMap is None:
            #TODO throw an exception
            return
        self.summarizationMap = summarizationMap

    def getSummarizedText(self):
        if 'sm_api_content' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_content']

    def getTitle(self):
        if 'sm_api_title' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_title']

    def getAPIRequestsRemaining(self):
        # 'sm_api_limitation': 'Waited 0 extra seconds due to API Free mode, 94 requests left to make for today.'
        if 'sm_api_limitation' in self.summarizationMap.keys():
            splitString = self.summarizationMap['sm_api_limitation'].split(',')
            splitString = splitString[1].split(' ')
            return splitString[1]

    def getPercentageReduced(self):
        if 'sm_api_content_reduced' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_content_reduced']

    def getAPIMessage(self):
        if 'sm_api_message' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_message']

    def getSummarizedCharacterCount(self):
        return self.summarizationMap['sm_api_character_count']

    def getErrorCode(self):
        if 'sm_api_error' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_error']

    def getKeywordArray(self):
        if 'sm_api_keyword_array' in self.summarizationMap.keys():
            return self.summarizationMap['sm_api_keyword_array']
