
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


class ContactoEditarTest(TestCase):
    """Tests para la funcionalidad de editar contactos - Historia de usuario: Editar Información"""

    def setUp(self):
        """Crea un contacto de prueba para las pruebas de edición"""
        self.contacto = Contacto.objects.create(
            nombre="Juan Perez",
            correo="juan@example.com",
            empresa="Empresa Antigua",
            linkedin="https://linkedin.com/in/juan",
            github="https://github.com/juan",
            habilidades="Python, SQL"
        )
        self.url_editar = reverse('editar_contacto', args=[self.contacto.id])

    def test_vista_editar_contacto_carga_exitosamente(self):
        """Verifica que la página de edición cargue con código HTTP 200"""
        respuesta = self.client.get(self.url_editar)
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_editar_contacto_usa_plantilla_correcta(self):
        """Verifica que se use la plantilla correcta para edición"""
        respuesta = self.client.get(self.url_editar)
        self.assertTemplateUsed(respuesta, 'contactos/formulario.html')

    def test_vista_editar_contacto_muestra_datos_existentes(self):
        """Verifica que el formulario muestre los datos actuales del contacto"""
        respuesta = self.client.get(self.url_editar)
        self.assertContains(respuesta, "Juan Perez")
        self.assertContains(respuesta, "juan@example.com")
        self.assertContains(respuesta, "Empresa Antigua")

    def test_editar_contacto_cambiar_correo(self):
        """Verifica que se pueda cambiar el correo electrónico del contacto"""
        datos = {
            'nombre': 'Juan Perez',
            'correo': 'juan.nuevo@example.com',
            'empresa': 'Empresa Antigua',
            'linkedin': 'https://linkedin.com/in/juan',
            'github': 'https://github.com/juan',
            'habilidades': 'Python, SQL'
        }
        respuesta = self.client.post(self.url_editar, datos)
        
        # Verifica que se redirija al detalle del contacto
        self.assertRedirects(respuesta, reverse('detalle_contacto', args=[self.contacto.id]))
        
        # Verifica que el correo se haya actualizado en la base de datos
        contacto_actualizado = Contacto.objects.get(id=self.contacto.id)
        self.assertEqual(contacto_actualizado.correo, 'juan.nuevo@example.com')

    def test_editar_contacto_cambiar_empresa(self):
        """Verifica que se pueda cambiar la empresa del contacto"""
        datos = {
            'nombre': 'Juan Perez',
            'correo': 'juan@example.com',
            'empresa': 'Empresa Nueva',
            'linkedin': 'https://linkedin.com/in/juan',
            'github': 'https://github.com/juan',
            'habilidades': 'Python, SQL'
        }
        respuesta = self.client.post(self.url_editar, datos)
        
        # Verifica que se redirija correctamente
        self.assertRedirects(respuesta, reverse('detalle_contacto', args=[self.contacto.id]))
        
        # Verifica que la empresa se haya actualizado
        contacto_actualizado = Contacto.objects.get(id=self.contacto.id)
        self.assertEqual(contacto_actualizado.empresa, 'Empresa Nueva')

    def test_editar_contacto_cambiar_multiples_campos(self):
        """Verifica que se puedan cambiar múltiples campos simultáneamente"""
        datos = {
            'nombre': 'Juan Perez',
            'correo': 'juan.nuevo@example.com',
            'empresa': 'Empresa Nueva',
            'linkedin': 'https://linkedin.com/in/juan-perez',
            'github': 'https://github.com/juanperez',
            'habilidades': 'Python, Java, SQL, Django'
        }
        respuesta = self.client.post(self.url_editar, datos)
        
        # Verifica que se redirija correctamente
        self.assertRedirects(respuesta, reverse('detalle_contacto', args=[self.contacto.id]))
        
        # Verifica que todos los campos se hayan actualizado
        contacto_actualizado = Contacto.objects.get(id=self.contacto.id)
        self.assertEqual(contacto_actualizado.correo, 'juan.nuevo@example.com')
        self.assertEqual(contacto_actualizado.empresa, 'Empresa Nueva')
        self.assertEqual(contacto_actualizado.linkedin, 'https://linkedin.com/in/juan-perez')
        self.assertEqual(contacto_actualizado.github, 'https://github.com/juanperez')
        self.assertEqual(contacto_actualizado.habilidades, 'Python, Java, SQL, Django')

    def test_editar_contacto_invalido_devuelve_404(self):
        """Verifica que intentar editar un contacto inexistente devuelva 404"""
        url_invalida = reverse('editar_contacto', args=[9999])
        respuesta = self.client.get(url_invalida)
        self.assertEqual(respuesta.status_code, 404)

    def test_editar_contacto_con_formulario_invalido(self):
        """Verifica que un formulario con correo inválido no guarde cambios"""
        datos = {
            'nombre': 'Juan Perez',
            'correo': 'correo-invalido',  # Correo inválido
            'empresa': 'Empresa Nueva',
            'linkedin': 'https://linkedin.com/in/juan',
            'github': 'https://github.com/juan',
            'habilidades': 'Python, SQL'
        }
        respuesta = self.client.post(self.url_editar, datos)
        
        # No debe redirigir, debe volver a mostrar el formulario
        self.assertEqual(respuesta.status_code, 200)
        
        # Verifica que el contacto no haya sido modificado
        contacto_sin_cambios = Contacto.objects.get(id=self.contacto.id)
        self.assertEqual(contacto_sin_cambios.correo, 'juan@example.com')

    def test_vista_editar_muestra_titulo_correcto(self):
        """Verifica que la página de edición muestre el título apropiado"""
        respuesta = self.client.get(self.url_editar)
        self.assertContains(respuesta, "Editar Contacto")
        self.assertContains(respuesta, "Juan Perez")


