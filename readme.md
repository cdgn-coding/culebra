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

## Características Principales

### **Tipos Primitivos**

- **Booleanos**: `true`, `false`
- **Enteros**: `123`, `-45`
- **Flotantes**: `3.14`, `-0.56`
- **Cadenas de texto**: `"Hola, mundo!"`, `"""Texto multilínea"""`

### **Tipos Incluidos**

1. **Array**: Lista ordenada de elementos.

   ```python
   numeros = [1, 2, 3]
   ```

2. **Map**: Colección clave-valor.

   ```python
   usuario = {"nombre": "Carlos", "edad": 25}
   ```

3. **Set**: Conjunto de elementos únicos.

   ```python
   numeros_unicos = {1, 2, 3, 3}
   ```

4. **Queue**: Cola para manejo FIFO.

   ```python
   cola = queue()
   cola.enqueue(10)
   valor = cola.dequeue()
   ```

5. **Stack**: Pila para manejo LIFO.

   ```python
   pila = stack()
   pila.push(20)
   valor = pila.pop()
   ```

6. **Priority Queue**: Cola con prioridad.

   ```python
   pq = priority_queue()
   pq.insert(5, priority=1)
   mayor = pq.remove()
   ```

### **Estructuras de Control**

#### **Condicional**

```python
if x > 10:
    print("x es mayor que 10")
elif x == 10:
    print("x es igual a 10")
else:
    print("x es menor que 10")
```

#### **Ciclo for con (declaración, condición y expresión)**

```python
for i = 0; i < 10; i = i + 1:
    print(i)
```

#### **Ciclo for con (condición)**

```python
while x > 0:
    print(x)
    x = x - 1
```

### **Variables**

```python
x = 10
y = "Hola"
z = 3.14
activo = true
```

### **Funciones**

#### **Definición**

```python
def suma(a, b):
    return a + b
```

#### **Llamado**

```python
resultado = suma(5, 7)
```

## Filosofía de Diseño

1. **Simplicidad**: Apuntar a una curva de aprendizaje baja y a tener una sóla forma de hacer las cosas, la correcta.

2. **Estructuras Integradas**: Arrays, mapas, pilas, colas y más para evitar dependencias externas.

3. **Extensibilidad**: Posibilidad de modificar el lenguaje para soportar dominios específicos.

## Ejemplo Completo

```python
# Programa ejemplo
numeros = [1, 2, 3, 4, 5]
suma_total = 0

for i = 0; i < len(numeros); i = i + 1:
    suma_total = suma_total + numeros[i]

if suma_total > 10:
    print("La suma es mayor que 10")
else:
    print("La suma es menor o igual a 10")

def cuadrado(x):
    return x * x

print(cuadrado(5))
```

## Filosofía de Diseño

1. **Simplicidad**: Enfocado en una curva de aprendizaje suave y en tener una única forma correcta de hacer las cosas.

2. **Estructuras Integradas**: Arrays, mapas, pilas, colas y más incluidos en el lenguaje para evitar dependencias externas.

3. **Extensibilidad**: Capacidad de adaptar el lenguaje para soportar dominios específicos.

