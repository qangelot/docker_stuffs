# Hands on Docker

# TP1

Ici, nous créons un wrapper qui retourne la météo d'un lieu donné avec sa latitude et sa longitude (passées en variable d'environnement) en utilisant Openweather API et le langage de programmation python.

Ensuite nous allons packager ce code dans une image Docker puis la mettre à disposition son image sur DockerHub.

## Quelques supports utiles 

- https://pypi.org/project/python-dotenv/ 
- https://lucasvidelaine.wordpress.com/2018/01/29/utilisation-de-dockerhub/
- https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

## Choix techniques

Au vu de la polyvalence et de la simplicité de Python, c'est le langage que j'ai choisi de retenir ici. En effet, c'est un langage de choix quand il s'agit de manipuler des données quelque soit la source et la nature. Il est aussi simple à prendre en main d'un point de vue syntaxique et nous pourrons ainsi nous concentrer sur l'objet de la séance : Docker. 


## Travaux préliminaires 

Afin d'isoler l'environnement de développement de celui de production, nous créons un environnement virtuel : 

``` python3 -m venv myvenv```

Nous pouvons ainsi y installer les packages nécessaires puis les collecter dans un fichier .txt pour ensuite les installer dans le conteneur Docker :

``` pip freeze -> requirements.txt```

## Code python

Nous récupérons la clé d'API sur le site [openweather.com](https://openweathermap.org/), nous la stockons ensuite en local dans un fichier .env.

Nous y accédons dans le code par le biais de la méthode ```python load_dotenv() ``` de la libraire dotenv, puis par l'utilisation de la ligne ```python os.environ['APIKEY'] ```

Nous récupérons les autres variables d'environnements (LAT, LONG) qui seront passées dans la commande ```bash docker run``` de la même façon.

Ensuite, nous construisons la requête auprès de l'API graĉe à la libraire requests :
```python 
response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + LAT + "&lon=" + LONG + "&appid=" + APIKEY + "&units=metric") 
```

Enfin, nous collectons la réponse : 
- son statut : ```python response.status_code ```
- son contenu au format json : ```python response.json() ```

## Conteneurisation 

### Dockerfile 

```
FROM python:3.8-buster

WORKDIR /tp1_

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

Docker construit automatiquement les images en lisant les instructions du Dockerfile, un fichier texte qui contient toutes les commandes, dans l'ordre, nécessaires pour construire une image donnée.

Chaque instruction crée une couche :

- FROM crée une couche à partir de l'image Docker python:3.8-buster.
- COPY ajoute les fichiers du répertoire courant de le client Docker.
- RUN est utilisé ici pour installer les packages utilisés dans notre application.
- CMD spécifie la commande à exécuter dans le conteneur pour lancer l'application.
- EXPOSE indique les ports sur lesquels un conteneur écoute les connexions. Ici, le port 5000.

### Construire l'image et la lancer

Pour construire l'image : ``` docker build --tag mywrapper .``` <br>
Pour la lancer localement : ``` docker run -p 5000:5000 --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=$APIKEY --rm mywrapper```

## Mise de l'image à disposition sur le DockerHub

- On récupère l'id de l'image : ``` docker images ```
- On se connecte au DockerHub : ``` docker login --username=qangelot```
- On tag l'image : ``` docker tag 3b14e019997f qangelot/tpdevops```
- On pousse l'image : ``` docker push qangelot/tpdevops ```
- On la récupère : ``` docker pull qangelot/tpdevops```
- On la run : ``` docker run --env LAT="5.902785" --env LONG="102.754175" --env API_KEY=$APIKEY  qangelot/tpdevops```

# TP2

Ici, l'objectif est de configurer un workflow Github Action, transformer le wrapper du TP1 en API Flask, publier automatiquement à chaque push sur Docker Hub

## Choix techniques

Nous avons retenu le framework Flask qui est excellent pour construire rapidement une API en Python. De plus, si nous souhaitons améliorer l'application, Flask permet le recours à une infinité de plugins afin de sécuriser l’application, de faciliter la gestion des formulaires et du statut de l’utilisateur, de simplifier le mailing, l’alimentation et le requêtage de la base de données… 

## Code python

On instancie l'application Flask:

```python app = flask.Flask(__name__) ```

Ensuite, on peut aisément construire un endpoint de notre API grâce à un décorateur intégré:

```python 
@app.route('/api/weather/', methods=['GET'])
def api_weather():
```

Puis on construit l'appel à l'API Openweather, en utilisant les variables passées dans l'environnement et notre clé d'API stockée dans les secrets DockerHub:
```python
LAT = request.args.get('lat')
LONG = request.args.get('lon')  
output = {}
uri = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={app.config['APIKEY']}&units=metric"
res = requests.get(uri)
```
Enfin, si la requête est valide, on récupère et formate les données souhaitées:

```python
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
```

## Configuration des Github Actions

Pour cela, on stock nos secrets nécessaires à la connexion au DockerHub dans le repository github concerné.

Ensuite on rédige un fichier YAML de configuration de la CI pipeline:
- on nomme la pipeline,
- on définit les différentes triggers d'exécution de celle-ci (ici un push sur la branche 'main' du repository),
- puis on rédige les différentes actions à accomplir.

Ici, on a recours à des Github Actions de la marketplace, car très standard : le login à DockerHub (à l'aide des secrets fournis) et le build et le push de l'image sur le DockerHub:

```   -
        name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
      -
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          push: true
          tags: ${{ secrets.USERNAME }}/tpdevops2:latest 
```

Nous avons ainsi construit un pipeline d'intégration continue qui, à chaque nouveau push de code, va construire une image Docker à partir de notre API Flask mise à jour et la publier sur le DockerHub. L'étape suivante est d'intégrer des tests à ce pipeline.

## Usage

Après avoir pull l'image sur le DockerHub, il faut lancer l'image en local et ouvrir un second terminal où exécuter une commande curl.

```docker run --network host --env APIKEY=$APIKEY qangelot/tpdevops2```
```curl "http://localhost:5000/api/weather/?lat=5.902785&lon=102.754175"```



