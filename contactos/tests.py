
from django.test import TestCase
from django.urls import reverse
from .models import Contacto

class ContactoModelTest(TestCase):

    def setUp(self):
        # El método setUp sirve para crear datos de prueba que usarán los tests
        self.contacto_prueba = Contacto.objects.create(
            nombre="Edwin Duran",
            correo="edwin@example.com",
            empresa="Politécnico",
            linkedin="https://linkedin.com/in/edwin",
            github="https://github.com/edwin",
            habilidades="Python, Django, SQL"
        )

    def test_creacion_contacto(self):
        """Verifica que el contacto se guarde correctamente con sus campos"""
        contacto = Contacto.objects.get(id=self.contacto_prueba.id)
        self.assertEqual(contacto.nombre, "Edwin Duran")
        self.assertEqual(contacto.correo, "edwin@example.com")

    def test_metodo_str_devuelve_nombre(self):
        """Verifica que el método __str__ devuelva el nombre del contacto"""
        contacto = Contacto.objects.get(id=self.contacto_prueba.id)
        self.assertEqual(str(contacto), contacto.nombre)

    def test_detalle_contacto_muestra_contacto(self):
        """Verifica que la vista de detalle cargue correctamente y muestre el nombre"""
        url = reverse('detalle_contacto', args=[self.contacto_prueba.id])
        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, self.contacto_prueba.nombre)
        self.assertContains(respuesta, self.contacto_prueba.correo)

    def test_detalle_contacto_id_invalido_devuelve_404(self):
        """Verifica que un ID inválido devuelva un error 404"""
        url = reverse('detalle_contacto', args=[9999])
        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 404)

    def test_borrar_contacto_redirige_y_elimina(self):
        """Verifica que borrar un contacto realice la eliminación y redirija a la lista"""
        url = reverse('borrar_contacto', args=[self.contacto_prueba.id])
        respuesta = self.client.post(url)

        self.assertRedirects(respuesta, reverse('lista_contactos'))
        self.assertFalse(Contacto.objects.filter(id=self.contacto_prueba.id).exists())

    def test_borrar_contacto_invalido_devuelve_404(self):
        """Verifica que intentar borrar un ID inexistente devuelva 404"""
        url = reverse('borrar_contacto', args=[9999])
        respuesta = self.client.post(url)

        self.assertEqual(respuesta.status_code, 404)
        
class ContactoViewsTest(TestCase):

    def setUp(self):
        # Creamos dos contactos de prueba en la base de datos temporal
        self.contacto1 = Contacto.objects.create(
            nombre="Edwin Duran",
            correo="edwin@example.com",
            habilidades="Python, SQL"
        )
        self.contacto2 = Contacto.objects.create(
            nombre="Ana Gomez",
            correo="ana@example.com",
            habilidades="Java, Spring"
        )
        # Obtenemos la URL de la lista de contactos usando su 'name' en urls.py
        self.url_lista = reverse('lista_contactos')

    def test_vista_lista_contactos_carga_exitosamente(self):
        """Verifica que la página principal cargue con código HTTP 200"""
        respuesta = self.client.get(self.url_lista)
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_lista_contactos_usa_plantilla_correcta(self):
        """Verifica que se esté renderizando el HTML correcto"""
        respuesta = self.client.get(self.url_lista)
        self.assertTemplateUsed(respuesta, 'contactos/lista.html')

    def test_vista_lista_contactos_muestra_los_registros(self):
        """Verifica que los nombres de los contactos aparezcan en el HTML"""
        respuesta = self.client.get(self.url_lista)
        # Comprobamos que el HTML contenga el texto de los nombres creados
        self.assertContains(respuesta, "Edwin Duran")
        self.assertContains(respuesta, "Ana Gomez")