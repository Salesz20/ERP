from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def vendas_opcoes(request):
    return render(request, "crm/vendas.html")


@login_required
def vendas_pedidos(request):
    return render(request, "crm/vendas_opcoes/vendas_pedidos.html")


@login_required
def vendas_produtos(request):
    return render(request, "crm/vendas_opcoes/vendas_produtos.html")


@login_required
def vendas_faturamento(request):
    return render(request, "crm/vendas_opcoes/vendas_faturamento.html")


@login_required
def vendas_relatorios(request):
    return render(request, "crm/vendas_opcoes/vendas_relatorios.html")

@login_required
def incluir_produtos(request):
    return render(request, "crm/vendas_opcoes/incluir_produtos.html")

@login_required
def incluir_pedidos(request):
    return render(request, "crm/vendas_opcoes/incluir_pedidos.html")
