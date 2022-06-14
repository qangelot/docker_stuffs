from flask import request, jsonify, Flask
import os, requests


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
            <li> /api/daylight/: get daylight infos about the provided LAT/LONG couple </li>
            <li> /api/weather/: get weather infos about the provided LAT/LONG couple </li>
           </ul>
           </p>
           """
    return html


@app.route('/api/daylight/', methods=['GET'])
def api_daylight(): 
    # get parameters
    LAT = request.args.get('lat')
    LONG = request.args.get('lon')  
    
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={app.config['APIKEY']}&units=metric"
    res = requests.get(uri)
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
    # get parameters
    LAT = request.args.get('lat')
    LONG = request.args.get('lon')  
    
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={app.config['APIKEY']}&units=metric"
    res = requests.get(uri)
    if res.status_code == 200:
        data = res.json()
        
        lat = data['coord']['lat']
        long = data['coord']['lon']
        weather = data['weather'][0]['main']
        more_details = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_feel = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
 
        output = {
            'latitude': lat,
            'longitude': long,
            'weather': weather,
            'detailed': more_details,
            'actual temperature': temp,
            'feeling': temp_feel,
            'pressure': pressure,
            'humidity': humidity            
        }
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    # host='0.0.0.0' -> accept connection from every host (to connect through a Docker virtual network)
