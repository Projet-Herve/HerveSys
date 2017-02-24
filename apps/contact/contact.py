global contact

class contact():

    def __init__(self, user):
        """
            Charge les contacts 
        """
        self.user = user
        self.s = myapp.settings()
        try:
            self.contacts = self.s[self.user]["datas"]
            self.contacts = self.contacts.get("contacts", list())
        except Exception as e :
            print(e)
            pass

    def list(self):
        return self.contacts

    def get_contact(self, search_value):
        result = list()
        for personne in self.contacts:
            for key in personne:
                if search_value in personne[key]:
                    result.append(personne)
        return result

    def create_contact(self, **kwargs):
        contact = kwargs
        self.contacts.append(contact)
        self.s[self.user]["datas"]["contacts"] = self.contacts
        update_datas(self.s, myapp.settings_file)




@webapp.route('/contact')
@login_required
def contact_index():
    contacts = contact(session["utilisateur"]).list()
    return render_template("contact/templates/index.html",list = contacts)
