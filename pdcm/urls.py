from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static

# ---- View Selecionar ----
@login_required
def selecionar(request):
    if request.method == 'POST':
        escolha = request.POST.get('escolha')
        caminhos = {
            'crm': '/crm/',
            'vendas': '/crm/vendas/',
            'servicos': '/crm/servicos/',
            'compras': '/crm/compras/',
            'financas': '/crm/financas/',
            'contador': '/crm/contador/',
        }
        return redirect(caminhos.get(escolha, '/crm/'))
    return render(request, 'crm/selecionar.html')

# ---- URLs do projeto ----
urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Seleção após login
    path('crm/selecionar/', selecionar, name='selecionar'),

    # CRM (agora usa o app 'escolha')
    path('crm/', include('escolha.urls')),

    # Reset de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='crm/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='crm/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='crm/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='crm/password_reset_complete.html'), name='password_reset_complete'),

    # Raiz redireciona para login
    path('', RedirectView.as_view(url='/login/', permanent=False)),
]

# ---- Configuração para servir arquivos de mídia durante o desenvolvimento ----
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
