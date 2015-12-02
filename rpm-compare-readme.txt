		rpm-compare 0.3

The rpm-compare program should be run from its own directory. Its fine
to use the directory that it installed to. The python helper script must
be in the same directory.

The rpm-compare program has dependencies on the following packages:
	* coreutils
	* file
	* python
	* gawk
	* rpm
	* cpio
	* diffutils
	* grep
	* binutils

They must be installed or the rpm-compare script will not work correctly.

The rpm-compare commandline options look like this:

rpm-compare [-v] [--verbose] rpm1 rpm2

To use the the rpm-compare script, you simply pass it the path to 2 rpms.
The path can be either relative to the rpm-compare command or an absolute
path to the rpms that are being compared. The script will tell you how many
differences it detected during the comparison. If you wish to see the
actual differences, then you can pass a --verbose command line option.
This will show more detail about what it detected as being different between
the rpms. The following is an example usage:

./rpm-compare --verbose \
  /var/cache/yum/updates/packages/rpm-python-4.11.1-1.fc19.x86_64.rpm \
  /var/cache/yum/updates/packages/rpm-python-4.11.1-3.fc19.x86_64.rpm


-Steve Grubb

