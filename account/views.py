from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.views.generic import View
from .models import User
from .forms import LoginForm, RegisterForm
from django.template import loader
from django.apps import apps
Offer = apps.get_model('advertisement', 'Offer')
SaveFile = apps.get_model('advertisement', 'SaveFile')


# handle login view
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # get posted data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # authenticate user
            user = authenticate(email=email, password=password)
            # handle user authentication
            if user is not None and user.is_active and user.is_authenticated:
                login(request, user)
                messages.success(request, 'Zostałeś zalogowany')
                return redirect('/')
            else:
                messages.warning(request, 'Zła nazwa użytkownika lub hasło')
                return redirect('/login/')
        else:
            messages.warning(request, 'Zła nazwa użytkownika lub hasło')
            return redirect('/login/')


# handle register view
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():

            # get posted data
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            user = User.objects.create_user(email, username, phone, password)
            user.save()
            messages.info(request, 'Konto utwożone')
            return redirect('/')

        else:
            # handle errors display
            error_list = []
            for field, errors in form.errors.items():
                errors_text = '{}'.format(','.join(errors))
                error_list = [x.strip() for x in errors_text.split(',')]

            if len(error_list) > 0:
                for error in error_list:
                    messages.warning(request, error)

            return redirect('/register/')


# handle delete user view
class DeleteView(View):
    template_name = 'delete_account.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        if 'delete' in request.POST:
            user = request.user
            user.delete()
            messages.info(request, 'Konto zostało usunięte')
        return redirect('/')


# handle default display view
class HomeView(View):
    template_name = 'base.html'
    template_list_view = 'base_list.html'

    def get(self, request):

        if 'logout' in request.GET:
            logout(request)
            cache.clear()
            messages.info(request, 'Zostałeś wylogowany')
            return redirect('/')

        def partition_data(offers_data, elements):
            # collect offers data
            packed_data = []
            for offer in offers_data:
                image = SaveFile.objects.get(offer=offer)
                packed_data.append((offer, image))

            portioned_data = []
            for i in range(0, len(packed_data), elements):
                portioned_data.append(packed_data[i:i + elements])
            return portioned_data

        if 'search' in request.GET:
            search_sequence = request.GET['search_sequence']
            offers_data = Offer.objects.filter(title__icontains=search_sequence).exclude(id=0).order_by('-update_date').order_by('-highlight')
            portioned_data = partition_data(offers_data, 4)
            return render(request, self.template_name, locals())

        if 'list_view' in request.GET:
            offers_data = Offer.objects.all().exclude(id=0).order_by('-update_date').order_by('-highlight')
            portioned_data = partition_data(offers_data, 1)
            return render(request, self.template_list_view, locals())

        if 'block_view' in request.GET:
            offers_data = Offer.objects.all().exclude(id=0).order_by('-update_date').order_by('-highlight')
            portioned_data = partition_data(offers_data, 4)
            return render(request, self.template_name, locals())

        if 'job-employment' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='praca - zatrudnie').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'job-looking' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='prace - poszukuje').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'electronic-bay' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='elektronika - kupie').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'electronic-sell' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='elektronika - sprzedam').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'services-order' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='usługi - zlece').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'services-do' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='usługi - wykonam').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'house-bay' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='dom - kupie').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        if 'house-sell' in request.GET:
            template = request.GET.get('template')
            offers_data = Offer.objects.filter(category='dom - sprzedam').exclude(id=0).order_by('-update_date').order_by('-highlight')
            if template == 'base':
                portioned_data = partition_data(offers_data, 4)
                return render(request, self.template_name, locals())
            else:
                portioned_data = partition_data(offers_data, 1)
                return render(request, self.template_list_view, locals())

        offers_data = Offer.objects.all().exclude(id=0).order_by('-update_date').order_by('-highlight')
        portioned_data = partition_data(offers_data, 4)
        return render(request, self.template_name, locals())

