from docutils.nodes import version

__author__ = 'vitush'

from xml.dom.minidom import *
import models
import threading
import os
from licenses import  settings

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.files_total = 0
        self.files_loaded = 0
        self.files_current = ''
        self.last_software = ''

    def run(self):
        print "Starting " + self.name
        self.load()
        print "Exiting " + self.name

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


    def load(self):
        dir = settings.DATA_ROOT
        docs = os.listdir(dir)
        self.files_total = len(docs)

        for doc in docs:
            f= dir+"/"+doc
            print("Loading %s" % f)
            dom = xml.dom.minidom.parse(f)
            self.files_loaded = self.files_loaded + 1
            self.files_current = doc

            pc_name = dom.getElementsByTagName('Computer_name')[0].firstChild.data
            pc_owner = dom.getElementsByTagName('User_name')[0].firstChild.data
            computer, created = models.Computer.objects.get_or_create(name=pc_name, owner=pc_owner)
            if created:
                print ("New Computer added to Database : %s"% pc_name)
                computer.save()

            # Parsing installed Software
            installed_sw_container = dom.getElementsByTagName('InstalledSoftware')
            if installed_sw_container is None:
                return False

            application = None
            for ind in range(0,installed_sw_container.length-1):
                node = installed_sw_container.item(ind)

                if node is None:
                    return False

                sw = self.parse_software(node)
                self.last_software = sw['name']

                publisher, created = models.Publisher.objects.get_or_create(name=sw["publisher"])
                if created:
                    publisher.save()

                application, created = models.Application.objects.get_or_create(
                                                name=sw["name"],
                                                publisher=publisher,
                                                version=sw["version"],
                                                )
                if created:
                    application.save()

                print ("=> Found : (%s , %s)"% (computer.name,sw["name"]))

                computer.applications.add(application)

    def parse_software(self,doc):
        sw = {'name': u"Unknown",'publisher':u"Unknown", 'version':u"Unknown"}

        element = doc.getElementsByTagName('DisplayName')
        if element is not None :
            if element[0].firstChild is not None:
                if element[0].firstChild.data is not None:
                     sw["name"] = element[0].firstChild.data

        element = doc.getElementsByTagName('DisplayVersion')
        if element is not None :
            if element[0].firstChild is not None:
                if element[0].firstChild.data is not None:
                     sw["version"] += element[0].firstChild.data
                     sw["name"] += " - "
                     sw["name"] += element[0].firstChild.data


        element = doc.getElementsByTagName('Publisher')
        if element is not None:
            if element[0].firstChild is not None:
                if element[0].firstChild.data is not None:
                     sw["publisher"] = element[0].firstChild.data
        return sw


thread1 = None

def LoadData():
    global thread1
    thread1 = myThread()
    thread1.start()

def getProgress():

    if thread1 is None:
        return 100

    if thread1.files_total == 0:
        return 100

    return int(float(thread1.files_loaded)/float(thread1.files_total)*100)

def getCurrent():
    if thread1 is None:
        return ""
    return thread1.files_current

def getlastSoftware():
    if thread1 is None:
        return ""
    return thread1.last_software




