from flask import Flask, Response, render_template, request
import mysql.connector

app = Flask(__name__)
lista_calidades = ["S", "A", "B", "C", "D"]
objetos = []

# Conectar a la base de daots
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto_api")


def get_filas_objetos():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM objetos")
    results = mycursor.fetchall()
    return [dict(zip(mycursor.column_names, row)) for row in results]


def get_filas_jefes():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM jefes")
    results = mycursor.fetchall()
    return [dict(zip(mycursor.column_names, row)) for row in results]


def get_filas_armas():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM armas")
    results = mycursor.fetchall()
    return [dict(zip(mycursor.column_names, row)) for row in results]


# Convertir la lista en json
objetos = get_filas_objetos()
jefes = get_filas_jefes()
armas = get_filas_armas()


# Obtener todos los objetos
@app.route('/get-all-objects', methods=["GET"])
def get_all_objets():
    return objetos


# Obtener todas las armas
@app.route('/get-all-guns', methods=["GET"])
def get_all_guns():
    return armas


# Obtener todos los jefes
@app.route('/get-all-jefes', methods=["GET"])
def get_all_jefes():
    return jefes


# Obtener objetos
@app.route('/get-objects', methods=["GET"])
def get_objects():
    # Parámetros de entrada ?calidad=A|B|C|S
    args = request.args
    base, url = request.url.split('?', 1)

    calidad_input = str(args.get('calidad'))
    tipo_input = str(args.get('tipo'))
    objetos_mostrar = []

    # Comrpbar cuántos parámetros se ha introducido
    if len(calidad_input) > 2:
        calidades = calidad_input.split(",")

        # Comprobar si las calidades introducidas son válidas
        if validar_calidades(calidades, lista_calidades):
            # Busca el objeto con las calidades introducidas
            for item in objetos:
                if item["CALIDAD"] in calidades:
                    objetos_mostrar.append(item)
            return objetos_mostrar
        else:
            # Si la caliad_input no está en la lista
            return Response("Bad Request", status=400)
    else:
        # Comprobar si la clase introducida es válida
        if calidad_input in lista_calidades:
            # Busca el objeto con la caliad_input introducida
            for item in objetos:
                if item["CALIDAD"] == calidad_input:
                    objetos_mostrar.append(item)
            return objetos_mostrar
        else:
            # Si la caliad_input no está en la lista
            return Response("Bad Request", status=400)


# Obtener armas
@app.route('/get-guns', methods=["GET"])
def get_guns():
    # Parámetros de entrada ?calidad=A|B|C|S
    args = request.args
    base, url = request.url.split('?', 1)

    calidad_input = request.args.get('calidad')
    danio_input = request.args.get('dano')
    armas_mostrar = []

    # Si solo se introduce daño
    if calidad_input is None and danio_input is not None:
        # Comprobar si el daño introducido es válido
        if danio_input.isdigit():
            # Comprobar que salgan solo las que tiene mayor o igual daño al introducido
            for item in armas:
                if item["DANIO"] >= int(danio_input):
                    armas_mostrar.append(item)
            if len(armas_mostrar) > 0:
                return armas_mostrar
            else:
                return Response("Not found", status=404)
        else:
            return Response("Bad Request", status=400)
        return "Hay damage"
    # Si solo se introduce calidad
    elif calidad_input is not None and danio_input is None:
        # Comrpbar cuántos parámetros se ha introducido
        if len(calidad_input) > 2:
            calidades = calidad_input.split(",")

            # Comprobar si las calidades introducidas son válidas
            if validar_calidades(calidades, lista_calidades):
                # Busca el objeto con las calidades introducidas
                for item in armas:
                    if item["CALIDAD"] in calidades:
                        armas_mostrar.append(item)
                if len(armas_mostrar) > 0:
                    return armas_mostrar
                else:
                    return Response("Not found", status=404)
            else:
                # Si la caliad_input no está en la lista
                return Response("Bad Request", status=400)
        else:
            # Comprobar si la clase introducida es válida
            if calidad_input in lista_calidades:
                # Busca el objeto con la caliad_input introducida
                for item in armas:
                    if item["CALIDAD"] == calidad_input:
                        armas_mostrar.append(item)
                if len(armas_mostrar) > 0:
                    return armas_mostrar
                else:
                    return Response("Not found", status=404)
            else:
                # Si la caliad_input no está en la lista
                return Response("Bad Request", status=400)
    # Si se introduce daño y calidad (Tarda mucho en cargar)
    elif calidad_input is not None and danio_input is not None:
        # Comprobar que el daño introducido es válido
        if danio_input.isdigit():
            # Comrpbar cuántos parámetros se ha introducido
            if len(calidad_input) > 2:
                calidades = calidad_input.split(",")

                # Comprobar si las calidades introducidas son válidas
                if validar_calidades(calidades, lista_calidades):
                    for item in armas:
                        # Buscar el arma con las calidades introducidas y el daño introducido mayor o igual
                        if item["CALIDAD"] in calidades and item["DANIO"] >= int(danio_input):
                            armas_mostrar.append(item)
                    if len(armas_mostrar) > 0:
                        return armas_mostrar
                    else:
                        return Response("Not found", status=404)
                else:
                    return Response("Bad Request", status=400)
            else:
                # Si solo hay 1 parámetro de calidad
                if calidad_input in lista_calidades:
                    for item in armas:
                        if item["CALIDAD"] == calidad_input and item["DANIO"] >= int(danio_input):
                            armas.append(item)
                    if len(armas_mostrar) > 0:
                        return armas_mostrar
                    else:
                        return Response("Not found", status=404)
                else:
                    return Response("Bad Request", status=400)
        else:
            return Response("Bad Request", status=400)
    else:
        return Response("Not found", status=404)


