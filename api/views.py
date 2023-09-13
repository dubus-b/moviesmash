from django.shortcuts import render
import openai

from api.constant import API_KEY

openai.api_key = API_KEY


# Create your views here.
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

class FilmSerializer(serializers.Serializer):
    film1 = serializers.CharField(max_length=255)
    film2 = serializers.CharField(max_length=255)

class Admin_FilmViewSet(APIView):
    
    serializer_class = FilmSerializer
    def post(self, request):
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            film1 = serializer.validated_data['film1']
            film2 = serializer.validated_data['film2']
            
            prompt = f"Génère un résumé combinant les synopsys des films : {film1} et {film2}. Remplace les noms des personnages par des périphrases. Ne réponds qu'avec le résumé. Essaye de faire 6 paragraphes en mélangeant les histoires sans mentionner qu'il s'agit de deux histoires et sans dire qu'il s'agit d'une fusion."

            # Effectuez l'appel à l'API OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}]
            )

            # Récupérez la réponse de l'API OpenAI
            response = completion['choices'][0]['message']['content']

            # Retournez la réponse générée dans la réponse de la vue
            response_data = {
                'film1': film1,
                'film2': film2,
                'resumé': response
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        



def film_summary_form(request):
    return render(request, 'api/film_summary_form.html')

