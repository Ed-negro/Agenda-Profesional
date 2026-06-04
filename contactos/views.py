from django.shortcuts import get_object_or_404, redirect, render
from .models import Contacto
from .forms import ContactoForm

# Vista para la pantalla principal (Lista de contactos)
def lista_contactos(request):
    contactos = Contacto.objects.all()  # Consulta todos los contactos en SQLite
    return render(request, 'contactos/lista.html', {'contactos': contactos})

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

# Vista para borrar un contacto existente
def borrar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        contacto.delete()
    return redirect('lista_contactos')