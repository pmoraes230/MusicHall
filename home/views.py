from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from . import models

# Create your views here.
def get_user_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = models.Usuario.objects.select_related('Perfil_ID').get(ID_Usuario=user_id)
            return {
                'user_id': user.id,
                'user_name': user.nome_usuario,
                'user_role': user.perfil.nome_perfil,
                'is_authenticated': True
            }
        except models.Usuario.DoesNotExist:
            return {'user_name': "", 'is_authenticated': False}
    return {'user_name': "", 'is_authenticated': False}

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

        if not all([name_user, email_user, cpf_user, id_profile]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(cpf_usuario=cpf_user).exclude(id_usuario=user_id).exists():
            messages.info(request, "CPF já cadastrado no sistema")
            return redirect("register_user")
        
        if models.Usuario.objects.filter(email_usuario=email_user).exclude(id_usuario=user_id).exists():
            messages.info(request, "Email já cadastrado no sistema")
            return redirect("register_user")

        try:
            perfil = models.Perfil.objects.get(id_perfil=id_profile)
        except models.Perfil.DoesNotExist:
            messages.error(request, "perfil não existente")
            return redirect("register_user")
        
        try: 
            user.nome_usuario = name_user
            user.email_usuario = email_user
            user.cpf_usuario = cpf_user
            user.perfil = perfil
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo usuário: {str(ve)}")
            return redirect("update_user", user_id=user_id)

    context.update({
        'user': user,
        'profiles': models.Perfil.objects.all()
    })
    return render(request, "users/update_user.html", context)