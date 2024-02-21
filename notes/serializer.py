from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Note, CustomUser, ShareNote, EditNote

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Note.objects.all(),
                fields=('email', 'title'),
                message="Note with same title already exist"
            )]
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': { 'write_only': True }}
    
    def create(self, data):
        user = CustomUser(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        user.save()
        return user
    

class ShareNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareNote
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShareNote.objects.all(),
                fields=('note_id', 'user_id'),
                message="Note already shared with user"
            )]
        

class EditNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditNote
        fields = '__all__'