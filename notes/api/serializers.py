from notes.models import Notes
from rest_framework import serializers

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'uploadingdate', 'branch', 'subject', 'notesfile']