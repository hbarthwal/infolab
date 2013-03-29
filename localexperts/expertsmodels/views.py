# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context

def heatmap(request):
    template = loader.get_template('heatmap.html')
    return HttpResponse(template.render(Context({'dummy':None})))

