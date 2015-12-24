Summary: GuardTime API
Name:    libgt
Version: 0.3.11
Release: 1%{?dist}
License: Apache Software License
Group:      Networking/Admin
URL: http://www.rsyslog.com/
Source0: https://github.com/rsyslog/libgt/archive/master.zip 
BuildRoot:  /var/tmp/%{name}-build
BuildRequires: openssl-devel
BuildRequires: curl-devel
Requires: /sbin/ldconfig

%description
LibGT - GuardTime client library 

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
LibGT - GuardTime client library 
The libgt-devel package contains the header files and libraries 
needed to develop applications using libgt.

%prep
%setup -q

%build
%configure 
	#	CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libgtbase.so
%{_libdir}/libgtbase.so.0
%{_libdir}/libgtbase.so.0.0.0
%{_libdir}/libgthttp.so
%{_libdir}/libgthttp.so.0
%{_libdir}/libgthttp.so.0.0.0
%{_libdir}/libgtpng.so
%{_libdir}/libgtpng.so.0
%{_libdir}/libgtpng.so.0.0.0
%{_defaultdocdir}/libgt/changelog
%{_defaultdocdir}/libgt/license.curl.txt
%{_defaultdocdir}/libgt/license.openssl.txt
%{_defaultdocdir}/libgt/license.txt

%files devel
%defattr(644,root,root,755)
%{_includedir}/gt_base.h
%{_includedir}/gt_http.h
%{_includedir}/gt_png.h
#%{_includedir}/librsgt.h
%{_libdir}/pkgconfig/libgt.pc
%{_libdir}/libgtbase.a
%{_libdir}/libgtbase.la
%{_libdir}/libgthttp.a
%{_libdir}/libgthttp.la
%{_libdir}/libgtpng.a
%{_libdir}/libgtpng.la

%changelog
* Mon Mar 11 2013 Andre Lorbach <alorbach@adiscon.com> 0.3.0-1
- Created initial RPM for libgt!

