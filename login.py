from flask import Flask, render_template,request,redirect,url_for
from flask import jsonify
import MySQLdb

import os
from urllib import parse

parse.uses_netloc.append("mysql")
url = parse.urlparse(os.environ["CLEARDB_DATABASE_URL"])

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('login.html')

@app.route("/templates/main_page.html", methods=["POST"])
def main_page():
    global url
    db = MySQLdb.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sigma.userdata;")
    data = cursor.fetchall()

    _username = request.form['user_input']
    _password = request.form['password_input']
    flag_1 = 0
    
    if request.method == 'POST': 
        for row in data :
            if row[1] == _username and row[2] == _password:
                flag_1 = 1
                break
        if flag_1 == 1:
            cursor.execute("SELECT * FROM sigma.sensors;")
            data = cursor.fetchall()
            return render_template('main_page.html', data = data)
        else:
            return render_template('login.html', flag_1 = 0)
    db.close()

@app.route("/templates/main_page/order", methods=["POST"])
def type():
    global url
    _sensortype = request.form['order_by']
    _coolroomid = request.form['coolroom_input']
    print(_coolroomid, _sensortype)
    db = MySQLdb.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname)
    cursor = db.cursor()

    if _sensortype and _coolroomid:
        query = "SELECT * FROM sigma.sensors WHERE SENSOR_TYPE = '%s' AND COOLROOM_ID = %s;" %(_sensortype, _coolroomid)
    elif not _sensortype and _coolroomid:
        query = "SELECT * FROM sigma.sensors WHERE COOLROOM_ID = %s;" %(_coolroomid)
    elif not _coolroomid and _sensortype:
        query = "SELECT * FROM sigma.sensors WHERE SENSOR_TYPE = '%s';" %(_sensortype)
    else:
        query = "SELECT * FROM sigma.sensors;"    
    
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()

    return render_template('main_page.html', data = data)

# cursor.execute("SELECT * FROM sigma.sensors, WHERE SENSOR_TYPE = %s" % type)

# Primera Alternativa:
# 1. Hacer una funcion de javascript que se llame a si misma con el metodo interval
#    cada 1 segundo
#    Tal funcion va a hacer una llamada a localhost:5000/obtener_datos (servidor flask)
# 2. Hacer la ruta /obtener_datos en Flask que haga una consulta a la base de datos
#    y que tenga de return un json
#
# 3. Con el json que se recibe de la peticion ajax, utilizar las funciones del DOM
#    para modificar la tabla y agregar la informacion del json
#
# Segunda Alternativa: SOCKETIO con Flask

if __name__ == "__main__":
    app.run()
