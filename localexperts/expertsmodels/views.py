# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getUserLocationsForExpertise(request):
    return Response({"message": "Hello for today! See you tomorrow!"})


def heatmap(request):
    template = loader.get_template('heatmap.html')
    return HttpResponse(template.render(Context({'dummy':None})))