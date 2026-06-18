from kanren import run, var, Relation, facts, lany, eq

servicio = Relation()
facts(servicio,
      (1, "Autentificacion", "us-east", 12000, True, ("Nose","Redis")),
      (2, "Procesamiento Pagos", "us-west", 4500, True, ("Java","Spring")),
      (3, "Recomendaciones AI", "eu-east", 25000, False, ("Python","TensorFlow")),
      (4, "Notificaciones", "eu-central", 8500, True, ("Node","RabbitMQ")),
      (5, "Reportes Historicos", "us-west", 500, False, ("Python","Pandas")))

id, nombre, zona, consultas, activo, tecnologias = var(), var(), var(), var(), var(), var()

no_activos = run(0, (id, nombre, consultas), servicio(id, nombre, zona, consultas, False, tecnologias))
activos = run(0, (id, nombre, consultas, zona), servicio(id, nombre, zona, consultas, True, tecnologias))
usa_node = run(0, (id, nombre, zona, consultas, tecnologias), servicio(id, nombre, zona, consultas, activo, tecnologias), lany(eq(zona, "us-east"), eq(zona, "us-west")))


def mantenimiento_urgente(no_activos):
    return [(x, y, z) for x, y, z in no_activos if z >= 10000]


def servicios_criticos(activos):
    return [(x, y, z) for x, y, z, w in activos if z >= 10000 or w in ("us-east", "us-west")]


def formatear_salida(no_activos, activos, usa_node):
    mu = mantenimiento_urgente(no_activos)
    sc = servicios_criticos(activos)
    suma = sum(z for _, _, z, _ in activos)
    return "\n".join(
        [f"El servicio {y} con ID {x} No esta activo y es de alta carga. Requiere mantenimiento urgente"
         for x, y, z in mu]
        + (["", "Servicios que requieren mantenimiento urgente:"] + [f"ID: {x}, Nombre: {y}, Consultas: {z}" for x, y, z in mu] if mu else [])
        + [f"El servicio {y} con ID {x} esta activo, es de alta carga y se encuentra en la zona {w}. Es un servicio critico."
            if z >= 10000 else
            f"El servicio {y} con ID {x} esta activo, se encuentra en la zona {w} y es de baja carga. Es un servicio critico"
            for x, y, z, w in activos
            if z >= 10000 or w in ("us-east", "us-west")]
        + (["", "Servicios criticos registrados:"] + [f"ID: {x}, Nombre: {y}, Consultas: {z}" for x, y, z in sc] if sc else [])
        + [f"El servicio {y} con ID {x} usa Node.js, esta en la zona {z} y tiene {w} consultas. Debe migrarse a CloudFare"
           for _, y, x, z, w in [(a, b, c, d, e) for a, b, c, d, e in usa_node if "Node" in e and d < 10000]]
        + [f"Suma de consultas de servicios activos: {suma}"]
    )


print(formatear_salida(no_activos, activos, usa_node))