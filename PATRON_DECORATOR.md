# Patrón Decorator - Documentación

## Descripción del Patrón

El **patrón Decorator** es un patrón de diseño estructural que permite agregar dinámicamente nuevas funcionalidades a objetos sin modificar su estructura. En lugar de crear nuevas clases heredando, se envuelven los objetos con decoradores que agregan responsabilidades adicionales.

### Ventajas

✅ **Flexibilidad**: Agregar funcionalidades en tiempo de ejecución  
✅ **Composición**: Combinar múltiples decoradores  
✅ **Abierto/Cerrado**: Abierto a extensión, cerrado a modificación  
✅ **Responsabilidad única**: Cada decorador tiene una responsabilidad específica  
✅ **Sin herencia múltiple**: Evita problemas de diamante  

---

## Estructura del Patrón en NetHub

### 1. **Interfaz Común: `ContactoDecorador`**

Define los métodos que todos los decoradores deben implementar:

```python
class ContactoDecorador(ABC):
    @abstractmethod
    def obtener_nombre(self) -> str: pass
    
    @abstractmethod
    def obtener_correo(self) -> str: pass
    
    @abstractmethod
    def obtener_empresa(self) -> str: pass
    
    @abstractmethod
    def obtener_descripcion_completa(self) -> str: pass
    
    @abstractmethod
    def obtener_informacion(self) -> Dict: pass
```

### 2. **Clase Base: `ContactoBase`**

Representa un contacto sin decoraciones:

```python
contacto = ContactoBase(
    nombre="Juan Perez",
    correo="juan@example.com",
    empresa="TechCorp"
)
```

Proporciona:
- `obtener_nombre()` → "Juan Perez"
- `obtener_correo()` → "juan@example.com"
- `obtener_empresa()` → "TechCorp"
- `obtener_descripcion_completa()` → Descripción básica
- `obtener_informacion()` → Dict con datos

### 3. **Clase Base Decoradora: `DecoradorContacto`**

Clase abstracta que implementa la lógica de delegación:

```python
class DecoradorContacto(ContactoDecorador):
    def __init__(self, contacto_decorado: ContactoDecorador):
        self._contacto_decorado = contacto_decorado
    
    # Delega todos los métodos al contacto decorado
    def obtener_nombre(self) -> str:
        return self._contacto_decorado.obtener_nombre()
```

### 4. **Decoradores Concretos**

#### **ContactoConEtiquetas**
Agrega clasificación mediante etiquetas:

```python
contacto = ContactoConEtiquetas(contacto_base)
contacto.agregar_etiqueta("VIP")
contacto.agregar_etiqueta("Cliente Frecuente")
```

Métodos adicionales:
- `agregar_etiqueta(etiqueta: str)`
- `remover_etiqueta(etiqueta: str)`
- `obtener_etiquetas() -> List[str]`

#### **ContactoConCalificacion**
Agrega valoración (1-5 estrellas):

```python
contacto = ContactoConCalificacion(contacto_base, calificacion=4)
contacto.establecer_calificacion(5)
print(contacto.obtener_estrellas())  # ★★★★★
```

Métodos adicionales:
- `establecer_calificacion(calificacion: int)`
- `obtener_calificacion() -> int`
- `obtener_estrellas() -> str`

#### **ContactoConHistorial**
Mantiene registro de interacciones:

```python
contacto = ContactoConHistorial(contacto_base)
contacto.agregar_interaccion("Llamada", "Contacto inicial")
contacto.agregar_interaccion("Email", "Propuesta enviada")
```

Métodos adicionales:
- `agregar_interaccion(tipo: str, descripcion: str)`
- `obtener_historial() -> List[Dict]`
- `obtener_ultima_interaccion() -> Dict`

#### **ContactoConPreferencias**
Define preferencias de contacto:

```python
contacto = ContactoConPreferencias(contacto_base)
contacto.establecer_preferencias(
    medio="Email",
    hora="Mañana",
    frecuencia="Semanal"
)
```

Métodos adicionales:
- `establecer_preferencias(medio, hora, frecuencia)`
- `obtener_preferencias() -> Dict`

---

## Ejemplos de Uso

### Ejemplo 1: Contacto Simple
```python
contacto = ContactoBase("Juan", "juan@example.com", "TechCorp")
print(contacto.obtener_descripcion_completa())
# Output: Contacto: Juan | Correo: juan@example.com | Empresa: TechCorp
```

### Ejemplo 2: Contacto con Etiquetas
```python
contacto = ContactoConEtiquetas(contacto)
contacto.agregar_etiqueta("VIP")
contacto.agregar_etiqueta("Cliente")
print(contacto.obtener_descripcion_completa())
# Output: ... | Etiquetas: [VIP, Cliente]
```

