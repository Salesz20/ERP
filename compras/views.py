from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def compras(request):
    return render(request, "crm/compras.html")


@login_required
def compras_fornecedores(request):
    return render(request, "crm/compras_opcoes/fornecedores.html")


@login_required
def compras_produtos(request):
    return render(request, "crm/compras_opcoes/produtos.html")


@login_required
def compras_receber(request):
    return render(request, "crm/compras_opcoes/receber.html")


@login_required
def compras_estoque(request):
    return render(request, "crm/compras_opcoes/estoque.html")

@login_required
def incluir_fornecedores(request):
    return render(request, "crm/compras_opcoes/incluir_fornecedores.html")

