import web
import sqlite3 # importar para la base de datos

urls = (   #Definición de las rutas del sistema
    '/', 'Index',
    r'/borrar/(\d+)', 'Borrar' # r - texto crudo, d+ - cualquier numero, saber a que registro eliminar
)

# inicialización del sistema y plantillas 
app = web.application(urls, globals()) # asocia rutas con las clases
render = web.template.render('templates/') # direccion para el interfaz

DB = 'artistas.db' # nombre de la base de datos 


def conectar():
    conexion = sqlite3.connect(DB) #busca, establece y devuelve una conexión a la base de datos
    conexion.row_factory = sqlite3.Row # sirve para devolver los registros como diccionarios y permite consultar cambios por su columna
    return conexion


# Columnas que el usuario puede elegir como regla principal
COLUMNAS_VALIDAS = [
    'id', 'nombre', 'pais', 'genero',
    'streams_anuales', 'ano_debut', 'premios_grammy', 'puesto_ranking'
]


def construir_clausula(columna_principal):
    """
    Arma la cascada de las 8 reglas.
    La columna que el usuario eligio se pone al frente,
    y detras van las 8 reglas en su orden normal.
    """
    # numeros de mayor a menor y texto/años de menor a mayor, para llevar un orden e ir midiendo los datos
    orden = "DESC" if columna_principal in ['streams_anuales', 'premios_grammy'] else "ASC"

    reglas_base = [
        f"{columna_principal} {orden}", # aqui posicionamos al regla elegida por el usuario
        "streams_anuales DESC",    # Regla 1 
        "premios_grammy DESC",     # Regla 2
        "nombre ASC",              # Regla 3
        "ano_debut ASC",           # Regla 4
        "pais ASC",                # Regla 5
        "genero ASC",              # Regla 6
        "puesto_ranking ASC",      # Regla 7
        "id ASC"                   # Regla 8
    ]

    # Quitamos reglas repetidas (si la columna elegida ya esta en la lista)
    cascada_final = [] # aqui es donde guardamos las reglas que si sirven y no están repetidas
    for regla in reglas_base: # revisa una por una 
        nombre_columna = regla.split()[0]  # extrae el nombre de la columna/regla
        if nombre_columna not in [r.split()[0] for r in cascada_final]:  
            cascada_final.append(regla) # guarda y agrega reglas no repetidas al final en una lista

    return ", ".join(cascada_final) # convierte esa lista en texto para que SQL aplique la cascada

# clase para la ruta principal y funcion que se ejecuta en automatico cuando alguien entra al sitio 
class Index:
    def GET(self):
        user_input = web.input(sort='id') # lee la URL para saber que columna solicitó el usuario
        columna_principal = user_input.sort # extrae la columna y lo guarda en la variable

# revisa que el nombre esté dentro de nuestra variable y sino sigue con id
        if columna_principal not in COLUMNAS_VALIDAS: 
            columna_principal = 'id'

        clausula_sql = construir_clausula(columna_principal) # le pasa la regla elegida y muestra los datos
        query = f"SELECT * FROM artistas ORDER BY {clausula_sql}" # une la base de datos con la cascada, generando la consulta

        conexion = conectar()
        cursor = conexion.cursor() # conecta la base de datos y ejecuta nuestra consulta 
        cursor.execute(query)
        artistas = cursor.fetchall() # extrae los datos devueltos y cierra conexion
        conexion.close()
#Pasa los datos recuperados para la interfaz
        return render.index(artistas=artistas, query_usada=query)

    def POST(self):
        datos = web.input() # recolecta la información que el usuario escribió

        conexion = conectar() # conectamos a nuestro archivo db y creamos un cursor 
        cursor = conexion.cursor() # para ejecutar las consultas SQL
        cursor.execute('''
            INSERT INTO artistas
                (nombre, pais, genero, streams_anuales, ano_debut, premios_grammy, puesto_ranking)
            VALUES (?, ?, ?, ?, ?, ?, ?)  
        ''', (  # orden para insertar un nuevo registro
            datos.nombre.strip(),  #.strip borra espacios accidentales al inicio o al final
            datos.pais.strip(),
            datos.genero.strip(),
            int(datos.streams_anuales), # int para convertirlos a numeros enteros 
            int(datos.ano_debut),
            int(datos.premios_grammy),
            int(datos.puesto_ranking)
        ))
        conexion.commit() 
        conexion.close()

        web.header('Location', '/')  # redirige a la pagina principal 
        web.ctx.status = '303 See Other' # evitamos datos duplicados
        return ''

class Borrar:
    def GET(self, id_artista):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM artistas WHERE id = ?', (id_artista,)) # ejecuta el borrar unicamente en el registro donde coincide el ID
        conexion.commit()
        conexion.close()

        web.header('Location', '/')
        web.ctx.status = '303 See Other'
        return ''


if __name__ == "__main__": #verificamos que lo estemos corriendo directamente
    app.run() # enciende el servidor web local  