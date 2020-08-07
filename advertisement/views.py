from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.views.generic import View
import os
from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta


# handle user offer view
class UserOffersView(View):

    offer_model = Offer
    save_file_model = SaveFile

    def get(self, request):
        # handle logout
        if 'logout' in request.GET:
            logout(request)
            cache.clear()
            messages.info(request, 'Zostałeś wylogowany')
            return redirect('/')

        # collect offers data
        user_offers = self.offer_model.objects.filter(user=request.user).order_by('-update_date')

        packed_data = []
        for offer in user_offers:
            # check offer deadline
            if offer.display_date < now().date() + relativedelta(days=-1):
                offer_ends = True
            else:
                offer_ends = False

            image = self.save_file_model.objects.get(offer=offer)
            packed_data.append((offer, image, offer_ends))

        return render(request, 'user_offers.html', locals())

    def post(self, request):

        # collect offers data
        user_offers = self.offer_model.objects.filter(user=request.user).order_by('-update_date')
        packed_data = []
        for offer in user_offers:
            image = self.save_file_model.objects.get(offer=offer)
            packed_data.append((offer, image))

        # get posted data
        get_offer_id = request.POST.get('offer_id')
        # get action
        get_action = request.POST.get('action')

        print(get_action)

        if get_action == 'delete':
            # delete offer
            selected_offer = self.offer_model.objects.get(id=int(get_offer_id))
            selected_image = self.save_file_model.objects.get(offer=selected_offer)
            os.remove(settings.MEDIA_ROOT + '/' + str(selected_image.file))
            selected_offer.delete()

        if get_action == 'extend':
            # extend offer live
            extend_offer = self.offer_model.objects.get(id=int(get_offer_id))
            extend_offer.display_date = now().date() + relativedelta(days=+extend_offer.display_period)
            extend_offer.save()

        return render(request, 'user_offers.html', locals())


# handle detailed offer view
class DetailsOfferView(View):
    offer_model = Offer
    save_file_model = SaveFile

    def get(self, request, offer_id):
        # handle logout
        if 'logout' in request.GET:
            logout(request)
            cache.clear()
            messages.info(request, 'Zostałeś wylogowany')
            return redirect('/')

        # collect offer data
        offer_data = self.offer_model.objects.get(id=offer_id)
        image = self.save_file_model.objects.get(offer=offer_data)
        image_name = image.file.name.rsplit('/', 1)[-1]

        return render(request, 'offer_details.html', locals())


# handle edit offer view
class EditOfferView(View):
    offer_model = Offer
    save_file_model = SaveFile

    def get(self, request, offer_id):
        # handle logout
        if 'logout' in request.GET:
            logout(request)
            cache.clear()
            messages.info(request, 'Zostałeś wylogowany')
            return redirect('/')

        proper_category_list = []
        for item in category_list:
            proper_category_list.append(item[0])

        # collect offer data
        offer_data = self.offer_model.objects.get(id=offer_id)
        image = self.save_file_model.objects.get(offer=offer_data)
        image_name = image.file.name.rsplit('/', 1)[-1]

        return render(request, 'edit_offer.html', locals())

    def post(self, request, offer_id):

        # get posted data
        get_category = request.POST.get('category')
        get_title = request.POST.get('title')
        get_short_description = request.POST.get('short_description')
        get_full_description = request.POST.get('full_description')
        # handle files save and load
        get_graphic = request.FILES.get('graphic')

        # update offer data
        offer_object = self.offer_model.objects.get(id=offer_id)
        offer_object.title = get_title
        offer_object.short_description = get_short_description
        offer_object.full_description = get_full_description
        offer_object.category = get_category
        offer_object.update_date = now()
        # upload single image
        if get_graphic is not False and get_graphic is not None:
            selected_image = self.save_file_model.objects.get(offer=offer_object)
            if get_graphic != selected_image.file.name:
                try:
                    selected_image = self.save_file_model.objects.get(offer=offer_object)
                    os.remove(settings.MEDIA_ROOT + '/' + str(selected_image.file))
                    selected_image.delete()
                except:
                    pass
                # save graphic files
                file_object = self.save_file_model(offer=offer_object, file=get_graphic)
                file_object.save()

        offer_object.save()
        messages.success(request, 'Ogłoszenie poprawione')

        return render(request, 'edit_offer.html', locals())


# handle add offer view
class AddOfferView(View):
    offer_model = Offer
    save_file_model = SaveFile

    def get(self, request):
        proper_category_list = []
        for item in category_list:
            proper_category_list.append(item[0])

        # handle logout
        if 'logout' in request.GET:
            logout(request)
            cache.clear()
            messages.info(request, 'Zostałeś wylogowany')
            return redirect('/')

        return render(request, 'add_offer.html', locals())

    def post(self, request):
        try:
            # get last available id
            last_id = int(self.offer_model.objects.latest('id').id)
        except:
            last_id = 1

        # get posted data
        get_category = request.POST.get('category')
        get_title = request.POST.get('title')
        get_short_description = request.POST.get('short_description')
        get_full_description = request.POST.get('full_description')
        # handle files save and load
        get_graphic = request.FILES['graphic']
        get_period = request.POST.get('period')

        if "highlight" in request.POST:
            highlight = True
        else:
            highlight = False

        if len(get_period) > 0:
            get_period = int(get_period)
            display_date = now() + relativedelta(days=get_period)
        else:
            get_period = 0
            display_date = now()

        # create new offer
        offer_object = self.offer_model(id=last_id + 1, user=request.user, title=get_title,
                                        short_description=get_short_description, full_description=get_full_description,
                                        category=get_category,
                                        display_period=get_period, display_date=display_date, highlight=highlight)
        offer_object.save()
        # upload single image
        if get_graphic is not False:
            # save graphic files
            file_object = self.save_file_model(offer=offer_object, file=get_graphic)
            file_object.save()

        messages.success(request, 'Ogłoszenie dodane')

        return redirect('/add_offer/')
