from abc import ABC, abstractmethod


# COMPONENTE
class ContactoComponent(ABC):

    @abstractmethod
    def obtener_info(self):
        pass


# COMPONENTE CONCRETO
class ContactoBase(ContactoComponent):

    def __init__(self, nombre, correo, empresa):
        self.nombre = nombre
        self.correo = correo
        self.empresa = empresa

    def obtener_info(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "empresa": self.empresa
        }

    # Métodos de compatibilidad esperados por la aplicación/tests
    def obtener_nombre(self):
        return self.nombre

    def obtener_correo(self):
        return self.correo

    def obtener_empresa(self):
        if self.empresa and str(self.empresa).strip():
            return self.empresa
        return "No especificada"

    def obtener_descripcion_completa(self):
        return f"{self.nombre} <{self.correo}> - {self.obtener_empresa()}"

    def obtener_informacion(self):
        info = self.obtener_info()
        info["tipo"] = "ContactoBase"
        return info


# DECORATOR ABSTRACTO
class ContactoDecorator(ContactoComponent):

    def __init__(self, contacto):
        self.contacto = contacto

    def obtener_info(self):
        return self.contacto.obtener_info()

    # Delegaciones de compatibilidad
    def obtener_nombre(self):
        return self.contacto.obtener_nombre()

    def obtener_correo(self):
        return self.contacto.obtener_correo()

    def obtener_empresa(self):
        return self.contacto.obtener_empresa()

    def obtener_descripcion_completa(self):
        return self.contacto.obtener_descripcion_completa()

    def obtener_informacion(self):
        info = self.obtener_info()
        info["tipo"] = type(self).__name__
        return info


# DECORADOR CONCRETO 1
class LinkedInDecorator(ContactoDecorator):

    def __init__(self, contacto, linkedin):
        super().__init__(contacto)
        self.linkedin = linkedin

    def obtener_info(self):
        info = super().obtener_info()
        info = dict(info)
        info["linkedin"] = self.linkedin
        return info


# DECORADOR CONCRETO 2
class GitHubDecorator(ContactoDecorator):

    def __init__(self, contacto, github):
        super().__init__(contacto)
        self.github = github

    def obtener_info(self):
        info = super().obtener_info()
        info = dict(info)
        info["github"] = self.github
        return info


# DECORADOR CONCRETO 3
class HabilidadesDecorator(ContactoDecorator):

    def __init__(self, contacto, habilidades):
        super().__init__(contacto)
        self.habilidades = habilidades

    def obtener_info(self):
        info = super().obtener_info()
        info = dict(info)
        info["habilidades"] = self.habilidades
        return info


# Clases de compatibilidad históricas (nombres usados en ejemplos/tests anteriores)
class ContactoConEtiquetas(ContactoDecorator):
    def __init__(self, contacto, etiquetas=None):
        super().__init__(contacto)
        self._etiquetas = list(etiquetas) if etiquetas else []

    def agregar_etiqueta(self, etiqueta):
        self._etiquetas.append(etiqueta)

    def obtener_etiquetas(self):
        return list(self._etiquetas)

    def obtener_info(self):
        info = super().obtener_info()
        info = dict(info)
        info["etiquetas"] = list(self._etiquetas)
        return info


class ContactoConCalificacion(ContactoDecorator):
    def __init__(self, contacto, calificacion=None):
        super().__init__(contacto)
        self.calificacion = calificacion

    def obtener_estrellas(self):
        return self.calificacion

    def obtener_info(self):
        info = super().obtener_info()
        info = dict(info)
        info["calificacion"] = self.calificacion
        return info