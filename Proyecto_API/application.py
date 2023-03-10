from flask import Flask, Response, render_template, request
import mysql.connector

app = Flask(__name__)
lista_calidades = ["S", "A", "B", "C", "D"]
lista_tipos = ["Activo", "Pasivo"]
objetos = []

# Conectar a la base de datos
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

# Obtener la página pricipal
@app.route('/', methods=["GET"])
def get_index():
    return render_template('index.html')


# Obtener objetos
@app.route('/get-objects', methods=["GET"])
def get_objects():
    # Parámetros de entrada ?calidad=A|B|C|S
    args = request.args
    base, url = request.url.split('?', 1)

    calidad_input = request.args.get('calidad')
    tipo_input = request.args.get('tipo')
    nombre = request.args.get('nombre')
    objetos_mostrar = []

    # Solo calidad
    if calidad_input is not None and tipo_input is None:
        # Comrpbar cuántos parámetros se ha introducido
        if len(calidad_input) > 2:
            calidades = calidad_input.split(",")

            # Comprobar si las calidades introducidas son válidas
            if validar_calidades(calidades, lista_calidades):
                # Busca el objeto con las calidades introducidas
                for item in objetos:
                    if item["CALIDAD"] in calidad_input:
                        objetos_mostrar.append(item)
                if len(objetos_mostrar) > 0:
                    return objetos_mostrar
                else:
                    return Response("ERROR: Not Found", status=404)
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
                if len(objetos_mostrar) > 0:
                    return objetos_mostrar
                else:
                    return Response("ERROR: Not Found", status=404)
            else:
                # Si la caliad_input no está en la lista
                return Response("ERROR: Bad Request", status=400)
    # Solo tipo
    elif calidad_input is None and tipo_input is not None:
        # Validar el tipo, está en la lista
        if tipo_input in lista_tipos:
            for item in objetos:
                if item["TIPO"] == tipo_input:
                    objetos_mostrar.append(item)
            if len(objetos_mostrar) > 0:
                return objetos_mostrar
            else:
                return Response("ERROR: Not found", status=404)
        else:
            return Response("ERROR: El tipo introducido no es válido", status=400)
    # Calidad y tipo
    elif tipo_input is not None and calidad_input is not None:
        if calidad_input in lista_calidades and tipo_input in lista_tipos:
            for item in objetos:
                if item["CALIDAD"] == calidad_input and item["TIPO"] == tipo_input:
                    objetos_mostrar.append(item)
            if len(objetos_mostrar) > 0:
                return objetos_mostrar
            else:
                return Response("ERROR: Not found", status=404)
        else:
            return Response("ERROR: La calidad y el tipo deben ser válidos", status=400)
    # Solo nombre (no puede ir con más)
    elif nombre is not None:
        # Comprobar que no está vacío
        if nombre != "":
            for item in objetos:
                if item["NOMBRE"] == nombre:
                    objetos_mostrar.append(item)
            if len(objetos_mostrar) > 0:
                return objetos_mostrar
            else:
                return Response("ERROR: Not Found", status=404)
        else:
            return Response("ERROR: El nombre no puede estar vacío", status=400)
    else:
        return Response("ERROR: Not found", status=404)


# Obtener armas
@app.route('/get-guns', methods=["GET"])
def get_guns():
    # Parámetros de entrada ?calidad=A|B|C|S
    args = request.args
    base, url = request.url.split('?', 1)

    calidad_input = request.args.get('calidad')
    danio_input = request.args.get('dano')
    nombre = request.args.get('nombre')
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
    # Si se introduce nombre
    elif nombre is not None:
        # Comprobar que no está vacío
        if nombre != "":
            for item in armas:
                if item["NOMBRE"] == nombre:
                    armas_mostrar.append(item)
            if len(armas_mostrar) > 0:
                return armas_mostrar
            else:
                return Response("ERROR: Not Found", status=404)
        else:
            return Response("ERROR: El nombre no puede estar vacío", status=400)
    else:
        return Response("Not found", status=404)


# Obtener jefes
@app.route('/get-jefes', methods=["GET"])
def get_jefes():
    # Parámetros de entrada ?piso=1|2|3|4|5
    args = request.args
    base, url = request.url.split('?', 1)

    nombre = request.args.get('nombre')
    piso_input = request.args.get('piso')

    jefes_mostrar = []

    if piso_input is not None:
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
    elif nombre is not None:
        # Comprobar que no está vacío
        if nombre != "":
            for item in jefes:
                if item["NOMBRE"] == nombre:
                    jefes_mostrar.append(item)
            if len(jefes_mostrar) > 0:
                return jefes_mostrar
            else:
                return Response("ERROR: Not Found", status=404)
        else:
            return Response("ERROR: El nombre no puede estar vacío", status=400)
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


