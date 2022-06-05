import requests


class CityRequests:
    headers = {
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
        "X-RapidAPI-Key": "d7360c6176msh05c380f41cd46aep1e92cbjsnc685dac8aac1"
    }

    def getCity(self, location):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        querystring = {"location": str(location), "limit": "9"}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text

    def getNearbyCities(self, radius, cityCode):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/" + str(cityCode) + "/nearbyCities"
        querystring = {"radius": str(radius), "limit": "9"}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text

    def getCityDetails(self, asciiMode, city):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/" + city
        querystring = {"asciiMode": asciiMode}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return response.text
