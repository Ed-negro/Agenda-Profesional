from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Contacto
from .forms import ContactoForm

# Vista para la pantalla principal (Lista de contactos)
def lista_contactos(request):
    contactos = Contacto.objects.all()
    busqueda = request.GET.get('busqueda', '')  # Obtiene el término de búsqueda del parámetro GET
    
    # Si hay un término de búsqueda, filtra los contactos por nombre (case-insensitive)
    if busqueda:
        contactos = contactos.filter(
            Q(nombre__icontains=busqueda) |  # Busca en el nombre
            Q(correo__icontains=busqueda) |   # También puede buscar en correo
            Q(empresa__icontains=busqueda)    # Y en la empresa
        )
    
    return render(request, 'contactos/lista.html', {
        'contactos': contactos,
        'busqueda': busqueda  # Pasa el término de búsqueda al template para mostrar en el campo
    })

# Vista para el detalle de un contacto
def detalle_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    return render(request, 'contactos/detalle.html', {'contacto': contacto})

# Vista para el formulario de registro
def crear_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda directamente en la base de datos si pasa las validaciones
            return redirect('lista_contactos')  # Redirige a la pantalla principal
    else:
        form = ContactoForm()
    
    return render(request, 'contactos/formulario.html', {'form': form})

# Vista para editar un contacto existente
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('detalle_contacto', contacto_id=contacto.id)
    else:
        form = ContactoForm(instance=contacto)
    
    return render(request, 'contactos/formulario.html', {'form': form, 'contacto': contacto, 'es_edicion': True})

# Vista para borrar un contacto existente
def borrar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        contacto.delete()
    return redirect('lista_contactos')


# --- Vista de visualización del patrón Decorator ---
from .decoradores import ContactoBase


def visualizar_decorator(request):
    """Vista de ejemplo que envuelve un contacto con decoradores y lo muestra."""
    # Vista simplificada: crear un contacto base y mostrarlo
    contacto = ContactoBase("Ana Pérez", "ana@example.com", "Empresa S.A.")
    return render(request, 'contactos/visualizar_decorator.html', {'contacto': contacto})