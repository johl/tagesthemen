from ARDProgram import ARDProgram
from flask import Flask
from flask import render_template
import pytz
from datetime import datetime

app = Flask(__name__)

def keys_exist(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

@app.route("/")
def index():
    tz = pytz.timezone('Europe/Berlin')
    today = str(datetime.now(tz).strftime('%Y-%m-%d'))
    program = ARDProgram()
    data = program.get_tv_broadcasts(today, "daserste")
    tagesthemen = {}
    when = "Entweder kommen heute keine Tagesthemen oder es gab einen Fehler beim Abruf der Programmdaten."
    who = []
    
    for i in data:
        if i["title"] == "Tagesthemen":
            tagesthemen = i

    if tagesthemen != {}:
        s = tagesthemen["begin"]
        dt = datetime.fromisoformat(s)
        when = "Die Tagesthemen kommen heute um " + str(dt.hour) + ":" + str(dt.minute) +" Uhr im Ersten." 

    if keys_exist(tagesthemen, "production", "participants"):
        for tt in tagesthemen["production"]["participants"]:
            if keys_exist(tt, "person", "showName") and keys_exist(tt, "role", "name"):
                person = tt["person"]["showName"]
                role = tt["role"]["name"]
                who.append(str(role + ": " + person))

    return render_template("index.html", when=when, who=who)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1024, debug=True)
