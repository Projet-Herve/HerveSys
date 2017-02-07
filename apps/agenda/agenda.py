global calendar
global datetime
from datetime import datetime


class calendar():

    def __init__(self, user):
        '''
                Build the calendar.
        '''
        self.s = myapp.settings()
        self.user = user
        self.agenda = self.s[self.user]["datas"]
        self.agenda = self.agenda.get("agenda", list())
        self.cal = dict()
        for event in self.agenda:
            if event['type'] == 'once':
                date = datetime.strptime(
                    event['date'], '%Y-%m-%d %H:%M').date()
                if self.cal.get(date):
                    self.cal[date].append(event)
                else:
                    self.cal[date] = [event]

    def get_future_events(self):
        '''
                Read calendar and get future events.
        '''
        Prochains = dict()
        for date in self.cal:
            if date > datetime.now().date():
                if Prochains.get(date):
                    Prochains[date].append(self.cal[date])
                else:
                    Prochains[date] = self.cal[date]
        return (Prochains)

    def create_a_new_event(self, title, datetime, type, description=None):
        '''
                Create a new event.
        '''
        try:
            NewEvent = dict()
            NewEvent['title'] = title
            NewEvent['date'] = datetime.strftime('%Y-%m-%d %H:%M')
            NewEvent['description'] = description
            NewEvent['type'] = type
            NewEvent['id'] = len(self.agenda) + 1
            self.agenda.append(NewEvent)
            self.s[self.user]["datas"]["agenda"] = self.agenda
            update_datas(self.s, myapp.settings_file)
            self.__init__(self.user)
            return(NewEvent)
        except Exception as e:
            return (False, e)



@webapp.route('/agenda')
@login_required
def agenda_index():
    user_cal = calendar(session["utilisateur"])
    future_events = user_cal.get_future_events()
    return render_template("agenda/templates/index.html", future_events=future_events)


@webapp.route("/agenda/new", methods=["POST"])
@login_required
def creat():
    user_cal = calendar(session["utilisateur"])
    if request.form.get("type") == "once":
        event = dict()
        event["title"] = request.form.get("title")
        event["type"] = request.form.get("type")
        event["description"] = request.form.get("description")
        event["datetime"] = datetime.strptime(request.form.get("date"), '%Y-%m-%d %H:%M')
        user_cal.create_a_new_event(**event)
        future_events = user_cal.get_future_events()
    return render_template("agenda/templates/index.html", future_events=future_events)
