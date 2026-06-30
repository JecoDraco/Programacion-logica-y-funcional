"""
================================================================================
CASO DE ESTUDIO 1: ANÁLISIS ULTRAEFICIENTE DE PETICIONES HTTP
================================================================================

ENUNCIADO:
Una empresa de desarrollo de software aloja sus bases de datos en un clúster en 
la nube. Recientemente, han sufrido intentos de inyección de código y saturación 
de memoria en sus servidores de producción. Se requiere diseñar un módulo en 
Python puro que analice un flujo masivo de peticiones HTTP de forma 
ultraeficiente (sin saturar la memoria RAM del servidor de monitoreo) y dispare 
alertas de seguridad bajo demanda[cite: 1].

ESTRUCTURA DE DATOS PROPUESTA:
peticiones_http = (
    MappingProxyType({"id": "REQ-01", "metodo": "GET", "ipOrigen": "192.168.1.50", "latenciaMs": 45, "tamanioPayloadKb": 2, "payload": "SELECT * FROM users"}),
    MappingProxyType({"id": "REQ-02", "metodo": "POST", "ipOrigen": "185.220.10.1", "latenciaMs": 2500, "tamanioPayloadKb": 1500, "payload": "DROP TABLE users;--"}),
    MappingProxyType({"id": "REQ-03", "metodo": "GET", "ipOrigen": "192.168.1.55", "latenciaMs": 12, "tamanioPayloadKb": 1, "payload": "ping"}),
    MappingProxyType({"id": "REQ-04", "metodo": "POST", "ipOrigen": "185.220.10.1", "latenciaMs": 1800, "tamanioPayloadKb": 950, "payload": "normal_profile_update"}),
    MappingProxyType({"id": "REQ-05", "metodo": "POST", "ipOrigen": "192.168.1.70", "latenciaMs": 3100, "tamanioPayloadKb": 1200, "payload": "upload_heavy_image"}),
    MappingProxyType({"id": "REQ-06", "metodo": "GET", "ipOrigen": "172.16.25.40", "latenciaMs": 50, "tamanioPayloadKb": 500, "payload": "exec MaliciousScript"})
)

DIRECTRICES DE IMPLEMENTACIÓN:
1. Inmutabilidad: Aplicar un congelamiento profundo sobre el conjunto 
   peticiones_http utilizando tuplas y mapas de solo lectura 
   (MappingProxyType) para asegurar que ningún registro pueda ser alterado de 
   forma imperativa durante el análisis[cite: 1].

2. Predicados Atómicos: Definir los siguientes criterios mediante funciones 
   puras o expresiones lambda[cite: 1]:
   - es_metodo_escritura(x): Verdadero si el método es "POST"[cite: 1].
   - es_latencia_alta(x): Verdadero si latenciaMs es estrictamente mayor o 
     igual a 2000 ms[cite: 1].
   - es_payload_sospechoso(x): Verdadero si el payload incluye las palabras 
     clave de ataque "DROP", "SELECT" o "MaliciousScript"[cite: 1].

3. Reglas Lógicas: Construir la regla combinada detectar_amenaza_potencial(x) 
   bajo el criterio: Es un Método de Escritura AND (Tiene Latencia Alta OR 
   Tiene un Payload Sospechoso)[cite: 1].

4. Optimización Lazy:
   - Pipeline de Evaluación Perezosa: Crear una función generadora llamada 
     analizador_seguridad_lazy(flujo, regla) con la firma de tipo 
     Generator[MappingProxyType, None, None] que examine las peticiones de una 
     en una, suspendiendo la ejecución con yield al detectar una amenaza[cite: 1].
   - Consumo Controlado: Consumir el flujo del generador utilizando la función 
     nativa next() únicamente hasta capturar las primeras 2 amenazas[cite: 1].
   - Reducción de Datos Funcional (reduce): Tomar las 2 amenazas capturadas y 
     calcular de forma declarativa el promedio de tamaño de payload (en KB) de 
     los incidentes detectados[cite: 1].
"""

from types import MappingProxyType
from typing import Iterable, Generator, Dict, Any
from functools import reduce

peticiones_http = (
    MappingProxyType({"id": "REQ-01", "metodo": "GET", "ipOrigen": "192.168.1.50", "latenciaMs": 45, "tamanioPayloadKb": 2, "payload": "SELECT * FROM users"}),
    MappingProxyType({"id": "REQ-02", "metodo": "POST", "ipOrigen": "185.220.10.1", "latenciaMs": 2500, "tamanioPayloadKb": 1500, "payload": "DROP TABLE users;--"}),
    MappingProxyType({"id": "REQ-03", "metodo": "GET", "ipOrigen": "192.168.1.55", "latenciaMs": 12, "tamanioPayloadKb": 1, "payload": "ping"}),
    MappingProxyType({"id": "REQ-04", "metodo": "POST", "ipOrigen": "185.220.10.1", "latenciaMs": 1800, "tamanioPayloadKb": 950, "payload": "normal_profile_update"}),
    MappingProxyType({"id": "REQ-05", "metodo": "POST", "ipOrigen": "192.168.1.70", "latenciaMs": 3100, "tamanioPayloadKb": 1200, "payload": "upload_heavy_image"}),
    MappingProxyType({"id": "REQ-06", "metodo": "GET", "ipOrigen": "172.16.25.40", "latenciaMs": 50, "tamanioPayloadKb": 500, "payload": "exec MaliciousScript"})
)

