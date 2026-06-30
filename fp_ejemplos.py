# ============================================================
# PROGRAMACIÓN FUNCIONAL EN PYTHON
# Teoría, ejemplos y comparaciones con JavaScript
# ============================================================

# ============================================================
# 1. DATOS INMUTABLES
# ============================================================
"""
En programación funcional los datos NO deben modificarse una vez creados.
En JavaScript necesitas Object.freeze() para lograr esto, porque const solo
evita la reasignación de la variable, no la mutación del objeto:

    const arr = [1, 2, 3];
    arr.push(4);  // Esto SÍ funciona aunque sea const

Python en cambio trae estructuras inherentemente inmutables de serie.
La regla general es: si no necesitas mutarlo, usa la versión inmutable.
"""

# --- tuple: la hermana inmutable de list ---
# Se comporta como una lista pero no se puede modificar después de creada.
# Soporta indexing, slicing, len(), etc. —todo lo que no sea mutación.

lista_mutable = [1, 2, 3]
lista_mutable.append(4)          # Válido: [1, 2, 3, 4]

tupla_inmutable = (1, 2, 3)
# tupla_inmutable.append(4)      # Error: tuple no tiene append
# del tupla_inmutable[0]         # Error: no soporta borrado

# ¿Cómo "cambiar" algo inmutable? Creando una copia modificada:
nueva_tupla = tupla_inmutable + (4,)  # (1, 2, 3, 4)
# La original sigue intacta.

# --- frozenset: la versión congelada de set ---
# Un set normal permite agregar y quitar elementos.
# frozenset es exactamente igual pero no se puede modificar.

conjunto_mutable = {1, 2, 3}
conjunto_mutable.add(4)

conjunto_congelado = frozenset([1, 2, 3])
# conjunto_congelado.add(4)      # Error: frozenset es inmutable

# Sirve cuando necesitas usar un conjunto como clave de diccionario
# o dentro de otro conjunto (los sets mutables no son hashable).

# --- NamedTuple: tupla con nombres ---
# Es una tupla donde cada posición tiene un nombre.
# Útil para modelar datos simples sin escribir una clase completa.

from typing import NamedTuple

class Punto(NamedTuple):
    x: float
    y: float

p = Punto(3.0, 4.0)
print(p.x)       # 3.0
print(p[0])      # 3.0  (sigue siendo una tupla, funciona indexación)
# p.x = 5.0      # Error: es inmutable

# --- dataclass con frozen=True ---
# Si necesitas más flexibilidad que NamedTuple (métodos, defaults complejos),
# usa dataclass con frozen=True. Logra exactamente el mismo efecto.

from dataclasses import dataclass

@dataclass(frozen=True)
class Persona:
    nombre: str
    edad: int

persona = Persona("Ana", 30)

# Para "actualizar" un campo, creas una nueva instancia:
persona_mayor = Persona(nombre=persona.nombre, edad=persona.edad + 1)
print(persona_mayor)  # Persona(nombre='Ana', edad=31)
# persona.edad = 31  # Error: no se puede modificar


# ============================================================
# 2. FUNCIONES PURAS Y DE ORDEN SUPERIOR
# ============================================================
"""
FUNCIÓN PURA: misma entrada -> misma salida, sin efectos secundarios.
No modifica variables globales, no escribe archivos, no muta argumentos.

BENEFICIOS:
  - Predecibles y fáciles de testear
  - Se pueden cachear (memoización)
  - Son seguras en paralelismo

FUNCIÓN DE ORDEN SUPERIOR: trata funciones como ciudadanos de primera clase.
    - Recibe funciones como argumento (callback)
    - Retorna funciones como resultado (closure)

En JS:  const suma = (a, b) => a + b;
En Python:  suma = lambda a, b: a + b
La lambda solo puede contener UNA expresión, ni más de una línea.
"""

# --- Función pura ---
# Depende solo de sus parámetros, no toca nada externo.

def sumar(a: int, b: int) -> int:
    return a + b

# --- Función impura (para contrastar) ---
total = 0
def sumar_impuro(valor):
    global total
    total += valor      # Efecto secundario: modifica estado global
    return total

sumar_impuro(5)   # Devuelve 5
sumar_impuro(5)   # Devuelve 10  (misma entrada, distinta salida)

"""
La función pura sumar(5, 3) siempre dará 8, sin importar cuándo
o desde dónde se llame. sumar_impuro con el mismo argumento da
resultados distintos según el estado. Esa es la diferencia clave.
"""

# --- Orden superior: pasar función como argumento ---

def aplicar_operacion(func, x, y):
    """Recibe una función y dos valores, aplica la función."""
    return func(x, y)

