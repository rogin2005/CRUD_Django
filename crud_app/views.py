import bcrypt
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging

API_URL = "https://minha-api-ten.vercel.app/usuarios"

logger = logging.getLogger(__name__)

def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')

def listar_usuarios(request):
    try:
        response = requests.get(f"{API_URL}/")
        response.raise_for_status()
        usuarios = response.json()
    except requests.exceptions.RequestException as e:
        usuarios = []
        print(f"Erro ao buscar usuarios: {e}")
        
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        response = requests.get('https://minha-api-ten.vercel.app/usuarios')
        
        if response.status_code == 200:
            usuarios = response.json()
            
            for usuario in usuarios:
                if usuario['email'] == email:
                    
                    if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
                        
                        return redirect('/usuarios/')
                    else:
                        return render(request, 'login.html', {'error': 'Senha incorreta'})            
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
        else:
            return render(request, 'login.html', {'error': 'Erro ao conectar com a API'})
    
    return render(request, 'login.html')

def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        
        response = requests.post('https://minha-api-ten.vercel.app/usuarios', json={
            'nome': nome,
            'email': email,
            'senha': senha
        })

        if response.status_code == 201:  # Cadastro bem-sucedido
            messages.success(request, 'Cadastro realizado com sucesso!')
            return render(request, 'cadastrar.html', {'success_message': 'Cadastro realizado com sucesso!'})
        else:  # Erro no cadastro
            messages.error(request, 'Erro ao realizar cadastro. Tente novamente.')
            return render(request, 'cadastrar.html', {'success_message': ''})

    return render(request, 'cadastrar.html')

def atualizar_usuario(request, id):
    
    logger.info(f"Acessando a view de atualização com ID: {id}")
    print(f"ID recebido: {id}")
    
    api_url = f"{settings.API_BASE_URL}/usuarios/{id}/"

    if request.method == "GET":
        # Busca os dados do usuário na API para pré-preencher o formulário
        response = requests.get(api_url)
        if response.status_code == 200:
            usuario = response.json()  # Dados do usuário
            return render(request, 'atualizar_usuario.html', {'usuario': usuario})
        else:
            messages.error(request, "Erro ao carregar dados do usuário.")
            return redirect('listar_usuarios')

    elif request.method == "POST":
        # Captura os dados enviados no formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')

        # Payload para enviar na requisição
        payload = {
            "nome": nome,
            "email": email
        }

        # Faz a requisição PUT para atualizar o usuário
        response = requests.put(api_url, json=payload)

        # Verifica a resposta
        if response.status_code == 200:
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect('listar_usuarios')
        else:
            messages.error(request, f"Erro ao atualizar usuário: {response.json().get('detail', 'Erro desconhecido')}")
            return redirect('atualizar_usuario', id=id)

    # Caso não seja GET ou POST, redireciona
    messages.error(request, "Método inválido.")
    return redirect('listar_usuarios')
    
def excluir_usuario(request, id):
    if request.method == "POST":
        # URL para a API de exclusão de usuários
        api_url = f"{settings.API_BASE_URL}/usuarios/{id}/"  # Certifique-se de ter `API_BASE_URL` configurado

        # Faz a requisição DELETE para a API
        response = requests.delete(api_url)

        # Verifica se a exclusão foi bem-sucedida
        if response.status_code == 204:  # Código 204 significa "No Content", ou seja, excluído com sucesso
            messages.success(request, "Usuário excluído com sucesso!")
        else:
            messages.error(request, f"Falha ao excluir usuário: {response.json().get('detail', 'Erro desconhecido')}")

        return redirect('listar_usuarios')

    messages.error(request, "Método inválido. Use o botão de exclusão para deletar um usuário.")
    return redirect('listar_usuarios')