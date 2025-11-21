        CREATE TABLE MASCOTA (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(50),
        edad INTEGER,
        especie VARCHAR(20),
        historial_medico TEXT,
        dueño_id INTEGER,
        FOREIGN KEY (dueño_id) REFERENCES dueño(id)
        )
    
        CREATE TABLE DUEÑO (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(50),
        apellido VARCHAR(50),
        edad INTEGER,
        rut VARCHAR(10),
        direccion VARCHAR(100),
        comuna VARCHAR(30)
        )
    
        CREATE TABLE PERRO (
        id INTERGER PRIMARY KEY,
        mascota_id INTEGER,
        raza VARCHAR(30)
        )

        CREATE TABLE GATO (
        id INTERGER PRIMARY KEY,
        mascota_id INTEGER,
        raza VARCHAR(20)
        )

        CREATE TABLE AVE (
        id INTERGER PRIMARY KEY,
        mascota_id INTEGER,
        especie VARCHAR(20)
        )