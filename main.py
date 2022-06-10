from flask import request, jsonify, Flask
import os, requests

# docker ne copie pas le .env, on le passe dans la commande:
# export APIKEY=MYAPIKEY
# docker run -p 5000:5000 --env APIKEY=$APIKEY --rm myapi

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object('config.Config')


@app.route('/', methods=['GET'])
def home():
    html = """
           <h1>Sunrise-sunset API</h1>
           <p>Example RESTful API for the course Lab. of Cloud Computing, Big Data and security @ UniCatt</p>
           """
    return html


@app.route('/api/<city>', methods=['GET'])
def api(city):
    output = {}
    if city:
        output = {
            'sunrise': 1,
            'sunset': 2,
            'city': city
        }
    return jsonify(output)

@app.route('/api/daylight/<city>', methods=['GET'])
def api_daylight(city):
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.config['APIKEY']}"
    print(uri)
    res = requests.get(uri)
    if res.status_code == 200:
        data = res.json()
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        output = {
            'sunrise': sunrise,
            'sunset': sunset,
            'daylight': sunset-sunrise,
            'city': city            
        }
    return output


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    # host='0.0.0.0' -> accept connection from every host (to connect through a Docker virtual network)
