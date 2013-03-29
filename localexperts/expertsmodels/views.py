# Create your views here.
from django.http import HttpResponse

def heatmap(request):
    return HttpResponse("Hello, world. You're at the heatmap page.")