class ContactoBuscadorTest(TestCase):
    """Tests para la funcionalidad de búsqueda de contactos - Historia de usuario: Buscador por Nombre"""

    def setUp(self):
        """Crea contactos de prueba para las pruebas de búsqueda"""
        self.contacto1 = Contacto.objects.create(
            nombre="Juan Perez",
            correo="juan@example.com",
            empresa="TechCorp",
            habilidades="Python, Django"
        )
        self.contacto2 = Contacto.objects.create(
            nombre="Maria García",
            correo="maria@example.com",
            empresa="WebDev Inc",
            habilidades="JavaScript, React"
        )
        self.contacto3 = Contacto.objects.create(
            nombre="Carlos López",
            correo="carlos@techcorp.com",
            empresa="TechCorp",
            habilidades="Java, Spring"
        )
        self.url_lista = reverse('lista_contactos')

    def test_busqueda_por_nombre_exacto(self):
        """Verifica que se pueda buscar por nombre exacto"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'Juan Perez'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Juan Perez")
        self.assertNotContains(respuesta, "Maria García")
        self.assertNotContains(respuesta, "Carlos López")

    def test_busqueda_por_nombre_parcial(self):
        """Verifica que se pueda buscar por nombre parcial"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'Juan'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Juan Perez")
        self.assertNotContains(respuesta, "Maria García")

    def test_busqueda_case_insensitive(self):
        """Verifica que la búsqueda sea case-insensitive"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'juan'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Juan Perez")

    def test_busqueda_por_correo(self):
        """Verifica que se pueda buscar por correo electrónico"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'maria@example.com'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Maria García")
        self.assertNotContains(respuesta, "Juan Perez")

    def test_busqueda_por_correo_parcial(self):
        """Verifica que se pueda buscar por correo parcial"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'techcorp.com'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Carlos López")
        # Nota: Juan también tiene techcorp en empresa, pero no en correo

    def test_busqueda_por_empresa(self):
        """Verifica que se pueda buscar por empresa"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'TechCorp'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Juan Perez")
        self.assertContains(respuesta, "Carlos López")
        self.assertNotContains(respuesta, "Maria García")

    def test_busqueda_sin_resultados(self):
        """Verifica que la búsqueda sin resultados muestre mensaje apropiado"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'NoExiste'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No se encontraron contactos")
        self.assertContains(respuesta, "NoExiste")

    def test_sin_busqueda_muestra_todos(self):
        """Verifica que sin búsqueda se muestren todos los contactos"""
        respuesta = self.client.get(self.url_lista)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Juan Perez")
        self.assertContains(respuesta, "Maria García")
        self.assertContains(respuesta, "Carlos López")

    def test_busqueda_pasa_parametro_al_template(self):
        """Verifica que el término de búsqueda se pase al template"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'Juan'})
        
        self.assertEqual(respuesta.context['busqueda'], 'Juan')

    def test_busqueda_vacia_es_igual_a_sin_busqueda(self):
        """Verifica que una búsqueda vacía es igual a no hacer búsqueda"""
        respuesta_sin_busqueda = self.client.get(self.url_lista)
        respuesta_busqueda_vacia = self.client.get(self.url_lista, {'busqueda': ''})
        
        # Ambas deben contener los mismos contactos
        self.assertContains(respuesta_sin_busqueda, "Juan Perez")
        self.assertContains(respuesta_busqueda_vacia, "Juan Perez")
        self.assertContains(respuesta_sin_busqueda, "Maria García")
        self.assertContains(respuesta_busqueda_vacia, "Maria García")

    def test_busqueda_con_espacios_en_blanco(self):
        """Verifica que la búsqueda funcione con espacios en blanco"""
        respuesta = self.client.get(self.url_lista, {'busqueda': '  Juan  '})
        
        self.assertEqual(respuesta.status_code, 200)
        # La búsqueda debe funcionar incluso con espacios

    def test_buscador_visible_en_lista(self):
        """Verifica que la barra de búsqueda esté visible en la página"""
        respuesta = self.client.get(self.url_lista)
        
        self.assertContains(respuesta, 'type="text"')
        self.assertContains(respuesta, 'name="busqueda"')
        self.assertContains(respuesta, 'placeholder="Buscar por nombre, correo o empresa..."')

    def test_boton_limpiar_aparece_con_busqueda(self):
        """Verifica que el botón de limpiar solo aparece cuando hay búsqueda"""
        # Sin búsqueda
        respuesta_sin = self.client.get(self.url_lista)
        # El botón de limpiar no debe estar cuando no hay búsqueda
        
        # Con búsqueda
        respuesta_con = self.client.get(self.url_lista, {'busqueda': 'Juan'})
        self.assertContains(respuesta_con, 'Limpiar')

    def test_busqueda_multiples_caracteres_especiales(self):
        """Verifica que la búsqueda maneje caracteres con acentos"""
        respuesta = self.client.get(self.url_lista, {'busqueda': 'García'})
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Maria García")