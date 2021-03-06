Summary: 	Creates a common metadata repository
Name: 		createrepo_c
Version: 	0.10.0
Release: 	1%{?dist}
License:	GPLv2+
Group: 		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0: 	%{name}-%{version}.tar.gz
%define sha1 createrepo_c=b2333b490575cf1199d78ca1945c5808f41c6440
URL: 		https://github.com/rpm-software-management/createrepo_c
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  file-devel
BuildRequires:  glib-devel
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
BuildRequires:  rpm-devel
BuildRequires:  xz-devel
BuildRequires:  sqlite-devel
Obsoletes:      createrepo
Provides:       createrepo

%description
C implementation of the createrepo.

%package devel
Summary:    Library for repodata manipulation
Requires:   %{name} = %{version}-%{release}

%description devel
headers and libraries for createrepo_c

%prep
%setup -q
sed -e '/find_package(GTHREAD2/ s/^#*/#/' -i CMakeLists.txt
sed -i 's|g_thread_init|//g_thread_init|'  src/createrepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/mergerepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/modifyrepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/sqliterepo_c.c

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}
ln -sf %{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
/etc/bash_completion.d/createrepo_c.bash
%{_bindir}/*
%{_lib64dir}/*.so.*
%{_mandir}/*
%exclude %{_libdir}/python*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_lib64dir}/*.so
%{_lib64dir}/pkgconfig/%{name}.pc

%changelog
* Wed Oct 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.10.0-1
- Initial