resultado = aplicar_operacion(sumar, 10, 5)
print(resultado)  # 15

# También podemos pasar una lambda directamente:
resultado2 = aplicar_operacion(lambda a, b: a * b, 4, 5)
print(resultado2)  # 20

# --- Orden superior: retornar función ---
# Esto se llama "closure" o clausura.

def crear_multiplicador(factor):
    def multiplicar(valor):
        return valor * factor
    return multiplicar

por_tres = crear_multiplicador(3)
print(por_tres(7))       # 21
print(por_tres(10))      # 30

"""
Explicación: crear_multiplicador retorna la función interna 'multiplicar'
que "recuerda" el factor aunque ya hayamos salido de la función externa.
"""


# ============================================================
# 3. CURRIFFICACIÓN Y COMPOSICIÓN
# ============================================================
"""
CURRIFFICACIÓN (Currying):
  Transformar una función de múltiples argumentos en una cadena de
  funciones que toman UN solo argumento cada una.

  En JS:  const suma = a => b => a + b
  En Python se logra con funciones anidadas o con functools.partial

COMPOSICIÓN:
  Encadenar funciones -> la salida de una es la entrada de la siguiente.
  f(g(h(x)))  o en notación de pipeline: x -> h -> g -> f
"""

# --- Currificación artesanal ---

def currificar_suma(a):
    def con_b(b):
        return a + b
    return con_b

suma_5 = currificar_suma(5)
print(suma_5(3))  # 8
print(suma_5(10)) # 15

# --- Currificación con partial (más práctico) ---

from functools import partial

def potencia(base, exponente):
    """Eleva base al exponente dado."""
    return base ** exponente

# partial "fija" un argumento y devuelve una función más pequeña
cuadrado = partial(potencia, exponente=2)
cubo     = partial(potencia, exponente=3)

print(cuadrado(4))  # 16
print(cubo(2))      # 8

"""
partial es la herramienta principal para currificación en Python.
Toma una función y algunos argumentos predefinidos y devuelve
una nueva función que solo espera los argumentos restantes.
"""

# --- Composición básica ---

def composicion(*funcs):
    """Toma N funciones y las compone en orden: primera a última."""
    def aplicar(x):
        resultado = x
        for f in funcs:
            resultado = f(resultado)
        return resultado
    return aplicar

# Definimos pequeñas funciones puras
doble      = lambda x: x * 2
incremento = lambda x: x + 1
elevar_cuad = lambda x: x ** 2

# Las componemos en un pipeline
pipeline = composicion(doble, incremento, elevar_cuad)

# 3 -> doble(3)=6 -> incremento(6)=7 -> 7^2=49
print(pipeline(3))  # 49

"""
La composición permite construir operaciones complejas juntando
operaciones simples y reutilizables. Es el equivalente funcional
de los pipes en Unix (|).
"""


# ============================================================
# 4. OPERADORES DE DESEMPAQUETADO (Spread)
# ============================================================
"""
En JS:  const nuevo = { ...original, clave: valor }
        const arr2 = [...arr1, 4, 5]

En Python se usa * para iterables (tuplas, listas) y ** para diccionarios.
"""

# --- Desempaquetado con * (tuplas / listas) ---

a = (1, 2, 3)
b = (4, 5, 6)

# Fusionar tuplas sin perder la original
combinado = (*a, *b)
print(combinado)  # (1, 2, 3, 4, 5, 6)
print(a)          # (1, 2, 3)  — intacta

# También funciona con listas:
lista_a = [1, 2]
lista_b = [3, 4]
fusion = [*lista_a, *lista_b, 5]
print(fusion)  # [1, 2, 3, 4, 5]

# --- Desempaquetado con ** (diccionarios) ---

original = {"x": 10, "y": 20}

# Clonar y extender en un solo paso
copia = {**original, "z": 30}
print(copia)             # {'x': 10, 'y': 20, 'z': 30}
print(original)          # {'x': 10, 'y': 20} — intacto

# "Actualizar" un valor de forma inmutable
actualizado = {**original, "x": 99}
print(actualizado)       # {'x': 99, 'y': 20}
print(original)          # {'x': 10, 'y': 20} — el original no cambió

"""
Esta técnica es fundamental en funcional porque evita mutar estructuras.
Cada "cambio" genera un nuevo objeto. Esto permite tracking de cambios,
undo/redo, y razonar sobre el estado con confianza.
"""


