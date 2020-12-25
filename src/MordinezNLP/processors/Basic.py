class BasicProcessor:
    def __init__(self, language: str = 'en'):
        self.months = BasicProcessor._load_language_months(language)
        self.months_regex = "|".join(["({month})".format(month=month) for month in self.months])

    @staticmethod
    def _load_language_months(language: str):
        if language == 'en':
            return [
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'October', 'September',
                'August', 'November', 'December'
            ]
        elif language == 'de':
            return [
                'Januar', 'Februar', 'März',
                'April', 'Mai', 'Juni',
                'Juli', 'August', 'September',
                'Oktober', 'November', 'Dezember'
            ]
        else:
            raise Exception('Cant\'t load language specified data')


if __name__ == '__main__':
    bp = BasicProcessor()
