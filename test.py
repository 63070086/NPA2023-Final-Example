import requests
import json
import time

accessToken = "Bearer NTliYTI2YmEtNWZhNC00NjRjLThhOWQtNGMzN2Y2ODg2ZDcyN2UyYzc4OGMtZTBj_P0A1_a61a0b2b-feba-43a3-8a20-e8cc10a43c9a" 

roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNzVmNGE1YjAtZTdhZC0xMWVlLWIyNjEtNDczYWNhMmVjYzEy" 

while True:
    time.sleep(1)

    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                        }
    
    r = requests.get("https://webexapis.com/v1/messages",
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    json_data = r.json()

    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")
    
    messages = json_data["items"]

    message = messages[0]["text"]
    print("Received message: " + message)

    if message.find("/") == 0:
        location = message[message.find(" ")+1:]
        
        openweatherGeoAPIGetParameters = {
            "q": location,
            "limit": 1,
            "appid": "1e54a279b8789387bd9b7dda161c4fe8",
        }

        r = requests.get("http://api.openweathermap.org/geo/1.0/direct", 
                             params = openweatherGeoAPIGetParameters
                        )
        
        json_data = r.json()
        print(json_data)
        
        if not r.status_code == 200:
            raise Exception("Incorrect reply from OpenWeather Geocoding API. Status code: {}".format(r.statuscode))
        
        locationLat = json_data[0]["lat"]
        locationLng = json_data[0]["lon"]

        openweatherAPIGetParameters = {
                                "lat": locationLat,
                                "lon": locationLng,
                                "appid": "1e54a279b8789387bd9b7dda161c4fe8"
                            }
        
        rw = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                             params = openweatherAPIGetParameters
                        )
        
        json_data_weather = rw.json()

        if not "weather" in json_data_weather:
            raise Exception("Incorrect reply from openweathermap API. Status code: {}. Text: {}".format(rw.status_code, rw.text))
        
        weather_desc = json_data_weather["weather"][0]["description"]
        weather_temp = json_data_weather["main"]["temp"]

        responseMessage = "In {} (latitude: {}, longitute: {}), the current weather is {} and the temperature is {} degree celsius.\n".format(location, locationLat, locationLng, weather_desc, weather_temp)

        HTTPHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        
        PostData = {
                            "roomId": roomIdToGetMessages,
                            "text": responseMessage
                        }
        
        r = requests.post( "https://webexapis.com/v1/messages", 
                              data = json.dumps(PostData), 
                              headers = HTTPHeaders
                         )
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))