class pluginnotexist(Exception):
    pass

import os
def web(webapp,plugins):
    for plugin in plugins:
        file = plugin.split(".")[0]+".py"
        if os.path.isfile("plugins/webapp/"+file):
            with open("plugins/webapp/"+file) as plugin_src:
                src = plugin_src.read()
                exec(src, {'webapp': webapp })
        else :
            raise pluginnotexist("Le module n'existe pas !")