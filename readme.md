# Lenguaje de Programación CULEBRA

```
      /^\/^\
    _|__|  O|
\/     /~   \_/ \
 \____|__________/  \
        \_______      \
                `\     \                 \
                  |     |                  \
                 /      /                    \
                /     /                       \\
              /      /                         \ \
             /     /                            \  \
           /     /             _----_            \   \
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~
```

Este lenguaje minimalista inspirado en Python y Go está diseñado para ser sencillo pero poderoso, con características modernas y estructuras de datos integradas.

## Estado Actual de Implementación

### Características Implementadas ✓
- [x] Expresiones Básicas
  - [x] Expresiones aritméticas (`+`, `-`, `*`, `/`)
  - [x] Expresiones de comparación (`>`, `<`, `>=`, `<=`, `==`, `!=`)
  - [x] Expresiones lógicas (`and`, `or`)
  - [x] Expresiones unarias (negativo `-`, `not`)
  - [x] Expresiones con paréntesis

- [x] Tipos Primitivos
  - [x] Números enteros
  - [x] Cadenas de texto
  - [x] Booleanos
  - [x] Números decimales

- [x] Variables
  - [x] Referencias a identificadores
  - [x] Asignaciones

### Características Pendientes ⏳
- [ ] Estructuras de Control
  - [ ] Condicionales (`if`, `elif`, `else`)
  - [ ] Bucles `while`
  - [ ] Bucles `for`

- [ ] Funciones
  - [ ] Definición de funciones
  - [ ] Llamadas a funciones
  - [ ] Sentencias `return`

- [ ] Estructuras de Datos Complejas
  - [ ] Arrays (`[...]`)
  - [ ] Mapas (`{clave: valor, ...}`)
  - [ ] Conjuntos (`{elemento, ...}`)

- [ ] Otras Características
  - [ ] Manejo de bloques (INDENT/DEDENT)
  - [ ] Valor nulo

- [ ] Manejo de Errores
  - [ ] Mejor reporte de errores
  - [ ] Recuperación de errores de análisis


- [ ] Interprete
  - [ ] Tree-walk interpreter
  - [ ] LLVM Just-in-time compiler
  - [ ] LLVM AOT compiler

## Características del Lenguaje

### Tipos Primitivos

- **Booleanos**: `true`, `false`
- **Enteros**: `123`, `-45`
- **Decimales**: `3.14`, `-0.56`
- **Cadenas de texto**: `"Hola, mundo!"`, `"""Texto multilínea"""`

### Estructuras de Datos Integradas

1. **Array**: Lista ordenada de elementos.
   ```python
   numeros = [1, 2, 3]
   ```

2. **Mapa**: Colección clave-valor.
   ```python
   usuario = {"nombre": "Carlos", "edad": 25}
   ```

3. **Conjunto**: Colección de elementos únicos.
   ```python
   numeros_unicos = {1, 2, 3, 3}  # Resultado: {1, 2, 3}
   ```

4. **Cola**: Estructura FIFO (primero en entrar, primero en salir).
   ```python
   cola = cola()
   cola.agregar(10)
   valor = cola.quitar()
   ```

5. **Pila**: Estructura LIFO (último en entrar, primero en salir).
   ```python
   pila = pila()
   pila.apilar(20)
   valor = pila.desapilar()
   ```

6. **Cola con Prioridad**: Cola ordenada por prioridad.
   ```python
   cp = cola_prioridad()
   cp.insertar(5, prioridad=1)
   mayor = cp.quitar()
   ```

### Estructuras de Control

#### Condicionales
```python
if x > 10:
    imprimir("x es mayor que 10")
elif x == 10:
    imprimir("x es igual a 10")
else:
    imprimir("x es menor que 10")
```

#### Bucle for (con declaración, condición y expresión)
```python
for i = 0; i < 10; i = i + 1:
    imprimir(i)
```

#### Bucle while
```python
while x > 0:
    imprimir(x)
    x = x - 1
```

### Variables y Funciones

```python
# Variables
x = 10
y = "Hola"
z = 3.14
activo = true

# Funciones
def suma(a, b):
    return a + b

resultado = suma(5, 7)
```

## Ejemplo Completo

```python
# Programa de ejemplo
numeros = [1, 2, 3, 4, 5]
suma_total = 0

for i = 0; i < longitud(numeros); i = i + 1:
    suma_total = suma_total + numeros[i]

if suma_total > 10:
    imprimir("La suma es mayor que 10")
else:
    imprimir("La suma es menor o igual a 10")

def cuadrado(x):
    return x * x

imprimir(cuadrado(5))
```

## Filosofía de Diseño

1. **Simplicidad**: Enfocado en una curva de aprendizaje suave y en tener una única forma correcta de hacer las cosas.

2. **Estructuras Integradas**: Arrays, mapas, pilas, colas y más incluidos en el lenguaje para evitar dependencias externas.

3. **Extensibilidad**: Capacidad de adaptar el lenguaje para soportar dominios específicos.

