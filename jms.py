import re

# Method(js)                                        Description                                     JMS
# document.getElementById(id)       	            Find an element by element id                   document>#id
# document.getElementsByTagName(name)	            Find elements by tag name                       document>name
# document.getElementsByClassName(name)	            Find elements by class name                     document>.name
# element.innerHTML =  new html content	            Change the inner HTML of an element             element.html> New html content
# element.attribute = new value	                    Change the attribute value of an HTML element   element.att> New attribute value
# element.setAttribute(attribute, value)    	    Change the attribute value of an HTML element      //   //    //      //     //
# element.style.property = new style	            Change the style of an HTML element             element.css> {New css property}
# document.createElement(element)                   Create an HTML element                          document>new()
# document.removeChild(element)	                    Remove an HTML element                          document>del()
# document.appendChild(element)	                    Add an HTML element                             document>append()
# document.replaceChild(element)	                Replace an HTML element                         document>replace()
# document.write(text)	                            Write into the HTML output stream               document>write()
# console.log                                       Log things
# log>"My log";


def parse(document):
    document = re.sub(
        r'log>(?P<log>.*) {0,1};', 'console.log(\g<log>);', document)
    document = re.sub(r'>[.](?P<class>("|\')?[a-zA-Z]*("|\')?)',
                      '.getElementsByClassName(\g<class>)', document)
    document = re.sub(r'[.]html>', '.innerHTML = ', document)
    document = re.sub(r'[.]att>', '.attribute = ', document)
    document = re.sub(r'>new\((?P<element>.*)\)',
                      '.createElement(\g<element>)', document)
    document = re.sub(r'>del\((?P<element>.*)\)',
                      '.removeChild(\g<element>)', document)
    document = re.sub(r'>append\((?P<element>.*)\)',
                      '.appendChild(\g<element>)', document)
    document = re.sub(r'>write\((?P<element>.*)\)',
                      '.write(\g<element>)', document)
    document = re.sub(r'>replace\((?P<element>.*)\)',
                      '.replaceChild(\g<element>)', document)
    document = re.sub(r'[.]css>\{(?P<css>.*)\}',
                      '.style.property = "\g<css>"', document)
    document = re.sub(
        r'>#(?P<id>("|\')?[a-zA-Z]*("|\')?)', '.getElementById(\g<id>)', document)
    #document = re.sub(r'>(?P<tag>("|\')?[a-zA-Z]*("|\')?)','.getElementsByTagName(\g<tag>)',document)
    return document
