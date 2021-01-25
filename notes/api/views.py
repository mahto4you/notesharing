from notes.models import Notes
from notes.api.serializers import NoteSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer