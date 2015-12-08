Summary: GuardTime KSI API
Name:    libksi1
Version: 3.4.0.5
Release: 1%{?dist}
License: Apache Software License
Group:      Networking/Admin
URL: http://www.rsyslog.com/
Source0: https://github.com/rsyslog/libksi/archive/v%{version}.tar.gz
BuildRoot:  /var/tmp/%{name}-build
BuildRequires: openssl-devel
BuildRequires: curl-devel
Requires: /sbin/ldconfig

%description
LibKSI - Keyless Signature Infrastructure GuardTime client library 

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
LibKSI - Keyless Signature Infrastructure GuardTime client library 
The libksi-devel package contains the header files and libraries 
needed to develop applications using libksi.

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
%{_libdir}/libksi.so
%{_libdir}/libksi.so.1
%{_libdir}/libksi.so.1.0.0
%{_defaultdocdir}/libksi/changelog
%{_defaultdocdir}/libksi/license.txt

%files devel
%defattr(644,root,root,755)
%{_includedir}/ksi/base32.h
%{_includedir}/ksi/common.h
%{_includedir}/ksi/compatibility.h
%{_includedir}/ksi/crc32.h
%{_includedir}/ksi/err.h
%{_includedir}/ksi/hashchain.h
%{_includedir}/ksi/hash.h
%{_includedir}/ksi/hmac.h
%{_includedir}/ksi/io.h
%{_includedir}/ksi/ksi.h
%{_includedir}/ksi/list.h
%{_includedir}/ksi/log.h
%{_includedir}/ksi/net.h
%{_includedir}/ksi/net_http.h
%{_includedir}/ksi/net_tcp.h
%{_includedir}/ksi/net_uri.h
%{_includedir}/ksi/pkitruststore.h
%{_includedir}/ksi/publicationsfile.h
%{_includedir}/ksi/signature.h
%{_includedir}/ksi/tlv.h
%{_includedir}/ksi/tlv_template.h
%{_includedir}/ksi/types_base.h
%{_includedir}/ksi/types.h
%{_includedir}/ksi/verification.h
%{_libdir}/pkgconfig/libksi.pc
%{_libdir}/libksi.a
%{_libdir}/libksi.la


%changelog
* Tue Dec 12 2015 Andre Lorbach <alorbach@adiscon.com> 3.4.0.5-1
- Updated RPMs for libksi 

* Fri Jun 26 2015 Florian Riedl <friedl@adiscon.com> 3.2.2.0-1
- Created initial RPM for libksi!

