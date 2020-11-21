import json

from django.shortcuts import render, redirect
from .forms import AdForm
# Create your views here.
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Category, City, Publication, AdType, Ad
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse


#
# class PersonListView(ListView):
#     model = Person
#     context_object_name = 'people'
#
class SearchAdView(View):
    model = AdType
    form_class = AdForm
    success_url = reverse_lazy('/')
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        ad_form = AdForm()
        # ad_form.fields['city'].choices = [(x.id, x) for x in City.objects.all()]
        cities = City.objects.all()
        categories = Category.objects.all()
        return render(self.request, 'index.html', {'form': ad_form, 'cities': cities, 'categories': categories})

    def post(self, request, *args, **kwargs):
        form = AdForm()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', self.request.POST)
        category = self.request.POST['category']
        citylist = self.request.POST.getlist('city')[1::]
        publicationList = self.request.POST.getlist('publication')
        print('>>>>>>>>>>', publicationList)
        ad = self.request.POST['ad']
        category = Category.objects.get(id=category)
        ad = Ad.objects.get(id=ad)
        category_name = category.name
        ad_name = ad.name
        filtered_ads = []
        categories = Category.objects.all().exclude(id=category.id)
        total_cities = [x.id for x in City.objects.all()]
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', total_cities)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> citylist ', citylist)
        remaining_cities = []
        remaining_publication = []

        for x in total_cities:
            print('ITERATING OVER TOTAL CITIES', x)
            if str(x) not in citylist:
                remaining_cities.append(int(x))

        print('____________________________________________________________________', remaining_cities)
        selected_cities = []
        selected_publication = []
        for publication in publicationList:
            print('publication ---->>', publication)
            publication = Publication.objects.get(id=publication)
            selected_publication.append(publication)
        print('Selected Publication ----------->>>', selected_publication)
        for x in Publication.objects.all():
            print('ITERATING OVER PUBLICATION LIST ', x)
            pub_obj = Publication.objects.get(id=int(x.id))
            if pub_obj not in selected_publication:
                remaining_publication.append(pub_obj)
        print('REMAINING PUBLICATION LIST ', remaining_publication)
        # remaining_publication_obj = []
        # for obj in remaining_publication:
        #     remaining_publication_obj.append(obj)
        # print('REMAINIG PUBLICATION OBJECT ',remaining_publication_obj)
        selected_ad = ad
        remaining_ad = Ad.objects.all().exclude(id=ad.id)
        for city in citylist:
            city = City.objects.get(id=city)
            city_name = city.city_name
            selected_cities.append(city)
            for publication in publicationList:
                publication = Publication.objects.get(id=publication)
                publication_name = publication.publication_name
                print('<<<<<<<<<<<<<<<Publication  ', publication)
                print('>>>>>>>>>>>>>>>>City   ', city_name)
                search = AdType.objects.filter(Q(category__name__icontains=category_name) &
                                               Q(city__city_name__icontains=city_name) &
                                               Q(publication__publication_name__icontains=publication_name) &
                                               Q(ad__name__icontains=ad_name))
                print('Search result--------------------', search)
                if len(search) != 0:
                    print("Ad name", search[0].sample_ad_text)
                    filtered_ads.append(search[0])
                    print('-----------------------', len(search))
        remaining_cities_obj = []
        for city in remaining_cities:
            remaining_cities_obj.append(City.objects.get(id=city))
        result = len(filtered_ads)
        if result > 0:
            return render(self.request, 'search.html',
                          {"search": filtered_ads, 'citylist': citylist, 'publicationList': remaining_publication,
                           'category': category, 'ad': ad, 'categories': categories,
                           'selected_cities': selected_cities, 'total_cities': remaining_cities_obj,
                           'selected_publication': selected_publication, 'selected_ad': selected_ad,
                           'remaining_ad': remaining_ad})
        else:
            messages.error(self.request, 'No result found')
            return render(self.request, 'index.html', {"form": form})
            # return HttpResponseRedirect(self.request.path_info)


#
# class PersonUpdateView(UpdateView):
#     model = Person
#     form_class = PersonForm
#     success_url = reverse_lazy('person_changelist')
#
@csrf_exempt
def load_publications(request):
    # publication_id = request.GET.get('publication')
    # cities = City.objects.filter(publication=publication_id).order_by('city_name')
    publication_list = []
    if request.method == 'POST':
        city_id = json.loads(request.POST['city'])
        print('>>>>>>>>>>>>>>>>>>>>', city_id)
        for city in city_id:
            for city in city:
                if city == '-Select City-':
                    pass
                else:
                    print('__________________________', city)
                    publications = Publication.objects.filter(city=int(city)).order_by('publication_name')
                    print('Publications  ', publications)
                    if len(publications) > 0:
                        publication_list.append([publication for publication in publications])
                    else:
                        pass
        # print(publication_list)
        y = []
        for x in publication_list:
            for z in x:
                y.append(z)
    return render(request, 'publication.html', {'publications': set(y)})


@csrf_exempt
def load_adtype(request):
    ad_list = []
    if request.method == 'POST':
        publication_id = json.loads(request.POST['publication'])
        print('---------- load ad  ', publication_id)
        pub = publication_id.pop()
        print('popped value   ', pub)
        for publication in pub:
            ad_type = Ad.objects.filter(publication=int(publication)).order_by('name').distinct()
            if (len(ad_type) != 0):
                if ad_type[0].name not in ad_list:
                    print('___________ AD NAME______', ad_type[0].name)
                    ad_list.append(ad_type[0].name)
    print(ad_list)
    return render(request, 'ad_type.html', {'ad_type': list(set(ad_list))})


class PackageDetails(DetailView):
    model = AdType
    template_name = 'package-detail.html'


class AddToCart(View):
    model = AdType

    def get(self, request, *args, **kwargs):
        print('inside ADD TO CART CLASS  ------')
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        print('>>>>>', object_id)
        self.request.session['order'] = object_id
        x = self.request.session['order']
        print('<<<<<<<', x)
        # print('<<<<<<< Count', x.count())
        # ad_obj = AdType.objects.filter()
        return HttpResponse()
