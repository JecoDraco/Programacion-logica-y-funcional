from kanren import run, var, Relation, facts

"""
hechos = [
    {"relacion": "es_humanos", "sujeto": "Juan"},
    {"relacion": "es_humanos", "sujeto": "daniela"},
    {"relacion": "estudiante", "sujeto": "Mario"},
    {"relacion": "estudiante", "sujeto": "yesi"},
    {"relacion": "perro", "sujeto": "guapo"}
]


#Programacion iperativa
for hecho in hechos:
    if hecho["relacion"] == "estudiante":
        print(f"-{hecho["sujeto"]}")

#Programacion funcional
filtrados = list(filter(lambda h: h["relacion"] == "estudiante", hechos))
estudiantes_formatiados = map(lambda h: f"-{h["sujeto"]}", filtrados)

for estudiante in estudiantes_formatiados:
    print(estudiante)
"""
#Programacion logica
declaracion = Relation()
facts(declaracion,
      ("Juan", "es_humanos"),
      ("daniela", "es_humanos"),
      ("Mario", "estudiante"),
      ("yesi", "estudiante"),
      ("guapo", "perro"))

Quien = var()

resultados = run(0, Quien, declaracion(Quien, "es_humanos"))

for humanos in resultados:
    print(f"-{humanos}")