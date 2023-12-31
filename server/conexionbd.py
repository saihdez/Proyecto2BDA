import couchdb, datetime
import math

# Configurar la conexión a CouchDB
def conectar_a_couchdb():
    server = couchdb.Server('http://admin:ariel@localhost:5984/')
    return server['viajescorporativos_nodo3']

# Función para registrar un colaborador
def registrar_colaborador(correo, contrasena):
    db = conectar_a_couchdb()
    colaborador_data = {
        "correo_electronico": correo,
        "clave": contrasena,
        "solicitudes": []
    }

    try:
        colaboradores_doc = db.get("colaboradores")  # Obtiene el documento de colaboradores

        if colaboradores_doc is None:
            # Si no existe el documento, crea uno nuevo
            colaboradores_doc = {"colaboradores": [colaborador_data]}
            db['colaboradores'] = colaboradores_doc
            return True
        else:
            # Si el documento ya existe, agrega el nuevo colaborador si no existe
            colaboradores = colaboradores_doc.get("colaboradores", [])
            if correo not in [colaborador['correo_electronico'] for colaborador in colaboradores]:
                colaboradores.append(colaborador_data)
                colaboradores_doc['colaboradores'] = colaboradores
                db['colaboradores'] = colaboradores_doc  # Actualiza el documento de colaboradores
                return True
            else:
                return False  # El colaborador ya existe
    except couchdb.ResourceConflict:
        # Maneja el conflicto de revisión aquí, puedes implementar la lógica necesaria
        # para resolver el conflicto si es necesario
        return False  # Error de conflicto de revisión

# Función para registrar un administrador
def registrar_admin(usuario, contrasena):
    db = conectar_a_couchdb()
    admin_data = {
        "usuario": usuario,
        "clave": contrasena
    }

    try:
        admin_doc = db.get("administradores")  # Obtiene el documento de administradores

        if admin_doc is None:
            # Si no existe el documento, crea uno nuevo
            admin_doc = {"administradores": [admin_data]}
            db['administradores'] = admin_doc
            return True
        else:
            # Si el documento ya existe, agrega el nuevo administrador si no existe
            admins = admin_doc.get("administradores", [])
            if usuario not in [admin['usuario'] for admin in admins]:
                admins.append(admin_data)
                admin_doc['administradores'] = admins
                db['administradores'] = admin_doc  # Actualiza el documento de administradores
                return True
            else:
                return False  # El administrador ya existe
    except couchdb.ResourceConflict:
        # Maneja el conflicto de revisión aquí, puedes implementar la lógica necesaria
        # para resolver el conflicto si es necesario
        return False  # Error de conflicto de revisión

# Función para autenticar colaboradores
def autenticar_colaborador(correo, contrasena):
    db = conectar_a_couchdb()
    colaboradores = db['colaboradores']['colaboradores']
    
    for colaborador in colaboradores:
        if colaborador.get('correo_electronico') == correo and colaborador.get('clave') == contrasena:
            return True
    return False  # Las credenciales no coinciden

# Función para autenticar administradores
def autenticar_admin(usuario, contrasena):
    db = conectar_a_couchdb()
    administradores = db['administradores']['administradores']
    
    for admin in administradores:
        if admin.get('usuario') == usuario and admin.get('clave') == contrasena:
            return True
    return False  # Las credenciales no coinciden

# Función para consultar viajes por destino específico
def consultar_viajes_por_destino(destino):
    db = conectar_a_couchdb()
    viajes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if viajes:
        solicitudes = viajes.get('solicitudes', [])
        viajes_destino = []

        for solicitud in solicitudes:
            if solicitud.get('pais_destino') == destino:
                viajes_destino.append(solicitud)

        return viajes_destino
    else:
        return []

def viajes_internacionales(trimestre, año):
    db = conectar_a_couchdb()  # Asegúrate de definir esta función correctamente

    if db is not None:
        solicitudes = db.get("solicitudes")

        if solicitudes:
            viajes_internacionales = solicitudes.get('solicitudes', [])
            viajes_filtrados = []

            for viaje in viajes_internacionales:
                fecha_inicio = viaje.get('fecha_inicio')

                fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")

                # Obtenemos el mes de la fecha.
                mes = fecha_inicio.month

                # Calculamos el trimestre.
                trimestre_viaje = int((mes - 1) // 3 + 1)
                año_viaje = fecha_inicio.year
                if trimestre_viaje == int(trimestre) and año_viaje == año and viaje.get('internacional') == True:
                    viajes_filtrados.append({
                        'nombre_completo_colaborador': viaje['nombre_completo_colaborador'],
                        'pais_destino': viaje['pais_destino']
                    })

            return viajes_filtrados
        else:
            return []
    else:
        return []

def solicitudes_colaborador(correoColaborador):
    db = conectar_a_couchdb()
    db_solicitudes = db.get("solicitudes")

    if db_solicitudes:
        solicitudes_registradas = db_solicitudes.get("solicitudes", [])
        listaSolicitudes = []

        for solicitud in solicitudes_registradas:
            if correoColaborador == solicitud.get("correo"):
                listaSolicitudes.append(solicitud)
            
        return listaSolicitudes
    else:
        return []


def viajes_programados(mes, año):
    db = conectar_a_couchdb()
    solicitudes = db.get("solicitudes")

    if solicitudes:
        viajes_programados = solicitudes.get('solicitudes', [])
        viajes_filtrados = []

        for viaje in viajes_programados:
            fecha_inicio = viaje.get('fecha_inicio')
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")

            # Obtenemos el mes y el año de la fecha.
            mes_viaje = fecha_inicio.month
            año_viaje = fecha_inicio.year

            if mes_viaje == mes and año_viaje == año and viaje.get('estado') == "aprobada":
                departamento = viaje.get('departamento', 'Sin departamento')

                viajes_filtrados.append({
                    'nombre_completo_colaborador': viaje['nombre_completo_colaborador'],
                    'departamento': departamento
                })

        return viajes_filtrados
    else:
        return []

