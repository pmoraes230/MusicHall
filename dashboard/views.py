from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64, io, numpy as np

# Create your views here.
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
            for sector in models.Setor.objects.filter(evento_id_evento=event):
                counts = {
                    'Limite do setor': sector.limite_setor,
                    'Emitidos': models.Ingresso.objects.filter(evento=event, setor=sector, status_ingresso='emitido').count(),
                    'Validado': models.Ingresso.objects.filter(evento=event, setor=sector, status_ingresso='validado').count(),
                    'Cancelado': models.Ingresso.objects.filter(evento=event, setor=sector, status_ingresso='cancelado').count(),
                }
                
                data = [v for v in counts.values() if v>0]
                labels = [f'{k}' for k,v in counts.items() if v>0]
                if not data: 
                    continue
                
                fig, ax = plt.subplots()
                bars = ax.bar(np.arange(len(data)), data, color=['#F8B62F', '#1331A1', '#A2CA02', '#0C0C0C'][:len(data)])
                ax.set_title(f"Setor: {sector.nome_setor}")
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(labels, rotation=30, ha='right')
                for bar in bars:
                    ax.text(bar.get_x(), bar.get_width()/2 + bar.get_height(), str(int(bar.get_height())),
                            ha='center', va='bottom')
                    
                buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close(fig)
                
                grafic_setor.append({"setor": sector.nome_setor, 'grafic': base64.b64encode(buf.getvalue()).decode()})
                
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("dash")
    
    context.update({
        'events': models.Evento.objects.all(),
        'event': event,
        'grafic_setor': grafic_setor
    })
    return render(request, "dash.html", context)