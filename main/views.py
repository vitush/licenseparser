# Create your views here.
from wsgiref.util import application_uri
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, HttpResponseRedirect, Http404
from models import Application,Computer
import licensesIO
from django.core.context_processors import csrf
import models
import csv
from licenses import settings
import urllib
from bs4 import BeautifulSoup
import re
import string

def softpedia_search(url):
    res = ""
    try:
        f = urllib.urlopen(url)
        html_doc = f.read()
        f.close()
        soup = BeautifulSoup(html_doc)
        res = ""
        for table in soup.find_all(class_="narrow_listheadings"):
            res += table.decode()
    except:
        pass

    return res

def computers(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        action = request.POST.get('action',None)
        license_id = request.POST.get('license_id',None)
        computer_id_list = request.POST.getlist('computer_id',None)

        if computer_id_list is None or license_id is None:
            return Http404()

        c['licenses_selected'] = int(license_id)


        license  = models.Licenses.objects.get(id=license_id)

        if license is None:
            return Http404()


        if action == "Add":
            for comp_id in computer_id_list:
                computer = models.Computer.objects.get(id=comp_id)
                computer.licenses.add(license)
                print ("Add to comp: %s, license: %s"%(comp_id,license_id))
        if action == "Remove":
            for comp_id in computer_id_list:
                computer = models.Computer.objects.get(id=comp_id)
                computer.licenses.remove(license)
                print ("Removed from comp: %s, license: %s"%(comp_id,license_id))

    c['computers'] = models.Computer.objects.all()
    c['licenses'] =  models.Licenses.objects.all()

    return render_to_response('computers.html',c)

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

def licenses(request):
    c = {}
    c.update(csrf(request))

    license_id = 1

    if request.method == 'POST':

        action = request.POST.get('action',None)
        license_id = int(request.POST.get('licenses','1'))
        license_owner = request.POST.get('license_owner','')
        print ("action = %s " % action)

        c['licenses_selected_id'] = license_id
        try:
            license = models.Licenses.objects.get(id=license_id)
        except:
            license = None

        if action is not None:
            if action == "Add License":
                print("Add License")
                license_name = request.POST.get('license_name',None)
                if license_name is not None:
                    license = models.Licenses.objects.create(name=license_name,owner=license_owner)
                    license.save()

        if action == "Remove License":
            license = models.Licenses.objects.get(id=license_id)
            license.delete()

        elif action == "Add Software":
            for app_id in request.POST.getlist('software_licensed'):
                app = models.Application.objects.get(id=app_id)
                license.applications.add(app)
                #print("Added %s"% app.name)

        elif action == "Remove Software":
            for app_id in request.POST.getlist('applications_included'):
                app = models.Application.objects.get(id=app_id)
                license.applications.remove(app)
                #print("Removed %s"% app.name)


    try:
        license = models.Licenses.objects.get(id=license_id)
    except:
        license = None


    if license is not None:
        #print("License: %s"% license)

        included_apps = license.applications.all()
        #print(included_apps )

        if len(included_apps) > 0 :
            #print("Getting filtered")
            c['software_licensed'] = models.Application.objects.exclude(id__in=included_apps).filter(license=2)
            #c['software_licensed'] = models.Application.objects.filter(license=2)
        else:
            #print("Getting All")
            c['software_licensed'] =  models.Application.objects.filter(license=2)

        c['applications_included'] = included_apps


    c['licenses_selected_id'] = license_id
    c['licenses'] = models.Licenses.objects.all()

    return render_to_response('licenses.html',c)


def z(request):
    c = {}
    c.update(csrf(request))

    apps = models.Application.objects.all()

    for app in apps:
        apindex = +1
        namedict = {}
        namedict['name'] = app.name
        namedict['name1'] = app.name
        app.name1 = app.name
        if app.version != "Unknown":
            ind = string.find(app.name," - "+app.version)
            if ind >= 0 :
                app.name1 = app.name[0:ind]

    c['all'] = models.Application.objects.all()
    c['new'] = apps

    return render_to_response('z.html',c)

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html',c)

def update(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('update.html',c)

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



def appinfo(request):
    c = {}
    c.update(csrf(request))
    c['return_page'] = "/manage/"

    suggestions_enable = request.session.get('suggestions_enable', 0)


    if request.method == 'POST':
        application_id = request.POST['software']

        # change suggestion status
        suggestions_id = request.POST.get("suggestions_id",None)
        if suggestions_id  is not None:
            suggestions_enable = suggestions_id
            request.session["suggestions_enable"] = suggestions_enable



        application = models.Application.objects.get(id=application_id)
        publisher = models.Publisher.objects.get(name=application.publisher)


        import re
        name_full = application.name

        name_full=application.name
        name_short = application.name
        name_short_vendor = application.name
        name_list = name_full.split("-")

        if len(name_list) > 1:
            name_list = name_list[:-1]
            name_list = name_full.split(" - ")[:-1]
            name_short = "-".join(name_list)

        m = re.match(r"(?P<name>[A-Z\-a-z_\ ]+).*", name_short)
        if m is not None:
            if m.group('name') is not None:
               name_short =  m.group('name')

            name_short_vendor= name_short
            if publisher.name != "Unknown" :
                name_short_vendor += " "
                name_short_vendor += publisher.name


        c['app_id'] = application_id
        c['app_name'] = application.name
        c['app_name_short'] = name_short
        c['app_name_short_vendor'] = name_short_vendor
        c['app_version'] = application.version
        c['app_publisher'] = publisher.name
        c['app_license'] = application.get_license_txt()
        c['app_cost'] = application.cost
        c['pclist'] = application.computer_set.all()
        c["app_installation"] = application.installation
        c["app_comment"] = application.comment
        c["softpedia_content"] = softpedia_search(
                                "http://www.softpedia.com/dyn-search.php?search_term=%s"%name_short)


        c["suggestions_enable"] = suggestions_enable


    return render_to_response('appinfo.html',c)

def prices(request):
    c = {}
    c.update(csrf(request))
    publisher = models.Publisher.objects.all()
    c['licensed_software'] = models.Application.objects.filter(license=2,publisher__in=publisher)
    return render_to_response('price.html',c)



def manage(request):
    c = {}
    c.update(csrf(request))



    if request.method == 'POST':

        action = request.POST.get("action",None)

        if action is not None:
            if action == "Prices":
                return HttpResponseRedirect("/prices/")


        sw_list = request.POST.getlist('software')

        new_comment = request.POST.get('comment', None)
        new_cost = request.POST.get('cost', None)

        actions = {"Mark Free":1,"Mark Licensed":2,"Mark Unknown":0}

        if action != "reload":
            for sw_id in sw_list:
                apps = models.Application.objects.filter(id=sw_id)
                for app in apps:
                    app.license = actions[action]
                    if new_comment  is not None:
                        app.comment = new_comment
                    if app.license == 1 :
                        app.cost = 0
                    elif new_cost is not None:
                        app.cost = new_cost
                    app.save()

    c['unknown_software'] = models.Application.objects.filter(license=0)
    c['free_software'] = models.Application.objects.filter(license=1)
    c['licensed_software'] = models.Application.objects.filter(license=2)

    return render_to_response('manage.html',c)

def write_pc(computer,writer,licensed_only=False):
        writer.writerow(['',''])
        writer.writerow(['',''])
        writer.writerow([computer])

        pc_licenses = computer.licenses.all()
        print("pc   = %s"% computer.name )
        print("pc_licenses  = %s"% pc_licenses )

        if len(computer.licenses.all()) > 0:
            pc_licenses1 = [ str(x) for x in pc_licenses ]
            pc_licenses2 = ", ".join(pc_licenses1)
            #print("pc_licenses1  = %s"% pc_licenses1 )
            #print("pc_licenses2  = %s"% pc_licenses2 )

            writer.writerow(['Applied Licenses', pc_licenses2 ])

        pc_cost_sum=0
        for app in computer.applications.all():
            license_applied = ",".join( [ str(x.name) for x in app.licenses_set.all() ])


            print (app.licenses_set.all())

            if licensed_only and app.license != 2:
                pass
            else:
                publ = models.Publisher.objects.get(name=app.publisher)
                writer.writerow(['',
                                 app.get_name(),
                                 publ.get_publisher(),
                                 app.get_license_txt(),
                                 license_applied,
                                 str(app.get_cost()),
                                 '',
                                 app.get_comment()

                ])
                pc_cost_sum += app.get_cost()


        writer.writerow(['','','','','',str(pc_cost_sum)])


def download(request):
    c = {}
    c.update(csrf(request))
    licensed_only=False

    if request.method == 'POST':

        action = request.POST.get("download",None)
        print (action)
        if action is not None:
            if action == "Download Total Report (Only Licensed)":
                licensed_only = True

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="software.csv"'
        writer = csv.writer(response)
        writer.writerow(['',''])
        writer.writerow(['Computer','Software', 'Publisher', 'License', 'Applied', 'Cost','Total Cost'])
        writer.writerow(['',''])

        comp_id = request.POST['computer_id']
        if comp_id == "all" :
            for pc in models.Computer.objects.all():
                write_pc(pc,writer,licensed_only)

        else :
            computer = models.Computer.objects.get(id=comp_id)
            write_pc(computer,writer)


    return response
