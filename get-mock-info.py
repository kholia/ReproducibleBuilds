#!/usr/bin/env python

import koji
import sys
from tasks import process_build
import common

# these are fixed!
topurl = 'http://kojipkgs.fedoraproject.org'
server = 'http://koji.fedoraproject.org/kojihub'
work_url = 'http://kojipkgs.fedoraproject.org/work'
taskID_url = "http://koji.fedoraproject.org/koji/taskinfo?taskID=%s"
buildrootID_url = "http://koji.fedoraproject.org/koji/buildrootinfo?buildrootID=%s"


def fetch_koji_build(build):
    """
    build ==> buildID or NVR
    """

    if build.endswith(".src.rpm"):  # be a bit more friendly
        build = build.replace(".src.rpm", "")

    if build.isdigit():
        build = int(build)

    urls = []  # output

    pathinfo = koji.PathInfo(topdir=topurl)
    session = koji.ClientSession(server)
    info = session.getBuild(build)

    if not info:
        print >> sys.stderr, "getBuild() returned nothing, check you NVR!"
        return

    # file where we record the buildroot environment information
    f = open(build + ".env", "wb")

    task_id = info["task_id"]
    nvr = info.get("nvr", str(task_id))
    package = info.get("name", str(task_id))

    task = session.getTaskInfo(task_id, request=True)
    if not task:
        return
    for item in task["request"]:
        if not isinstance(item, str):
            continue
    if not task:
        print('Invalid task ID: %i' % task_id)
    elif task['state'] in (koji.TASK_STATES['FREE'], koji.TASK_STATES['OPEN']):
        print('Task %i has not completed' % task['id'])
    elif task['state'] != koji.TASK_STATES['CLOSED']:
        print('Task %i did not complete successfully' % task['id'])

    if task['method'] == 'build':
        # print 'Getting artifacts from children of task %i: %s' % (task['id'], \
        #        koji.taskLabel(task))
        tasks = session.listTasks(opts={'parent': task_id, \
            'method': 'buildArch', \
            'state': [koji.TASK_STATES['CLOSED']], \
            'decode': True})
    elif task['method'] == 'buildArch':
        tasks = [task]
    else:
        print('Task %i is not a build or buildArch task' % task['id'])

    # results from the worker(s)
    results = []

    for task in tasks:
        task_id = task['id']
        # print ">>>>", task, task['id']
        # print ">>>> Processing taskID", task['id'], taskID_url % task_id
        # arch = task.get('arch', 'unkwown')
        # output = session.listTaskOutput(task['id'])
        # print ">>>> Output =>", arch, output
        brootid = task['result'][0]["brootid"]
        print ">>>>", buildrootID_url % brootid, "\n"
        # logs = [filename for filename in output if filename.endswith('.log')]
        # broots = session.listBuildroots(taskID=task_id)
        # print broots
        opts = {}
        opts['componentBuildrootID'] = brootid
        data = session.listRPMs(**opts)
        pathinfo = koji.PathInfo(topdir=topurl)

        for rpm in data:
            nvr = rpm["nvr"]
            arch = rpm["arch"]
            name = (nvr + "." + arch + ".rpm")

            # XXX is this OK for now?
            if arch != "x86_64" and arch != "noarch":
                print "[*] skipping", name
                continue
            f.write("%s\n" % (nvr + "." + arch + ".rpm"))
            # if common.cache_lookup(name):
            #    print "[+] already have", name
            #     continue
            print "[!] pushing", rpm["nvr"], rpm["build_id"]
            result = process_build.delay(str(rpm["build_id"]))
            results.append(result)

    for result in results:
        urls = list(result.collect())[0][1]  # [0][0] is some status
        for url in urls:
            basename = url.split("/")[-1]
            if not "-debuginfo-" in basename and \
                not basename.endswith("src.rpm"):
                f.write("%s\n" % basename)
                print "[^] back-processing", basename

    f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: %s <buildID or NVR>" % sys.argv[0]

        sys.exit(-1)

    common.cache_initialize()

    fetch_koji_build(sys.argv[1])
