# Create your views here.
from wsgiref.util import application_uri
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, HttpResponseRedirect
from models import Application,Computer
import licensesIO
from django.core.context_processors import csrf
import models
import csv
from licenses import  settings



def reload(request):
    print("Reload")
    licensesIO.loadData(settings.DATA_DIR)
    return HttpResponseRedirect("/")

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html',c)

def search(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'GET':
        list_of_pc = models.Computer.objects.all()
        c['list_pcs'] = models.Computer.objects.all()
        c['list_publishers'] = models.Publisher.objects.all()

        return render_to_response('search.html',c)

    elif request.method == 'POST':

        comp_id = request.POST['computer']
        print ("Computer ID = %s"% comp_id)
        computer = models.Computer.objects.get(id=comp_id)

        publisher_id = request.POST['publisher']
        print ("Publisher = %s"% publisher_id)
        if publisher_id == "all":
            publisher = models.Publisher.objects.all()
        else:
            publisher = models.Publisher.objects.filter(id=publisher_id)


        print (computer)
        for app in computer.applications.filter(publisher__in=publisher):
            print ("  " + app.name)

        c['computer'] = computer
        c['computer_id'] = comp_id
        c['unknown_software'] =  computer.applications.filter(license=0,publisher__in=publisher)
        c['free_software'] =  computer.applications.filter(license=1,publisher__in=publisher)
        c['licensed_software'] = computer.applications.filter(license=2,publisher__in=publisher)
        return render_to_response('report_pc.html',c)




def applicationinfo(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        application_id = request.POST['application_id']
        application = models.Application.objects.filter(id=application_id)
        publisher = models.Publisher.objects.filter(publisher=application.publisher)
        license = application.license


        c['application_name'] = application.name
        c['publisher'] = publisher
        c['license'] = license
        c['price'] = 0

    return render_to_response('manage.html',c)


def manage(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        action = request.POST['action']
        sw_list = request.POST.getlist('software')

        actions = {"Mark Free":1,"Mark Licensed":2,"Mark Unknown":0}

        for sw_id in sw_list:
            apps = models.Application.objects.filter(id=sw_id)
            for app in apps:
                app.license = actions[action]
                app.save()


    c['unknown_software'] = models.Application.objects.filter(license=0)
    c['free_software'] = models.Application.objects.filter(license=1)
    c['licensed_software'] = models.Application.objects.filter(license=2)
    return render_to_response('manage.html',c)


def download(request):
    c = {}
    c.update(csrf(request))


    if request.method == 'POST':

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="software.csv"'

        comp_id = request.POST['computer_id']
        computer = models.Computer.objects.get(id=comp_id)

        writer = csv.writer(response)
        writer.writerow(['Computer :', computer])
        writer.writerow(['',''])
        writer.writerow(['Software', 'Publisher', 'License'])
        writer.writerow(['',''])

        for app in computer.applications.all():
            print ("  " + app.name)
            publ = models.Publisher.objects.get(name=app.publisher)
            writer.writerow([app.get_name(),publ.get_publisher(),app.get_license_txt()])

    return response
