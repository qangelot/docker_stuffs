# Hands on Docker

Ici, nous créons un wrapper qui retourne la météo d'un lieu donné avec sa latitude et sa longitude
(passées en variable d'environnement) en utilisant Openweather API et le langage de
programmation python.

Ensuite nous allons packager ce code dans une image Docker puis la mettre à disposition son image sur DockerHub.

## Quelques supports utiles sur Docker

- https://mldv.it/home/posts/lectures/restapi-python-docker-2020/
- https://pypi.org/project/python-dotenv/ 
- https://lucasvidelaine.wordpress.com/2018/01/29/utilisation-de-dockerhub/

## Choix techniques

Au vu de la polyvalence et de la simplicité de Python, c'est le langage que j'ai choisi de retenir ici. En effet, c'est un langage de choix quand il s'agit de manipuler des données quelqu'en soit la source et la nature. Il est aussi simple à prendre en main d'un point de vue syntaxique et nous pourrons ainsi nous concentrer sur l'objet de la séance : Docker. 


## Travaux préliminaires 

Afin d'isoler l'environnement de développement de celui de production, nous créons un environnement virtuel : 

```bash python3 -m venv myvenv```

Nous pouvons ainsi y installer les packages nécessaires puis les collecter dans un fichier .txt pour ensuite les installer dans le conteneur Docker :

```bash pip freeze -> requirements.txt```

## Code python

Nous récupérons la clé d'API sur le site [openweather.com](https://openweathermap.org/), nous la stockons ensuite en local dans un fichier .env.

Nous y accédons dans le code par le biais de la méthode ```python load_dotenv() ``` de la libraire dotenv, puis par l'utilisation de la ligne ```python os.environ['APIKEY'] ```

Nous récupérons les autres variables d'environnements (LAT, LONG) qui seront passées dans la commande ```bash docker run``` de la même façon.

Ensuite, nous construisons la requête auprès de l'API graĉe à la libraire requests :
```python response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + LAT + "&lon=" + LONG + "&appid=" + APIKEY + "&units=metric") ```

Enfin, nous collectons la réponse : 
- son statut : ```python response.status_code ```
- son contenu au format json : ```python response.json() ```

## Conteneurisation 

### Dockerfile 

```bash
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

Pour construire l'image : ```bash docker build --tag mywrapper .```
Pour la lancer localement : ```bash docker run -p 5000:5000 --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=$APIKEY --rm mywrapper```

## Mise de l'image à disposition sur le DockerHub

- On récupère l'id de l'image : ```bash docker images ```
- On se connecte au DockerHub : ```bash docker login --username=qangelot```
- On tag l'image : ```bash docker tag 3b14e019997f qangelot/tpdevops```
- On pousse l'image : ```bash docker push qangelot/tpdevops ```
- On la récupère : ```bash docker pull qangelot/tpdevops```
- On la run : ```bash docker run --env LAT="5.902785" --env LONG="102.754175" --env API_KEY=$APIKEY  qangelot/tpdevops```



