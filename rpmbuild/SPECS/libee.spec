Summary: An event expression library inspired by CEE
Name:    libee
Version: 0.4.1
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://www.libee.org/
Source0: http://www.libee.org/download/files/download/%{name}-%{version}.tar.gz
# Patch1: libee-0.4.1-makefile.patch
BuildRoot:  /var/tmp/%{name}-build
BuildRequires: libestr-devel
Requires: /sbin/ldconfig

%description
CEE is an upcoming standard used to describe network events in a number of
normalized formats. It's goal is to unify they currently many different
representations that exist in the industry.

The core idea of libee is to provide a small but hopefully convenient API layer
above the CEE standard. However, CEE is not finished. At the time of this writing,
CEE is under heavy development and even some of its core data structures (like
the data dictionary and taxonmy) have not been fully specified.

libee should be thought of as a useful library that helps you get your events
normalized. If you program cleanly to libee, chances are not bad that only
relatively little effort is required to move your app over to be CEE compliant
(once the standard is out).

%package devel
Summary: include files for libee
Group: Networking/Admin
Requires: %name = %version-%release
Requires: /usr/bin/pkg-config

%description devel
Libee, an Event Expression Library inspired by CEE. The
libee-devel package contains the header files and libraries needed
to develop applications using libee.

%prep
%setup -q -n %{name}-%{version}
# %patch1 -p1

%build
%configure CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

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
%{_libdir}/libee.so
%{_libdir}/libee.so.0
%{_libdir}/libee.so.0.0.0

%files devel
%defattr(644,root,root,755)
%{_sbindir}/libee-convert
%{_libdir}/pkgconfig/libee.pc
%{_libdir}/libee.a
%{_libdir}/libee.la
%{_includedir}/libee/apache.h
%{_includedir}/libee/ctx.h
%{_includedir}/libee/event.h
%{_includedir}/libee/field.h
%{_includedir}/libee/fieldbucket.h
%{_includedir}/libee/fieldset.h
%{_includedir}/libee/fieldtype.h
%{_includedir}/libee/int.h
%{_includedir}/libee/internal.h
%{_includedir}/libee/libee.h
%{_includedir}/libee/namelist.h
%{_includedir}/libee/obj.h
%{_includedir}/libee/parser.h
%{_includedir}/libee/primitivetype.h
%{_includedir}/libee/tag.h
%{_includedir}/libee/tagbucket.h
%{_includedir}/libee/tagset.h
%{_includedir}/libee/timestamp.h
%{_includedir}/libee/valnode.h
%{_includedir}/libee/value.h
%{_includedir}/libee/valuetype.h

%changelog
* Tue Jun 12 2012 Abby Edwards <abby.lina.edwards@gmail.com> 0.4.1-1
- initial version, used to build latest git master
