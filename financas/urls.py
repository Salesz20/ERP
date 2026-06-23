from django.urls import path
from . import views

app_name = "financas"

urlpatterns = [
    path("", views.financas, name="financas"),

    path("contas/", views.contas_bancarias, name="contas"),
    path("pessoas/", views.clientes_fornecedores, name="pessoas"),
    path("contas-pagar", views.contas_pagar, name="contas_pagar"),
    path("contas-receber", views.contas_receber, name="contas_receber"),
    path("baixa/", views.baixa_financeira, name="baixa"),
    path("conciliacao/", views.conciliacao_bancaria, name="conciliacao"),

    #
    path("incluir/contas-pagar", views.incluir_contas_pagar, name="incluir_contas_pagar"),
    path("incluir/contas-receber", views.incluir_contas_receber, name="incluir_contas_receber"),
]
