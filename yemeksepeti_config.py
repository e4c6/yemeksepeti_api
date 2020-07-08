"""
Do not modify API_CLIENT_SECRET, it's anchored to application, not user. Refer to api docs for all known API endpoints.
"""
### API CLIENT ###

API_CLIENT_SECRET = "E369A71D-2D0F-4D9F-B6C5-932081BD66CB"

### API ENDPOINTS ###

ANON_LOGIN = "https://token.yemeksepeti.com/OpenAuthentication/OAuthService.svc/LoginAnonymous"
CATALOGS = "https://api.yemeksepeti.com/YS.WebServices/CatalogService.svc/GetCatalogs"
# VersionInfo = "https://api.yemeksepeti.com/YS.WebServices/CatalogService.svc/GetVersionInfo"
AREAS = "https://api.yemeksepeti.com/YS.WebServices/CatalogService.svc/GetAreas"
# GetCampusAreas = "https://api.yemeksepeti.com/YS.WebServices/CatalogService.svc/GetCampusAreas"
SEARCH_RESTAURANTS = "https://api.yemeksepeti.com/YS.WebServices/CatalogService.svc/SearchRestaurants"
REVIEW_BASE = "https://gate.yemeksepeti.com/review/api/v1/Gateway/restaurant/"
REVIEW_AUTH = "https://oauthcore.yemeksepeti.com/v1/oauth/authorize?client_id=" + API_CLIENT_SECRET + "&grant_type=client_credentials"
