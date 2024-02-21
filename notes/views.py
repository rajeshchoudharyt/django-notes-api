from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.validators import ValidationError
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser, ShareNote, Note, EditNote
from .serializer import NoteSerializer, UserSerializer, ShareNoteSerializer, EditNoteSerializer
from django.views.decorators.csrf import csrf_exempt

# Create Note
@csrf_exempt
def create(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    if not request.user.is_authenticated:
        return HttpResponse('User not authenticated', status=401)
    
    data = JSONParser().parse(request)
    
    serializer = NoteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    
    return JsonResponse(serializer.errors, status=400)


# Register User
@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    data = JSONParser().parse(request)

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    
    return JsonResponse(serializer.errors, status=400)


# User Login
@csrf_exempt
def user_login(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    data = JSONParser().parse(request)

    user = None
    user = CustomUser.objects.filter(username=data['username']).values_list('username', flat=True)
    
    if not user.exists():
        user = CustomUser.objects.filter(email=data['username']).values_list('username', flat=True)

    if not user.exists():
        return HttpResponse('User not registered', status=400)

    user = authenticate(username=user[0], password=data['password'])

    if user:
        login(request, user)
        return HttpResponse('Authenticated: Logged in successfully', status=200)

    return JsonResponse( { 'error': 'Invalid credentials' }, status=400)
    

# User logout
def user_logout(request):
    logout(request)
    return HttpResponse('Logged out successfully', status=200)

# Share Note
@csrf_exempt
def share_note(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    if not request.user.is_authenticated:
        return HttpResponse('User not authenticated', status=401)
    
    data = JSONParser().parse(request)

    instance_obj = []
    note_id = data['note_id']
    for email in data['users']:
        
        note_obj = Note.objects.filter(note_id=note_id)
        user_obj = CustomUser.objects.filter(email=email)

        errors = {}
        if note_obj == None:
            errors['note_id'] = 'Note with given id does not exist'

        if user_obj == None:
            errors['email'] = 'Shared user not registered'
        
        if errors != {}:
            return JsonResponse(errors, status=400)


        instance_obj.append(ShareNote(
            note_id=note_obj.first(),
            user_id=user_obj.first()
        ))


        user_id = user_obj.values()[0]['id']
        serializer = ShareNoteSerializer(data={
            "note_id": note_id,
            "user_id": user_id
        })

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
    try:
        ShareNote.objects.bulk_create(instance_obj)
    except:
        raise ValidationError('Note already shared with user')

    return HttpResponse('Note shared successfully', status=200)


# Retrieve/edit note by id
@csrf_exempt
def retrieve_note(request, note_id):
    # Retrieve note
    if request.method != 'GET' and request.method != 'PUT':
        return HttpResponse(status=405)

    if not request.user.is_authenticated:
        return HttpResponse('User not authenticated', status=401)
    
    note = Note.objects.filter(note_id=note_id).values('email')
    if not note.exists():
        return HttpResponse('Note with given id does not exist', status=400)

    # Edit note util function
    def edit_note():
        data = JSONParser().parse(request)
        data['note_id'] = Note.objects.get(note_id=note_id).note_id
        data['user_id'] = CustomUser.objects.get(username=request.user).id

        
        serializer = EditNoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)

    
    # Check if owner
    is_authorized = False
    owner = CustomUser.objects.filter(email=note[0]['email']).values('username')[0]
    if (owner['username'] == str(request.user)):
        is_authorized = True

    if is_authorized:
        if request.method == 'GET':
            return JsonResponse(note.values()[0], status=200)
        else:
            return edit_note()
            
    
    # Check if shared with user
    is_authorized = False
    shared_users = ShareNote.objects.filter(note_id=note_id).values('user_id')
    shared_users = list(shared_users)

    user = None
    for obj in shared_users:
        user = CustomUser.objects.filter(id=obj['user_id']).values('username')[0]
        if (user['username'] == str(request.user)):
            is_authorized = True
            break
        
    if is_authorized:
        if request.method == 'GET':
            return JsonResponse(note.values()[0], status=200)
        else:
            return edit_note()


    return HttpResponse('Permission Denied: Note is not shared with this user', status=401)


# Note version history
@csrf_exempt
def note_version(request, note_id):
    if request.method != 'GET':
        return HttpResponse(status=405)
    
    if not request.user.is_authenticated:
        return HttpResponse('User not authenticated', status=401)
    
    
    note = Note.objects.filter(note_id=note_id).values('email')
    owner = CustomUser.objects.filter(email=note[0]['email']).values('username')[0]

    if (owner['username'] == str(request.user)):
        data = EditNote.objects.filter(note_id=note_id).order_by(
            'date_created').values('user_id', 'content', 'date_created')

        if not data:
            return HttpResponse('Not Modified: Note not edited', status=204)
        
        response = { 'note_id': note_id, 'data': list(data) }
        return JsonResponse(response, status=200)


    return HttpResponse('Unauthorized', status=401)