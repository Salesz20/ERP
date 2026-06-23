from django.urls import path
from . import views

urlpatterns = [

    path("", views.vendas_opcoes, name="vendas"),
    path("pedidos/", views.vendas_pedidos, name="vendas_pedidos"),
    path("produtos/", views.vendas_produtos, name="vendas_produtos"),
    path("faturamento/", views.vendas_faturamento, name="vendas_faturamento"),
    path("relatorios/", views.vendas_relatorios, name="vendas_relatorios"),

    # vendas opçoes
    path("produtos/novo", views.incluir_produtos, name="incluir_produtos"),
    path("incluir/pedido", views.incluir_pedidos, name="incluir_pedidos"),
    
]
