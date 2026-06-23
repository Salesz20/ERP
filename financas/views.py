from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def financas(request):
    return render(request, "crm/financas.html")

@login_required
def contas_bancarias(request):
    return render(request, "crm/financas_opcoes/contas.html")

@login_required
def clientes_fornecedores(request):
    return render(request, "crm/financas_opcoes/pessoas.html")

@login_required
def contas_pagar(request):
    return render(request, "crm/financas_opcoes/contas_pagar.html")

@login_required
def contas_receber(request):
    return render(request, "crm/financas_opcoes/contas_receber.html")

@login_required
def baixa_financeira(request):
    return render(request, "crm/financas_opcoes/baixa.html")

@login_required
def conciliacao_bancaria(request):
    return render(request, "crm/financas_opcoes/conciliacao.html")

@login_required
def incluir_contas_pagar(request):
    return render(request, "crm/financas_opcoes/incluir_contas_pagar.html")

@login_required
def incluir_contas_receber(request):
    return render(request, "crm/financas_opcoes/incluir_contas_receber.html")