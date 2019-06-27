from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import FormRegister, FormUserUpdate, FormProfileTravelerUpdate, FormProfileHostUpdate, \
    FormProfileHostUpdate2, FormProfileTravelerUpdate2, FormAddress, FormProgram, FormSpace, \
    DeleteProgramForm, DeleteSpaceForm, LinkForm, DeleteLinkForm
from django.contrib.auth.decorators import login_required
from .decorators import traveler_required, host_required
from .models import ProfileTraveler, ProfileHost, Space, Program, Language, Link
from app_main.models import Trip
from django.contrib.auth import logout, login, authenticate
from .constants import BRAND_LIST
from .forms import LinkFormset
from decouple import config
from django.db.models import Q
from django.utils.timezone import localdate


def viewregister(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            new_user=form.save()
            username = form.cleaned_data.get('username')
            type = form.cleaned_data.get('type')
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(request, f"{username}! Thanks for signing up with us! You are now logged in.")
            return redirect('index')
    else:
        form = FormRegister()
    return render(request, 'app_user/register.html', {'form': form})


@login_required()
def viewindex(request):
    return render(request, 'app_main/index.html')


@traveler_required()
@login_required()
def profile_update_traveler(request):
    if request.method == 'POST':
        u_form = FormUserUpdate(request.POST, instance=request.user)
        t_form = FormProfileTravelerUpdate(request.POST, request.FILES, instance=request.user.profiletraveler)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request, "Personal section has been updated!")
            if request.POST['save'] == "next":
                return redirect('profile_update_traveler2')
            elif request.POST['save'] == "prev":
                return redirect('index')
    else:
        u_form = FormUserUpdate(instance=request.user)
        t_form = FormProfileTravelerUpdate(instance=request.user.profiletraveler)

    context = {'u_form': u_form, 't_form': t_form}
    return render(request, "app_user/profile_traveler.html", context)


@traveler_required()
@login_required()
def profile_update_traveler2(request):
    if request.method == 'POST':
        form = FormProfileTravelerUpdate2(request.POST, instance=request.user.profiletraveler)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            messages.success(request, "Professional section has been updated!")
            if request.POST['save'] == "next":
                return redirect('profile_update_traveler3')
            elif request.POST['save'] == "prev":
                return redirect('profile_update_traveler')
    else:
        form = FormProfileTravelerUpdate2(instance=request.user.profiletraveler)

    context = {'form': form}
    return render(request, "app_user/profile_traveler2.html", context)


@traveler_required()
@login_required()
def profile_update_traveler3(request):
    '''Add social links'''
    heading_message = 'Social links'
    links = Link.objects.filter(user=request.user)

    if request.method == 'GET':
        formset = LinkFormset(request.GET or None)
    elif request.method == 'POST':
        formset = LinkFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name, url from each form and save
                name = form.cleaned_data.get('name')
                url = form.cleaned_data.get('url')
                # save link instance
                if name:
                    Link(name=name, url=url, user=request.user).save()
            messages.success(request, "Social section has been updated!")
            if request.POST['save'] == "next":
                return redirect('program_add')
            elif request.POST['save'] == "prev":
                return redirect('profile_update_traveler2')
            elif request.POST['save'] == 'add':
                return redirect('profile_update_traveler3')

    context = {
        'formset': formset,
        'heading': heading_message,
        'brands': BRAND_LIST,
        'links': links
    }
    return render(request, 'app_user/profile_traveler3.html', context)


@traveler_required()
@login_required()
def program_add(request):
    program = Program.objects.filter(owner=request.user)
    if request.method != 'POST':
        form = FormProgram()
    else:
        form = FormProgram(request.POST, request.user)
        if form.is_valid():
            new_program = form.save(commit=False)
            new_program.owner = request.user
            form.clean()
            new_program.save()
            form.save_m2m()
            messages.success(request, "New program offer has been added!")
            if request.POST['save'] == "next":
                return HttpResponseRedirect(reverse('index'))
            elif request.POST['save'] == "prev":
                return redirect('profile_update_traveler3')

    context = {'form': form, 'program': program}
    return render(request, 'app_user/program_add.html', context)