# Eliminar objetos
@app.route('/eliminar-objeto', methods=['DELETE'])
def eliminar_objeto():
    nombre_input = request.args.get("nombre")
    encontrado = False
    if nombre_input != "":
        # Comprobar que el nombre existe
        for item in objetos:
            if item["NOMBRE"] == nombre_input:
                encontrado = True

        # En el caso de que exista se elimina
        if encontrado:
            mycursor = mydb.cursor()
            query = "DELETE FROM objetos WHERE `objetos`.`NOMBRE` = '{}';".format(nombre_input)
            mycursor.execute(query)
            mydb.commit()
            return Response("Objeto eliminado", status=200)
        else:
            return Response("ERROR: Not found", status=404)
    # Si el campo de nombre está vacío
    else:
        return Response("ERROR: No has rellenado el campo", status=400)


# Eliminar arma
@app.route('/eliminar-arma', methods=['DELETE'])
def eliminar_arma():
    nombre = request.args.get("nombre")
    encontrado = False
    if nombre != "":
        for item in armas:
            if item["NOMBRE"] == nombre:
                encontrado = True
        if encontrado:
            mycursor = mydb.cursor()
            query = "DELETE FROM armas WHERE `armas`.`NOMBRE` = '{}';".format(nombre)
            mycursor.execute(query)
            mydb.commit()
            return Response("Arma eliminada", status=200)
        else:
            return Response("ERROR: Not found", status=404)
    else:
        return Response("ERROR: No has rellenado el campo", status=400)


# Eliminar jefe
@app.route('/eliminar-jefe', methods=['DELETE'])
def eliminar_jefe():
    nombre = request.args.get("nombre")
    encontrado = False
    if nombre != "":
        for item in jefes:
            if item["NOMBRE"] == nombre:
                encontrado = True
        if encontrado:
            mycursor = mydb.cursor()
            query = "DELETE FROM jefes WHERE `jefes`.`NOMBRE` = '{}';".format(nombre)
            mycursor.execute(query)
            mydb.commit()
            return Response("Jefe eliminado", status=200)
        else:
            return Response("ERROR: Not found", status=404)
    else:
        return Response("ERROR: No has rellenado el campo", status=400)


# Modificar un objeto
@app.route('/modificar-objeto', methods=['PUT'])
def modificar_objeto():
    nombre_input = request.args.get('nombre')
    nuevo_nombre = request.args.get('nuevo_nombre')
    efecto = request.args.get('efecto')
    breve = request.args.get('breve')
    imagen = request.args.get('imagen')
    calidad = request.args.get('calidad')
    tipo = request.args.get('tipo')
    encontrado = False
    existe = False

    # Si no hay nombre no se puede modificar
    if nombre_input is not None:
        # Si el nombre no existe no se puede modificar
        for i in objetos:
            if i["NOMBRE"] == nombre_input:
                encontrado = True
        if encontrado:
            # Validar todos los campos
            # Si uno de los campos no se introduce se busca cuál era su antiguo valor
            if efecto is None:
                for i in objetos:
                    if i["NOMBRE"] == nombre_input:
                        efecto = i["EFECTO"]
            if breve is None:
                for i in objetos:
                    if i["NOMBRE"] == nombre_input:
                        breve = i["BREVE"]
            if imagen is None:
                for i in objetos:
                    if i["NOMBRE"] == nombre_input:
                        imagen = i["IMAGEN"]
            if calidad is None:
                for i in objetos:
                    if i["NOMBRE"] == nombre_input:
                        calidad = i["CALIDAD"]
            if tipo is None:
                for i in objetos:
                    if i["NOMBRE"] == nombre_input:
                        tipo = i["TIPO"]
            # Validar el tipo, calidad y nuevo_nombre
            if calidad is not None:
                if calidad not in lista_calidades:
                    return Response("ERROR: El valor de la calidad es inválido", status=400)
            if tipo is not None:
                if tipo not in lista_tipos:
                    return Response("ERROR: El valor del tipo es inválido", status=400)
            if nuevo_nombre is not None:
                existe = False
                for i in objetos:
                    if i["NOMBRE"] == nuevo_nombre:
                        existe = True
            if nuevo_nombre is None:
                nuevo_nombre = nombre_input
            if existe:
                return Response("ERROR: El nuevo nombre que quieres introducir ya existe", status=400)

            query = "UPDATE `objetos` SET `NOMBRE` = '{}', `EFECTO` = '{}', `BREVE` = '{}', `IMAGEN` = '{}'," \
                    " `CALIDAD` = '{}', `TIPO` = '{}' WHERE `objetos`.`NOMBRE` = '{}'; ".format(nuevo_nombre,
                                                                                                efecto, breve,
                                                                                                imagen, calidad,
                                                                                                tipo, nombre_input)
            mycursor = mydb.cursor()
            mycursor.execute(query)
            mydb.commit()
            return Response("Objeto modificado", status=201)
        else:
            return Response("ERROR: Not found", status=404)
    else:
        return Response("ERROR: Bad Request", status=400)


