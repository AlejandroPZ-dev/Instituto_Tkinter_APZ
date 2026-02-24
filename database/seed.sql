-- -----------------------------------------
-- Convocatorias
-- -----------------------------------------
INSERT INTO convocatoria (nombre) VALUES
('1ª Evaluación'),
('2ª Evaluación'),
('Final'),
('Extraordinaria');

-- -----------------------------------------
-- Aulas
-- -----------------------------------------
INSERT INTO aula (codigo, capacidad) VALUES
('A101', 30),
('B202', 25);

-- -----------------------------------------
-- Asignaturas
-- -----------------------------------------
INSERT INTO asignatura (nombre, departamento) VALUES
('Matemáticas', 'Ciencias'),
('Lengua Castellana', 'Lengua');

-- -----------------------------------------
-- Profesores
-- -----------------------------------------
INSERT INTO profesor (nombre, apellidos, departamento, email) VALUES
('Ana', 'López García', 'Ciencias', 'ana.lopez@instituto.es'),
('Carlos', 'Pérez Martín', 'Lengua', 'carlos.perez@instituto.es');

-- -----------------------------------------
-- Dirección
-- -----------------------------------------
-- Ana López es directora
INSERT INTO direccion (profesor_id, cargo)
VALUES (1, 'director');

-- -----------------------------------------
-- Alumnos
-- -----------------------------------------
INSERT INTO alumno (nombre, apellidos, fecha_nacimiento, email) VALUES
('Juan', 'Martín Ruiz', '2008-03-15', 'juan.martin@gmail.com'),
('Lucía', 'Sánchez Gómez', '2007-11-02', 'lucia.sanchez@gmail.com'),
('Pedro', 'Fernández Díaz', '2008-07-21', NULL);

-- -----------------------------------------
-- Matrículas (año académico)
-- -----------------------------------------
INSERT INTO matricula (alumno_id, anio_academico) VALUES
(1, '2025-2026'),
(2, '2025-2026'),
(3, '2025-2026');

-- -----------------------------------------
-- Clases
-- -----------------------------------------
-- Matemáticas con Ana en A101
INSERT INTO clase (profesor_id, asignatura_id, aula_id, anio_academico)
VALUES (1, 1, 1, '2025-2026');

-- Lengua con Carlos en B202
INSERT INTO clase (profesor_id, asignatura_id, aula_id, anio_academico)
VALUES (2, 2, 2, '2025-2026');

-- -----------------------------------------
-- Alumnos en clases
-- -----------------------------------------
-- Clase 1 (Matemáticas)
INSERT INTO clase_alumno (clase_id, alumno_id) VALUES
(1, 1),
(1, 2);

-- Clase 2 (Lengua)
INSERT INTO clase_alumno (clase_id, alumno_id) VALUES
(2, 2),
(2, 3);

-- -----------------------------------------
-- Materiales
-- -----------------------------------------
INSERT INTO material (aula_id, nombre, descripcion) VALUES
(1, 'Proyector', 'Proyector Epson HD'),
(1, 'Pizarra digital', 'Pizarra interactiva'),
(2, 'Ordenador', 'PC del aula');

-- -----------------------------------------
-- Calificaciones
-- -----------------------------------------
-- Juan y Lucía en Matemáticas (1ª Evaluación)
INSERT INTO calificacion (alumno_id, clase_id, convocatoria_id, nota) VALUES
(1, 1, 1, 7.5),
(2, 1, 1, 8.0);

-- Lucía y Pedro en Lengua (1ª Evaluación)
INSERT INTO calificacion (alumno_id, clase_id, convocatoria_id, nota) VALUES
(2, 2, 1, 6.5),
(3, 2, 1, 7.0);
