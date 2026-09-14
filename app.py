import web
import sqlite3

# Agregamos la nueva ruta para borrar
urls = (
    '/', 'Index',
    '/borrar/(\d+)', 'Borrar'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

class Index:
    def GET(self):
        user_input = web.input(sort='id')
        columna_principal = user_input.sort

        columnas_validas = ['id', 'nombre', 'pais', 'genero', 'streams_anuales', 'ano_debut', 'premios_grammy', 'puesto_ranking']
        if columna_principal not in columnas_validas:
            columna_principal = 'id'

        orden = "DESC" if columna_principal in ['streams_anuales', 'premios_grammy'] else "ASC"

        reglas_base = [
            f"{columna_principal} {orden}",
            "streams_anuales DESC",
            "premios_grammy DESC",
            "nombre ASC",
            "ano_debut ASC",
            "pais ASC",
            "genero ASC",
            "puesto_ranking ASC",
            "id ASC"
        ]

        cascada_final = []
        for regla in reglas_base:
            if regla.split()[0] not in [r.split()[0] for r in cascada_final]:
                cascada_final.append(regla)
        
        clausula_sql = ", ".join(cascada_final)

        conexion = sqlite3.connect('artistas.db')
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        
        query = f"SELECT * FROM artistas ORDER BY {clausula_sql}"
        cursor.execute(query)
        artistas = cursor.fetchall()
        conexion.close()

        return render.index(artistas=artistas, query_usada=query)

    def POST(self):
        datos = web.input()
        
        conexion = sqlite3.connect('artistas.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO artistas (nombre, pais, genero, streams_anuales, ano_debut, premios_grammy, puesto_ranking)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos.nombre,
            datos.pais,
            datos.genero,
            int(datos.streams_anuales),
            int(datos.ano_debut),
            int(datos.premios_grammy),
            int(datos.puesto_ranking)
        ))
        conexion.commit()
        conexion.close()

        return self.GET()

# Nueva clase para eliminar artistas
class Borrar:
    def GET(self, id_artista):
        conexion = sqlite3.connect('artistas.db')
        cursor = conexion.cursor()
        # Borra al artista por su ID
        cursor.execute('DELETE FROM artistas WHERE id = ?', (id_artista,))
        conexion.commit()
        conexion.close()
        
        # Recargamos la vista principal sin romper la URL de Codespaces
        return Index().GET()

if __name__ == "__main__":
    app.run()