# ============================================================
# 5. TRANSFORMACIÓN DE COLECCIONES: map, filter, reduce
# ============================================================
"""
En lugar de usar ciclos for/while (imperativo), la FP usa tres operaciones:

  map(function, iterable)
      Aplica function a cada elemento, devuelve un iterable con los resultados.
      Es un FUNCTOR: transforma el contenido sin cambiar la estructura.

  filter(predicate, iterable)
      Retiene solo los elementos donde predicate(elemento) es True.

  reduce(function, iterable, initial)
      Acumula los elementos en un solo valor.
      Hay que importarlo de functools.

COMPARATIVA CON LIST COMPREHENSION:
  La comunidad Python prefiere comprehensions por ser más legibles.
  Pero map/filter/reduce son más explícitos en la INTENCIÓN:
    - ¿Vas a TRANSFORMAR? -> map
    - ¿Vas a FILTRAR?     -> filter
    - ¿Vas a ACUMULAR?    -> reduce
"""

from functools import reduce

datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# --- map: transformar cada elemento ---
# Versión funcional:
dobles = list(map(lambda x: x * 2, datos))
print(dobles)  # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Versión con list comprehension (más idiomática en Python):
assert [x * 2 for x in datos] == dobles

# --- filter: seleccionar según condición ---
pares = list(filter(lambda x: x % 2 == 0, datos))
print(pares)  # [2, 4, 6, 8, 10]

# List comprehension:
assert [x for x in datos if x % 2 == 0] == pares

# --- reduce: condensar a un valor ---
suma_total = reduce(lambda acc, x: acc + x, datos, 0)
print(suma_total)  # 55

# reduce(modelo) acepta tres argumentos:
#   1. Función de acumulación (acumulador, elemento_actual) -> nuevo_acumulador
#   2. Iterable a recorrer
#   3. Valor inicial (opcional, si se omite usa el primer elemento)

# Ejemplo más interesante: encontrar el máximo
mayor = reduce(lambda a, b: a if a > b else b, datos)
print(mayor)  # 10

# --- Encadenando map + filter + reduce ---
# Calcular la suma de los cuadrados de los números pares
resultado = reduce(
    lambda acc, x: acc + x,
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, datos)),
    0
)
print(resultado)
# pares: [2, 4, 6, 8, 10] -> cuadrados: [4, 16, 36, 64, 100] -> suma: 220

# Lo mismo con list comprehension (más legible):
assert sum(x ** 2 for x in datos if x % 2 == 0) == 220


# ============================================================
# 6. ÁRBOLES Y RECURSIVIDAD
# ============================================================
"""
Los árboles son estructuras no lineales. En FP se modelan sin punteros
mutables usando datos inmutables y recursividad.

RECORRIDOS:
  Preorden:  Raíz -> Izquierdo -> Derecho
  Inorden:   Izquierdo -> Raíz -> Derecho
  Postorden: Izquierdo -> Derecho -> Raíz

  En un BST, Inorden devuelve los valores ORDENADOS.
"""

@dataclass(frozen=True)
class ArbolBinario:
    """
    Nodo inmutable de un árbol binario.
    Cada nodo tiene un valor, y referencias a los subárboles izquierdo y derecho.
    Como es frozen=True, una vez creado no puede modificarse.
    """
    valor: int
    izquierdo: "ArbolBinario | None" = None
    derecho: "ArbolBinario | None" = None

# Construimos el árbol:
#         4
#       /   \
#      2     6
#     / \   / \
#    1   3 5   7

hoja1 = ArbolBinario(1)
hoja3 = ArbolBinario(3)
hoja5 = ArbolBinario(5)
hoja7 = ArbolBinario(7)

sub_izq = ArbolBinario(2, hoja1, hoja3)
sub_der = ArbolBinario(6, hoja5, hoja7)
arbol = ArbolBinario(4, sub_izq, sub_der)

# --- Recorridos recursivos puros ---
# Cada función retorna UNA NUEVA TUPLA. No modifican el árbol.

def preorden(nodo):
    """
    Preorden: visita la raíz PRIMERO, luego izquierda, luego derecha.
    Útil para copiar un árbol o serializarlo.
    """
    if nodo is None:
        return ()
    return (nodo.valor,) + preorden(nodo.izquierdo) + preorden(nodo.derecho)

def inorden(nodo):
    """
    Inorden: visita izquierda, luego raíz, luego derecha.
    En un BST los valores salen ORDENADOS ascendentemente.
    """
    if nodo is None:
        return ()
    return inorden(nodo.izquierdo) + (nodo.valor,) + inorden(nodo.derecho)

def postorden(nodo):
    """
    Postorden: visita izquierda, luego derecha, luego raíz al FINAL.
    Útil para borrar árboles (borras hijos antes que el padre).
    """
    if nodo is None:
        return ()
    return postorden(nodo.izquierdo) + postorden(nodo.derecho) + (nodo.valor,)

