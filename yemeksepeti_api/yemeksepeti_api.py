import pytz
import requests
import re
from datetime import datetime, timedelta
from dateutil import parser
from . import yemeksepeti_config as config


def netdate2py(jsondate, tzinfo=pytz.utc):
    """
    Converts an ASP.NET json date: "/DATE(x)/" to tz-aware datetime object.
    Credit: https://stackoverflow.com/a/54495227
    """
    regex = (
        r"/Date\("
        r"(?P<milleseconds>[\-]?\d+)"
        r"(?P<offset>"
        r"(?P<offset_sign>[\+\-])"
        r"(?P<offset_hours>[01][0-9]|2[0-3])"
        r"(?P<offset_mins>[0-5][0-9])"
        r")?\)/"
    )
    try:
        parts = re.match(regex, jsondate).groupdict()
        since_epoch = timedelta(microseconds=1000 * int(parts["milleseconds"]))
        if parts.get("offset"):
            since_epoch += timedelta(
                hours=int("%s%s" % (parts["offset_sign"], parts["offset_hours"])),
                minutes=int("%s%s" % (parts["offset_sign"], parts["offset_mins"])),
            )
        return datetime(year=1970, month=1, day=1, tzinfo=tzinfo) + since_epoch
    except (AttributeError, TypeError):
        raise ValueError("Unsupported ASP.NET JSON Date Format: {}".format(jsondate))


def parse_date(date):
    try:
        date = parser.parse(date)
    except Exception as e:
        print("Parser couldn't parse {} with error: {}".format(date, e))
    finally:
        return date


