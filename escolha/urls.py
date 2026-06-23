from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

app_name = 'escolha'

urlpatterns = [
    path("servicos/", include("servicos.urls")),
    path("vendas/", include("vendas.urls")),
    path('compras/', include('compras.urls')),    # COMPRAS
    path("financas/", include("financas.urls")),
    path("contador/", include("contador.urls")),


    # ------------------------------
    # PÁGINAS PRINCIPAIS
    # ------------------------------
    path('', views.crm_home, name='crm_home'),
    path('vendas/', views.vendas_home, name='vendas_home'),
    path('servicos/', views.servicos_home, name='servicos_home'),
    path('compras/', views.compras_home, name='compras_home'),
    path('financas/', views.financas_home, name='financas_home'),
    path('contador/', views.contador_home, name='contador_home'),

    # ------------------------------
    # CRM
    # ------------------------------
    path('contas/', views.contas, name='contas'),
    path('contas/<int:empresa_id>/', views.detalhes_empresa, name='detalhes_empresa'),
    path('contatos/', views.contatos, name='contatos'),
    path('contatos/<int:contato_id>/', views.detalhes_contato, name='detalhes_contato'),
    path('oportunidades/', views.oportunidades, name='oportunidades'),
    path('tarefas/', views.tarefas_view, name='tarefas'),


    # ------------------------------
    # OPORTUNIDADES
    # ------------------------------
    
    # Criar nova oportunidade para um contato
    path('oportunidade/<int:contato_id>/detalhes/', views.detalhes_oportunidade, name='detalhes_oportunidade'),

    # Editar oportunidade existente
    path('oportunidade/<int:contato_id>/detalhes/<int:oportunidade_id>/', views.detalhes_oportunidade, name='detalhes_oportunidade'),

    # ------------------------------
    # Criar tarefas 
    # ------------------------------
    
    path('tarefas/create/', views.create_task, name='create_task'),
    # Listar tarefas por oportunidade
    path('tarefas/list_by_opportunity/', views.list_tasks_by_opportunity, name='list_tasks_by_opportunity'),
    # Marcar como concluída
    path('tarefas/mark_done/', views.mark_task_done, name='mark_task_done'),
    # tarefas popup
    path("tarefas/popup/<int:pk>/", views.popup_tarefas, name="popup_tarefas"),
    # Página kanban de tarefas por oportunidade
    path('tarefas/<int:pk>/', views.tarefas_view, name='view_tarefas'),


    # novas endpoints para editar/excluir/mover via AJAX
    path('tarefas/update/', views.update_task, name='update_task'),       # POST: {id, description, due_date}
    path('tarefas/delete/', views.delete_task, name='delete_task'),       # POST: {id}
    path('tarefas/move/', views.move_task, name='move_task'),             # POST: {id, column}


    # Nova URL para o kanban
    path('oportunidades/kanban/', views.oportunidades_view, name='oportunidades_kanban'),

    # ------------------------------
    # EXCLUSÕES
    # ------------------------------
    path('contas/excluir/<int:empresa_id>/', views.excluir_empresa, name='excluir_empresa'),
    path('contatos/excluir/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),
    path('oportunidade/excluir/<int:oportunidade_id>/', views.excluir_oportunidade, name='excluir_oportunidade'),
    
    # mudar card
    path('update_oportunidade_stage/', views.update_oportunidade_stage, name='update_oportunidade_stage'),
]

# ------------------------------
# MÍDIA EM MODO DEBUG
# ------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
