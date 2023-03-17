from babel.plural import PluralRule
import glob, json, os
from datetime import datetime
from babel.dates import format_datetime
from string import Template
from babel.plural import PluralRule

supported_format = ['json']

class Translator:
    def __init__(self, translation_folder: str, file_format: str = 'json', default_locale='en') -> None:
        # initialization
        self.data = {}
        self.locale = default_locale
        self.plural_rule = PluralRule({'one': 'n is 1'})

        # check if format is supported
        if file_format in supported_format:
            # get lst of file with specific extensions
            files = glob.glob(os.path.join(translation_folder, f"*.{file_format}"))
            for f in files:
                # get the name of the file without extension, will be used as locale name
                locale = os.path.splitext(os.path.basename(f))[0]
                with open(f, 'r', encoding='utf8') as fd:
                    if file_format == 'json':
                        self.data[locale] = json.load(fd)

    def get_data(self):
        return self.data

    def set_locale(self, locale):
        if locale in self.data:
            self.locale = locale
        else:
            print(['[+]Invalid locale'])
    
    def get_locale(self):
        return self.locale
    
    def set_plural_rule(self, rule):
        try:
            self.plural_rule = PluralRule(rule)
        except Exception:
            print('[+]Invalid plural rule')
     
    def get_plural_rule(self):
        return self.plural_rule
    
    def translate(self, key, **kwargs):
        # return the key instead of translation if the locale is not supported
        if self.locale not in self.data:
            return key
        
        text = self.data[self.locale].get(key, key)

        # type dict represents key with plural form
        if type(text) == dict:
            count = kwargs.get('count', 1)
            # parse count to int
            try:
                count = int(count)
            except Exception:
                print('[+]Invalid count')
                return key
            text = text.get(self.plural_rule(count), key)
        # string interpolation
        return Template(text).safe_substitute(**kwargs)
    
def str_to_datetime(dt_str: str, format: str = '%Y-%m-%d'):
    return datetime.strptime(dt_str, format)

def datetime_to_str(dt: datetime, format: str = 'yyyy-MM-dd', locale='en'):
    return format_datetime(dt, format=format, locale=locale)