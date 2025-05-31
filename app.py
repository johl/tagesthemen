from ARDProgram import ARDProgram
from flask import Flask
from flask import render_template
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    tz = pytz.timezone('Europe/Berlin')
    today = str(datetime.now(tz).strftime('%Y-%m-%d'))
    program = ARDProgram()
    data = program.get_tv_broadcasts(today, "daserste")

    tagesthemen = {}
    for i in data:
        if i["title"] == "Tagesthemen":
            tagesthemen = i

    if tagesthemen != {}:
        s = tagesthemen["begin"]
        dt = datetime.fromisoformat(s)
        when = "Die Tagesthemen kommen heute um " + str(dt.hour) + ":" + str(dt.minute) +" Uhr im Ersten." 
    return render_template("index.html", when=when)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1024, debug=True)
