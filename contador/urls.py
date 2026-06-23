from django.urls import path
from . import views


urlpatterns = [
    path("", views.contador, name="contador"),

    path("incluir_contador/", views.incluir_contador, name="incluir_contador"),
    path("configurar_plano/", views.configurar_plano, name="configurar_plano"),
    path("integracao_contabil/", views.integracao_contabil, name="integracao_contabil"),
    path("gerar_arquivos/", views.gerar_arquivos, name="gerar_arquivos"),
    path("fechamento/", views.fechamento, name="fechamento"),

    #
    path("incluir_plano/", views.incluir_plano, name="incluir_plano"),
]