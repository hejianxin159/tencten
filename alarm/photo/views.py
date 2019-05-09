from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import View
from photo.models import Photo
import time, datetime
from django.core.paginator import Paginator
# Create your views here.


class DayView(View):
    def get(self, request):
        all_photos_days = Photo.objects.all()
        photos_day = []
        photos_days = []
        for photo_day in all_photos_days:
            time = str(photo_day.create_time).split(' ')[0]
            photos_day.append(time)
            photos_day = list(set(photos_day))

        for day in photos_day:
            photo_create_time = Photo.objects.filter(create_time__startswith=day)[0]
            photo_create_time.day = day
            photos_days.append(photo_create_time)
        context = {'photos_days': photos_days}
        return render(request, 'day.html', context)

    def post(self, request):
        create_time = request.POST.get('create_time', '1')
        photo_name = request.POST.get('photo_name', '1')
        photo = Photo()
        photo.create_time = create_time
        photo.image = photo_name
        photo.save()
        print (create_time, photo_name)
        return JsonResponse({"res":1, "message":"chenggong"})
class PhotosView(View):
    def get(self, request, day, page):
        create_time = time.strftime('%Y-%m-%d', time.localtime())
        all_photos = Photo.objects.filter(create_time__startswith=day).order_by('-create_time')
        # all_photos = Photo.objects.filter(create_time__gt=datetime.date(2019,3,7)).order_by('-create_time')
        for photos in all_photos:
            image_id = (str(photos.image)).split('/')[-1]
            photos.image_id = image_id

        paginator = Paginator(all_photos, 5)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages
        photos = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)


        context = {'all_photos': all_photos,
                   'day': day,
                   'photos': photos,
                   'pages': pages}
        return render(request, 'photos.html', context=context)


class  PhotoView(View):
    def get(self, request, image_id):
        image_id = 'group1/M00/00/00/'+image_id
        image = Photo.objects.get(image=image_id)
        content = {'image': image}
        print(content)
        return render(request, 'photos.html')


