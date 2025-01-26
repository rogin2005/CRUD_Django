from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('login/', views.login_view, name='login'),
    path("cadastrar/", views.cadastrar_usuario, name="cadastrar"),
    path('usuarios/atualizar/<int:id>/', views.atualizar_usuario, name='atualizar_usuario'),
    path('usuarios/excluir/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
]