# Modificar un arma
@app.route('/modificar-arma', methods=['PUT'])
def modificar_arma():
    nombre_input = request.args.get("nombre")
    nuevo_nombre = request.args.get("nuevo_nombre")
    imagen = request.args.get("imagen")
    dano = request.args.get("dano")
    breve = request.args.get("breve")
    calidad = request.args.get("calidad")
    descripcion = request.args.get("descripcion")
    encontrado = False
    existe = False

    # Si no hay nombre no se puede modificar
    if nombre_input is not None:
        # Si el nombre no existe no se puede modificar
        for i in armas:
            if i["NOMBRE"] == nombre_input:
                encontrado = True
        if encontrado:
            # Validar todos los campos
            # Si uno de los campos no se introduce se busca cuál era su antiguo valor
            if imagen is None:
                for a in armas:
                    if a["NOMBRE"] == nombre_input:
                        imagen = a["IMAGEN"]
            if dano is None:
                for a in armas:
                    if a["NOMBRE"] == nombre_input:
                        dano = a["DANIO"]
            if breve is None:
                for a in armas:
                    if a["NOMBRE"] == nombre_input:
                        breve = a["BREVE"]
            if calidad is None:
                for a in armas:
                    if a["NOMBRE"] == nombre_input:
                        calidad = a["CALIDAD"]
            if descripcion is None:
                for a in armas:
                    if a["NOMBRE"] == nombre_input:
                        descripcion = a["DESCRIPCION"]
            # Validar calidad y nombre
            if calidad is not None:
                if calidad not in lista_calidades:
                    return Response("ERROR: El valor de la calidad es inválido", status=400)
            if nuevo_nombre is not None:
                existe = False
                for i in armas:
                    if i["NOMBRE"] == nuevo_nombre:
                        existe = True
            if nuevo_nombre is None:
                nuevo_nombre = nombre_input
            if existe:
                return Response("ERROR: El nuevo nombre que quieres introducir ya existeee", status=400)

            query = "UPDATE `armas` SET `NOMBRE` = '{}', `IMAGEN` = '{}', `DESCRIPCION` = '{}', `BREVE` = '{}', " \
                    "`DANIO` = '{}', `CALIDAD` = '{}' WHERE `armas`.`NOMBRE` = '{}';".format(nuevo_nombre, imagen,
                                                                                             descripcion, breve, dano,
                                                                                             calidad, nombre_input)
            mycursor = mydb.cursor()
            mycursor.execute(query)
            mydb.commit()
            return Response("Arma modificada", status=201)
        else:
            return Response("ERROR: Not Found", status=404)

    else:
        return Response("ERROR: Bad Request", status=400)


# Modificar un jefe
@app.route('/modificar-jefe', methods=['PUT'])
def modificar_jefe():
    nombre = request.args.get("nombre")
    nombre_nuevo = request.args.get("nuevo_nombre")
    piso = request.args.get("piso")
    descripcion = request.args.get("descripcion")
    encontrado = False
    exsite = False

    if nombre is not None:
        for j in jefes:
            if j["NOMBRE"] == nombre:
                encontrado = True
        if encontrado:
            if piso is None:
                for j in jefes:
                    if j["NOMBRE"] == nombre:
                        piso = j["PISO"]
            if descripcion is None:
                for j in jefes:
                    if j["NOMBRE"] == nombre:
                        descripcion = j["DESCRIPCION"]
            if nombre_nuevo is not None:
                for j in jefes:
                    if j["NOMBRE"] == nombre_nuevo:
                        exsite = True
            if nombre_nuevo is None:
                nombre_nuevo = nombre
            if exsite:
                return Response("ERROR: El nuevo nombre que intentas introducir ya existe", status=400)
            query = "UPDATE `jefes` SET `NOMBRE` = '{}', `PISO` = '{}', `DESCRIPCION` = '{}' " \
                    "WHERE `jefes`.`NOMBRE` = '{}';".format(nombre_nuevo, piso, descripcion, nombre)
            mycursor = mydb.cursor()
            mycursor.execute(query)
            mydb.commit()
            return Response("Jefe modificado", status=201)
            # return query
        else:
            return Response("ERROR: Not Found", status=404)
    else:
        return Response("ERROR: Bad request", status=400)


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
