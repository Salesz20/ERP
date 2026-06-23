from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def contador(request):
    return render(request, "crm/contador.html")

@login_required
def incluir_contador(request):
    return render(request, "crm/contador_opcoes/incluir_contador.html")

@login_required
def integracao_contabil(request):
    return render(request, "crm/contador_opcoes/integracao_contabil.html")

@login_required
def configurar_plano(request):
    return render(request, "crm/contador_opcoes/configurar_plano.html")

@login_required
def gerar_arquivos(request):
    return render(request, "crm/contador_opcoes/gerar_arquivos.html")

@login_required
def fechamento(request):
    return render(request, "crm/contador_opcoes/fechamento.html")

@login_required
def incluir_plano(request):
    return render(request, "crm/contador_opcoes/incluir_plano.html")