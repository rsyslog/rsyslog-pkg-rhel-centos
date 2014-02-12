Name:		liblogging
Version:	1.0.1
Release:	2%{?dist}
Summary:	LibLogging stdlog library
License:	2-clause BSD
Group:		System Environment/Libraries
URL:		http://www.liblogging.org
Source0:	http://download.rsyslog.com/liblogging/%{name}-%{version}.tar.gz 
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	chrpath

%description
LibLogging stdlog library
Libstdlog component is used for standard logging (syslog replacement)
purposes via multiple channels (driver support is planned)

%package devel
Summary:	Development files for LibLogging stdlog library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libee-devel%{?_isa} libestr-devel%{?_isa}
Requires:	pkgconfig

%description devel
The liblogging-devel package includes header files, libraries necessary for
developing programs which use liblogging library.

%prep
%setup -q

%build
%configure
V=1 make

%install
make install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"
rm -f %{buildroot}%{_libdir}/*.{a,la}
chrpath -d %{buildroot}%{_libdir}/liblogging-stdlog.so.0.0.0

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun
if [ "$1" = "0" ] ; then
    /sbin/ldconfig
fi

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/liblogging-stdlog.so.*

%files devel
%{_libdir}/liblogging-stdlog.so
%{_includedir}/liblogging/*.h
%{_libdir}/pkgconfig/liblogging-stdlog.pc


%changelog
* Tue Jan 21 2014 Andre Lorbach
- Initial Version
