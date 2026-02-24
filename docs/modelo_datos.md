
# 📘 Modelo de Datos – Aplicación Instituto (Tkinter)

## 1. Introducción

Este documento describe el **modelo de datos** de la aplicación de gestión de un instituto educativo.
El diseño se ha realizado siguiendo criterios de **normalización en Tercera Forma Normal (3FN)** y cumpliendo las restricciones funcionales indicadas en el enunciado del proyecto.

El modelo permite:

* Gestionar alumnado, profesorado y equipo directivo
* Organizar aulas, materiales y asignaturas
* Crear clases por curso académico
* Gestionar matrículas anuales
* Registrar calificaciones por convocatoria
* Exportar calificaciones por materia

---

## 2. Entidades principales

### 2.1 Alumno

Representa a un alumno del instituto.

**Campos principales:**

* `id` (PK)
* `nombre`
* `apellidos`
* `fecha_nacimiento`
* `email` (opcional)

**Observaciones:**

* Un alumno puede tener **varias matrículas**, pero **solo una por año académico**.
* Un alumno puede pertenecer a **varias clases**.

---

### 2.2 Profesor

Representa al profesorado del centro.

**Campos principales:**

* `id` (PK)
* `nombre`
* `apellidos`
* `departamento`

**Observaciones:**

* Un profesor puede impartir **varias clases**.
* Parte del profesorado puede pertenecer al equipo directivo.

---

### 2.3 Dirección

Representa a los miembros del equipo directivo.

**Campos principales:**

* `id` (PK)
* `profesor_id` (FK → Profesor)
* `cargo` (director, jefe de estudios, secretario)

**Observaciones:**

* Se modela como entidad separada para no duplicar datos del profesor.
* Un profesor puede o no formar parte de la dirección.
* En este proyecto se ha considerado que los miembros del equipo directivo
forman parte del profesorado, por lo que la entidad Dirección se modela como
una especialización de Profesor mediante una clave foránea.

---

### 2.4 Aula

Representa un aula física del instituto.

**Campos principales:**

* `id` (PK)
* `codigo` (ej. A101)
* `capacidad`

**Observaciones:**

* Un aula puede tener **varios materiales**.
* Un aula puede asignarse a **varias clases** en distintos cursos académicos.

---

### 2.5 Material

Representa material asignado a un aula.

**Campos principales:**

* `id` (PK)
* `nombre`
* `descripcion`
* `aula_id` (FK → Aula)

**Observaciones:**

* Cada material pertenece a **un único aula**.
* Los materiales pueden importarse desde un archivo externo.

---

### 2.6 Asignatura

Representa una materia impartida en el centro.

**Campos principales:**

* `id` (PK)
* `nombre`
* `departamento`

**Observaciones:**

* Una asignatura puede impartirse en **varias clases**.
* No se duplican asignaturas por curso académico.

---

### 2.7 Clase

Representa una clase concreta en un año académico.

**Campos principales:**

* `id` (PK)
* `profesor_id` (FK → Profesor)
* `asignatura_id` (FK → Asignatura)
* `aula_id` (FK → Aula)
* `anio_academico`

**Observaciones:**

* Una clase está asociada a **un profesor, una asignatura y un aula**.
* Una clase tiene **un número indeterminado de alumnos**.
* Un alumno puede pertenecer a **varias clases** → relación N:M.

---

### 2.8 Clase_Alumno (tabla intermedia)

Tabla de relación **muchos a muchos** entre alumnos y clases.

**Campos principales:**

* `id` (PK)
* `clase_id` (FK → Clase)
* `alumno_id` (FK → Alumno)

**Restricciones:**

* `UNIQUE(clase_id, alumno_id)`

---

### 2.9 Matrícula

Representa la matrícula anual de un alumno.

**Campos principales:**

* `id` (PK)
* `alumno_id` (FK → Alumno)
* `anio_academico`

**Restricciones importantes:**

* Un alumno **solo puede tener una matrícula por año**
  → `UNIQUE(alumno_id, anio_academico)`

---

### 2.10 Convocatoria

Representa una convocatoria de evaluación.

**Campos principales:**

* `id` (PK)
* `nombre`
  (Ej.: 1ª Evaluación, 2ª Evaluación, Final, Extraordinaria)

**Observaciones:**

* Se separa como entidad para evitar valores repetidos y asegurar 3FN.

---

### 2.11 Calificación

Representa la calificación obtenida por un alumno.

**Campos principales:**

* `id` (PK)
* `alumno_id` (FK → Alumno)
* `clase_id` (FK → Clase)
* `convocatoria_id` (FK → Convocatoria)
* `nota`

**Restricciones importantes:**

* Un alumno **solo puede tener una calificación por convocatoria y clase**
  → `UNIQUE(alumno_id, clase_id, convocatoria_id)`

---

## 3. Relaciones entre entidades

* Alumno 1:N Matrícula
* Alumno N:M Clase (mediante Clase_Alumno)
* Profesor 1:N Clase
* Asignatura 1:N Clase
* Aula 1:N Material
* Clase 1:N Calificación
* Convocatoria 1:N Calificación

---

## 4. Normalización (3FN)

El modelo cumple 3FN porque:

* No existen campos multivaluados
* No hay dependencias parciales
* No hay dependencias transitivas
* Las entidades independientes (Convocatoria, Asignatura, Aula) no se duplican como texto en otras tablas

---

## 5. Observaciones finales

Este modelo:

* Cumple todas las restricciones del enunciado
* Es escalable (permite nuevos cursos, materias y convocatorias)
* Facilita la exportación de calificaciones por materia
* Se integra fácilmente con una arquitectura MVC en Python

---
