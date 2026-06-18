"""
Tests para la implementación del patrón Decorator en contactos.

Estos tests validan que el patrón Decorator funciona correctamente,
permitiendo agregar dinámicamente funcionalidades a los contactos.
"""

from django.test import TestCase
from .decoradores import ContactoBase


class DecoradorContactoBaseTest(TestCase):
    """Tests para la clase base ContactoBase"""

    def setUp(self):
        """Crea un contacto base para las pruebas"""
        self.contacto_base = ContactoBase(
            nombre="Juan Perez",
            correo="juan@example.com",
            empresa="TechCorp"
        )

    def test_contacto_base_obtiene_nombre(self):
        """Verifica que se obtenga el nombre correctamente"""
        self.assertEqual(self.contacto_base.obtener_nombre(), "Juan Perez")

    def test_contacto_base_obtiene_correo(self):
        """Verifica que se obtenga el correo correctamente"""
        self.assertEqual(self.contacto_base.obtener_correo(), "juan@example.com")

    def test_contacto_base_obtiene_empresa(self):
        """Verifica que se obtenga la empresa correctamente"""
        self.assertEqual(self.contacto_base.obtener_empresa(), "TechCorp")

    def test_contacto_base_obtiene_empresa_vacia(self):
        """Verifica que contacto sin empresa retorna 'No especificada'"""
        contacto = ContactoBase(nombre="Ana", correo="ana@test.com", empresa="")
        self.assertEqual(contacto.obtener_empresa(), "No especificada")

    def test_contacto_base_descripcion_completa(self):
        """Verifica que la descripción completa incluye todos los campos"""
        descripcion = self.contacto_base.obtener_descripcion_completa()
        self.assertIn("Juan Perez", descripcion)
        self.assertIn("juan@example.com", descripcion)
        self.assertIn("TechCorp", descripcion)

    def test_contacto_base_obtiene_informacion(self):
        """Verifica que obtiene la información como diccionario"""
        info = self.contacto_base.obtener_informacion()
        self.assertEqual(info['nombre'], "Juan Perez")
        self.assertEqual(info['correo'], "juan@example.com")
        self.assertEqual(info['empresa'], "TechCorp")
        self.assertEqual(info['tipo'], 'ContactoBase')
if __name__ == "__main__":
    import unittest
    unittest.main()

