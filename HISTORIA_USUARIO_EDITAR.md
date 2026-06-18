# Historia de Usuario: Editar Información

## Descripción
**Título:** Editar Información  
**Como usuario**, quiero poder modificar los datos de un contacto existente por si cambió de empleo o de correo electrónico.

---

## Criterios de Aceptación

✅ El usuario puede acceder a una página de edición desde el detalle del contacto  
✅ El formulario pre-carga los datos actuales del contacto  
✅ El usuario puede modificar cualquiera de los campos del contacto  
✅ El usuario puede cambiar el correo electrónico  
✅ El usuario puede cambiar la empresa  
✅ El usuario puede cambiar otros campos como LinkedIn, GitHub, habilidades y descripción  
✅ Al guardar los cambios, los datos se actualizan en la base de datos  
✅ Después de guardar, el usuario es redirigido al detalle del contacto actualizado  
✅ Si el formulario es inválido, se muestran los errores sin guardar los cambios  

---

## Cambios Implementados

### 1. Vista de Edición (`contactos/views.py`)
Se agregó la función `editar_contacto()` que:
- Obtiene el contacto por ID (devuelve 404 si no existe)
- Maneja solicitudes GET mostrando el formulario con datos pre-cargados
- Maneja solicitudes POST para guardar cambios
- Redirige al detalle del contacto después de guardar

```python
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('detalle_contacto', contacto_id=contacto.id)
    else:
        form = ContactoForm(instance=contacto)
    
    return render(request, 'contactos/formulario.html', 
                  {'form': form, 'contacto': contacto, 'es_edicion': True})
```

### 2. URL de Edición (`contactos/urls.py`)
Se agregó la ruta para la vista de edición:
```python
path('editar/<int:contacto_id>/', views.editar_contacto, name='editar_contacto')
```

### 3. Template del Formulario (`contactos/templates/contactos/formulario.html`)
El template se actualizó para ser reutilizable tanto para crear como para editar:
- Muestra título diferente según si es creación o edición
- Pre-carga datos cuando es edición
- Redirecciona al lugar correcto al cancelar

### 4. Detalle del Contacto (`contactos/templates/contactos/detalle.html`)
Se agregó un botón de edición al template del detalle:
- Botón "Editar contacto" en color amarillo (warning)
- Mejor disposición de los botones de acción

### 5. Tests (`contactos/tests.py`)
Se agregó la clase `ContactoEditarTest` con 9 tests que validan:
- ✅ La página de edición carga correctamente (HTTP 200)
- ✅ Se usa la plantilla correcta
- ✅ Los datos existentes se pre-cargan
- ✅ Se puede cambiar el correo electrónico
- ✅ Se puede cambiar la empresa
- ✅ Se pueden cambiar múltiples campos
- ✅ Un ID inexistente devuelve 404
- ✅ Un formulario inválido no guarda cambios
- ✅ El título de la página es correcto

---

## Resultados de Tests

```
Ran 18 tests in 0.533s
OK ✅

Breakdown:
- ContactoModelTest: 6 tests ✅
- ContactoViewsTest: 3 tests ✅
- ContactoEditarTest: 9 tests ✅ (NUEVOS)
```

---

## Flujo de Usuario

1. **Usuario ve la lista de contactos**
   - Desde `/` (lista_contactos)

2. **Usuario click en un contacto**
   - Va a `/contacto/<id>/` (detalle_contacto)

3. **Usuario presiona "Editar contacto"**
   - Va a `/editar/<id>/` (editar_contacto)

4. **El formulario carga con datos existentes**
   - Se muestra `ContactoForm` con instancia del contacto
   - Título: "Editar Contacto: [Nombre]"

5. **Usuario modifica los datos deseados**
   - Puede cambiar correo, empresa, LinkedIn, GitHub, habilidades, descripción

6. **Usuario presiona "Guardar Cambios"**
   - Si el formulario es válido:
     - Los cambios se guardan en la BD
     - Se redirige a `/contacto/<id>/` (detalle actualizado)
   - Si el formulario tiene errores:
     - Se muestra nuevamente con mensajes de error

---

## Campos Editables

- **Nombre** (Requerido)
- **Correo** (Requerido, debe ser válido)
- **Empresa** (Opcional)
- **LinkedIn** (Opcional, debe ser URL válida si se completa)
- **GitHub** (Opcional, debe ser URL válida si se completa)
- **Habilidades** (Requerido)
- **Descripción** (Opcional)

---

## Recursos Utilizados

- **Modelo:** `Contacto` (campos existentes)
- **Formulario:** `ContactoForm` (existente, reutilizado)
- **Vista:** Nueva función `editar_contacto()`
- **Template:** `formulario.html` actualizado
- **URLs:** Nueva ruta `/editar/<int:contacto_id>/`
- **Tests:** 9 nuevos tests en `ContactoEditarTest`

---

## Estado: ✅ COMPLETADO

La historia de usuario ha sido implementada completamente con:
- Funcionalidad completa de edición
- Validación de formularios
- Manejo de errores
- Tests unitarios completos
- UI mejorada con botón de edición
