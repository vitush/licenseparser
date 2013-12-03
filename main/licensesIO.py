__author__ = 'vitush'

from xml.dom.minidom import *
import models
import os

def parse_software(doc):
    sw = {'name': u"Unknown",'publisher':u"Unknown"}

    element = doc.getElementsByTagName('DisplayName')
    if element is not None :
        if element[0].firstChild is not None:
            if element[0].firstChild.data is not None:
                 sw["name"] = element[0].firstChild.data

#    element = doc.getElementsByTagName('DisplayVersion')
#    if element is not None :
#        if element[0].firstChild is not None:
#            if element[0].firstChild.data is not None:
#                 sw["name"] += " "
#                 sw["name"] += element[0].firstChild.data

    element = doc.getElementsByTagName('Publisher')
    if element is not None:
        if element[0].firstChild is not None:
            if element[0].firstChild.data is not None:
                 sw["publisher"] = element[0].firstChild.data
    return sw


def loadData(dir):
    docs = os.listdir(dir)

    for doc in docs:
        f= dir+"/"+doc
        print("Loading %s" % f)
        dom = xml.dom.minidom.parse(f)

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

            sw = parse_software(node)

            publisher, created = models.Publisher.objects.get_or_create(name=sw["publisher"])
            if created:
                publisher.save()

            application, created = models.Application.objects.get_or_create(
                                            name=sw["name"],
                                            publisher=publisher
                                            )
            if created:
                application.save()
                print ("=> Added to SoftwareDB: (%s , %s) - New!"% (computer.name,sw["name"]))
            else:
                print ("=> Added to SoftwareDB: (%s , %s)"% (computer.name,sw["name"]))

            computer.applications.add(application)




