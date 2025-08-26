from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.contrib.auth import logout
from . import models

# Create your views here.
def get_user_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = models.Usuario.objects.select_related('perfil').get(id_usuario=user_id)
            return {
                'user_id': user.id_usuario,
                'user_name': user.nome_usuario,
                'user_role': user.perfil.nome_perfil,
                'is_authenticated': True
            }
        except models.Usuario.DoesNotExist:
            return {'user_name': "", 'is_authenticated': False}
    return {'user_name': "", 'is_authenticated': False}

def login(request):
    if request.method == "GET":
        return render(request, "login/login.html")
    
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        
        if not all([login, password]):
            messages.info(request, "Insira o seu login e sua senha para entrar no sistema.")
            return redirect("login")
        
        if models.Usuario.objects.filter(email_usuario=login).first() or models.Usuario.objects.filter(cpf_usuario=login).first():
            user = models.Usuario.objects.filter(email_usuario=login).first() or models.Usuario.objects.filter(cpf_usuario=login).first()
            if check_password(password, user.senha_usuario):
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.nome_usuario
                request.session['user_role'] = user.perfil.nome_perfil
                
                messages.success(request, f"Bem vindo {user.nome_usuario}!")
                if user.perfil.nome_perfil == "Validador":
                    return redirect("validador")
                return redirect("home")
            else:
                messages.error(request, "Senha Incorreta.")
                return redirect("login")
        else:
            messages.error(request, "Usuário não encontrado")
            return redirect("login")
        
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect("login")
        
def home(request):
    context = get_user_profile(request)
    context['events'] = models.Evento.objects.all()
    return render(request, "home/home.html", context)

def details_event(request, id_event):
    context = get_user_profile(request)
    
    event = models.Evento.objects.get(id_evento=id_event)
    sectors = models.Setor.objects.filter(evento_id_evento=event)
    search_client = []
    client = None
    
    if request.method == "POST" and "search_client" in request.POST:
        input_search = request.POST.get("search_client")
        if input_search:
            search_client = models.Cliente.objects.filter(
                nome_cliente__icontains=input_search
            )[:10]
            if not search_client:
                messages.info(request, "Cliente não encontrado no sistema.")
                return redirect("deteils_event", id_event=id_event)
        else:
            messages.info(request, "Informe o nome do cliente")
            return redirect("deteils_event", id_event=id_event)
    
    context.update({
        'event': event
    })
    return render(request, "event/deteils_event.html", context)
            
def list_user(request):
    context = get_user_profile(request)
    context['users'] = models.Usuario.objects.all()
    return render(request, "users/list_users.html", context)

def register_user(request):
    context = get_user_profile(request)
    context['profiles'] = models.Perfil.objects.all()

    if request.method == "POST":
        name_user = request.POST.get("nome_usuario")
        email_user = request.POST.get("email_usuario")
        cpf_user = request.POST.get("cpf_usuario")
        id_profile = request.POST.get("perfil_usuario")
        password = request.POST.get("password_usuario")
        conf_password = request.POST.get("confirm_password")

        if not all([name_user, email_user, cpf_user, id_profile, password, conf_password]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(cpf_usuario=cpf_user).exists():
            messages.info(request, "CPF já cadastrado no sistema")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(email_usuario=email_user).exists():
            messages.info(request, "Email já cadastrado no sistema")
            return redirect("register_user")
        
        if password != conf_password:
            messages.info(request, "Senha não são iguais")
            return redirect("register_user")

        heshers = make_password(password)

        try:
            perfil = models.Perfil.objects.get(id_perfil=id_profile)
        except models.Perfil.DoesNotExist:
            messages.error(request, "perfil não existente")
            return redirect("register_user")

        try:
            new_user = models.Usuario.objects.create(
                nome_usuario=name_user,
                email_usuario=email_user,
                cpf_usuario=cpf_user, 
                senha_usuario=heshers,
                perfil=perfil
            )
            new_user.full_clean()
            new_user.save()

            messages.success(request, f"Usuário {new_user.nome_usuario} cadastrado com sucesso")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo usuário: {str(ve)}")
            return redirect("register_user")

    return render(request, "users/register_user.html", context)

def update_user(request, user_id):
    context = get_user_profile(request)
    user = models.Usuario.objects.get(id_usuario=user_id)

    if request.method == "POST":
        name_user = request.POST.get("nome_usuario")
        email_user = request.POST.get("email_usuario")
        cpf_user = request.POST.get("cpf_usuario")
        id_profile = request.POST.get("perfil_usuario")
        print(cpf_user)

        if not all([name_user, email_user, cpf_user, id_profile]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("update_user", user_id=user_id)
        
        if models.Usuario.objects.filter(cpf_usuario=cpf_user).exclude(id_usuario=user_id).exists():
            messages.info(request, "CPF já cadastrado no sistema")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(email_usuario=email_user).exclude(id_usuario=user_id).exists():
            messages.info(request, "Email já cadastrado no sistema")
            return redirect("update_user", user_id=user_id)

        try:
            perfil = models.Perfil.objects.get(id_perfil=id_profile)
        except models.Perfil.DoesNotExist:
            messages.error(request, "perfil não existente")
            return redirect("update_user", user_id=user_id)
        
        try: 
            user.nome_usuario = name_user
            user.email_usuario = email_user
            user.cpf_usuario = cpf_user
            user.perfil = perfil
            
            user.full_clean()
            user.save()
            
            messages.success(request, f"Cadastro do usuário {user.nome_usuario} atualizado.")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo usuário: {str(ve)}")
            return redirect("update_user", user_id=user_id)

    context.update({
        'user': user,
        'profiles': models.Perfil.objects.all()
    })
    return render(request, "users/update_user.html", context)