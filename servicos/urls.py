from django.urls import path
from . import views


urlpatterns = [
    path('clientes/', views.clientes, name='clientes'),

    path('cadastrar-servicos/', views.cadastrar_servicos, name='cadastrar_servicos'),
    path('oportunidade-servicos/', views.oportunidade_servicos, name='oportunidade_servicos'),
    path('servicos-recorrentes/', views.servicos_recorrentes, name='servicos_recorrentes'),

    path('servicos/', views.servicos_opcoes, name='servicos_opcoes'),

    # Criar novo cliente
    path('detalhes-clientes/', views.detalhes_clientes, name='detalhes_clientes'),

    # Editar cliente existente
    path('detalhes-clientes/<int:empresa_id>/', views.detalhes_clientes, name='editar_cliente'),

     # Criar novo serviço
    path('servicos/detalhes-servicos/', views.detalhes_servicos, name='detalhes_servicos'),
    # Editar serviço existente
    path('servicos/detalhes-servicos/<int:servico_id>/', views.detalhes_servicos, name='editar_servico'),
    
    path('nova-os/', views.adicionar_ordem_servico, name='adicionar_ordem_servico'),
    path('ordem-servico/editar/<int:os_id>/', views.adicionar_ordem_servico, name='editar_ordem_servicos'),

    path('ordem-servico/excluir/<int:os_id>/', views.excluir_ordem_servico, name='excluir_ordem_servico'),


]
