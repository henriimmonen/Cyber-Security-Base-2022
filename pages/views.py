from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import ModifiedUserForm

from .models import Note, UserProfile


def index(request):
    if request.method == 'POST': # post a note
        author = request.user
        header = request.POST.get('header')
        text = request.POST.get('text')
        date = datetime.datetime.now()

        Note.objects.create(author=author, note_header=header, note_text=text, note_date=date)

    notes = []
    if str(request.user) != 'AnonymousUser': # check if user is logged in
        notes = Note.objects.filter(author = request.user)
    context = {'latest_note_list': notes}

    return render(request,'pages/index.html', context)

def register(request): # register user
    if request.method == 'POST':
        form = ModifiedUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created')
            return redirect("/")
        messages.error(request, "Registration went wrong, invalid information.")
    else:
        form = ModifiedUserForm()
    return render(request,'pages/register.html', {'form': form})

@login_required
def personal_info(request):
    try:
        profile = UserProfile.objects.get(username=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        if profile is None:
            username = request.user
            address = request.POST.get('address')

            profile = UserProfile.objects.create(username=username, address=address)
        else:
            profile.delete()
            username = request.user
            address = request.POST.get('address')

            profile = UserProfile.objects.create(username=username, address=address)

        context = {'username':request.user, 'address':profile.address}

    if request.method == 'GET':
        if profile is None:
            context = {'username':request.user, 'address':''}
        else:
            context = {'username':request.user, 'address':profile.address}
    return render(request, 'pages/profile.html', context)


@login_required # view note based on id
def one_note(request, note_id):
    note = get_object_or_404(Note, pk = note_id)
    return render(request, 'pages/text.html', {'note': note})