### Ejemplo 3: Combinación de Decoradores (Composición)
```python
# Crear base
contacto = ContactoBase("Ana", "ana@example.com", "WebDev")

# Decorar con etiquetas
contacto = ContactoConEtiquetas(contacto, ["Premium"])

# Decorar con calificación
contacto = ContactoConCalificacion(contacto, 5)

# Decorar con historial
contacto = ContactoConHistorial(contacto)
contacto.agregar_interaccion("Reunión", "Negociación")

# Resultado final
print(contacto.obtener_descripcion_completa())
# Output: Contacto: Ana | ... | Etiquetas: [Premium] | 
#         Calificación: ★★★★★ | Interacciones: 1 | Última: Reunión
```

### Ejemplo 4: Obtener Información Completa
```python
info = contacto.obtener_informacion()
# {
#     'nombre': 'Ana',
#     'correo': 'ana@example.com',
#     'empresa': 'WebDev',
#     'etiquetas': ['Premium'],
#     'calificacion': 5,
#     'estrellas': '★★★★★',
#     'historial': [{...}],
#     'total_interacciones': 1,
#     'preferencias': {...},
#     'tipo': 'ContactoConPreferencias'
# }
```

---

## Diagrama de Clases

```
┌─────────────────────────┐
│  ContactoDecorador      │ (Interface)
│  (Abstract)             │
│ ─────────────────────── │
│ - obtener_nombre()      │
│ - obtener_correo()      │
│ - obtener_empresa()     │
│ - obtener_descripcion() │
│ - obtener_informacion() │
└────────────┬────────────┘
             △
             │
    ┌────────┴────────┐
    │                 │
┌───────────────┐  ┌──────────────────────┐
│ ContactoBase  │  │  DecoradorContacto   │
│               │  │  (Abstract)          │
│ - nombre      │  │                      │
│ - correo      │  │ - _contacto_decorado │
│ - empresa     │  │ + (delega métodos)   │
└───────────────┘  └──────────┬───────────┘
                              △
                              │
        ┌─────────────────────┼──────────────────────┬──────────────────┐
        │                     │                      │                  │
┌───────────────────┐  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ ContactoConEtiquetas │ ContactoConCalif │ ContactoConHistorial │ ContactoConPref  │
├───────────────────┤  ├─────────────────┤  ├──────────────────┤  ├──────────────────┤
│ - etiquetas       │  │ - calificacion  │  │ - historial      │  │ - medio          │
│ + agregar_etiqueta│  │ + get_estrellas │  │ + agregar_int    │  │ - hora           │
│ + remover_etiqueta│  │ + set_calif     │  │ + get_ultima_int │  │ - frecuencia     │
└───────────────────┘  └─────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## Casos de Uso

### 1. **Clasificación de Contactos**
```python
# Cliente VIP con máxima calificación
vip = ContactoConEtiquetas(
    ContactoConCalificacion(
        ContactoBase("Carlos", "carlos@..."),
        calificacion=5
    ),
    ["VIP", "Cliente Frecuente"]
)
```

### 2. **Seguimiento de Interacciones**
```python
# Contacto con historial completo
contacto = ContactoConHistorial(ContactoBase(...))
contacto.agregar_interaccion("Llamada", "Seguimiento")
contacto.agregar_interaccion("Email", "Propuesta")
contacto.agregar_interaccion("Reunión", "Cierre")
```

### 3. **Preferencias de Comunicación**
```python
contacto = ContactoConPreferencias(ContactoBase(...))
contacto.establecer_preferencias(
    medio="LinkedIn",
    hora="Tarde",
    frecuencia="Mensual"
)
```

---

## Ventajas en NetHub

1. **Extensibilidad**: Agregar nuevos decoradores sin modificar existentes
2. **Flexibilidad**: Combinar cualquier combinación de decoradores
3. **Separación de Responsabilidades**: Cada decorador maneja una funcionalidad
4. **Reutilización**: Los decoradores se pueden reutilizar en diferentes contextos

---

## Tests

Se proporcionan **42 tests** que validan:

- ✅ Funcionamiento de cada decorador
- ✅ Composición de múltiples decoradores
- ✅ Delegación de métodos
- ✅ Información completa
- ✅ Casos de error

Ejecutar tests:
```bash
python manage.py test contactos.test_decoradores -v 2
```

---

## Conclusión

El patrón Decorator es ideal para NetHub porque permite:

1. Agregar dinámicamente funcionalidades a contactos
2. Mantener flexibilidad sin modificar el código existente
3. Combinar características de forma limpia y ordenada
4. Facilitar el mantenimiento y la expansión futura

Este patrón demuestra la potencia del diseño orientado a objetos y es un ejemplo práctico de los principios SOLID, especialmente el Principio de Abierto/Cerrado (Open/Closed Principle).
