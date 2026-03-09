# Sliding Puzzle — BFS-IDA* con horizonte limitado

Resolución del puzzle deslizante (N×N) mediante búsqueda BFS-IDA* con horizonte limitado. Incluye generación de tableros aleatorios, resolución por lotes y visualización de resultados.

## Requisitos

- **Python 3.9 o superior** (por el uso de anotaciones de tipo como `dict[str, Node]`).

## Estructura del proyecto

```
try/
├── board.py          # Tablero y operaciones
├── board_io.py       # Lectura/escritura de tableros en archivo
├── constants.py      # Pesos y cotas de la función de evaluación
├── evaluator.py      # Heurísticas (g, h1..h5) y evaluación
├── factory.py        # Generación de tableros (ordenado, aleatorio)
├── node.py           # Nodos y listas para la búsqueda
├── sli_puzz.py       # Algoritmo BFS-IDA*
├── test/
│   ├── boards/       # Archivos de tableros generados (entrada)
│   ├── results/      # Archivos de soluciones (salida)
│   ├── generate_boards_script.py
│   └── resolve_boards_script.py
├── data_vision.ipynb # Visualización de métricas
└── pseudocode.txt    # Pseudocódigo del algoritmo
```

---

## 1. Generación de tableros

Genera archivos de tableros aleatorios en `test/boards/`. Cada archivo contiene una dimensión y una lista de tableros (estados iniciales), generados aplicando un número fijo de movimientos aleatorios desde el estado meta.

**Desde la raíz del proyecto (`try/`):**

```bash
python test/generate_boards_script.py
```

- Crea la carpeta `test/boards/` si no existe.
- Para cada **dimensión** 3, 4, 5, 6, 7, 8 y cada **dificultad** (random steps) 20, 30, 50, genera un archivo con **100 tableros**.
- Nombre del archivo: `b_{dim}x{dim}_100boards_{steps}random_steps.txt`  
  Ejemplo: `b_3x3_100boards_20random_steps.txt`.

**Formato de cada archivo generado:**

- Primera línea: dimensión `n`.
- A continuación: `n` líneas por tablero (números separados por comas, del 0 a n²−1; 0 = hueco).

Para cambiar dimensiones, dificultades o cantidad de tableros, edita `test/generate_boards_script.py` (bucles `DIMENSION`, `RANDOM_STEPS`, `BOARDS_COUNT`).

---

## 2. Resolución de tableros generados

Resuelve todos los archivos `.txt` de `test/boards/` y escribe las soluciones en `test/results/` con el mismo nombre de archivo.

**Desde la raíz del proyecto (`try/`):**

```bash
python test/resolve_boards_script.py
```

- Lee cada archivo en `test/boards/`.
- Para cada tablero del archivo, ejecuta el solver (BFS-IDA*) hacia el estado meta estándar (1,2,…,n²−1,0).
- Escribe en `test/results/` un archivo por archivo de entrada con:
  - **Cabecera:** dimensión, random steps, boards count, listas de tiempos y pasos de solución, medias, etc. Los tableros no resueltos se registran con `-1` en tiempo y en pasos.
  - **Por cada tablero:** estado inicial, tiempo (ms), pasos de solución y secuencia de movimientos (U/D/L/R) del hueco.

En consola se muestra, por cada tablero resuelto, el tablero inicial, el número de pasos y el nombre del archivo de salida. Los no resueltos o con error de memoria también se indican.

**Requisito:** tener ya generados los archivos en `test/boards/` (paso 1). El script crea `test/results/` si no existe.

---

## Resumen del flujo

1. **Generar tableros:**  
   `python test/generate_boards_script.py`  
   → se llenan `test/boards/*.txt`.

2. **Resolver todos:**  
   `python test/resolve_boards_script.py`  
   → se generan `test/results/*.txt` con soluciones y métricas.

3. **Visualizar:** abrir `data_vision.ipynb`, ejecutar la celda de extracción de datos y las celdas de gráficas (medias, dispersión, accuracy, % fallos). Ejecutar el notebook desde la raíz del proyecto para que encuentre `test/results/`.

---

## Un solo puzzle (tablero inicial + meta en un archivo)

Si tienes un archivo con **un** tablero inicial y **un** tablero meta (formato: primera línea = dimensión, siguientes n líneas = inicial, siguientes n líneas = meta, números separados por comas, 0 = hueco), puedes usar la función de `board_io`:

- `load_boards_from_file(ruta)` devuelve `(dimensión, tablero_inicial, tablero_meta)`.

Integrar la resolución con `sli_puzz.bfs_puzzle()` y los `Constants` correspondientes a esa dimensión (como en `resolve_boards_script.py`) para obtener la secuencia de tableros o de movimientos.
