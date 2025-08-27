from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import logout
from . import models
import uuid
import pdfkit

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
    
    if request.method == "POST" and "search" in request.POST:
        input_search = request.POST.get("search_client")
        print(input_search)
        if input_search:
            search_client = models.Cliente.objects.filter(
                Q(nome_cliente__icontains=input_search)
            )[:10]
            if not search_client:
                messages.info(request, "Cliente não encontrado no sistema.")
                return redirect("deteils_event", id_event=id_event)
            else:
                messages.success(request, f"{search_client.count()} clientes encontrados")
        else:
            messages.info(request, "Informe o nome do cliente")
            return redirect("deteils_event", id_event=id_event)
        
    if request.method == 'POST' and "client_selected" in request.POST:
        id_client = request.POST.get("client_id")
        request.session['id_client'] = id_client
        if id_client:
            client = models.Cliente.objects.get(id_cliente=id_client)
            messages.success(request, f"Cliente {client.nome_cliente} selecionado")
    
    context.update({
        'event': event,
        'search_client': search_client,
        'client': client,
        'sectors': sectors
    })
    return render(request, "event/deteils_event.html", context)

def buy_ticket(request, id_event):
    context = get_user_profile(request)
    
    event = models.Evento.objects.get(id_evento=id_event)
    sectors = models.Setor.objects.filter(evento_id_evento=event)
    search_client = []
    client = None
    
    if request.method == "POST" and "buy_ticket" in request.POST:
        id_client = request.session.get("id_client")
        try:
            client = models.Cliente.objects.get(id_cliente=id_client)
        except models.Cliente.DoesNotExist:
            messages.error(request, "Cliente não encontrado")
            return redirect("buy_client", id_event=id_event)
        
        id_sector = request.POST.get("sectors")
        amount = int(request.POST.get("amount"), 0)
        
        if not all([id_sector, amount]):
            messages.info(request, "Informe o setor e a quantidade de ingressos que deseje adquirir.")
            
        try:
            sector = models.Setor.objects.get(id_setor=id_sector)
        except models.Setor.DoesNotExist:
            messages.error(request, "Setor não encontrado")
            
        if amount == 0:
            messages.info(request, "Insira a quantidade de ingresso desejados")
        elif amount >= 10:
            messages.info(request, "Quantidade de ingresso por cliente é de 10 unidades.")
        else:
            tickets = []
            for ticket in range(amount):
                ticket = models.Ingresso.objects.create(
                    cliente=client,
                    evento=event,
                    setor=sector,
                    id_ingresso=str(uuid.uuid4()),
                    data_emissao_ingresso=timezone.now(),
                    status_ingresso='emitido'
                )
                ticket.full_clean()
                ticket.save()
            
            sector.limite_setor -= 1
            sector.save()    
            tickets.append(tickets)
            
            messages.success(request, f"Ingressos para o cliente {client.nome_cliente} emitidos")
            return redirect("ticket_generate", id_ticket=ticket.id_ingresso)
        
            # tickets = [ticket for ticket in tickets]
            # return reverse("tickets_list")
            
    
    context.update({
        'event': event,
        'search_client': search_client,
        'client': client,
        'sectors': sectors
    })
    return render(request, "event/deteils_event.html", context)

def list_tickets(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id_evento=id_event)
    context['event'] = event
    context['tickets'] = models.Ingresso.objects.filter(evento=event)
    
    return render(request, "event/list_tickets.html", context)

def register_event(request):
    context = get_user_profile(request)
    
    if request.method == "POST":
        nome = request.POST.get("nome_usuario")
        limite_pessoas = request.POST.get("limite_pessoas")
        data_evento = request.POST.get("date_event")
        horario_evento = request.POST.get("time_event")
        imagem_evento = request.FILES.get("image_event")
        descricao_evento = request.POST.get("descricao_event")
        
        if not all([nome, limite_pessoas, data_evento, horario_evento, imagem_evento, descricao_evento]):
            messages.info(request, "Todos os campos são de preechimento obrigatórios.")
            return redirect("register_event")
        
        if models.Evento.objects.filter(data_evento=data_evento, horario_evento=horario_evento).exists():
            messages.info(request, "Data e horario já reservado com outro evento")
            return redirect("register_event")
        
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "Usuário não autenticado")
            return redirect("login")
        
        try:
            user = models.Usuario.objects.get(id_usuario=user_id)
        except models.Usuario.DoesNotExist:
            messages.info(request, "Usuário não autenticado.")
            return redirect("register_event")
        
        try:
            new_event = models.Evento.objects.create(
                nome_evento=nome,
                limitepessoas_evento=limite_pessoas,
                data_evento=data_evento,
                horario_evento=horario_evento,
                descricao_evento=descricao_evento,
                imagem_evento=imagem_evento,
                usuario_id_usuario=user
            )
            
            new_event.full_clean()
            new_event.save()
            
            messages.success(request, f"Evento {new_event.nome_evento} criado.")
            return redirect("deteils_event", id_event=new_event.id_evento)
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar o evento: {str(ve)}")
            return redirect("register_event")
        
        
    return render(request, "event/register_event.html", context)

