#!/usr/bin/env python

import xmltodict
import sys


def something(fname, group_name):
    data = open(fname).read()
    groups = xmltodict.parse(data)["comps"]["group"]

    for group in groups:
        if group["id"].lower() == group_name.lower():
            print group_name
            packages = group["packagelist"]["packagereq"]
            for package in packages:
                print package["#text"]
        """
        if "group" in item["@type"]:
            rurl = item["location"]["@href"]
            url = base_url % release + rurl
            m = re.search("-(comps-.+?.xml)", url)
            basename = url.split("/")[-1]
            name = m.groups()[0]
            print "Getting ...%s ===> %s" % (basename[-32:], name)
            urlgrabber.grabber.urlgrab(url, name)
        """

if len(sys.argv) < 3:
    sys.stderr.write("Usage: %s <comps.xml file> <group>\n" % sys.argv[0])
    sys.exit(-1)

something(sys.argv[1], sys.argv[2])
