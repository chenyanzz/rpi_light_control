#coding: utf-8

from flask import *

app = Flask('cy server',static_url_path='/static/',template_folder='www/')

@app.route('/')
def test_page():
    if 'act' in request.args:
        action = request.args['act']
        if action=='flip':  
            return '开关灯！'

    return render_template("light.html", num = 1)


app.run(port=80,debug=True)