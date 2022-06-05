import json

from requestsHttp import CityRequests, CountryRequests


class WyswietlOdpowiedz:
    country = CountryRequests()
    city = CityRequests()

    def getCountryFromCurrency(self, currency):

        return "Nie dostepne w tej wersji"

    def getCountryDetailsFromCountry(self, asciiCode, countryCode):
        return "Nie dostepne w tej wersji"

    def getRegionsDetailsFromCountryAndRegionCode(self, asciiCode, languageCode, countryCode, regionCode):
        httpResult = self.country.getCountryRegionsDetails(asciiCode, languageCode, countryCode, regionCode)
        result = ""
        result += str(json.loads(httpResult)['data']['name']) + ", "
        result += str(json.loads(httpResult)['data']['capital']) + ", "
        result += str(json.loads(httpResult)['data']['countryCode'])
        result += "\n"
        return result

    def CountryRegionsCitiesFromCountryAndRegionCode(self, asciiCode, languageCode, countryCode, regionCode):
        return "Nie dostepne w tej wersji"

    def getCityListFromLocation(self, location):
        httpResult = self.city.getCity(location)
        list1 = json.loads(httpResult)['data']
        result = ""
        for info in list1:
            result += str(info['city']) + ", "
            result += str(info['country']) + ", "
            result += str(info['countryCode']) + ", "
            result += str(info['region']) + ", "
            result += str(info['regionCode']) + ", "
            result += str(info['population']) + ", "
            result += "\n"
        return result

    def getNearbyCitiesFromRadiusNearOtherCity(self, radius, cityCode):
        return "Nie dostepne w tej wersji"

    def getCityDetailsFromCityCode(self, asciiMode, cityID):
        httpResult = self.city.getCityDetails(asciiMode, cityID)
        result = str(json.loads(httpResult)['data']['city']) + ", "
        result += str(json.loads(httpResult)['data']['country']) + ", "
        result += str(json.loads(httpResult)['data']['countryCode']) + ", "
        result += str(json.loads(httpResult)['data']['region']) + ", "
        result += str(json.loads(httpResult)['data']['regionCode']) + ", "
        result += str(json.loads(httpResult)['data']['population']) + ", "
        result += "\n"
        return result
