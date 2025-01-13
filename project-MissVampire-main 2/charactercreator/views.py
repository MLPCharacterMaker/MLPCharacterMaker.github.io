from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import CharacterForm
from .models import Character, Perk


# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'charactercreator/register.html', {'form': form})


def index(request):
    return render(request, 'charactercreator/index.html')


@login_required
def create_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)  # Save Character without M2M relationships
            character.owner = request.user

            # Set defaults based on 'origin'
            if character.origin == 'E':
                character.health = 3
                character.movement = '45 feet ground'
            elif character.origin == 'U':
                character.health = 2
                character.movement = '30 feet ground'
            elif character.origin == 'P':
                character.health = 2
                character.movement = form.cleaned_data['pegasus_movement']
            else:
                character.health = 0
                character.movement = '0 feet'

            character.save()  # Save Character object
            if character.background_bonds.exists():
                form.cleaned_data['background_bonds'].set(form.cleaned_data['background_bonds'])
            form.save_m2m()  # Save Many-to-Many relationships (influences, perks, hangups)
            selected_influences = form.cleaned_data.get('influences', [])
            associated_perks = Perk.objects.filter(influence__in=selected_influences)
            character.perks.set(associated_perks)
            return redirect(reverse('view-character', args=[character.pk]))
        else:
            print(form.errors)  # Log form errors for debugging
    else:
        form = CharacterForm()

    return render(request, 'charactercreator/create_character.html', {'form': form})


@login_required
def character_list(request):
    user = request.user
    characters = Character.objects.filter(Q(owner=user) | Q(public=True))
    return render(request, 'charactercreator/character_list.html', {'characters': characters})


@login_required
def edit_character(request, pk):
    character = get_object_or_404(Character, pk=pk)

    # Permission check
    if character.owner != request.user:
        return HttpResponse("You do not have permission to edit this character", status=403)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            character.delete()
            return redirect('character-list')

        # Handle edit action
        form = CharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            updated_character = form.save(commit=False)

            # Update defaults based on 'origin'
            if updated_character.origin == 'E':
                updated_character.health = 3
                updated_character.movement = '45 feet ground'
            elif updated_character.origin == 'U':
                updated_character.health = 2
                updated_character.movement = '30 feet ground'
            elif updated_character.origin == 'P':
                updated_character.health = 2
                updated_character.movement = form.cleaned_data.get('pegasus_movement', '')
            else:
                updated_character.health = 0
                updated_character.movement = '0 feet'

            updated_character.save()  # Save the Character object
            form.save_m2m()  # Save Many-to-Many relationships (influences, perks, hangups)
            updated_character.background_bonds.set(form.cleaned_data['background_bonds'])

            # Automatically associate perks based on selected influences
            selected_influences = form.cleaned_data.get('influences', [])
            associated_perks = Perk.objects.filter(influence__in=selected_influences)
            updated_character.perks.set(associated_perks)

            return redirect(reverse('view-character', args=[updated_character.pk]))
        else:
            print(form.errors)  # Log form errors for debugging
    else:
        # Load form with character data
        form = CharacterForm(instance=character)

    return render(request, 'charactercreator/edit_character.html', {
        'form': form,
        'character': character,
    })


@login_required
def view_character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    bonus = character.level_bonus()
    is_owner = character.owner == request.user

    # Retrieve related perks and hangups
    perks = character.perks.all()
    hangups = character.hangups.all()

    return render(request, 'charactercreator/view_character.html', {
        'character': character,
        'is_owner': is_owner,
        'bonus': bonus,
        'perks': perks,
        'hangups': hangups
    })

def map(request):
    return render(request, 'charactercreator/map.html')