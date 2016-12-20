# Documentation:

/!\ Toutes les commandes indiquées doivent être executées dans le dossier Hervé !

## Exécuter Hervé :

Pour éxecuté Hervé utilisez la commande :

```python3 __main__.py run [-h/--host] [IP] [-p/--port] [PORT] ```

## Les applications:

### Création d'une application:

Que les applications créées soient des applications web ou backend elles s'initialisent de la même façon. Pour en créer une, exécutez dans le dossier Hervé la commande : 

```python3__main__.py creatapp [nom du packet] ```

Cette commande aura pour effet de poser certaines questions puis générer une application déja installée dans Hervé. Seul l'utilisateur 'sys' pourra utiliser l'application par défaut. Les utilisateurs devrons l'activée eux-mêmes.

### Installer une application:

Pour installer une application, executez l'a commande :

```python3__main__.py installapp [path de l'application] ```

L'application devrait être instlée si les arguments donnés ne sont pas erronés. Seul l'utilisateur 'sys' pourra utiliser l'application par défaut. Les utilisateurs devrons l'activée eux-mêmes.

### Exportation d'une application

Pour exporter votre application par exemple pour le store, exécutez la commande :

```python3 __main__.py exportapp [nom du packet] [path du dossier où exporter l'application] ```

Cette commande exportera votre application dans `[path du dossier où exporter l'application]` si l'application demandée existe. Le packet créé sera installable.