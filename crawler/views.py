from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.response import Response


from .utils import google_search

class CrawlerSerializer(serializers.Serializer):
  #email = serializers.EmailField()
  query = serializers.CharField()
  location = serializers.CharField()
  duration = serializers.IntegerField(required=False)



class CrawlerSet(viewsets.ViewSet):

  def create(self, request):
    serializer = CrawlerSerializer(data=request.data)
    if serializer.is_valid():
      #email = serializer.validated_data['email']
      query = serializer.validated_data['query']
      location = serializer.validated_data['location']
      duration = serializer.validated_data.get('duration', 5)
      results =  google_search(query, duration, location)



      return Response({'message': 'success', 'details': results}, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)