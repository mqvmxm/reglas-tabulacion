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

    # Solo 4 artistas base
    artistas_data = [
        ('Taylor Swift', 'Estados Unidos', 'Pop', 20000, 2006, 14, 1),
        ('Bad Bunny', 'Puerto Rico', 'Reguetón', 15000, 2016, 3, 1),
        ('Michael Jackson', 'Estados Unidos', 'Pop', 12000, 1971, 13, 1),
        ('SADE', 'Reino Unido', 'R&B', 5000, 1984, 4, 3)
    ]

    cursor.executemany('''
    INSERT INTO artistas (nombre, pais, genero, streams_anuales, ano_debut, premios_grammy, puesto_ranking)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', artistas_data)

    conexion.commit()
    conexion.close()
    print("Base de datos creada con 4 artistas iniciales.")

if __name__ == '__main__':
    crear_bd()