# Obtener jefes
@app.route('/get-jefes', methods=["GET"])
def get_jefes():
    # Parámetros de entrada ?piso=1|2|3|4|5
    args = request.args
    base, url = request.url.split('?', 1)

    piso_input = request.args.get('piso')
    jefes_mostrar = []

    # Comprobar que se ha introducido un número
    if piso_input.isdigit():
        if int(piso_input) < 6:
            for item in jefes:
                if item["PISO"] == int(piso_input):
                    jefes_mostrar.append(item)
            if len(jefes_mostrar) > 0:
                return jefes_mostrar
            else:
                return Response("Not Found", status=404)
        else:
            return Response("Bad Request", status=400)
    else:
        return Response("Bad Request", status=400)


# Insertar un nuevo objeto
@app.route('/insertar-objeto', methods=["POST", "GET"])
def insertar_objeto():
    if request.method == 'GET':
        return render_template('objetos.html')

    elif request.method == 'POST':
        nombre = request.form.get("nombre")
        efecto = request.form.get("efecto")
        breve = request.form.get("breve")
        imagen = request.form.get("imagen")
        calidad = request.form.get("calidad")
        tipo = request.form.get("tipo")

        if calidad != "Calidad" or tipo != "Tipo":
            if nombre != "" or efecto != "" or breve != "" or imagen != "":
                mycursor = mydb.cursor()
                query = "INSERT INTO objetos (ID, NOMBRE, EFECTO, BREVE, IMAGEN, CALIDAD, TIPO) " \
                        "VALUES (NULL, %s, %s, %s, %s, %s, %s);"
                values = (nombre, efecto, breve, imagen, calidad, tipo)
                mycursor.execute(query, values)
                mydb.commit()
                return Response("Objeto creado", status=201)
            else:
                return Response("ERROR: Faltan uno o varios datos", status=400)
        else:
            return Response("ERROR: Por favor, selecciona una calidad o tipo ", status=400)


# Insertar una nueva arma
@app.route('/insertar-arma', methods=["POST", "GET"])
def insertar_arma():
    if request.method == 'GET':
        return render_template('armas.html')

    elif request.method == 'POST':
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        breve = request.form.get("breve")
        imagen = request.form.get("imagen")
        calidad = request.form.get("calidad")
        danio = request.form.get("danio")

        if calidad != "Calidad":
            if nombre != "" and descripcion != "" and breve != "" and imagen != "":
                mycursor = mydb.cursor()
                query = "INSERT INTO armas (ID, NOMBRE, IMAGEN, DESCRIPCION, BREVE, DANIO, CALIDAD) " \
                        "VALUES (NULL, %s, %s, %s, %s, %s, %s);"
                values = (nombre, imagen, descripcion, breve, danio, calidad)
                mycursor.execute(query, values)
                mydb.commit()
                return Response("Arma creada", status=201)
            else:
                return Response("ERROR: Faltan uno o varios datos", status=400)
        else:
            return Response("ERROR: Por favor, selecciona una calidad", status=400)


# Insertar un nuevo jefe
@app.route('/insertar-jefe', methods=['POST', 'GET'])
def insertar_jefe():
    if request.method == 'GET':
        return render_template('jefes.html')

    else:
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        piso = request.form.get("piso")

        if piso != "Piso":
            if nombre != "" and descripcion != "":
                mycursor = mydb.cursor()
                query = "INSERT INTO jefes (ID, NOMBRE, PISO, DESCRIPCION) " \
                        "VALUES (NULL, %s, %s, %s);"
                values = (nombre, piso, descripcion)
                mycursor.execute(query, values)
                mydb.commit()
                return Response("Jefe creado", status=201)
            else:
                return Response("ERROR: Faltan campos", status=400)
        else:
            return Response("ERROR: Piso no seleccionado", status=400)


def validar_calidades(lista1, lista2):
    # Comprobar si alguna letra es número
    for s in lista1:
        for c in s:
            if c.isdigit():
                return False

    for letter in lista1:
        if letter in lista2:
            return True
        else:
            return False
