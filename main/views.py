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
    c = {}
    c.update(csrf(request))

    progress = licensesIO.getProgress()
    if progress == 100:
        licensesIO.LoadData()
    elif progress == 0:
        licensesIO.LoadData()
    return HttpResponseRedirect("/load/")
    #return render_to_response('load.html',c)

def load(request):
    c = {}
    c.update(csrf(request))
    progress = licensesIO.getProgress()
    c['progress_level'] = progress
    c['current_file'] = licensesIO.getCurrent()
    c['last_sw'] = licensesIO.getlastSoftware()

    if progress == 100:
        return render_to_response('index.html',c)
    else:
        return render_to_response('load.html',c)

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

        c['computer'] = computer
        c['computer_id'] = comp_id
        c['unknown_software'] =  computer.applications.filter(license=0,publisher__in=publisher)
        c['free_software'] =  computer.applications.filter(license=1,publisher__in=publisher)
        c['licensed_software'] = computer.applications.filter(license=2,publisher__in=publisher)
        return render_to_response('report_pc.html',c)



def saveapp(request):
    pass

def appinfo(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':


        application_id = request.POST['software']

        application = models.Application.objects.get(id=application_id)
        publisher = models.Publisher.objects.get(name=application.publisher)

        # Save Data
        act = request.POST.get('action', None)
        if act == "save":
            application.comment = request.POST['comment']
            application.cost= request.POST['cost']
            if application.cost > 0:
                application.license = 2
            application.save()
            return HttpResponseRedirect("/manage/")


        c['app_id'] = application_id
        c['app_name'] = application.name
        c['app_version'] = application.version
        c['app_publisher'] = publisher.name
        c['app_license'] = application.get_license_txt()
        c['app_cost'] = application.cost
        c['pclist'] = application.computer_set.all()
        c["app_installation"] = application.installation
        c["app_comment"] = application.comment

    return render_to_response('appinfo.html',c)


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

def write_pc(computer,writer):
        writer.writerow(['',''])
        writer.writerow(['',''])
        writer.writerow([computer])

        for app in computer.applications.all():
            publ = models.Publisher.objects.get(name=app.publisher)
            writer.writerow(['',app.get_name(),publ.get_publisher(),app.get_license_txt(),str(app.get_cost())])

def download(request):
    c = {}
    c.update(csrf(request))


    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="software.csv"'
        writer = csv.writer(response)
        writer.writerow(['',''])
        writer.writerow(['Computer','Software', 'Publisher', 'License', 'Cost'])
        writer.writerow(['',''])

        comp_id = request.POST['computer_id']
        if comp_id == "all" :
            for pc in models.Computer.objects.all():
                write_pc(pc,writer)

        else :
            computer = models.Computer.objects.get(id=comp_id)
            write_pc(computer,writer)


    return response
