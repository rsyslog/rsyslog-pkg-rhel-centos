Name:    adisconbuild-librdkafka
# NOTE: Make sure to update this to match rdkafka.h version
Version: 1.9.2
Release: 5
%define soname 1
%define _unpackaged_files_terminate_build 0

Summary: The Apache Kafka C library
Group:   Development/Libraries/C and C++
License: BSD-2-Clause
URL:     https://github.com/edenhill/librdkafka
Source:	 adisconbuild-librdkafka-%{version}.tar.gz

BuildRequires: wget curl openssl-devel libcurl-devel libtool zlib-devel libstdc++-devel gcc >= 4.1 gcc-c++ cyrus-sasl-devel 
%if %{?rhel} >= 8
BuildRequires: python3-devel
%else
BuildRequires: python-devel
%endif
 
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
librdkafka is a C/C++ library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.
It was designed with message delivery reliability and high performance in mind, current figures exceed 800000 msgs/second for the producer and 3 million msgs/second for the consumer.


%package -n %{name}%{soname}
Summary: The Apache Kafka C library
Group:   Development/Libraries/C and C++
Requires: zlib libstdc++ cyrus-sasl

%description -n %{name}%{soname}
librdkafka is a C/C++ library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.


%package -n %{name}-devel
Summary: The Apache Kafka C library (Development Environment)
Group:   Development/Libraries/C and C++
Requires: %{name}%{soname} = %{version}

%description -n %{name}-devel
librdkafka is a C/C++ library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.

This package contains headers and libraries required to build applications
using librdkafka.


%prep
%setup -q -n %{name}-%{version}

%configure --install-deps --disable-lz4-ext --disable-hdrhistogram --enable-static 

%build
cat config.log
make
examples/rdkafka_example -X builtin.features

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} make install

%clean
rm -rf %{buildroot}

%post   -n %{name}%{soname} -p /sbin/ldconfig
%postun -n %{name}%{soname} -p /sbin/ldconfig

%files -n %{name}%{soname}
%defattr(444,root,root)
%{_libdir}/librdkafka.so.%{soname}
%{_libdir}/librdkafka++.so.%{soname}
%defattr(-,root,root)
%doc %{_docdir}/librdkafka/README.md
%doc %{_docdir}/librdkafka/LICENSE
%doc %{_docdir}/librdkafka/CONFIGURATION.md
%doc %{_docdir}/librdkafka/INTRODUCTION.md
%doc %{_docdir}/librdkafka/STATISTICS.md
%doc %{_docdir}/librdkafka/CHANGELOG.md
%doc %{_docdir}/librdkafka/LICENSES.txt

%defattr(-,root,root)
#%{_bindir}/rdkafka_example
#%{_bindir}/rdkafka_performance


%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/librdkafka
%defattr(444,root,root)
%{_libdir}/librdkafka.a
%{_libdir}/librdkafka-static.a
%{_libdir}/librdkafka.so
%{_libdir}/librdkafka++.a
%{_libdir}/librdkafka++.so
%{_libdir}/pkgconfig/rdkafka++.pc
%{_libdir}/pkgconfig/rdkafka.pc
%{_libdir}/pkgconfig/rdkafka-static.pc
%{_libdir}/pkgconfig/rdkafka++-static.pc

%changelog
* Thu Nov 17 2022 Andre Lorbach
- Add missing static build files

* Wed Nov 16 2022 Andre Lorbach
- ReBuild for static building

* Wed Aug 25 2022 Andre Lorbach
- Build dependency package 1.9.2

* Wed Oct 31 2018 Florian Riedl
- Re-Build dependency package 0.11.6

* Tue Oct 30 2018 Florian Riedl
- Build dependency package 0.11.6

* Thu Aug 02 2018 Florian Riedl
- Build dependency package 0.11.5

* Tue Jan 09 2018 Florian Riedl
- Build dependency package 0.11.4

* Tue Jan 09 2018 Florian Riedl
- Build dependency package 0.11.3

* Tue Nov 28 2017 Florian Riedl
- Build dependency package 0.11.1

* Wed Oct 04 2017 Florian Riedl
- Re-build for SSL support

* Mon Oct 02 2017 Florian Riedl
- Build dependency package 0.11.0

* Mon Jun 26 2017 Florian Riedl
- Build dependency package 0.9.5

* Mon Jun 29 2015 Florian Riedl
- New RPM for librdkafka 0.8.6

* Tue Mar 17 2015 Florian Riedl
- Initial package build for librdkafka 0.8.5 to support rsyslog and omkafka packages

* Fri Oct 24 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.5-0
- 0.8.5 release

* Mon Aug 18 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.4-0
- 0.8.4 release

* Mon Mar 17 2014 Magnus Edenhill <vk@edenhill.se> 0.8.3-0
- Initial RPM package
