from kanren import run, var, Relation, facts, lany


#Ejercicio 1:
"""
lista_de_cursos = [
    { "titulo": 'React Avanzado', "categoria": 'Desarrollo', "esGratis": False, "tieneCertificado": True },
    { "titulo": 'Introducción a UX/UI', "categoria": 'Diseño', "esGratis": True, "tieneCertificado": False },
    { "titulo": 'Node.js y MongoDB', "categoria": 'Desarrollo', "esGratis": True, "tieneCertificado": True },
    { "titulo": 'Figma para Principiantes', "categoria": 'Diseño', "esGratis": False, "tieneCertificado": False }
]

def filtrar_desarrollo(cursos):
    cursos_desarrollo = []

    for curso in cursos:
        if curso["categoria"] == "Desarrollo":
            cursos_desarrollo.append(curso)
    
    print(cursos_desarrollo)


def filtrar_gratis_o_diseño(cursos):
    cursos_filtrados = []

    for curso in cursos:
        if curso["esGratis"] or curso["categoria"] == "Diseño":
            cursos_filtrados.append(curso)
    
    print(cursos_filtrados)


def filtrar_curso_sin_certificado(cursos):
    cursos_sin_certidicado = []

    for curso in cursos:
        if curso["tieneCertificado"] == True:
            cursos_sin_certidicado.append(cursos)

    print(cursos_sin_certidicado)

def filtrar_desarrollo_con_beneficio(cursos):
    cursos_desarrollo_plus = []

    for curso in cursos:
        if (curso["esGratis"] or curso["tieneCertificado"] == True) and curso["categoria"] == "Desarrollo":
            cursos_desarrollo_plus.append(curso)
    
    print(cursos_desarrollo_plus)



filtrar_desarrollo(lista_de_cursos)
filtrar_gratis_o_diseño(lista_de_cursos)
filtrar_curso_sin_certificado(lista_de_cursos)
filtrar_desarrollo_con_beneficio(lista_de_cursos)
"""





#Ejercicio 2:
"""
es_padre_de = Relation()
facts(es_padre_de,
      ("Juan", "Luis"),
      ("Juan", "Pedro"),
      ("Abraham", "Juan")
)

# =====================================================================
# 2. VARIABLES LÓGICAS (INCÓGNITAS)
# =====================================================================
Padre            = var()
hermano1         = var()
hermano2         = var()
Abuelos          = var()
Padre_intermedio = var()
Nieto            = var()

# Variables específicas para las nuevas consultas puntuales
Padre_Buscado    = var()
Hijo_Buscado     = var()

# =====================================================================
# 3. PROCESAMIENTO DE LAS REGLAS GENERALES
# =====================================================================

# Regla de Hermanos
resultados_brutos_hermanos = run(0, (hermano1, hermano2), 
                                  es_padre_de(Padre, hermano1), 
                                  es_padre_de(Padre, hermano2))

resultados_hermanos = []
for h1, h2 in resultados_brutos_hermanos:
    if h1 != h2:
        resultados_hermanos.append((h1, h2))

# Regla de Abuelos
resultados_abuelos = run(0, (Abuelos, Nieto),
                            es_padre_de(Abuelos, Padre_intermedio),
                            es_padre_de(Padre_intermedio, Nieto))


# =====================================================================
# 4. PROCESAMIENTO DE LAS CONSULTAS PUNTUALES SOLICITADAS
# =====================================================================

# Consulta A: ¿Abraham es padre de Juan?
# Se utiliza el identificador '_' provisto por kanren para verificar la existencia del hecho puro.
Variable_Prueba = var()

# Consulta A: ¿Abraham es padre de Juan?
# Al pasar 'Variable_Prueba', si el hecho existe, run() devolverá una tupla
# que contiene a la variable (indicando éxito). Si no existe, devolverá ().
consulta_abraham_juan = run(0, Variable_Prueba, es_padre_de("Abraham", "Juan"))
abraham_es_padre = "Sí, se confirma en la base de hechos." if len(consulta_abraham_juan) > 0 else "No consta en los hechos."

# Consulta B: ¿Quién es el padre de Luis?
consulta_padre_luis = run(0, Padre_Buscado, es_padre_de(Padre_Buscado, "Luis"))

# Consulta C: ¿Quiénes son los hijos de Juan?
consulta_hijos_juan = run(0, Hijo_Buscado, es_padre_de("Juan", Hijo_Buscado))

print(f"Hermanos determinados válidos:\n    {resultados_hermanos}\n")
print(f"Relaciones Abuelo-Nieto determinadas:\n    {list(resultados_abuelos)}\n")

print("-------------------------------------------------")
print("          RESPUESTAS A CONSULTAS PUNTUALES       ")
print("-------------------------------------------------")

print(f"¿Abraham es padre de Juan?: \n    {abraham_es_padre}\n")
print(f"¿Quién es el padre de Luis?: \n    {list(consulta_padre_luis)}\n")
print(f"¿Quiénes son los hijos de Juan?: \n    {list(consulta_hijos_juan)}")

"""



