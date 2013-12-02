Name:           czmq
Version:        1.3.2
Release:        1%{?dist}
Summary:        High-level C binding for 0MQ (ZeroMQ)

Group:          Development/Libraries
License:        LGPLv3+
URL:            http://czmq.zeromq.org/
Source0:        http://download.zeromq.org/czmq-%{version}.tar.gz

BuildRequires:  libuuid-devel
BuildRequires:  zeromq3-devel

%description
CZMQ has the following goals:
  i) To wrap the ØMQ core API in semantics that are natural and lead to
     shorter, more readable applications.
 ii) To hide the differences between versions of ØMQ.
iii) To provide a space for development of more sophisticated API semantics.


%package devel
Summary:        Development files for the czmq package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zeromq3-devel
Requires:       pkgconfig

%description devel
This package contains files needed to develop applications using czmq.


%prep
%setup -q

chmod -c a-x AUTHORS COPYING* NEWS


%build
%configure

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/libczmq.{a,la}


%check
LD_LIBRARY_PATH=%{buildroot}/%{_libdir} make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING* NEWS
%{_libdir}/*.so.*

%files devel
%{_bindir}/czmq_selftest
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man7/*.7*


%changelog
* Thu Dec 20 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3.2-1
- Improve the description.

* Wed Dec 12 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3.2-0
- Update to 1.3.2.

* Sun Oct 28 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3.1-1
- Update to 1.3.1.

* Thu Oct 25 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3.0-0
- Rename to libczmq.
- Update to v1.3.0 git snapshot.

* Tue Oct 23 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.2.0-3
- Make czmq-devel require zeromq3-devel.

* Sat Oct 20 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.2.0-2
- Build against limzmq v3.x (BR zeromq3-devel instead of zeromq-devel).

* Sat Oct 20 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.2.0-1
- First Fedora build.

# vim:set ai ts=4 sw=4 sts=4 et:
