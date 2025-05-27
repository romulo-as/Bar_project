# bar/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Coquetel, Cliente, Servico, Pacote, Funcionario, Reserva, Fornecedor, Produto, Evento
from .forms import CoquetelForm, ClienteForm 

# VIEWS BASEADAS EM CLASSE (para Coquetel) 

# Requisito: 1 Classes Listar
class CoquetelListView(ListView):
    model = Coquetel
    template_name = 'bar/coquetel_list.html'
    context_object_name = 'coqueteis'
    paginate_by = 5 # Exemplo de paginação

# Requisito: 1 Classes Detalhar
class CoquetelDetailView(DetailView):
    model = Coquetel
    template_name = 'bar/coquetel_detail.html'
    context_object_name = 'coquetel'

# Requisito: 1 Classes Criar
class CoquetelCreateView(CreateView):
    model = Coquetel
    form_class = CoquetelForm
    template_name = 'bar/coquetel_form.html'
    success_url = reverse_lazy('coquetel_list') # Redireciona para a lista após criar

# Requisito: 1 Classes Editar
class CoquetelUpdateView(UpdateView):
    model = Coquetel
    form_class = CoquetelForm
    template_name = 'bar/coquetel_form.html'
    success_url = reverse_lazy('coquetel_list') # Redireciona para a lista após editar

# Requisito: 1 Classes Deletar
class CoquetelDeleteView(DeleteView):
    model = Coquetel
    template_name = 'bar/coquetel_confirm_delete.html'
    success_url = reverse_lazy('coquetel_list') # Redireciona para a lista após deletar

# VIEWS BASEADAS EM FUNÇÃO (para Cliente)

# Requisito: 1 Método Listar
def cliente_list(request):
    clientes = Cliente.objects.all()
    # Exemplo de filtro (simples)
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(nome__icontains=query)
    
    context = {'clientes': clientes}
    return render(request, 'bar/cliente_list.html', context)

# Requisito: 1 Método Detalhar
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    context = {'cliente': cliente}
    return render(request, 'bar/cliente_detail.html', context)

# Requisito: 1 Método Criar
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    context = {'form': form, 'titulo': 'Criar Novo Cliente'}
    return render(request, 'bar/cliente_form.html', context)

# Requisito: 1 Método Editar
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    context = {'form': form, 'titulo': f'Editar Cliente: {cliente.nome}'}
    return render(request, 'bar/cliente_form.html', context)

# Requisito: 1 Método Deletar
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    context = {'cliente': cliente}
    return render(request, 'bar/cliente_confirm_delete.html', context)