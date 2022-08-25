# Created by mborzymowski at 24.08.2022
import re
from typing import List


class DateTagger:
    def __init__(self, language: str = 'en'):
        self.language = language
        assert language in ['en'], 'Language not supported'

        # replace more than 2 spaces to a single one
        self.space_regex = re.compile(r"(\s{2,})")

        # place space before and after all digits
        self.no_space_digits_regex = re.compile(r"(\d+)(th|st|nd|rd)*")

        # ==== DATES SECTION ====
        # common dates - a common dates formats used in multiple languages
        self.common_dates = re.compile(r"(^|(?<=[^\d]))((\d{1,2}[./\-]\d{1,2}[./\-](17|18|19|20|21|22)\d{2})|((17|18|19|20|21|22)\d{2}[./\-]\d{1,2}[./\-]\d{1,2})|(\d{1,2}[./\-]\d{1,2}[./\-]\d{2})|(\d{2}[./\-]\d{1,2}[./\-]\d{1,2}))($|(?=[^\d]))", re.IGNORECASE)

        # en dates
        self.en_dates = re.compile(r"(((early|late)\s*\d{2,4}s*)|(in\s+\d{2}s))", re.IGNORECASE)
        self.en_dates_combined = re.compile(
            r"((" + "|".join(DataTagger.get_language_day_names(language)) + ")*\s*((" + "|".join(
                DataTagger.get_date_ordinals(
                    language)) + ")|(0*([1-9]{1,2})(st|nd|rd|th)*))\s+(of\s+)*(" + "|".join(
                DataTagger.get_language_month_names(language) + [month[:3] for month in DataTagger.get_language_month_names(
                    language)]) + "))\s*(in\s+)*\d{0,4}s*", re.IGNORECASE)
        # print(self.en_dates_combined.pattern)
        self.en_dates_combined2 = re.compile(
            r"(February)(\s+\d{1,2}),*\s+\d{2,4}", re.IGNORECASE)

        # aggregate language specific dates processing into a list
        self.dates = []

        # build language specified processing functions for dates
        if language == 'en':
            self.dates = [
                self.common_dates,
                self.en_dates_combined,
                self.en_dates,
                self.en_dates_combined2
            ]
        else:
            raise Exception('Cant\'t load language specified data')

    @staticmethod
    def get_language_day_names(language: str) -> List[str]:
        """
        Return language specific names of days of the week
        Args:
            language (str): a language in which return name of days of the week

        Returns:
            List[str]: a list of day names in specified language
        """
        if language == 'en':
            return [
                'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
            ]
        elif language == 'de':
            return [
                'montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag'
            ]
        else:
            raise Exception('Cant\'t load language specified data')

    @staticmethod
    def get_language_month_names(language: str) -> List[str]:
        """
        Function returns language specific names of months

        Args:
            language (str): language in which return names

        Returns:
            List[str]: a list of months in specified language
        """
        if language == 'en':
            return [
                'january', 'february', 'march',
                'april', 'may', 'june',
                'july', 'october', 'september',
                'august', 'november', 'december'
            ]
        elif language == 'de':
            return [
                'januar', 'februar', 'märz',
                'april', 'mai', 'juni',
                'juli', 'august', 'september',
                'oktober', 'november', 'dezember'
            ]
        else:
            raise Exception('Cant\'t load language specified data')

    @staticmethod
    def get_numerals(language: str) -> List[str]:
        """
        Build language specific numerals.
        Currently supported numerals are from 1 to 99.

        Args:
            language (str): a language in which function will return numerals

        Returns:
            List[str]: a list of numerals in specified language
        """
        if language == 'en':
            base = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
            tenths = ['ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

            numerals = base + \
                tenths[0:1] + \
                ['eleven', 'twelve', 'thirteen'] + \
                [''.join([base_num, 'teen']) for base_num in base[3:]]

            for i, tenth in enumerate(tenths[1:]):
                numerals += tenths[i + 1:i + 2]
                numerals += [' '.join([tenths[i + 1], base_num]) for base_num in base]

            return numerals
        elif language == 'de':
            # todo add german language version
            raise Exception('Cant\'t load language specified data')
        else:
            raise Exception('Cant\'t load language specified data')

    @staticmethod
    def get_ordinals(language: str) -> List[str]:
        """
        Build a language specific ordinals.
        Currently supported ordinals from 1 to 99

        Args:
            language (str): a language in which function will return ordinals

        Returns:
            List[str]: a list of ordinals in specified language
        """
        if language == 'en':
            base_numerals = DataTagger.get_numerals(language)
            ordinals_base = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
            ordinals = ordinals_base[:]

            for i, num in enumerate(base_numerals[9:19]):
                ordinals.append("".join([num, 'th']))

            for tenth_num in range(19, len(base_numerals), 10):
                ordinals.append("".join([base_numerals[tenth_num][:-1], 'ieth']))

                for num in ordinals_base:
                    ordinals.append("-".join([base_numerals[tenth_num], num]))

            return ordinals
        elif language == 'de':
            # todo add german language version
            raise Exception('Cant\'t load language specified data')
        else:
            raise Exception('Cant\'t load language specified data')

    @staticmethod
    def get_date_ordinals(language: str) -> List[str]:
        """
        Load ordinals for dates and prepare it for multi use cases

        Args:
            language (str): an ordinals language

        Returns:
            List[str]: a list of regex ready date ordinals
        """
        if language == 'en':
            to_return = []
            for ordinal in DataTagger.get_ordinals(language)[:31]:
                if ' ' in ordinal:
                    to_return.append(ordinal.replace(' ', ''))

                if '-' in ordinal:
                    to_return.append(ordinal.replace('-', ''))

                to_return.append(ordinal)
            return to_return
        elif language == 'de':
            # todo add german language version
            raise Exception('Cant\'t load language specified data')
        else:
            raise Exception('Cant\'t load language specified data')

    def tag_dates(self, text: str):
        found_entities = []
        for date_regex in self.dates:
            # print(date_regex)
            for entity in re.finditer(date_regex, text):
                # print(entity)
                found_entities.append((
                    entity.span(),
                    entity.group()
                ))

        are_in = set()
        for found_entity in found_entities:
            for found_entity2 in found_entities:
                if found_entity[0] != found_entity2[0]:
                    if found_entity[0][0] <= found_entity2[0][0] and found_entity[0][1] >= found_entity2[0][1]:
                        are_in.add(found_entity2)

        return sorted(list(set(found_entities) - are_in), key=lambda x: x[0][0])


# if __name__ == '__main__':
    #     print('main')
    # tagger = DataTagger('en')
    # print(tagger.tag_dates("22.08.2022, 31st May 2022,"))

#     sample_text = "This is my sample text containg dates. " \
#     "I was born on the 1st of January, and I am currently in the 2nd of February. " \
#     "I am also in the 3rd of March, and the 4th of April. " \
#     "I am also in the fifth of May, and the sixth of June in 1999 " \
#     "I am also in the seventh of July, and the eighth of August in 2000 " \
#     "I am also in the twelfth of December, and the thirteenth of January in 2001 " \
#     "I am also in the fourteenth of February, and the fifteenth of March in 2002 " \
#     "I am also in the thirty-first of December, and the twenty-fifth of January in 2003, " \
#     "I am also in the twenty-sixth of February, and the twenty-seventh of March in 2004, " \
#     "I am also in the twenty-eighth of April, and the twenty-ninth of May in 2005, " \
#     "In 20 minutes"
#     print(tagger.tag_dates(sample_text))

# print(tagger.common_dates)
# print(tagger.common_dates_combined)
# print(DataTagger.get_language_day_names('en'))
# print(DataTagger.get_language_month_names('en'))
# print(DataTagger.get_numerals('en'))
# print(DataTagger.get_ordinals('en'))
# print(DataTagger.get_date_ordinals('en'))
