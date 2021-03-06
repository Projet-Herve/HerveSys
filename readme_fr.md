# Hervé | Documentation :
![](https://img.shields.io/badge/language-python3.4-green.svg)

## Installer Hervé

```shell
git clone http://github.com/Projet-Herve/HerveSys
cd HerveSys/
virtualenv venv
source venv/bin/activate
pip3 install --upgrade -r requirements.txt
```

Si vous souhaitez utiliser un tunnel [Ngrok](https://ngrok.com/) pour Hervé, suivez les [instructions d’installation de Ngrok](https://ngrok.com/download). N'oubliez pas de vous situez dans le dossier Hervé.
Déplacez l’exécutable de Ngrok à la racine du dossier Hervé.

Lorsque vous exécuterez Hervé, une instance Ngrok serra créée.


## Exécuter Hervé :

```shell
python3 __main__.py run [-host IP] [-port PORT]
```
Concernant les arguments, tous les arguments commençant par `-` peuvent modifier les variables de `myapp`.


## Les applications :


### Création d'une application :



Que les applications créées soient des applications web ou backend elles s'initialisent de la même façon. Pour en créer une, exécutez dans le dossier Hervé la commande :

```shell
python3 __main__.py createapp
```

Cette commande aura pour effet de vous poser certaines questions puis générer une application `tmp/`.

#### Pendant le développement :

##### Définir un widget pour son application :

Pour définir un widget dans son application ajouter dans le manifest.json les valeurs `"[élément de la page] [url de la page]"` à la liste `widgets`.
Généralement les widgets sont des éléments déjà présent dans les templates. Si votre widget ne l'est pas, vous pouvez générer du HTML depuis python :

```python

@webapp.route("/url")
@login_required
def index_mynewapp():
	html = tag("div",
		class_ = ["my_class"],
		contenu=tag("p",
			contenu="Mon super text"
		)
	)
	return Response(response=html,status=200,mimetype="text/html")
```

Ainsi vous pourrez sélectionner votre widget de la sorte :

```json
...

"widgets":[
	".my_class /url"
],

...
```

##### Définir une tache périodique

```python
def mafonctionperiodique():
	print("Je fonctionne")

schedule.every(10).seconds().do(mafonctionperiodique)

```
Il est possible d'utiliser un décorateur mais il ne fera que rendre votre code plus sale.
Le code ci-dessous est l'équivalent de celui du dessus.

```python
decorator = schedule.every(10).seconds().do

@decorator
def mafonctionperiodique():
	print("Je fonctionne")

```

##### Définir une tache perpétuelle

Pour rendre une fonction perpétuelle, utilisez le décorateur `myapp.forever`

```python
@myapp.forever
def mafonctionperpetuel():
	print("Je fonctionne")
```
##### Définir une tache en arrière plant

Pour exécuter une fonction en background, utilisez le décorateur `myapp.in_thread`

```python
@myapp.in_thread
def mafonction():
	print("Je fonctionne en background")
```

##### Autoriser l’accès qu'aux utilisateurs ayants activés l'application :

```python
@need_app_active
```


### Installer une application :

Pour installer une application, exécutez la commande :

```python3__main__.py installapp [path de l'application] ```

L'application devrait être installée si les arguments donnés ne sont pas erronés. L'application serra installée mais pas activée.


## Les utilisateurs :

Par défaut, il n'existe qu'un utilisateur.

| Id           | null  |
|--------------|-------|
| Pseudo       | sys   |
| Mot de passe | 1234  |
| Profile      | Non   |

L'utilisateur `sys` est le super-utilisateur il a donc tout les pouvoirs sur votre infrastructure.

Il n'est pas encore possible de modifier un profile sauf en éditant le fichier `settings.json` qui se trouve dans `/datas`.

L'utilisateur `sys` est le seul utilisateur qui ne doit pas être supprimé. Si une suppression a lieux, votre installation Hervé ne fonctionnera plus.

