from datetime import date

class Reviews:
    def __init__(self):
        self.rate = 0
        self.context = ''
        self.good_num = 0
class Referenced:
    def __init__(self):
        self.from_url = ''
        self.evaluation_date = None
class ScrapingData:
    def __init__(self):
        self.url = 'https://'
        self.normalized_url = 'https://'
        self.date = 0
        self.title = ''
        self.description = ''
        self.html = None
        self.html_context = ''
        self.amazon_rating = 0
        self.reviews = []
        self.craw_revision = 0
        self.evaluated = []
        self.count = 0
