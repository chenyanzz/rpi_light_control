from flask import *
import hardware
import atexit

app = Flask('cy server',static_url_path='/static/',template_folder='template/')

light = hardware.Light()
switch = hardware.Switch()

def main():
    hardware.init()
    light.init()
    switch.init(on_state_change)
    app.run(host='0.0.0.0', port = 80, debug=False) # The HOST must be '0.0.0.0' not '127.0.0.1' in LINUX!

@atexit.register
def on_exit():
    hardware.tini()

def on_state_change(is_on):
    light.flipState()


@app.route('/light', methods=['GET','POST'])
def handle_page():
    if 'act' in request.form:
        action = request.form['act']
        if action=='flip': 
            light.flipState()
        elif action=='on': 
            light.turnOn()
        elif action=='off': 
            light.turnOff()

    return render_template("light.html", is_on = light.is_on)
