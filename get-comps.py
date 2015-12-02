#!/usr/bin/env python

import urlgrabber
import requests
import xmltodict
import re

def fetch_comps(base_url, release):
    # fetch "repomd.xml"
    r = requests.get(base_url % release + "repodata/repomd.xml")

    # parse "repomd.xml"
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    items= xmltodict.parse(r.text)["repomd"]["data"]

    for item in items:
        if "group" in item["@type"]:
            rurl = item["location"]["@href"]
            url = base_url % release + rurl
            m = re.search("-(comps-.+?.xml)", url)
            basename = url.split("/")[-1]
            name = m.groups()[0]
            print "Getting ...%s ===> %s" % (basename[-32:], name)
            urlgrabber.grabber.urlgrab(url, name)
        break


base_url_releases = "http://dl.fedoraproject.org/pub/fedora/linux/releases/%s/Everything/x86_64/os/"
releases = ["22", "23"]  # XXX can we avoid this hardcoding?

for release in releases:
    fetch_comps(base_url_releases, release)

base_url_development = "http://dl.fedoraproject.org/pub/fedora/linux/development/%s/x86_64/os/"
devs = ["rawhide"]  # XXX can we avoid this hardcoding?

for dev in devs:
    fetch_comps(base_url_development, dev)
