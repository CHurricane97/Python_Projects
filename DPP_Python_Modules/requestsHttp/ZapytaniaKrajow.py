import requests


class CountryRequests:
    headers = {
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
        "X-RapidAPI-Key": "d7360c6176msh05c380f41cd46aep1e92cbjsnc685dac8aac1"
    }

    def getCountry(self, currencyCode):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries"
        querystring = {"currencyCode": currencyCode, "limit": "9"}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text

    def getCountryDetails(self, asciiMode, countryCode):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + countryCode
        querystring = {"asciiMode": asciiMode}
        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return response.text

    def getCountryRegionsDetails(self, asciiMode, languageCode, country, regionCode):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country + "/regions/" + regionCode
        querystring = {"asciiMode": asciiMode, "languageCode": languageCode}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text

    def getCountryRegionsCities(self, asciiMode, languageCode, country, regionCode):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/" + country + "/regions/" + regionCode + "/cities"
        querystring = {"languageCode": languageCode, "asciiMode": asciiMode, "limit": "9"}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text
