%global reldate 20151218
# AVOIDS CRASH BUG in make https://bugzilla.redhat.com/show_bug.cgi?id=903009
%global debug_package %{nil} 

Name:		libfastjson4
Version:	0.99.4
Release:	1%{?dist}
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/rsyslog/libfastjson
Source0:	https://github.com/rsyslog/libfastjson/archive/libfastjson-%{version}.tar.gz


BuildRoot:	%{_tmppath}/libfastjson-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool

%description
LIBFASTJSON implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the development headers and library for libfastjson.


#%package doc
#Summary:	Reference manual for json-c
#Group:		Documentation
#%if 0%{?fedora} > 10 || 0%{?rhel}>5
#BuildArch:	noarch
#%endif

#%description doc
#This package contains the reference manual for json-c.

%prep
%setup -q -n libfastjson-%{version}

#for doc in ChangeLog; do
# iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
# touch -r $doc $doc.new &&
# mv $doc.new $doc
#done

# regenerate auto stuff to avoid rpath issue
autoreconf -fi


%build
%configure  --prefix=%{_prefix} --enable-shared --disable-static --disable-rpath
# parallel build is broken for now, make %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la

# yum cannot replace a dir by a link
# so switch the dir names
#rm -rf %{buildroot}%{_includedir}/libfastjson
#mv %{buildroot}%{_includedir}/libfastjson \
#   %{buildroot}%{_includedir}/json
#ln -s libfastjson \
#   %{buildroot}%{_includedir}/libfastjson

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.html
%{_libdir}/libfastjson.so.*
#%{_libdir}/libfastjson-c.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

#%files doc
#%defattr(-,root,root,-)
#%doc doc/html/*

%changelog
* Mon Aug 03 2016 Florian Riedl <friedl@adiscon.com> - 0.99.4-1
- New RPM for libfastjson4 0.99.4

* Mon Jul 11 2016 Florian Riedl <friedl@adiscon.com> - 0.99.3-1
- New RPM for libfastjson4 0.99.3