class YemeksepetiApi:
    """
    Yemeksepeti API is available to anonymous access.

    Proxy Usage:

    proxies = {}
    proxies['http'] = 'socks5h://localhost:9050'
    proxies['https'] = 'socks5h://localhost:9050'
    """

    def __init__(self, proxy=None):
        self.SESSION = requests.session()
        self.SESSION.proxies = proxy
        self.API_TOKEN = None
        self.REVIEW_TOKEN = None
        self.API_CLIENT_SECRET = config.API_CLIENT_SECRET
        self.__cfduid = None
        self.login()

    def login(self, timeout=5):
        try:
            self.SESSION.headers.clear()
            self.SESSION.cookies.clear()
            login_headers = {
                "appversion": "Androidv3.4.0",
                "appversioncode": "74",
                "content-type": "application/json",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/4.3.1",
            }
            self.SESSION.headers = login_headers
            login_data = {"apiKey": self.API_CLIENT_SECRET}
            api_request = self.SESSION.post(
                config.ANON_LOGIN, json=login_data, timeout=timeout
            )
            review_request = self.SESSION.post(config.REVIEW_AUTH)
            self.API_TOKEN = api_request.json()["d"]["Result"]["Token"]["TokenId"]
            self.__cfduid = (
                api_request.headers["set-cookie"].split(";")[0].split("=")[1]
            )
            self.REVIEW_TOKEN = review_request.json()["access_token"]
        except Exception as e:
            print("Login failed. Error message: {}".format(e))

    def get_review_session(self, catalog="TR_ISTANBUL"):
        """
        Reviews are requested with different headers for each catalog, so we spawn a separate requests session.
        TODO: Solve the need for a separate session
        :param catalog: Province
        :return: Session
        """
        session = requests.session()
        headers = {
            "appversion": "Androidv3.4.0",
            "appversioncode": "74",
            "authorization": "Bearer " + self.REVIEW_TOKEN,
            "ys-culture": "tr-TR",
            "ys-catalog": catalog,
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.3.1",
        }
        session.headers = headers
        session.cookies["__cfduid"] = self.SESSION.cookies["__cfduid"]
        session.proxies = self.SESSION.proxies
        return session

    def get_catalogs(self, catalog="TR_ISTANBUL"):
        """
        :param catalog: This variable is mandatory however has no effect.
        :return: Catalogs. (Provinces)

        TODO: Catalog class.
        """
        try:
            data = {
                "ysRequest": {
                    "ApiKey": self.API_CLIENT_SECRET,
                    "CatalogName": catalog,
                    "Culture": "tr-TR",
                    "PageNumber": 0,
                    "PageRowCount": 1000,
                    "Token": self.API_TOKEN,
                }
            }
            request = self.SESSION.post(config.CATALOGS, json=data)
            catalogs = request.json()["d"]["ResultSet"]
            return catalogs
        except Exception as e:
            print("Failed to get catalogs. Error message: {}".format(e))

    def get_catalog_areas(self, catalog="TR_ISTANBUL"):
        """
        :param catalog: Province which areas belong to.
        :return: Areas, including their ids.

        TODO: Area class.
        """
        try:
            data = {
                "ysRequest": {
                    "ApiKey": self.API_CLIENT_SECRET,
                    "CatalogName": catalog,
                    "Culture": "tr-TR",
                    "PageNumber": 0,
                    "PageRowCount": 1000,
                    "Token": self.API_TOKEN,
                }
            }
            request = self.SESSION.post(config.AREAS, json=data)
            areas = request.json()["d"]["ResultSet"]
            return areas
        except Exception as e:
            print("Failed to get catalog areas. Error message: {}".format(e))

    def search_restaurants(
        self, catalog="TR_ISTANBUL", area_id="e0b46c42-6718-4c7c-95be-208e835acd6a"
    ):
        """
        :param catalog: Catalog name ("CategoryName") from get_catalogs()
        :param area_id: Area id ("Id") from get_catalog_areas()
        :return: List of restaurants

        TODO: Restaurants class, Args, kwargs.
        """
        try:
            data = {
                "searchRequest": {
                    "AreaId": area_id,
                    "CuisineId": "",
                    "DetailedTotalPoints": 0.0,
                    "HavingPromotion": False,
                    "IsNewQuery": False,
                    "MinimumDeliveryPrice": 0,
                    "OnlyOneArea": False,
                    "OpenOnly": False,
                    "PaymentMethodId": "",
                    "RestaurantCategory": "",
                    "RestaurantName": "",
                    "RestaurantPrimaryCategory": "",
                    "SortDirection": "0",
                    "SortField": "1",
                    "SpecialCategoryId": "",
                    "SuperDelivery": False,
                },
                "ysRequest": {
                    "ApiKey": self.API_CLIENT_SECRET,
                    "CatalogName": catalog,
                    "Culture": "tr-TR",
                    "PageNumber": 1,
                    "PageRowCount": 21337,
                    "Token": self.API_TOKEN,
                },
            }
            request = self.SESSION.post(config.SEARCH_RESTAURANTS, json=data)
            restaurants = request.json()["d"]["ResultSet"]["searchResponseList"]
            for restaurant in restaurants:
                # Adding extra pieces of information to make data handling easier.
                restaurant["LastChecked"] = datetime.utcnow()
                restaurant["AreaId"] = area_id
                restaurant["CreatedDate"] = netdate2py(restaurant["CreatedDate"])
            return restaurants
        except Exception as e:
            print("Failed to get restaurants. Error message: {}".format(e))

    def get_restaurant_reviews(
        self,
        category_name="556149dd-3dd5-49d7-b6cf-1f2ebda27bee",
        catalog="TR_ISTANBUL",
        area_id="e0b46c42-6718-4c7c-95be-208e835acd6a",
        page_no=1,
    ):
        """
        Returns the top 2000 comments for each restaurant.

        :param page_no: Api returns a maximum of 2000 reviews in a page.
        :param category_name: restaurant specific id ("CategoryName") from search_restaurants()
        :param catalog: Catalog name ("CategoryName") from get_catalogs()
        :param area_id: Area id ("Id") from get_catalog_areas()
        :return: List of reviews
        """
        review_session = self.get_review_session(catalog=catalog)
        try:
            review_link = config.REVIEW_BASE + category_name
            params = {
                "UserAreaId": area_id,
                "CommentPageNumber": page_no,
                "PointCount": 10,
                "PointWeekCount": 6,
                "CommentPageSize": 2000,
            }
            request = review_session.get(review_link, params=params)
            reviews = request.json()["Data"]["CommentsServiceResponse"]["Comments"]
            for review in reviews:
                review["CommentDate"] = parse_date(review["CommentDate"])
            return reviews
        except Exception as e:
            print("Failed to get restaurant reviews. Error message: {}".format(e))
        finally:
            review_session.close()