escritura_metodo = lambda x: x["metodo"] == "POST"
latencia_alta = lambda x: x["latenciaMs"] >= 2000
payload_malicioso = lambda x: x["payload"].find("DROP") != -1 or x["payload"].find("SELECT") != -1 or x["payload"].find("MaliciousScript") != -1

amenaza_potencial = lambda x: escritura_metodo(x) and (latencia_alta(x) or payload_malicioso(x))

def analizador_seguridad_lazy(flujo: Iterable[MappingProxyType], regla) -> Generator[MappingProxyType, None, None]:
    for peticion in flujo:
        if regla(peticion):
            yield peticion

pipeline_alertas = analizador_seguridad_lazy(peticiones_http, amenaza_potencial)

amenazas_capturadas = []
for _ in range(2):
    try:
        amenazas_capturadas.append(next(pipeline_alertas))
    except StopIteration:
        break

for amenaza in amenazas_capturadas:
    print(f"- ID: {amenaza['id']}, Método: {amenaza['metodo']}, Latencia: {amenaza['latenciaMs']}ms, Payload: '{amenaza['payload']}'")


if amenazas_capturadas:
    tamanio_total = reduce(lambda acumulado, p: acumulado + p["tamanioPayloadKb"], amenazas_capturadas, 0.0)
    promedio_payload = tamanio_total / len(amenazas_capturadas)
    print(f"\nPromedio del tamaño de payload de los incidentes: {promedio_payload} KB")


"""
================================================================================
CASO DE ESTUDIO 2: OPTIMIZADOR LOGÍSTICO DE COMERCIO ELECTRÓNICO
================================================================================

ENUNCIADO:
Una plataforma de comercio electrónico maneja miles de despachos de mercancía 
diariamente. Durante las horas pico, la base de datos central se satura debido a 
que los algoritmos tradicionales leen e intentan enrutar todas las órdenes del 
almacén simultáneamente. Se solicita desarrollar un servicio en Python funcional 
que analice de forma perezosa el inventario de paquetes y asigne de manera 
inmediata las órdenes a los repartidores motorizados, deteniendo el flujo en 
cuanto un camión complete su capacidad[cite: 1].

ESTRUCTURA DE DATOS PROPUESTA:
ordenes_envio = (
    MappingProxyType({"id": "ORD-101", "tipo": "estandar", "destino": "Tabasco", "pesoKg": 4.0, "distanciaKm": 8.0, "asegurado": False}),
    MappingProxyType({"id": "ORD-102", "tipo": "express", "destino": "Veracruz", "pesoKg": 22.0, "distanciaKm": 120.0, "asegurado": True}),
    MappingProxyType({"id": "ORD-103", "tipo": "estandar", "destino": "Tabasco", "pesoKg": 1.5, "distanciaKm": 15.0, "asegurado": False}),
    MappingProxyType({"id": "ORD-104", "tipo": "express", "destino": "Tabasco", "pesoKg": 5.0, "distanciaKm": 3.0, "asegurado": False}),
    MappingProxyType({"id": "ORD-105", "tipo": "express", "destino": "Yucatán", "pesoKg": 18.0, "distanciaKm": 250.0, "asegurado": False}),
    MappingProxyType({"id": "ORD-106", "tipo": "express", "destino": "Chiapas", "pesoKg": 35.0, "distanciaKm": 190.0, "asegurado": True})
)

DIRECTRICES DE IMPLEMENTACIÓN:
1. Inmutabilidad: Implementar el congelamiento profundo mediante el uso de tuplas 
   de objetos MappingProxyType para asegurar que la colección ordenes_envio y 
   sus propiedades no sufran alteraciones en memoria durante el proceso de 
   asignación[cite: 1].

2. Predicados Atómicos: Definir los siguientes predicados[cite: 1]:
   - es_envio_express(x): Verdadero si el tipo de orden es "express"[cite: 1].
   - es_paquete_pesado(x): Verdadero si el pesoKg es estrictamente mayor o 
     igual a 15 kg[cite: 1].
   - es_ruta_foranea(x): Verdadero si el destino NO es local, es decir, diferente 
     a "Tabasco" (aplicando la negación lógica not)[cite: 1].

3. Reglas: Definir la regla es_despacho_prioritario(x): Una orden debe salir 
   inmediatamente si: Es un Envío Express AND (Es un Paquete Pesado OR Es una 
   Ruta Foránea)[cite: 1].

4. Optimización del Flujo Lazy:
   - Pipeline Lazy: Diseñar la función generadora despachador_ordenes_lazy(flujo, 
     regla) que recorra el inventario de una en una, pausando con yield al 
     encontrar un paquete prioritario[cite: 1].
   - Consumo por Demanda: Consumir el flujo del generador con la función next() 
     estrictamente hasta seleccionar los primeros 2 paquetes requeridos para 
     llenar la ruta del transporte actual[cite: 1].
   - Reducción Funcional (reduce): Con las 2 órdenes prioritarias capturadas, 
     calcular el promedio de distancia en kilómetros de la ruta de despacho de 
     manera puramente funcional[cite: 1].
"""