def update_event(request, id_event):
    context = get_user_profile(request)
    
    try:
        event = models.Evento.objects.get(id_evento=id_event)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("home")
    
    if request.method == "POST":
        nome = request.POST.get("nome_usuario")
        limite_pessoas = request.POST.get("limite_pessoas")
        data_evento = request.POST.get("date_event")
        horario_evento = request.POST.get("time_event")
        imagem_evento = request.FILES.get("image_event")
        descricao_evento = request.POST.get("descricao_event")
        
        if not all([nome, limite_pessoas, data_evento, horario_evento, descricao_evento]):
            messages.info(request, "Todos os campos são de preechimento obrigatórios.")
            return redirect("update_event", id_event=id_event)
        
        if models.Evento.objects.filter(data_evento=data_evento, horario_evento=horario_evento).exclude(id_evento=id_event).exists():
            messages.info(request, "Data e horario já reservado com outro evento")
            return redirect("update_event", id_event=id_event)
    
        try:
            event.nome_evento = nome
            event.limitepessoas_evento = limite_pessoas
            event.data_evento = data_evento
            event.horario_evento = horario_evento
            if imagem_evento:
                event.imagem_evento = imagem_evento
            event.descricao_evento = descricao_evento
            
            event.full_clean()
            event.save()
            
            messages.success(request, f"Cadastro do evento {event.nome_evento} atualizado com sucesso")
            return redirect("deteils_event", id_event=event.id_evento)
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar o evento: {str(ve)}")
            return redirect("update_event", id_event=id_event)
    
    context['event'] = event
    return render(request, "event/update_event.html", context)

def delete_event(request, id_event):
    try:
        event = models.Evento.objects.get(id_evento=id_event)
        if request.method == "POST":
            event.delete()
            messages.success(request, "Evento apagado do sistema.")
            return redirect("home")
        context = {
            'event': event,
            **get_user_profile(request)
        }
        return render(request, "event/delete_event.html", context)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado.")
        return redirect("home")
    
def list_sector(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id_evento=id_event)
    context['sectors'] = models.Setor.objects.filter(evento_id_evento=event)
    context['event'] = event
    
    return render(request, "sector/list_sector.html", context)

def register_sector(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id_evento=id_event)
    
    if request.method == "POST":
        nome_setor = request.POST.get("nome_setor")
        limite_setor = request.POST.get("limite_setor")
        preco_setor = request.POST.get("preco_setor")
        id_evento = request.POST.get("id_evento")
        
        if not all([nome_setor, limite_setor, preco_setor, id_evento]):
            messages.info(request, "Preechimento de campos são obrigatórios.")
            return redirect("register_sector", id_event=id_event)
        
        try:
            evento = models.Evento.objects.get(id_evento=id_evento)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("register_sector", id_event=id_event)
        
        try:
            new_sector = models.Setor.objects.create(
                nome_setor=nome_setor,
                limite_setor=limite_setor,
                preco_setor=preco_setor,
                evento_id_evento=evento
            )
            new_sector.full_clean()
            new_sector.save()
            
            messages.success(request, f"Setor {new_sector.nome_setor} criado com sucesso.")
            return redirect("list_sector", id_event=id_event)
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar o setor: {str(ve)}")
            return redirect("register_sector", id_event=id_event)
    
    context.update({
        'event': event,
        'events': models.Evento.objects.all()
    })
    return render(request, "sector/register_sector.html", context)

