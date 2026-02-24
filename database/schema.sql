CREATE TABLE IF NOT EXISTS alumno (
    ALUMNO_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE TEXT NOT NULL,
    APELLIDOS TEXT NOT NULL,
    FECHA_NACIMIENTO TEXT NULL,
    EMAIL TEXT NULL,

    CHECK (LENGTH(TRIM(NOMBRE))>0),
    CHECK (LENGTH(TRIM(NOMBRE))>0),
    CHECK (EMAIL IS NULL OR instr(EMAIL,'@')>1)

);
CREATE INDEX IF NOT EXISTS idx_alumno_apellidos_nombre
ON alumno (apellidos, nombre);

create table if not exists profesor(
    profesor_id integer primary key autoincrement,
    nombre text not null,
    apellidos text not null,
    departamento text not null,
    email text null,

    check (length(trim(nombre))>0),
    check (length(trim(apellidos))>0),
    check (length(trim(departamento))>0),
    check (email is null or instr(email,'@')>1)
);
CREATE INDEX IF NOT EXISTS idx_profesor_apellidos_nombre
ON profesor (apellidos, nombre);



CREATE TABLE IF NOT EXISTS direccion (
    direccion_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id     INTEGER NOT NULL,
    cargo           TEXT    NOT NULL,


    UNIQUE (profesor_id),

    CHECK (length(trim(cargo)) > 0),
    CHECK (
        lower(trim(cargo)) IN (
            'director',
            'jefe de estudios',
            'secretario'
        )
    ),


    FOREIGN KEY (profesor_id) REFERENCES profesor(profesor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


CREATE INDEX IF NOT EXISTS idx_direccion_cargo
ON direccion (cargo);





CREATE TABLE IF NOT EXISTS aula (
    aula_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT    NOT NULL,
    capacidad   INTEGER NOT NULL,

    CHECK (length(trim(codigo)) > 0),

    CHECK (capacidad > 0),

    UNIQUE (codigo)
);



CREATE TABLE IF NOT EXISTS material (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    aula_id     INTEGER NOT NULL,
    nombre      TEXT    NOT NULL,
    descripcion TEXT    NULL,


    CHECK (length(trim(nombre)) > 0),

    FOREIGN KEY (aula_id) REFERENCES aula(aula_id)
        ON UPDATE CASCADE
        ON DELETE cascade
);

CREATE INDEX IF NOT EXISTS idx_material_aula
ON material (aula_id);




CREATE TABLE IF NOT EXISTS asignatura (
    asignatura_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre         TEXT    NOT NULL,
    departamento   TEXT    NOT NULL,

    CHECK (length(trim(nombre)) > 0),
    CHECK (length(trim(departamento)) > 0),

    UNIQUE (nombre)
);

CREATE INDEX IF NOT EXISTS idx_asignatura_nombre
ON asignatura (nombre);





CREATE TABLE IF NOT EXISTS clase (
    clase_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id     INTEGER NOT NULL,
    asignatura_id   INTEGER NOT NULL,
    aula_id         INTEGER NOT NULL,
    anio_academico  TEXT    NOT NULL,

    CHECK (length(trim(anio_academico)) > 0),

    UNIQUE (profesor_id, asignatura_id, aula_id, anio_academico),

    FOREIGN KEY (profesor_id) REFERENCES profesor(profesor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (asignatura_id) REFERENCES asignatura(asignatura_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (aula_id) REFERENCES aula(aula_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_clase_anio
ON clase (anio_academico);

CREATE INDEX IF NOT EXISTS idx_clase_asignatura
ON clase (asignatura_id);




CREATE TABLE IF NOT EXISTS clase_alumno (
    clase_alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clase_id        INTEGER NOT NULL,
    alumno_id       INTEGER NOT NULL,

    UNIQUE (clase_id, alumno_id),

    FOREIGN KEY (clase_id) REFERENCES clase(clase_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (alumno_id) REFERENCES alumno(alumno_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_clase_alumno_clase
ON clase_alumno (clase_id);

CREATE INDEX IF NOT EXISTS idx_clase_alumno_alumno
ON clase_alumno (alumno_id);




CREATE TABLE IF NOT EXISTS matricula (
    matricula_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id      INTEGER NOT NULL,
    anio_academico TEXT    NOT NULL,

    CHECK (length(trim(anio_academico)) > 0),

    UNIQUE (alumno_id, anio_academico),

    FOREIGN KEY (alumno_id) REFERENCES alumno(alumno_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_matricula_anio
ON matricula (anio_academico);

CREATE INDEX IF NOT EXISTS idx_matricula_alumno
ON matricula (alumno_id);




CREATE TABLE IF NOT EXISTS convocatoria (
    convocatoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL,

    CHECK (length(trim(nombre)) > 0),

    UNIQUE (nombre)
);

CREATE INDEX IF NOT EXISTS idx_convocatoria_nombre
ON convocatoria (nombre);




CREATE TABLE IF NOT EXISTS calificacion (
    calificacion_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id        INTEGER NOT NULL,
    clase_id         INTEGER NOT NULL,
    convocatoria_id  INTEGER NOT NULL,
    nota             REAL    NOT NULL,

    CHECK (nota >= 0 AND nota <= 10),

    UNIQUE (alumno_id, clase_id, convocatoria_id),

    FOREIGN KEY (alumno_id) REFERENCES alumno(alumno_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (clase_id) REFERENCES clase(clase_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (convocatoria_id) REFERENCES convocatoria(convocatoria_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_calificacion_alumno
ON calificacion (alumno_id);

CREATE INDEX IF NOT EXISTS idx_calificacion_clase
ON calificacion (clase_id);

CREATE INDEX IF NOT EXISTS idx_calificacion_convocatoria
ON calificacion (convocatoria_id);







