#!/usr/bin/env python

import requests
import urlgrabber
import urlgrabber.progress
import os
import koji

def download_urls(urls):
    for url in urls:
        basename = url.split('/')[-1]
        # basepath = os.path.expanduser("~/cache")
        basepath = "cache"
        path = os.path.join(basepath, basename)
        if not url.startswith("http"):
            return

        # XXX is this OK?
        if (not url.endswith("x86_64.rpm") and not url.endswith("noarch.rpm")) or "-debuginfo-" in url:
            if "noarch" in url:
                print "[!] badly skipped", url
            print "[+] skipping", url
            continue

        try:
            os.makedirs(basepath)
        except:
            pass

        # fetch stuff
        if os.path.exists(path):
            # print "[+] already have", basename
            continue

        print "[*] getting", url

        try:
            prog_meter = urlgrabber.progress.TextMeter()
            urlgrabber.grabber.urlgrab(url, path, progress_obj=prog_meter)
        except:
            print "XXX ;("

    return urls

# these are fixed!
topurl = 'http://kojipkgs.fedoraproject.org'
server = 'http://koji.fedoraproject.org/kojihub'
work_url = 'http://kojipkgs.fedoraproject.org/work'
taskID_url = "http://koji.fedoraproject.org/koji/taskinfo?taskID=%s"
buildrootID_url = "http://koji.fedoraproject.org/koji/buildrootinfo?buildrootID=%s"

def process_build(build_id):
    build_id = int(build_id)

    pathinfo = koji.PathInfo(topdir=topurl)
    session = koji.ClientSession(server)
    rinfo = session.getBuild(build_id)
    rpms = session.listRPMs(buildID=build_id)

    urls = []

    for rpm in rpms:
        fname = koji.pathinfo.rpm(rpm)
        url = os.path.join(pathinfo.build(rinfo), fname)
        urls.append(url)
        # print ">>", url
        # status = requests.request("HEAD", url).status_code
        # if status == 404:
        #    print "[-] failed for", url
        #    sys.exit(-1)

    return download_urls(urls)
