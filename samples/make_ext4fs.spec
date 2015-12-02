%global commit0 bd53eaafbc2a89a57b8adda38f53098a431fa8f4
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
# XXX
%define debug_package %{nil}

Name:		make_ext4fs
Version:	0
Release:	0.1.20151203git%{shortcommit0}%{?dist}

Summary:	Reproducible ext4 image creator
License:	ASL 2.0
Vendor:		OpenWRT
URL:		http://git.openwrt.org/?p=project/make_ext4fs.git

Source0:	http://git.openwrt.org/?p=project/%{name}.git;a=snapshot;h=%{commit0};sf=tgz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:	zlib-devel

%description
Tool to create reproducible ext4 image files.

%prep
%setup -qn %{name}-%{shortcommit0}
# find %{_builddir}/%{name}-%{shortcommit0} -exec touch -d @"$RPM_CHANGELOG_DATE" {} \;

%build
make

%install
install -m 755 -d %{buildroot}/usr/bin
install -m 755 -t %{buildroot}/usr/bin make_ext4fs
mkdir -p %{buildroot}/usr/share/licenses/make_ext4fs
cp -pr %{_builddir}/%{name}-%{shortcommit0}/NOTICE %{buildroot}/usr/share/licenses/make_ext4fs

%files
# this breaks reproducibility!
%license NOTICE
/usr/bin/make_ext4fs

%changelog
* Wed Dec 02 2015 Wojtek Porczyk <woju@invisiblethingslab.com> 0-0.1.20151203gitbd53eaa
- initial package
