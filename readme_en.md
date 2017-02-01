# Hervé | Documentation:
![](Https://img.shields.io/badge/language-python3.4-green.svg)

## Install Hervé

```Shell
git clone http://github.com/Projet-Herve/HerveSys
cd HerveSys /
virtualenv venv
source venv / bin / activate
pip3 install --upgrade -r requirements.txt
```

If you want to use a [Ngrok](https://ngrok.com/) tunnel for Hervé, follow the [Ngrok installation instructions](https://ngrok.com/download). Do not forget to place yourself in the folder Hervé. Move the Ngrok executable to the root of the Hervé folder.

When you run Hervé, a Ngrok instance will be created.


## Execute Hervé:

```Shell
python3 __main__.py run [-host IP] [-port PORT]
```

Concerning the arguments, all arguments starting with `-` can modify the` myapp` variables.


## Applications :

#### During development:

During the creation of your application it will be necessary to submit to certain conventions.

```python

@webapp.route ("/mynewapp")
@login_required
def index_mynewapp ():
	"" "
	Your code
	"" "
return render_template ("apps/mynewapp/index.html", datas = locals (), myapp = myapp)
```

It will be necessary to define the arguments `datas` and` myapp` to have a good functioning of Hervé and your application:
Otherwise, Flask will report an error.

##### Defining a widget for its application:

To define a widget in its application add in the manifest.json the `` [page element] [url of the page] `` to the `widgets` list.
Generally widgets are elements already present in templates. If your widget is not, you can generate HTML from python:

```Python

@webapp.route ("/url")
@login_required
def index_mynewapp ():
html = tag ("div",
	class_ = ["my_class"],
	content = tag ("p",
		content = "My super text"
	)
)

return Response (response = html, status = 200, mimetype = "text/html")
```

So you can select your widget in this way:

```json
...

"widgets": [
	".my_class /url"
],

...
```

##### Defining a periodic task

```python
def periodicfunction ():
	print ("I work")

schedule.every(10).seconds().do(periodicunction)

```

It is possible to use a decorator but it will only make your code more dirty.
The code below is equivalent to the one above.

```python
decorator = schedule.every(10).seconds().do

@decorator
Defperiodicfunction ():
Print ("I work")

```

##### Defining a Perpetual Spot

To make a perpetual function, use the `myapp.forever` decorator

```Python
@myapp.forever
def myperpetualfunction ():
	print ("I work")
```
##### Defining a stain back plant

To run a background function, use the `myapp.in_thread` decorator

```Python
@myapp.in_thread
def mafunction ():
	print ("I work in background")
```

##### Allow access only to users who have activated the application:

```Python
@need_app_active
```


## The users :

By default, there is only one user.

| Id | Null |
| -------------- | ------- |
| Home | Sys |
| Home | 1234 |
| Profile | No |

The `sys` user is the superuser so it has all the power over your infrastructure.

It is not yet possible to edit a profile except by editing the `settings.json` file in `/datas`.

The `sys` user is the only user that should not be deleted. If a deletion occurs, your Hervé installation will no longer work.