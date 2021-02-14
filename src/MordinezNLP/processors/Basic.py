import re
from typing import List, Callable, Union

from cleantext import clean


class BasicProcessor:
    """
    The aim of the class is to make use of NLP-dirty texts
    """

    def __init__(self, language: str = 'en'):
        """
        Initializer of all of regexes, to make processing function as fast as possible

        Args:
            language (str): a language shortcut in which we want to clean the input text
        """

        # ==== BASE PROCESSING RULES SECTION ====
        # remove everything what is in a html tags
        self.base_brackets_regex = re.compile(r"<([^\s]*)>")
        # replace sequence of digit more/more or equal than digit to <digit> <more> <digit>
        self.more_than_regex = re.compile(r"\d+\s*(>|>=)\s*\d+")
        # replace sequence of digit less/less or equal than digit to <digit> <less> <digit>
        self.less_than_regex = re.compile(r"\d+\s*(<|<=)\s*\d+")

        # process lists
        #                                           /---- Positive and Negative Lookbehind
        self.list_last_item_regex = re.compile(r"(?<=\n)(-|>)\s*([^,\n]*)\n([^-^>]|$)")
        #                                       /---- Positive and Negative Lookbehind
        self.list_item_regex = re.compile(r"(?<=\n)(-|>)\s*([^,\n]*),*\n")

        # fix a>>>>> <<<<another>>  ->   a another
        self.fix_base_brackets_1 = re.compile(r"(\s+(<|>)+\s+)|(\s+>+)+|(<+\s+)+|(\s+(<|>){2,}\s+)")
        # fix other> -> other
        self.fix_base_brackets_2_left = re.compile(r"(\s+([a-zA-Z0-9äöüÄÖÜßùàûâüæÿçéèêëïîôœ,.()!?\-:']+)(>+)\s+)")
        # fix <and -> and
        self.fix_base_brackets_2_right = re.compile(r"(\s+(<+)([a-zA-Z0-9äöüÄÖÜßùàûâüæÿçéèêëïîôœ,.()!?\-:']+)\s+)")

        # fix la<te don>'t  ->  late don't
        self.fix_brackets_in_words = re.compile(r"\s+(([^\s^<^>])+)(<|>)+(([^\s^<^>])+)\s+")

        # limit to a specified set of characters
        self.limit_regex = re.compile(r"(([^a-zA-Z0-9,\.<> !?äöüÄÖÜßùàûâüæÿçéèêëïîôœ@\-:()\[\]'])|([^\s]{30,}))",
                                      re.IGNORECASE)

        # replace more than 2 spaces to a single one
        self.space_regex = re.compile(r"(\s{2,})")
        # split each word which has two uppercase letters ReCure -> Re Cure
        self.double_upper_case_letters = re.compile(r"([A-Z][^\s^A-Z^\-^.^,^?^!]+)([A-Z][^\s^A-Z^\-^.^,^?^!]+)")
        # escape eveything what is in brackets
        self.none_regex = re.compile(r"(\s*(((\()([^\)]+)(\)))|((\[)([^\]]+)(\])))\s*)", re.IGNORECASE)

        # place space before and after all digits
        self.no_space_digits_regex = re.compile(r"(\d+)(th|st|nd|rd)*")

        # match texts " ." and replace it to "."
        self.dot_regex = re.compile(r"\s+\.")
        # match texts " ," and replace it to ","
        self.com_regex = re.compile(r"\s+,")
        # replace all custom tags where one exists after one to a single one, from <date> <date>    <date> -> <date>
        self.multi_tag_regex = re.compile(
            r"(((<date>[\s,]*){2,})|((<unk>[\s,]*){2,})|((<number>[\s,]*){2,})|((<url>[\s,]*){2,})|((<email>[\s,]*){2,})|((<less>[\s,]*){2,})|((<more>[\s,]*){2,})|((<bracket>[\s,]*){2,}))",
            re.IGNORECASE)
        # replace special token occurences one by one with colons
        self.multi_tag_colon_regex = re.compile(
            r"(((<date>[:]*){2,})|((<unk>[:]*){2,})|((<number>[:]*){2,})|((<url>[:]*){2,})|((<email>[:]*){2,})|((<less>[:]*){2,})|((<more>[:]*){2,})|((<bracket>[:]*){2,}))", re.IGNORECASE)

        # remove starting space
        self.starting_space_regex = re.compile(r"^(\s)+", re.IGNORECASE)
        # remove ending space
        self.ending_space_regex = re.compile(r"(\s)+$", re.IGNORECASE)

        # match emails
        self.email_regex = re.compile(
            r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*")
        # match urls and emails that where not matched by a *self.email_regex*
        self.url_email_regex = re.compile(
            r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)")
        # fix cleantext url removing dot "." at the end of string
        self.url_fix_regex = re.compile("(<url>)\s+([A-Z])")

        # remove quote marks
        self.quote_regex = re.compile(r'["\'‘’]([^ts])', re.IGNORECASE)

        # regexes used by *process_multiple_characters* function #
        self.multiple_characters_regex = re.compile(r"(.)\1{3,}")
        self.multiple_characters_non_sense = re.compile(
            r"(<number>|<date>|<unknown>|<url>|<email>|<more>|<less>)|[,\.<>!?]", re.IGNORECASE)

        # final regex which removes double dots and newline (from HTML_Parser)
        self.double_dots = re.compile(r"\.\.\n")

        # remove hyphenated
        self.hyphenated_regex = re.compile(r"\s+([^\-<>\s]+)-([^\-<>\s]+)\s+")

        # ==== DATES SECTION ====
        # common dates - a common dates formats used in multiple languages
        self.common_dates = re.compile(r"(\s+\d{1,4}\s*([-./])\s*\d{1,4}([-./])\s*\d{2,4})", re.IGNORECASE)
        self.common_dates_combined = re.compile(
            r"((" + "|".join(BasicProcessor.load_language_days(language)) + ")*\s*((" + "|".join(
                BasicProcessor._load_date_ordinals(
                    language)) + ")|(0*([1-9]{1,2})(st|nd|rd|th)*))\s+(of\s+)*(" + "|".join(
                BasicProcessor.load_language_months(language)) + "))\s*\d{0,4}s*", re.IGNORECASE)

        # en dates
        self.en_dates = re.compile(r"(((early|late)\s*\d{2,4}s*)|(in\s+\d{2,4}s*)|(\d{2,4}s))", re.IGNORECASE)

        # aggregate language specific dates processing into a list
        self.dates = []

        # build language specified processing functions for dates
        if language == 'en':
            self.dates = [
                lambda x, y: re.sub(self.common_dates, " " + y + " ", x),
                lambda x, y: re.sub(self.common_dates_combined, " " + y + " ", x),
                lambda x, y: re.sub(self.en_dates, " " + y + " ", x)
            ]
        else:
            raise Exception('Cant\'t load language specified data')

        # remeber last used tokens
        # needed for tokenizer such as SentencePiece
        self.used_special_tokens: List[str] = []

    def _run_dates(self, text: str, date_token: str) -> str:
        """
        Iterate over language specific lambdas

        Args:
            text (str): text to process
            date_token (str): a date token to replace

        Returns:
            str: a post-processed text with *data* tokens replaced
        """
        for date_lambda in self.dates:
            text = date_lambda(text, date_token)
        return text

    @staticmethod
    def load_language_days(language: str) -> List[str]:
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
    def load_language_months(language: str) -> List[str]:
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
    def _load_date_ordinals(language: str) -> List[str]:
        """
        Load ordinals for dates and prepare it for multi use cases

        Args:
            language (str): an ordinals language

        Returns:
            List[str]: a list of regex ready date ordinals
        """
        if language == 'en':
            to_return = []
            for ordinal in BasicProcessor.load_ordinals(language)[:31]:
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

    @staticmethod
    def load_ordinals(language: str) -> List[str]:
        """
        Build a language specific ordinals.
        Currently supported ordinals from 1 to 99

        Args:
            language (str): a language in which function will return ordinals

        Returns:
            List[str]: a list of ordinals in specified language
        """
        if language == 'en':
            base_numerals = BasicProcessor.load_numerals(language)
            ordinals_base = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'nineth']
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
    def load_numerals(language: str) -> List[str]:
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
    def _basic_clean(
            text_to_clean: str,
            language: str = 'en',
            fix_unicode: bool = True,
            lower: bool = False,
            no_line_breaks: bool = False,
            no_urls: bool = False,
            no_emails: bool = True,
            no_phone_numbers: bool = True,
            no_numbers: bool = True,
            no_digits: bool = False,
            no_currency_symbols: bool = True,
            no_punct: bool = False,
            replace_with_url: str = "<url>",
            replace_with_email: str = "<email>",
            replace_with_phone_number: str = "<phone>",
            replace_with_number: str = "<number>",
            replace_with_digit: str = "0",
            replace_with_currency_symbol: str = "<currency>",
    ) -> str:
        """
        A cleantext wrapper designed for MordinezNLP

        Args:
            text_to_clean (str): a text input to process
            language (str): a language in which process the input data
            fix_unicode (bool): replace all non unicode characters to unicode
            lower (bool): lowercase all characters
            no_line_breaks (bool): fully strip line breaks as opposed to only normalizing them
            no_urls (bool): replace all URLs with a special token
            no_emails (bool): replace all email addresses with a special token
            no_phone_numbers (bool): replace all phone numbers with a special token
            no_numbers (bool): replace all numbers with a special token
            no_digits (bool): replace all digits with a special token
            no_currency_symbols (bool): replace all currency symbols with a special token
            no_punct (bool): remove punctuations
            replace_with_url (str): a special token used to replace urls
            replace_with_email (str): a special token used to replace emails
            replace_with_phone_number (str): a special token used to replace phone numbers
            replace_with_number (str): a special token used to replace numbers
            replace_with_digit (str): a special token used to replace digits
            replace_with_currency_symbol (str): a special token used to replace currency symbol

        Returns:
            str: post-processed text
        """
        return clean(
            text_to_clean,
            fix_unicode=fix_unicode,
            to_ascii=False,
            lower=lower,
            no_line_breaks=no_line_breaks,
            no_urls=no_urls,
            no_emails=no_emails,
            no_phone_numbers=no_phone_numbers,
            no_numbers=no_numbers,
            no_digits=no_digits,
            no_currency_symbols=no_currency_symbols,
            no_punct=no_punct,
            replace_with_punct="",
            replace_with_url=replace_with_url,
            replace_with_email=replace_with_email,
            replace_with_phone_number=replace_with_phone_number,
            replace_with_number=replace_with_number,
            replace_with_digit=replace_with_digit,
            replace_with_currency_symbol=replace_with_currency_symbol,
            lang=language
        )

    def process(
            self,
            text_to_process: Union[str, List[str]],
            pre_rules: List[Callable] = [],
            post_rules: List[Callable] = [],
            language: str = 'en',
            fix_unicode: bool = True,
            lower: bool = False,
            no_line_breaks: bool = False,
            no_urls: bool = True,
            no_emails: bool = True,
            no_phone_numbers: bool = True,
            no_numbers: bool = True,
            no_digits: bool = False,
            no_currency_symbols: bool = True,
            no_punct: bool = False,
            no_math: bool = True,
            no_dates: bool = True,
            no_multiple_chars: bool = True,
            no_lists: bool = True,
            no_brackets: bool = True,
            replace_with_url: str = "<url>",
            replace_with_email: str = "<email>",
            replace_with_phone_number: str = "<phone>",
            replace_with_number: str = "<number>",
            replace_with_digit: str = "0",
            replace_with_currency_symbol: str = "<currency>",
            replace_with_date: str = "<date>",
            replace_with_bracket: str = "<bracket>",
            replace_more: str = "<more>",
            replace_less: str = "<less>"
    ) -> Union[str, List[str]]:
        """
        Main text processing function. It mainly uses regexes to find specified patterns in texts and replace them by
        a defined custom token or fixes parts that are not valuable for humans and machines.

        Function also enables users to set *pre_rules* and *post_rules*. You can use those lists of Callables to add
        pre and post processing rules. A good use case is processing CommonCrawl reddit data, where each page has
        the same schema (headers, navigation bars etc.). In such case You can use *pre_rules* to filter them and then
        pass such text into the *process* function pipeline. Also feel free to add *post_rules* to match other cases
        which are not used here.

        Depending on parameters function can replace a specified type of data.

        Currently supported entities:
         - dates,
         - brackets,
         - simple math strings,
         - phone numbers,
         - emails,
         - urls,
         - numbers and digits
         - multiple characters in single words

        **Dates**

        Examples of dates matching in strings for english:
         - 1.02.2030
         - 1st of December   3990
         - first of DecEmber 1233
         - first december 2020
         - early 20s
         - 01.03.4223
         - 11-33-3222
         - 2020s
         - Friday 23 October
         - late 90s
         - in 20s

        **Brackets**

        Examples of brackets matching in strings for english:
         - [tryrty]
         - (other text)

        **Simple math strings**

        Examples of simple math strings for english:
         - 2 > 3
         - 4<6
         - 4>=4
         - 5<= 4

         If You decide to use *no_math=False* than such cases will be processed with other functions. It meas that one
         function will remove math operator (<,>,<=,>=) and another will replace numbers with special token.

        **Multiple characters in single words**

        Table below show string *before* and *after* using a *multiple characters in signle word* processing function

        ======================  ===================
        Before                  After
        ======================  ===================
        'EEEEEEEEEEEE'          ''
        'supeeeeeer'            'super'
        'EEEE<number>!'         ''
        'suppppprrrrrpper'      'suprpper'
        ======================  ===================

        Processing multiple characters is extremly usefull in processing CommonCrawl reddit data.

        **Lists replacement**

        Lists in a text with leading "-" or ">" for each item can be parsed to simple and more understandable text.
        For example list:

        ::

            Mylist:
            - item 1
            - item 2,
            -item 3

        Will be parsed to:

        ::

            Mylist: item 1, item 2, item 3.

        Use *no_lists* argument to enable this feature.

        **Supported languages**

        ===========================  =============================
        Fully supported languages    Partially supported languages
        ===========================  =============================
        English                      German
        ===========================  =============================

        **Be careful**

        Please don't replace special tokens in function, because it can wrongly process strings.
        It will be fixed in feature releases
        # todo fix regexes in __init__ for special tokens

        Args:
            text_to_process (Union[str, List[str]]): An input text or a list of texts (for multiprocess processing) to process by a function
            pre_rules (List[Callable]): A list of lambdas that are applied before main preprocessing rules
            post_rules (List[Callable]): A list of lambdas that are applied after *pre_rules* and function processing rules
            language (str): A input text language
            fix_unicode (bool): replace all non unicode characters to unicode
            lower (bool): lowercase all characters
            no_line_breaks (bool): fully strip line breaks as opposed to only normalizing them
            no_urls (bool): replace all URLs with a special token
            no_emails (bool): replace all email addresses with a special token
            no_phone_numbers (bool): replace all phone numbers with a special token
            no_numbers (bool): replace all numbers with a special token
            no_digits (bool): replace all digits with a special token
            no_currency_symbols (bool): replace all currency symbols with a special token
            no_punct (bool): remove punctuations
            no_math (bool): remove >= <= in math strings
            no_dates (bool):  remove dates strings in input text 'early 80s' -> '<date>'
            no_lists (bool): replace all texts lists
            no_brackets (bool): replace brackets: '[', ']', '(', ')'
            no_multiple_chars (bool): reduce multiple characters in string into a single ones 'supeeeeeer' -> 'super'
            replace_with_url (str): a special token used to replace urls
            replace_with_email (str): a special token used to replace emails
            replace_with_phone_number (str): a special token used to replace phone numbers
            replace_with_number (str): a special token used to replace numbers
            replace_with_digit (str): a special token used to replace digits
            replace_with_currency_symbol (str): a special token used to replace currency symbol
            replace_with_date (str): a special token used to replace dates
            replace_with_bracket (str): a special token used to replace brackets
            replace_more (str): a special token used to replace more '>' and more or equal '>=' symbols in math texts
            replace_less (str): a special token used to replace less '<' and less or equal '<=' symbols in math texts

        Returns:
            Union[str, List[str]]: Post-processed text

        """
        # add all special tokens to list of used special tokens
        self.used_special_tokens = [
            replace_with_url,
            replace_with_email,
            replace_with_phone_number,
            replace_with_number,
            replace_with_digit,
            replace_with_currency_symbol,
            replace_with_date,
            replace_with_bracket,
            replace_more,
            replace_less
        ]

        rules = [
            lambda x: re.sub(self.base_brackets_regex, r"\1 ", x),
            lambda x: re.sub(self.double_dots, ".\n", x),
        ]

        if no_lists:
            rules += [
                lambda x: re.sub(self.list_last_item_regex, r" \2. \3", x),
                # lambda x: print(x)
                lambda x: re.sub(self.list_item_regex, r"\2, ", x)
            ]

        if no_math:
            rules += [
                lambda x: re.sub(self.more_than_regex,
                                 "{replace_with_number} {replace_more} {replace_with_number}".format(
                                     replace_more=replace_more, replace_with_number=replace_with_number), x),
                lambda x: re.sub(self.less_than_regex,
                                 "{replace_with_number} {replace_less} {replace_with_number}".format(
                                     replace_less=replace_less, replace_with_number=replace_with_number), x),
            ]

        rules += [
            lambda x: re.sub(self.fix_base_brackets_1, " ", x),
            lambda x: re.sub(self.fix_base_brackets_2_left, r" \2 ", x),
            lambda x: re.sub(self.fix_base_brackets_2_right, r" \3 ", x),
            lambda x: re.sub(self.fix_brackets_in_words, r" \1\4 ", x),
            lambda x: re.sub(self.quote_regex, r"\1", x),
        ]

        if no_multiple_chars:
            rules += [
                lambda x: self.process_multiple_characters(x),
            ]

        if no_dates:
            rules += [
                lambda x: self._run_dates(x, replace_with_date),
            ]

        rules += [
            lambda x: self._basic_clean(
                text_to_clean=x,
                language=language,
                fix_unicode=fix_unicode,
                lower=lower,
                no_line_breaks=no_line_breaks,
                no_urls=no_urls,
                no_emails=no_emails,
                no_phone_numbers=no_phone_numbers,
                no_numbers=no_numbers,
                no_digits=no_digits,
                no_currency_symbols=no_currency_symbols,
                no_punct=no_punct,
                replace_with_url=replace_with_url,
                replace_with_email=replace_with_email,
                replace_with_phone_number=replace_with_phone_number,
                replace_with_number=replace_with_number,
                replace_with_digit=replace_with_digit,
                replace_with_currency_symbol=replace_with_currency_symbol
            ),
            lambda x: re.sub(self.space_regex, " ", x),
            lambda x: re.sub(self.double_upper_case_letters, r" \1 \2 ", x),
        ]

        if no_brackets:
            rules += [
                lambda x: re.sub(self.none_regex, r" {replace_with_bracket} \5 \9 {replace_with_bracket} ".format(
                    replace_with_bracket=replace_with_bracket), x),
            ]
        else:
            rules += [
                lambda x: re.sub(self.none_regex, r" \4\8 \5\9 \6\10 ", x),
            ]

        # if there will be occurences where multiple characters were not reoved, uncomment this section
        # in such case there will be doubled removal of a multiplied characters
        #
        # if no_multiple_chars:
        #     rules += [
        #         lambda x: self.process_multiple_characters(x),
        #     ]

        if no_numbers:
            rules += [
                lambda x: re.sub(self.no_space_digits_regex,
                                 " {replace_with_number} ".format(replace_with_number=replace_with_number), x),
            ]

        rules += [
            lambda x: re.sub(self.limit_regex, " ", x),
            lambda x: re.sub(self.dot_regex, ".", x),
            lambda x: re.sub(self.com_regex, ",", x),
            lambda x: re.sub(self.multi_tag_regex, r"\3\5\7\9\11\13\15", x),
            lambda x: re.sub(self.starting_space_regex, "", x),
            lambda x: re.sub(self.ending_space_regex, "", x),
        ]

        if no_urls or no_emails:
            rules += [
                lambda x: re.sub(self.url_email_regex,
                                 r" {replace_with_url} ".format(replace_with_url=replace_with_url), x),
            ]

        rules += [
            lambda x: x.replace(" > ", " "),
            lambda x: x.replace(" < ", " "),
            lambda x: re.sub(self.space_regex, " ", x),
            lambda x: re.sub(self.multi_tag_regex, r"\3\5\7\9\11\13\15", x),
            lambda x: re.sub(self.url_fix_regex, r"\1. \2", x),
            lambda x: re.sub(self.hyphenated_regex, r" \1\2 ", x),
            lambda x: re.sub(self.multi_tag_colon_regex, r"\3\5\7\9\11\13\15 : \3\5\7\9\11\13\15", x)
        ]

        rules = pre_rules + rules + post_rules

        if type(text_to_process) is str:
            for i, rule in enumerate(rules):
                text_to_process = rule(text_to_process)
                # print(i, "\n", text_to_process)
                # print("==========================================================\n\n\n\n")
            return text_to_process
        else:
            processed_texts = []
            for text in text_to_process:
                for i, rule in enumerate(rules):
                    text = rule(text)
                    # print(text, "\n\n")
                processed_texts.append(text)
                # if text_num % 1000 == 0:
                # print(text_num)
            return processed_texts

    def process_multiple_characters(self, text_to_process: str) -> str:
        """
        Function can detect multiplied characters in a word and replace them by a single one.

        ==================  ===========
        Before              After
        ==================  ===========
        'EEEEEEEEEEEE!'     ''
        'supeeeeeer'        'super'
        'EEEE<number>!'     ''
        'suppppprrrrrpper'  'suprpper'
        ==================  ===========

        Args:
            text_to_process (str): An input text to process

        Returns:
            str: Text with removed duplicated characters in each word
        """

        for entity in re.findall(self.multiple_characters_regex, text_to_process):
            match = ""
            if match not in ['.']:
                # secure entity if it is a regex character
                entity = '\\'+entity
                for match in re.findall("(([^" + entity + "^\s.]*)([" + entity + "]{3,})([^" + entity + "^\s.]*))",
                                        text_to_process):
                    text_replaced = re.sub(self.multiple_characters_non_sense, "", match[0])

                    if text_replaced == match[2]:
                        text_to_process = text_to_process.replace(match[0], "")
                    else:
                        text_to_process = text_to_process.replace(match[1] + match[2] + match[3],
                                                                  match[1] + entity + match[3])

        return text_to_process

    def get_special_tokens(self) -> List[str]:
        """
        Function can return all of the special tokens used by *process* function. It can be needed when
        training SentencePiece tokenizer.

        Returns:
             List[str]: all of the special tokens used in *process* function
        """
        if len(self.used_special_tokens) == 0:
            raise Exception('You can\'t retrieve list of special tokens without using "process" function before.')
        else:
            return self.used_special_tokens


if __name__ == '__main__':
    import os
    from helper import BASE_DIR

    bp = BasicProcessor()

    with open(os.path.join(BASE_DIR, "benchmarks", "ds", "ds_bpe_roberta_base_train_mordineznlp_sm2.txt"), encoding="utf8") as f:
        # f_content = f.read()
        # post_process = bp.process(f_content, language='en', no_brackets=False)
        # print(post_process)

        post_process = bp.process(f.readlines(), language='en', no_brackets=False)