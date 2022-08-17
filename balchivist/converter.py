import json
import logging
import os
import requests
import requests_cache


class Converter:
    DBNAME_SUFFIXES: list = [
        'wiki', 'wiktionary', 'wikibooks', 'wikinews', 'wikiquote',
        'wikisource', 'wikiversity', 'wikivoyage'
    ]
    DEFAULT_FALLBACK_LANGUAGE = 'en'
    LOCALES_DIRECTORY = 'locales'
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        requests_cache.install_cache('converter_cache')

    def getNameFromDB(self, dbname: str, code: str) -> str:
        """
        This function converts Wikimedia-specific database names into
        human-readable names in the specified language.
        :param code: Language code to display the name in
        :param dbname: Wikimedia-specific database name to convert
        :return: Human-readable name in the specified language
        """
        specials = self.__getSpecials()

        if dbname in specials:
            return self.__getSpecialNameAfterFallback(code, dbname)

        project = ''
        langcode = ''

        for i in range(len(self.DBNAME_SUFFIXES)):
            if dbname.endswith(self.DBNAME_SUFFIXES[i]):
                project = self.DBNAME_SUFFIXES[i]
                langcode = dbname[:(dbname.index(project))]
                break

        if project == '' or langcode == '':
            self.LOGGER.error('Invalid dbname provided: %s', dbname)
            return dbname

        return self.__getNameAfterFallback(code, langcode, project)

    def __getNameAfterFallback(self, code, language_code, project) -> str:
        if project == 'wiki':
            project = 'wikipedia'

        langcodes = self.__getFallbackLanguageCodes(code)
        message_key = 'backend-converter-project-' + project

        for langcode in langcodes:
            json_file = self.LOCALES_DIRECTORY + '/' + langcode + '.json'
            if not os.path.exists(json_file):
                continue

            with open(json_file) as language_json_file:
                language_json = json.load(language_json_file)
                if message_key not in language_json:
                    continue

                return language_json[message_key] \
                    .replace('{0}', self.__getLocalLanguageName(langcode,
                                                                language_code))

    def __getSpecialNameAfterFallback(self, code, dbname) -> str:
        langcodes = self.__getFallbackLanguageCodes(code)
        message_key = 'backend-converter-dbname-' + dbname

        for langcode in langcodes:
            json_file = self.LOCALES_DIRECTORY + '/' + langcode + '.json'
            if not os.path.exists(json_file):
                continue

            with open(json_file) as language_json_file:
                language_json = json.load(language_json_file)
                if message_key not in language_json:
                    continue

                return language_json[message_key]

    def __getLocalLanguageName(self, to_language, translate_code) -> str:
        url = 'https://meta.wikimedia.org/w/api.php?action=sitematrix&format' \
              '=json&smtype=language&smstate=all&smlangprop=code%7Clocalname' \
              '&formatversion=2&uselang=' + to_language
        res = requests.get(url)

        lang_mapper = {x['code']: x['localname'] for x in
                       res.json()['sitematrix'].values() if type(x) != int}

        if translate_code not in lang_mapper:
            self.LOGGER.error('Provided translate_code not found: %s',
                              translate_code)
            return translate_code

        return lang_mapper[translate_code]

    def __getFallbackLanguageCodes(self, code) -> list:
        with open('data/languageFallback.json') as fallback_json:
            fallback = json.load(fallback_json)
            output = [code]
            queue = [code]

            while len(queue) > 0:
                langcode = queue.pop(0)

                if langcode not in fallback:
                    continue

                output += fallback[langcode]
                queue += fallback[langcode]

            output.append(self.DEFAULT_FALLBACK_LANGUAGE)
            return output

    def __getSpecials(self) -> list:
        url = "https://meta.wikimedia.org/w/api.php?action=sitematrix&format" \
              "=json&smtype=special&smstate=all&formatversion=2"
        res = requests.get(url)

        return list(
            map(lambda x: x['dbname'], res.json()['sitematrix']['specials']))
