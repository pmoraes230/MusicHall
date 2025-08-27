from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models

# Create your views here.
def validation(request):
    context = get_user_profile(request)
    if request.method == "POST":
        input_ticket = request.POST.get("ticket_input").replace(" ", "")
        if not input_ticket:
            messages.info(request, "Informe o código de validação do ingresso.")
            return redirect("validador")
        try:
            ticket = models.Ingresso.objects.get(id_ingresso=input_ticket)
            if ticket.status_ingresso == "validado":
                messages.info(request, "Ingresso já com status de validado. Valide outro ingresso.")
                return redirect("validador")
            elif ticket.status_ingresso == "cancelado":
                messages.info(request, "Ingresso com status de cancelado. Valide outro ingresso.")
                return redirect("validador")
            elif ticket.status_ingresso == "emitido":
                ticket.status_ingresso = "validado"
                ticket.save()
                messages.success(request, "Ingresso validado com sucesso. Bom show!")
                return redirect("validador")
        except models.Ingresso.DoesNotExist:
            messages.error(request, "Ingresso não encontrado")
            return redirect("validador")
    return render(request, "validador.html", context)