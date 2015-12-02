Reproducible Builds
===================

It should be possible to reproduce every build of every package in Fedora
(strong, long-term goal).

It should be possible for the users to verify that the binary matches what the
source intended to produce, in an independent fashion.

I want to be able to show that our binary was the result of our source code
from our compiler and nobody added anything along the way.

Can we (upstream / vendor) show that one of our rpms was built from the source
we ship?

We (the distribution provider) shouldn't be forced to say "Trust Us" to our
users at all.

Current Problems
----------------

* `mock` needs to be enhanced to generate .buildinfo files. Debian folks would
  like to diff their own builds of the same package.

* `mock` should support the SOURCE_DATE_EPOCH specification.

* The "%files" section in the .spec files creates folders, and files with new
  timestamps (which breaks reproducibility). Currently, we get around this
  problem by pre-creating those folders in the "%install" section.

* We also use `%define debug_package %{nil}` currently to reduce the differeces
  between the builds.

Setup
-----

```
# On Fedora
sudo dnf install python-celery python-requests koji \
    python-urlgrabber python-setuptools python-billiard \
    redis python-redis createrepo -y

sudo service redis start; sudo chkconfig redis on

# On Ubuntu
sudo apt-get install mock python-celery python-requests \
      python-urlgrabber python-setuptools python-billiard \
      redis-server python-redis

# steal "group" information from upstream files
python get-comps.py

ln -s comps-f23.xml comps.xml  # use "comps-f22.xml" file or others if need be

mkdir ~/cache  # RPM cache for mock
```


Usage
-----

* Initially, we have a NVR (Name-Version-Release) we want to verify (e.g. git-2.5.0-3.fc23).

  Let us assume that we have the corresponding RPM file(s) which are provided
  by the vendor, and which we want to verify.

* First, we obtain the SRPM corresponding to the target RPM file(s).

  ``https://dl.fedoraproject.org/pub/fedora/linux/releases/23/Everything/source/``

* Next, we need to replicate the original buildroot.


  - Gather information about the buildroot corresponding to the NVR.

    ```
    python get-mock-info.py git-2.5.0-3.fc23
    ```

    This step will populate the RPM "cache" and generate
    ``git-2.5.0-3.fc23.env`` file which contains the buildroot replication
    information (aka `buildinfo` file).

  - Start the Celery job to download the packages.

    ``
    celery worker --autoscale=10,0 -A tasks
    ``

  - Make repository which will be used by Mock.

    ```
    ./makerepo.sh git-2.5.0-3.fc23.env myrepo
    ```

    This command will create ``myrepo`` folder (which is our repository) by using
    the RPM "cache".

    This command will also create a ``myrepo.cfg`` file which is a Mock
    configuration file.

* Build the SRPM using mock.

  ```
  mock -r myrepo --configdir=. --rebuild git-2.5.0-3.fc23.src.rpm
  ```

* Compare upstream build with our local build.

  ```
  ./rpm-compare /upstream/git-2.5.0-3.fc23.x86_64.rpm \
      /var/lib/mock/myrepo/result/git-2.5.0-3.fc23.x86_64.rpm
  ```

TODO
----

* Package "Koji" for Debian.
  - https://ftp-master.debian.org/new/koji_1.10.0-1.html

* Package "diffoscope" for Fedora.
  - https://fedorapeople.org/~halfie/packages/diffoscope/
  - https://fedorapeople.org/~halfie/packages/python-libarchive-c/ (conflicts with python-libarchive potentially)
  - https://reproducible.debian.net/rb-pkg/unstable/amd64/bash.html

* Verify the packages while they are being downloaded.

* RPM and redhat-rpm-config patches (get them upstream)
  - https://github.com/kholia/rpm/commits/reproducible-builds
  - https://github.com/kholia/redhat-rpm-config
  - https://bugzilla.redhat.com/show_bug.cgi?id=1288713 (Allow SOURCE_DATE_EPOCH to override RPMTAG_BUILDTIME)
  - https://anonscm.debian.org/cgit/reproducible/dpkg.git/log/?h=pu/reproducible_builds

* Rename `.env` to `.buildinfo`

Patched Tools Repository
------------------------

https://fedorapeople.org/~halfie/repository/

```
mock -r ./fedora-23-x86_64-reproducible-builds.cfg diffoscope-42-1.fc23.src.rpm
```

`fedora-23-x86_64-reproducible-builds.cfg` uses the above repository automatically.

Current State
-------------

* Packages like git and john are 100% reproducible as far as code is concerned
  :-)

* We support "Recursive Verification". For example, if building "Z" requires
  installing "Y" RPM, then, once we have verified that Z is OK, we can ask our
  tool to verify "Y" too and so on.

Credits
-------

* Ximin Luo for the name "remock".

Current Challenges
------------------

See https://reproducible-builds.org/docs/

Links
-----

https://fedoraproject.org/wiki/Reproducible_Builds

https://mikem.fedorapeople.org/Talks/flock-2015-koji-reproducibility/#/

https://securityblog.redhat.com/2013/09/18/reproducible-builds-for-fedora/

https://wiki.debian.org/ReproducibleBuilds

http://fedoraproject.org/wiki/Releases/FeatureBuildId#Unique_build_ID

http://blogs.kde.org/2013/06/19/really-source-code-software

https://blog.torproject.org/blog/deterministic-builds-part-one-cyberwar-and-global-compromise

https://trac.torproject.org/projects/tor/ticket/5837

https://trac.torproject.org/projects/tor/ticket/3688

http://bazaar.launchpad.net/~ubuntu-security/ubuntu-security-tools/trunk/files/head:/package-tools/