print("Preorden:",  preorden(arbol))    # (4, 2, 1, 3, 6, 5, 7)
print("Inorden:",   inorden(arbol))     # (1, 2, 3, 4, 5, 6, 7)
print("Postorden:", postorden(arbol))   # (1, 3, 2, 5, 7, 6, 4)

"""
NOTA: cada llamada recursiva crea una nueva tupla concatenada.
No hay mutación en ningún paso —todo es inmutable y puro.
El caso base (nodo is None) retorna tupla vacía, que es el
elemento neutro de la concatenación.
"""


# ============================================================
# 7. EVALUACIÓN PEREZOSA (Lazy Evaluation)
# ============================================================
"""
En la evaluación tradicional (estricta) se calcula todo de inmediato.
Esto puede llenar la memoria si trabajas con colecciones enormes.

La evaluación perezosa calcula los valores JUSTO cuando se necesitan,
no antes. Esto permite:
  - Trabajar con secuencias INFINITAS (números naturales, Fibonacci...)
  - No cargar todo en memoria a la vez
  - Ahorrar cómputo si no necesitas todos los resultados

En Python se implementa con GENERADORES (yield) e itertools.

En JS existen los generators function* y yield, mismo concepto.
"""

# --- Generador Fibonacci infinito ---

def fibonacci():
    """
    Generador infinito: produce números de Fibonacci uno a uno
    bajo demanda, sin almacenar toda la secuencia.
    """
    a, b = 0, 1
    while True:          # Bucle infinito, pero no bloquea
        yield a          # "pausa" aquí y devuelve el valor
        a, b = b, a + b  # cuando se pida el siguiente, continúa aquí

# Cada llamada a next() reanuda el generador hasta el próximo yield
fib = fibonacci()
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1
print(next(fib))  # 2
print(next(fib))  # 3

# Podemos tomar los primeros N sin generar el resto:
import itertools

def take(n, iterable):
    """Toma los primeros n elementos de un iterable (posiblemente infinito)."""
    return list(itertools.islice(iterable, n))

primeros_10 = take(10, fibonacci())
print(primeros_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

"""
Sin lazy evaluation no podrías tener una secuencia infinita:
  - Una lista infinita llenaría la memoria
  - Un bucle infinito sin yield nunca devolvería el control
Con yield, el generador se "congela" entre valores.
"""

# --- Más herramientas de itertools ---

# count: generador infinito de números
naturales = itertools.count(1)  # 1, 2, 3, 4, 5, ...
primeros_5 = take(5, naturales)
print(primeros_5)  # [1, 2, 3, 4, 5]

# filter perezoso: solo calcula cuando iteramos
pares_lazy = filter(lambda x: x % 2 == 0, itertools.count(1))
print(take(4, pares_lazy))  # [2, 4, 6, 8]

# chain: concatenar iterables sin crear nuevas listas
concatenado = itertools.chain([1, 2], [3, 4], [5, 6])
print(list(concatenado))  # [1, 2, 3, 4, 5, 6]

# compress: filtrar con máscara booleana
mascara = [True, False, True, False, True, False]  # o [1, 0, 1, 0, 1, 0]
filtrado = itertools.compress("ABCDEF", mascara)
print(list(filtrado))  # ['A', 'C', 'E']

# starmap: como map pero desempaqueta tuplas como argumentos
pares_sumandos = [(1, 2), (3, 4), (5, 6)]
sumas = list(itertools.starmap(lambda a, b: a + b, pares_sumandos))
print(sumas)  # [3, 7, 11]

"""
Resumen de herramientas clave de itertools:
  count(start, step)  ->  secuencia numérica infinita
  cycle(iterable)     ->  repite infinitamente
  repeat(x, times)    ->  repite x n veces o infinito
  chain(*iterables)   ->  concatena perezosamente
  islice(iter, stop)  ->  slice perezoso (el take manual)
  starmap(func, iter) ->  map con desempaquetado
  compress(data, sel) ->  filtrar con máscara
  zip_longest(...)    ->  zip que no corta en el más corto
"""

# ============================================================
# CIERRE
# ============================================================
"""
Estos 7 conceptos forman la base del paradigma funcional en Python.
No todos se usan en código Python cotidiano (las comprehensions
suelen preferirse sobre map/filter, por ejemplo), pero entenderlos
te da herramientas poderosas para escribir código más:

  - PREVISIBLE  (misma entrada -> misma salida)
  - MODULAR     (funciones pequeñas que se combinan)
  - TESTEABLE   (sin estado oculto que configurar)
  - PARALELIZABLE (sin condiciones de carrera por mutación)
"""
