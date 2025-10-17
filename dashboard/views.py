from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64, io, numpy as np


def dash(request):
    context = get_user_profile(request)
    event, grafic_setor = None, []

    if request.method == "POST":
        input_event = request.POST.get("id_evento")
        if not input_event:
            messages.info(request, "Escolha um evento antes de pesquisar.")
            return redirect("dash")
        try:
            event = models.Evento.objects.get(id_evento=input_event)
            setores = models.Setor.objects.filter(evento_id_evento=event)

            total_limite = 0
            total_emitidos = 0
            total_validados = 0

            for sector in setores:
                limite = sector.limite_setor
                emitidos = models.Ingresso.objects.filter(
                    evento=event, setor=sector, status_ingresso='emitido'
                ).count()
                validados = models.Ingresso.objects.filter(
                    evento=event, setor=sector, status_ingresso='validado'
                ).count()
                cancelados = models.Ingresso.objects.filter(
                    evento=event, setor=sector, status_ingresso='cancelado'
                ).count()

                total_limite += limite
                total_emitidos += emitidos
                total_validados += validados

                # --- GERAÇÃO DOS GRÁFICOS DE CADA SETOR ---
                counts = {
                    'Limite do setor': limite,
                    'Emitidos': emitidos,
                    'Validado': validados,
                    'Cancelado': cancelados,
                }

                data = [v for v in counts.values() if v > 0]
                labels = [f'{k}' for k, v in counts.items() if v > 0]
                if not data:
                    continue

                fig, ax = plt.subplots()
                bars = ax.bar(np.arange(len(data)), data,
                              color=['#F8B62F', '#1331A1', '#A2CA02', '#0C0C0C'][:len(data)])
                ax.set_title(f"Setor: {sector.nome_setor}")
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(labels, rotation=30, ha='right')
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                            str(int(bar.get_height())), ha='center', va='bottom')

                buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close(fig)

                grafic_setor.append({
                    "setor": sector.nome_setor,
                    'grafic': base64.b64encode(buf.getvalue()).decode()
                })

            # --- CÁLCULO DE OCUPAÇÃO E ALERTAS ---
            ocup_emitidos = (total_emitidos / total_limite) * 100 if total_limite > 0 else 0
            ocup_validados = (total_validados / total_limite) * 100 if total_limite > 0 else 0

            alert_emitidos, alert_validados = None, None
            color_emitidos, color_validados = "primary", "primary"

            # ALERTAS PARA INGRESSOS EMITIDOS
            if ocup_emitidos >= 100:
                alert_emitidos = "Evento atingiu 100% da ocupação de ingressos emitidos!"
                color_emitidos = "danger"
            elif ocup_emitidos >= 90:
                alert_emitidos = f"O evento chegou a {ocup_emitidos:.1f}% de ingressos emitidos."
                color_emitidos = "warning"

            # ALERTAS PARA INGRESSOS VALIDADOS
            if ocup_validados >= 100:
                alert_validados = "Evento atingiu 100% dos ingressos validados!"
                color_validados = "danger"
            elif ocup_validados >= 90:
                alert_validados = f"O evento chegou a {ocup_validados:.1f}% de ingressos validados."
                color_validados = "warning"

            context.update({
                'event': event,
                'grafic_setor': grafic_setor,
                'ocup_emitidos': ocup_emitidos,
                'ocup_validados': ocup_validados,
                'alert_emitidos': alert_emitidos,
                'alert_validados': alert_validados,
                'color_emitidos': color_emitidos,
                'color_validados': color_validados,
            })

        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("dash")

    context.update({
        'events': models.Evento.objects.all(),
        'event': event,
        'grafic_setor': grafic_setor
    })
    return render(request, "dash.html", context)
