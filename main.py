import requests
import os
from dotenv import load_dotenv

# docker run -p 5000:5000 --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=$APIKEY --rm mywrapper
# docker run --env LAT="5.902785" --env LONG="102.754175" --env API_KEY=$APIKEY  qangelot/tpdevops

load_dotenv()
APIKEY = os.environ['APIKEY']  # reads the environment variable
LAT = os.environ['LAT']  # reads the environment variable
LONG = os.environ['LONG']  # reads the environment variable

response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + LAT + "&lon=" + LONG + "&appid=" + APIKEY + "&units=metric")

print(response.status_code)
print(response.json())