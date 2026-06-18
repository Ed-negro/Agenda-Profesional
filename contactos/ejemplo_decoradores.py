"""Ejemplos de uso del patrón Decorator (versión canónica).

Este script muestra cómo usar `ContactoBase`, `ContactoConEtiquetas`,
`ContactoConCalificacion` y los decoradores concretos disponibles.
"""

from contactos.decoradores import (
    ContactoBase,
    ContactoConEtiquetas,
    ContactoConCalificacion,
    LinkedInDecorator,
    GitHubDecorator,
    HabilidadesDecorator,
)


def ejemplo_contacto_basico():
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Contacto Base")
    print("=" * 60)
    contacto = ContactoBase(nombre="Juan Perez", correo="juan@example.com", empresa="TechCorp")
    print("Nombre:", contacto.obtener_nombre())
    print("Correo:", contacto.obtener_correo())
    print("Empresa:", contacto.obtener_empresa())
    print("Descripcion:", contacto.obtener_descripcion_completa())
    print("Info dict:", contacto.obtener_informacion())


def ejemplo_contacto_con_etiquetas():
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Contacto con Etiquetas")
    print("=" * 60)
    contacto = ContactoBase(nombre="Maria Garcia", correo="maria@example.com", empresa="WebDev Inc")
    contacto_etiquetado = ContactoConEtiquetas(contacto)
    contacto_etiquetado.agregar_etiqueta("VIP")
    contacto_etiquetado.agregar_etiqueta("Cliente Frecuente")
    print("Descripcion:", contacto_etiquetado.obtener_descripcion_completa())
    print("Etiquetas:", contacto_etiquetado.obtener_etiquetas())
    print("Info dict:", contacto_etiquetado.obtener_informacion())


def ejemplo_contacto_con_calificacion():
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Contacto con Calificacion")
    print("=" * 60)
    contacto = ContactoBase(nombre="Carlos Lopez", correo="carlos@example.com", empresa="DevStudio")
    contacto_calificado = ContactoConCalificacion(contacto, calificacion=4)
    print("Descripcion:", contacto_calificado.obtener_descripcion_completa())
    print("Estrellas:", contacto_calificado.obtener_estrellas())
    print("Info dict:", contacto_calificado.obtener_informacion())


def ejemplo_multiples_decoradores():
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Multiples Decoradores")
    print("=" * 60)
    contacto_base = ContactoBase(nombre="Sofia Diaz", correo="sofia@example.com", empresa="StartupCo")
    contacto = ContactoConEtiquetas(contacto_base, etiquetas=["VIP", "Cliente Premium"]) 
    contacto = ContactoConCalificacion(contacto, calificacion=5)
    print("Descripcion:", contacto.obtener_descripcion_completa())
    import json
    print("Info completa:\n", json.dumps(contacto.obtener_informacion(), indent=2, ensure_ascii=False))


def ejemplo_decoradores_extras():
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Decoradores LinkedIn/GitHub/Habilidades")
    print("=" * 60)
    contacto_base = ContactoBase(nombre="Luis Alvarez", correo="luis@example.com", empresa="InfraTech")
    contacto = LinkedInDecorator(contacto_base, linkedin="luis-linkedin")
    contacto = GitHubDecorator(contacto, github="luis-gh")
    contacto = HabilidadesDecorator(contacto, habilidades=["Python", "Django"]) 
    print("Descripcion:", contacto.obtener_descripcion_completa())
    print("Info dict:", contacto.obtener_informacion())


if __name__ == "__main__":
    print("\n" + "🎨 PATRÓN DECORATOR - EJEMPLOS DE USO 🎨".center(60))
    ejemplo_contacto_basico()
    ejemplo_contacto_con_etiquetas()
    ejemplo_contacto_con_calificacion()
    ejemplo_multiples_decoradores()
    ejemplo_decoradores_extras()
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados!")
    print("=" * 60 + "\n")
