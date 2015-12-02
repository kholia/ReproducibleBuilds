TODO
====

Many of these improvements were suggested by Florian and Dan.

* Improve "rpm-compare" script.

  - We should compare the contents of ELF data sections as well.

  - We should check executable contents in the RPM headers, like %pre and %post
    scripts.

  - The rpm2cpio unpacking discards file permissions and the like, and doesn't
    cover ghost files. Porting this to Python using librpm can solve this and
    other problems.

  - It might also make sense to do an extremely low-level comparison of the RPM
    header, showing differences that cannot be explained in some way. This
    would catch the addition of new RPM tags with scripts, too. I'm not sure
    if this is possible with librpm. PyRPM might be of help there because it
    has tools to do such diffing which were used during its development.

* Support lookups in directories in "cache.

* Add "Visual Diff" support.


Steps Involved
==============

* Recording the build environment (DONE)

  - Koji does this automatically :-)

* Re-producing the build environment (DONE)

  - Fetch all artefacts from upstream (optional)

    - Confirm the upstream binary is the one you have (trivial)

  - Retrieve "brootid" (buildrootID) corresponding to the NVR we want to test from
    Koji

    - Example task: http://koji.fedoraproject.org/koji/taskinfo?taskID=5447934

    - Example buildroot: http://koji.fedoraproject.org/koji/buildrootinfo?buildrootID=1701634

    - We now have script(s) to do this.

  - Replicate this buildroot (DONE)

    - http://tinyurl.com/replicate-buildroot-using-mock

    - koji mock-config --buildroot=<buildrootID> name

    - e.g. koji mock-config --buildroot=1701634 UpEnv --topurl=http://kojipkgs.fedoraproject.org/ > UpEnv.cfg

  - Create replica build environment using "Mock" (DONE)

* Do re-builds locally using mock (DONE)

* Verify new build against upstream (DONE, Steve's script works great)

Notes
-----

* rpm-compare-0.3.tar.gz is used currently.
