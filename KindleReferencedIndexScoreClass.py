from datetime import datetime

class Review:
    def __init__(self):
        self.star       = 0
        self.context    = ''
        self.vote       = 0
        self.hashes     = None
class Referenced:
    def __init__(self):
        self.from_url = ''
        self.evaluation_date = None
class ScrapingData:
    def __init__(self):
        self.url            = 'https://'
        self.normalized_url = 'https://'
        self.asin           = 'B'
        self.date           = 0
        self.title          = ''
        self.description    = ''
        self.html           = None
        self.html_context   = ''
        self.amazon_rating  = 0
        self.reviews        = []
        self.reviews_datetime = datetime.fromtimestamp(0) 
        self.craw_revision  = 0
        self.evaluated      = []
        self.count          = 0
        self.asins          = []
        self.harmonic_mean  = None
        self.normal_mean    = None
        self.relevancy      = 0.
        self.review_tf      = []
        self.product_info   = ''
        self.product_info_tf = []
        self.cooccurrence   = 0.0
        self.all_tf  = []
