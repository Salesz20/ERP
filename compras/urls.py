from django.urls import path
from . import views

app_name = "compras"

urlpatterns = [
    path("", views.compras, name="compras"),
    path("fornecedores/", views.compras_fornecedores, name="fornecedores"),
    path("produtos/", views.compras_produtos, name="produtos"),
    path("receber/", views.compras_receber, name="receber"),
    path("estoque/", views.compras_estoque, name="estoque"),

    # compras opções
    path("incluir/fornecedores", views.incluir_fornecedores, name="incluir_fornecedores"),
]