@traveler_required()
@login_required()
def program_update(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        form = FormProgram(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program has been updated!")
            if request.POST['save'] == "next":
                return HttpResponseRedirect(reverse("program_detail", args=[program.id]))
            elif request.POST['save'] == "prev":
                return redirect('program_update')
        else:
            messages.warning(request, "Form is not valid!")
    else:
        form = FormProgram(instance=program)
    context = {'form': form, 'program': program}
    return render(request, "app_user/program_update.html", context)


@traveler_required()
@login_required
def program_delete(request, program_id):
    '''delete an existng program.'''
    program = Program.objects.get(id=program_id)
    program_to_delete = get_object_or_404(Program, id=program_id)
    if request.method != 'POST':
        form = DeleteProgramForm(instance=program)
    else:
        form = DeleteProgramForm(instance=program, data=request.POST)
        if form.is_valid():
            program_to_delete.delete()
            return HttpResponseRedirect(reverse('app_main:home'))
    context = {'program': program, 'form': form}
    return render(request, 'app_user/program_delete.html', context)

@traveler_required()
@login_required
def program_detail(request, program_id):
    '''show a program'''
    program = Program.objects.filter(owner=request.user).get(id=program_id)
    context = {"program": program}
    return render(request, "app_user/program_detail.html", context)


def program_list(request, userid):
    '''show a program'''
    program = Program.objects.filter(owner_id=userid)
    context = {"program": program}
    return render(request, "app_user/program_list.html", context)

@host_required()
@login_required()
def profile_update_host(request):
    if request.method == 'POST':
        h_form = FormProfileHostUpdate(request.POST,
                           request.FILES, instance=request.user.profilehost)
        if h_form.is_valid():
            h_form.save()
            messages.success(request, "Basic section has been updated!")
            if request.POST['save'] == "next":
                return redirect('profile_update_host2')
            elif request.POST['save'] == "prev":
                return HttpResponseRedirect(reverse('profile_host', args=[request.user.id]))
    else:
        h_form = FormProfileHostUpdate(instance=request.user.profilehost)
    context = {'h_form': h_form}
    return render(request, "app_user/profile_host.html", context)


@host_required()
@login_required()
def profile_update_host2(request):
    if request.method == 'POST':
        form = FormProfileHostUpdate2(request.POST, instance=request.user.profilehost)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            messages.success(request, "Interest section has been updated!")
            if request.POST['save'] == "next":
                return redirect('profile_update_host3')
            elif request.POST['save'] == "prev":
                return redirect('profile_update_host')
    else:
        form = FormProfileHostUpdate2(instance=request.user.profilehost)
    context = {'form': form}
    return render(request, "app_user/profile_host2.html", context)


@host_required()
@login_required()
def profile_update_host3(request):
    heading_message = 'Social links'
    links = Link.objects.filter(user=request.user)

    if request.method == 'GET':
        formset = LinkFormset(request.GET or None)
    elif request.method == 'POST':
        formset = LinkFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name, url from each form and save
                name = form.cleaned_data.get('name')
                url = form.cleaned_data.get('url')
                # save link instance
                if name:
                    Link(name=name, url=url, user=request.user).save()
            messages.success(request, "Social section has been updated!")
            if request.POST['save'] == "next":
                return redirect('space_add')
            elif request.POST['save'] == "prev":
                return redirect('profile_update_host2')
            elif request.POST['save'] == 'add':
                return redirect('profile_update_host3')
                # return HttpResponseRedirect(reverse('link_list', args=[request.user.id]))

    context = {
        'formset': formset,
        'heading': heading_message,
        'brands': BRAND_LIST,
        'links': links
    }
    return render(request, 'app_user/profile_host3.html', context)


@host_required()
@login_required()
def space_add(request):
    space = Space.objects.filter(owner=request.user)
    if request.method == 'POST':
        form = FormSpace(request.POST, request.FILES)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            messages.success(request, "Availability has been added!")
            if request.POST['save'] == "next":
                return HttpResponseRedirect(reverse("space_list", args=[request.user.id]))
            elif request.POST['save'] == "save":
                return redirect('profile_update_host2')
    else:
        form = FormSpace()
    context = {'form': form, 'space': space}
    return render(request, "app_user/space_add.html", context)


@host_required()
@login_required()
def space_update(request, space_id):
    space = Space.objects.filter(owner=request.user).get(id=space_id)
    if request.method == 'POST':
        form = FormSpace(request.POST, request.FILES, instance=space)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            messages.success(request, "Space Availability has been updated!")
            if request.POST['save'] == "next":
                return redirect('index')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host2')
    else:
        form = FormSpace(instance=space)
    context = {'form': form}
    return render(request, "app_user/space_update.html", context)


@host_required()
@login_required
def space_detail(request, space_id):
    '''show a program'''
    space = Space.objects.filter(owner=request.user).get(id=space_id)
    context = {"space": space}
    return render(request, "app_user/space_detail.html", context)


def space_list(request, userid):
    '''show a program'''
    space = Space.objects.filter(owner_id=userid)
    context = {"space": space}
    return render(request, "app_user/space_list.html", context)


@host_required()
@login_required
def space_delete(request, space_id):
    '''delete an existng space instance.'''
    space = Space.objects.get(id=space_id)
    space_to_delete = get_object_or_404(Space, id=space_id)
    if request.method != 'POST':
        form = DeleteSpaceForm(instance=space)
    else:
        form = DeleteSpaceForm(instance=space, data=request.POST)
        if form.is_valid():
            space_to_delete.delete()
            return HttpResponseRedirect(reverse('index'))
    context = {'space': space, 'form': form}
    return render(request, 'app_user/space_delete.html', context)


def profile_traveler(request, userid):
    profile = ProfileTraveler.objects.get(user_id=userid)
    lan = profile.languages.all()
    expertise = profile.expertise.all()
    link = Link.objects.filter(user_id=userid)
    offer = Program.objects.filter(owner_id=userid)
    trips = Trip.objects.filter(user_id=userid, end_date__gt=localdate())
    context = {"profile": profile, 'lan': lan, 'expertise': expertise, "link": link,
               'offer': offer, 'trips': trips}

    return render(request, 'app_user/preview_traveler.html', context)


def profile_host(request, userid):
    profile = ProfileHost.objects.get(user_id=userid)
    lan = profile.languages.all()
    interest = profile.interests.all()
    lat, lon = profile.geolocation.lat, profile.geolocation.lon
    link = Link.objects.filter(user_id=userid)
    offer = Space.objects.filter(owner_id=userid)

    key = config('GOOGLE_MAPS_API_KEY')
    context = {"profile": profile, 'lan': lan, 'interest': interest, 'link': link,
               'offer': offer, 'lat': lat, 'lon': lon, 'key': key}

    return render(request, 'app_user/preview_host.html', context)


@host_required()
@login_required()
def address_update(request):
    if request.method == 'POST':
        form = FormAddress(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            geolocation = form.cleaned_data.get('geolocation')
            form.save()
        return HttpResponseRedirect(reverse('profile_update_host'))
    else:
        form = FormAddress()
    return render(request, "app_user/profile_address.html", {'form': form})


@login_required()
def link_add(request):
    template_name = 'app_user/links.html'
    heading_message = 'Formset Link Name Demo'
    if request.method == 'GET':
        formset = LinkFormset(request.GET or None)
    elif request.method == 'POST':
        formset = LinkFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Link(name=name, user=request.user).save()

            # once all books are saved, redirect to book list view
            return redirect('link_list')
    context = {
                'formset': formset,
                'heading': heading_message,
                'brands': BRAND_LIST,
                }
    return render(request, template_name, context)


def link_list(request, userid):
    links = Link.objects.filter(user_id=userid)
    BRAND_LIST.sort(reverse=True)

    return render(request, "app_user/link_list.html", {'links': links, 'brands': BRAND_LIST})


@login_required
def link_delete(request, link_id):
    '''delete an existng space instance.'''
    link = Link.objects.get(id=link_id, user=request.user)
    link_to_delete = get_object_or_404(Link, id=link_id, user=request.user)
    if request.method != 'POST':
        form = DeleteLinkForm(instance=link)
    else:
        form = DeleteLinkForm(instance=link, data=request.POST)
        if form.is_valid():
            link_to_delete.delete()
            return redirect('profile_update_host3')
    context = {'link': link, 'form': form}
    return render(request, 'app_user/link_delete.html', context)


@login_required
def link_detail(request, link_id):
    '''show a program'''
    link = Link.objects.filter(user=request.user).get(id=link_id)
    context = {"link": link}
    return render(request, "app_user/link_detail.html", context)

@login_required
def link_update(request): # link_add
    template_name = 'app_user/link_update.html'
    heading_message = 'Social links'
    links = Link.objects.filter(user=request.user)

    if request.method == 'GET':
        formset = LinkFormset(request.GET or None, instance=links)
    elif request.method == 'POST':
        formset = LinkFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name, url from each form and save
                name = form.cleaned_data.get('name')
                url=form.cleaned_data.get('url')
                # save book instance
                if name:
                    Link(name=name, url=url, user=request.user).save()

            # once all books are saved, redirect to book list view
            return redirect('link_list')
    context = {
                'formset': formset,
                'heading': heading_message,
                'brands': BRAND_LIST,
                'links': links
                }
    return render(request, template_name, context)