#Ejercicio 3:
"""
usuario_info = Relation()
facts(usuario_info,
      ("Ana", 25, "admin", True),
      ("Carlos", 17, "user", True),
      ("Beto", 30, "user", False)
)

nombre = var()
edad = var()
rol = var()
cuenta_activa = var()



#1. Se necesita enviar un correo a los usuarios que tienen su cuenta deshabilitada.

usuarios_deshabilitados = run(0, (nombre), 
                                  usuario_info(nombre, edad, rol, False))

print(f"El usuario al que hay que mandar correo es: {list(usuarios_deshabilitados)}")

#2. Para poder entrar a una sección el usuario debe cumplir con dos condiciones estrictas: ser mayor de edad y tener cuenta activa.

usuarios_activos = run(0, (nombre, edad, rol),
                       usuario_info(nombre, edad, rol, True))

mayores_activos = []
for x, y, z in usuarios_activos:
    if y >= 18:
        mayores_activos.append((x,y))

print(f"Los usuarios mayores y activos son: {list(mayores_activos)}")

#3. Se requiere una lista de usuarios especiales, si cuenta con un rol de admin y si es menor
#edad.

admins = run(0, (nombre, edad),
                  usuario_info(nombre, edad, "admin", cuenta_activa))

admin_menor = []
for x, y in admins:
    if y < 18:
        admin_menor.append((x,y))

if len(admin_menor) > 0:
    print(f"Los adminsitradore menores son: {list(admin_menor)}")
else:
    print("No existen adminsitradores menores de edad")

#4. Queremos saber quiénes tienen permiso para editar, la regla dicta que, el usuario debe
#estar activo (o debe ser administrador o mayor de edad).

mayores_activos = []
for x, y, z in usuarios_activos:
    if y >= 18 or z == "admin":
        mayores_activos.append((x,y, z))

print(f"Los Editores de reglas son: {list(mayores_activos)}")
"""



#Ejercicio 4
"""
banco_info = Relation()
facts(banco_info,
      ("Luis", True, True),
      ("Maria", True, False),
      ("Jorge", False, True))

nombre = var()
historial_Limpio = var()
ingresos_Estables = var()

#1. El banco ofrece una tarjeta de crédito "Black" de alta seguridad. Para calificar, el cliente
#debe demostrar una estabilidad total: tener un historial crediticio limpio y percibir ingresos estables.

estables = run(0,(nombre),
               banco_info(nombre, True, True))

print(f"Los usuarios estables totales son: {list(estables)}")

#2. El banco quiere lanzar un programa de reactivación financiera y apoyo. Se busca a clientes
#que tengan problemas en al menos una de sus áreas: que no tengan un historial limpio o que no tengan ingresos estables.

jodidos = run(0, (nombre), lany(
              banco_info(nombre,False,ingresos_Estables),
              banco_info(nombre,historial_Limpio,False)))

print(f"Los usuarios canditos al apoyo son: {list(jodidos)}")

#3. El departamento de cobranza e inversiones quiere identificar clientes de riesgo medio para
#un producto de reestructuración. Buscan perfiles que tengan ingresos estables, pero que no tengan un historial limpio.

estables_sucios = run(0, (nombre),
              banco_info(nombre,False,True))

print(f"Los usuarios con ingresos estables sin hsitorial limpio son: {list(estables_sucios)}")

#4. Auditoría interna quiere saber si la sucursal está en riesgo operativo. El sistema disparará una alerta general si existe 
#al menos un cliente en la base de datos que tenga un historial manchado y también carezca de ingresos estables (Riesgo Crítico).

riesgo = run(0,(nombre),
               banco_info(nombre, False, False))

if len(list(riesgo)) > 0:
    print(f"Los usuarios riesgosos son: {list(riesgo)}")
else:
    print("No existen usuarios riesgosos")

#5. Para que el banco reciba una certificación internacional de calidad de cartera, se requiere que todos los clientes cumplan con 
#no ser un perfil fraudulento. Un cliente es seguro si no ocurre que tenga el historial manchado y carezca de ingresos al mismo tiempo.

certificacion_aprobada = len(riesgo) == 0
estado_certificacion = "Aprobada" if certificacion_aprobada else "Denegada"
print(f"Estado de la Certificación Internacional: {estado_certificacion}")
"""

#Ejercicio 5

transaccion = Relation()

facts(transaccion,
      (1, "deposito", 10000),
      (2, "retiro", 6000),
      (3, "retiro", 1500),
      (4, "retiro", 8000)
)

id_transaccion = var()
tipo_movimiento = var()
monto = var()

#1.    Filtrar solo las transacciones que sean de tipo "retiro" y superen los $5,000.

riesgo = run(0, (id_transaccion, monto),
             transaccion(id_transaccion, "retiro", monto))

riesgo_alto = []
for x, y in riesgo:
    if y > 5000:
        riesgo_alto.append((x,y))

print(f"Las transacciones de alto riesgo son: {list(riesgo_alto)}")

#2.    Aplicarles una tarifa/multa de penalización del 5% por movimiento de alto riesgo.

multas_individuales = [(id_t, monto * 0.05) for id_t, monto in riesgo_alto]
print(f"Detalle de penalizaciones (ID, Multa): {multas_individuales}")

#3.    Calcular el monto total de dinero penalizado que el banco recaudará.

total_recaudado = sum(multa for id_t, multa in multas_individuales)
print(f"Monto total recaudado por penalizaciones: ${total_recaudado:.2f}")