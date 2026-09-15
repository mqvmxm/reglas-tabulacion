import sqlite3


def crear_bd():
    conexion = sqlite3.connect('artistas.db')
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais TEXT NOT NULL,
        genero TEXT NOT NULL,
        streams_anuales INTEGER NOT NULL,
        ano_debut INTEGER NOT NULL,
        premios_grammy INTEGER NOT NULL,
        puesto_ranking INTEGER NOT NULL
    )
    ''')

    cursor.execute('DELETE FROM artistas')
    # Reiniciamos el contador de IDs para que empiecen en 1
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'artistas'")

    # -----------------------------------------------------------
    # Artistas disenados para que cada regla se active en algun punto.
    # (nombre, pais, genero, streams, debut, grammys, ranking)
    # -----------------------------------------------------------
    artistas_data = [
        # Regla 1: gana solo por tener mas streams que todos
        ('Taylor Swift',    'Estados Unidos', 'Pop',       20000, 2006, 14, 1),

        # Regla 2: empatan en streams, decide quien tiene mas Grammys
        ('Bad Bunny',       'Puerto Rico',    'Reggaeton', 15000, 2016,  3, 1),
        ('Beyonce',         'Estados Unidos', 'R&B',       15000, 1997, 32, 2),

        # Regla 3: empatan en streams y Grammys, decide el nombre (alfabetico)
        ('Adele',           'Reino Unido',    'Pop',       12000, 2008, 16, 4),
        ('Ed Sheeran',      'Reino Unido',    'Pop',       12000, 2011, 16, 5),

        # Regla 4: empatan hasta el nombre, decide el debut mas antiguo
        ('Grupo Nova',      'Colombia',       'Cumbia',    10000, 2010,  5, 6),
        ('Grupo Nova',      'Colombia',       'Cumbia',    10000, 2018,  5, 6),

        # Regla 5: empatan hasta el debut, decide el pais (alfabetico)
        ('Grupo Sol',       'Argentina',      'Folk',       8000, 2012,  2, 7),
        ('Grupo Sol',       'Brasil',         'Folk',       8000, 2012,  2, 7),

        # Regla 6: empatan hasta el pais, decide el genero (alfabetico)
        ('Grupo Luna',      'Chile',          'Cumbia',     6000, 2014,  1, 9),
        ('Grupo Luna',      'Chile',          'Folk',       6000, 2014,  1, 9),

        # Regla 7: empatan hasta el genero, decide el mejor puesto de ranking
        ('Grupo Mar',       'Peru',           'Pop',        4000, 2013,  0, 11),
        ('Grupo Mar',       'Peru',           'Pop',        4000, 2013,  0, 15),

        # Regla 8: empatan en absolutamente todo, decide el orden de ingreso (id)
        ('Grupo Cielo',     'Mexico',         'Rock',       2000, 2015,  0, 20),
        ('Grupo Cielo',     'Mexico',         'Rock',       2000, 2015,  0, 20),
    ]

    cursor.executemany('''
    INSERT INTO artistas
        (nombre, pais, genero, streams_anuales, ano_debut, premios_grammy, puesto_ranking)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', artistas_data)

    conexion.commit()
    conexion.close()

    print(f"Base de datos creada con {len(artistas_data)} artistas.")
    print("Cada par de artistas demuestra una regla distinta de la cascada.")


if __name__ == '__main__':
    crear_bd()