def update_sector(request, id_sector):
    context = get_user_profile(request)
    sector = models.Setor.objects.get(id_setor=id_sector)
    
    if request.method == "POST":
        nome_setor = request.POST.get("nome_setor")
        limite_setor = request.POST.get("limite_setor")
        preco_setor = request.POST.get("preco_setor")
        id_evento = request.POST.get("id_evento")
    
        if not all([nome_setor, limite_setor, preco_setor, id_evento]):
            messages.info(request, "Preechimento de campos são obrigatórios.")
            return redirect("update_sector", id_sector=id_sector)
        
        try:
            evento = models.Evento.objects.get(id_evento=id_evento)
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("register_sector", id_event=id_sector)
        
        try:
            sector.nome_setor = nome_setor
            sector.limite_setor = limite_setor
            sector.preco_setor = preco_setor
            sector.evento_id_evento = evento
            
            sector.full_clean()
            sector.save()
            
            messages.success(request, f"{sector.nome_setor} atualizado com sucesso.")
            return redirect("list_sector", id_event=sector.evento_id_evento.id_evento)
            
        except ValueError as ve:
            messages.error(request, f"Setor não encontrado: {str(ve)}")
            return redirect("register_sector", id_event=id_sector)
    
    context.update({
        'sector': sector,
        'events': models.Evento.objects.all()
    })
    return render(request, "sector/update_sector.html", context)

def delete_sector(request, id_sector):
    try:
        sector = models.Setor.objects.get(id_setor=id_sector)
        if request.method == "POST":
            sector.delete()
            messages.success(request, "Setor apagado com sucesso!")
            return redirect("home")
        context = {
            'sector': sector,
            **get_user_profile(request)
        }
        return render(request, "sector/delete_sector.html", context)
    except models.Setor.DoesNotExist:
        messages.error(request, "Setor não encontrado")
        return redirect("home")
    
def register_client(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id_evento=id_event)
    context['event'] = event
    
    if request.method == "POST":
        nome_usuario = request.POST.get("nome_usuario")
        email_usuario= request.POST.get("email_usuario")
        cpf_usuario = request.POST.get("cpf_usuario")
        
        if not all([nome_usuario, email_usuario, cpf_usuario]):
            messages.info(request, "Preenchimento de campos são obrigatórios")
            return redirect("register_client", id_event=event.id_evento)
        
        if models.Cliente.objects.filter(cpf_cliente=cpf_usuario).exists():
            messages.info(request, "CPF já cadastrado no sistema")
            return redirect("register_client", id_event=event.id_evento)
        
        if models.Cliente.objects.filter(email_cliente=email_usuario).exists():
            messages.info(request, "Email já cadastrado no sistema")
            return redirect("register_client", id_event=event.id_evento)
        
        try:
            new_client = models.Cliente.objects.create(
                nome_cliente=nome_usuario,
                cpf_cliente=cpf_usuario,
                email_cliente=email_usuario
            )
            new_client.full_clean()
            new_client.save()
            
            messages.success(request, f"Cliente {new_client.nome_cliente} cadastrado com sucesso.")
            return redirect("deteils_event", id_event=event.id_evento)
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar o cliente no sistema: {str(ve)}")
            
            
    
    return render(request, "event/register_client.html", context)

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

def delete_user(request, id_user):
    try:
        user = models.Usuario.objects.get(id_usuario=id_user)
        if request.method == "POST":
            user.delete()
            return redirect("list_user")
        context = {
            'user': user,
            **get_user_profile(request)
        }
        return render(request, "users/delete_user.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("home")
    
def generate_ticket(request, id_ticket):
    ticket = get_object_or_404(models.Ingresso, id_ingresso=id_ticket)
    page_html = render_to_string("event/ticket.html", {'ticket': ticket})
    configuration = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    
    options = {
        'page-size': 'A5',
        'page-width': '440mm',
        'page-height': '44mm',
        'encoding': "UTF-8",
    }
    
    try:
        pdf = pdfkit.from_string(page_html, False, configuration=configuration, options=options)
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="ingresso_no_show_{ticket.evento.nome_evento}_cliente_{ticket.cliente.nome_cliente}.pdf"'
        response.write(pdf)
        
        return response
    except ValueError as ve:
        return HttpResponse(f"Erro ao emitir o pdf: {str(ve)}")
        