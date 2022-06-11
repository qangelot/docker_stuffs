from flask import request, jsonify, Flask
import os, requests


# docker ne copie pas le .env, on le passe dans la commande: export APIKEY=MYAPIKEY
# docker run -p 5000:5000 --env APIKEY=$APIKEY --rm myapi

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object('config.Config')


@app.route('/', methods=['GET'])
def home():
    html = """
           <h1>Weather API</h1>
           <p>RESTful API made to provide infos about the weather to the end user.
           <br> Usage:
           <ul>
            <li> /api/daylight/'city_name': get daylight infos about the provided LAT/LONG couple</li>
            <li> /api/weather/: get weather infos about the provided LAT/LONG couple</li>
           </ul>
           </p>
           """
    return html


@app.route('/api/daylight/', methods=['GET'])
def api_daylight():
    # reads the environment variables
    LAT = os.environ['LAT']  
    LONG = os.environ['LONG']
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={app.config['APIKEY']}&units=metric"
    print(uri)
    res = requests.get(uri)
    print(res)    
    if res.status_code == 200:
        data = res.json()
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        output = {
            'sunrise': sunrise,
            'sunset': sunset,
            'daylight': sunset-sunrise            
        }
    return jsonify(output)


@app.route('/api/weather/', methods=['GET'])
def api_weather():
    # reads the environment variables
    LAT = os.environ['LAT']  
    LONG = os.environ['LONG']
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={app.config['APIKEY']}&units=metric"
    print(uri)
    res = requests.get(uri)
    print(res)
    if res.status_code == 200:
        data = res.json()
        temp = data['main']['temp']
        temp_feel = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        output = {
            'actual temperature': temp,
            'feeling': temp_feel,
            'pressure': pressure,
            'humidity': humidity            
        }
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    # host='0.0.0.0' -> accept connection from every host (to connect through a Docker virtual network)
