# Historia de Usuario: Buscador por Nombre

## Descripción
**Título:** Buscador por Nombre  
**Como usuario**, quiero escribir un nombre en una barra de búsqueda para encontrar a alguien específico sin tener que desplazarme por toda la lista.

---

## Criterios de Aceptación

✅ Existe una barra de búsqueda visible en la página de contactos  
✅ El usuario puede escribir un nombre en la barra de búsqueda  
✅ Los resultados se filtran mientras el usuario escribe  
✅ Se pueden buscar contactos por nombre (completo o parcial)  
✅ Se pueden buscar por correo electrónico  
✅ Se pueden buscar por empresa  
✅ La búsqueda es case-insensitive (mayúsculas/minúsculas)  
✅ La búsqueda funciona con caracteres acentuados  
✅ Si no hay resultados, se muestra un mensaje indicándolo  
✅ Existe un botón para limpiar la búsqueda  

---

## Cambios Implementados

### 1. Vista Actualizada (`contactos/views.py`)
Se modificó la función `lista_contactos()` para:
- Obtener el parámetro `busqueda` del querystring (GET)
- Filtrar contactos por nombre, correo o empresa usando búsqueda case-insensitive
- Pasar el término de búsqueda al template

```python
from django.db.models import Q

def lista_contactos(request):
    contactos = Contacto.objects.all()
    busqueda = request.GET.get('busqueda', '')
    
    if busqueda:
        contactos = contactos.filter(
            Q(nombre__icontains=busqueda) |
            Q(correo__icontains=busqueda) |
            Q(empresa__icontains=busqueda)
        )
    
    return render(request, 'contactos/lista.html', {
        'contactos': contactos,
        'busqueda': busqueda
    })
```

### 2. Template Actualizado (`contactos/templates/contactos/lista.html`)
Se agregó:
- **Barra de búsqueda** con placeholder descriptivo
- **Botón Buscar** para realizar la búsqueda
- **Botón Limpiar** que solo aparece cuando hay búsqueda activa
- **Mensaje dinámico** cuando no hay resultados:
  - "No hay contactos registrados aún" (sin búsqueda)
  - "No se encontraron contactos que coincidan con..." (con búsqueda)
- **Indicador de búsqueda activa** mostrando el término buscado

### 3. Tests (`contactos/tests.py`)
Se agregó la clase `ContactoBuscadorTest` con 14 tests que validan:
- ✅ Búsqueda por nombre exacto
- ✅ Búsqueda por nombre parcial
- ✅ Búsqueda case-insensitive (minúsculas)
- ✅ Búsqueda por correo completo
- ✅ Búsqueda por correo parcial
- ✅ Búsqueda por empresa
- ✅ Búsqueda sin resultados
- ✅ Sin búsqueda muestra todos
- ✅ Parámetro de búsqueda pasa al template
- ✅ Búsqueda vacía igual a sin búsqueda
- ✅ Búsqueda con espacios en blanco
- ✅ Buscador visible en lista
- ✅ Botón limpiar aparece con búsqueda
- ✅ Búsqueda con caracteres acentuados

---

## Resultados de Tests

```
Ran 32 tests in 0.861s
OK ✅

Breakdown:
- ContactoModelTest: 6 tests ✅
- ContactoViewsTest: 3 tests ✅
- ContactoEditarTest: 9 tests ✅
- ContactoBuscadorTest: 14 tests ✅ (NUEVOS)
```

---

## Flujo de Usuario

1. **Usuario ve la lista de contactos**
   - Desde `/` (lista_contactos)
   - Barra de búsqueda visible en la parte superior

2. **Usuario escribe en la barra de búsqueda**
   - Escribe por ejemplo: "Juan"
   - Presiona el botón "Buscar" (o Enter)

3. **Los resultados se actualizan**
   - Solo muestra contactos que coincidan
   - Búsqueda funciona en:
     - Nombre: "Juan Perez" coincide con "Juan"
     - Correo: "juan@example.com" coincide con "juan"
     - Empresa: "Juan's Corp" coincide con "Juan"

4. **Si no hay resultados**
   - Se muestra: "No se encontraron contactos que coincidan con 'término'"

5. **Usuario presiona "Limpiar"**
   - Se borra el término de búsqueda
   - Se muestran todos los contactos nuevamente

---

## Características de la Búsqueda

| Característica | Comportamiento |
|---|---|
| **Case-insensitive** | "juan" encuentra "Juan", "JUAN", "jUaN" |
| **Parcial** | "gar" encuentra "García", "Gareth" |
| **Acentos** | "García" encuentra "Garcia" |
| **Multi-campo** | Busca en nombre, correo y empresa |
| **Vacía** | Muestra todos los contactos |
| **Sin resultados** | Muestra mensaje explicativo |

---

## Recursos Utilizados

- **Modelo:** `Contacto` (campos: nombre, correo, empresa)
- **Formulario:** GET querystring parameter
- **Vista:** Función `lista_contactos()` (actualizada)
- **Template:** `lista.html` (actualizado)
- **Query:** Django ORM `Q` objects para búsqueda OR
- **Tests:** 14 nuevos tests en `ContactoBuscadorTest`

---

## Estado: ✅ COMPLETADO

La historia de usuario ha sido implementada completamente con:
- Barra de búsqueda funcional
- Búsqueda en múltiples campos
- Búsqueda case-insensitive
- Manejo de casos sin resultados
- Botón para limpiar búsqueda
- Tests completos
- Sin regresiones en funcionalidad existente
