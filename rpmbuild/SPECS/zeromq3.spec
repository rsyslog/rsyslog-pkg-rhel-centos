%bcond_without pgm

Name:           zeromq3
Version:        3.2.2
Release:        2%{?dist}
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.zeromq.org
# VCS:          git:git://github.com/zeromq/libzmq.git
# VCS:          git:git://github.com/zeromq/zeromq3-x.git
#####
#Source0:        http://download.zeromq.org/zeromq-%%{version}.tar.gz
#####
# created with:
# git clone git:http://github.com/zeromq/libzmq.git && cd limzmq
# git archive --format=tar.gz --prefix=zeromq-3.2.0/ 1ef63bc2adc3d50 > zeromq-3.2.0.tar.gz
#Source0:        zeromq-%%{version}.tar.gz
# needed BR for checkout
#BuildRequires:  autoconf
#BuildRequires:  libtool
#####
# rc's
Source0:        http://download.zeromq.org/zeromq-%{version}.tar.gz
#####
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
%if %{with pgm}
BuildRequires:  openpgm-devel >= 5.1
%endif


%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library for versions 3.x.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      zeromq-devel%{?_isa}


%description devel
The %{name}-devel package contains libraries and header files for 
developing applications that use %{name} 3.x.


%prep
%setup -qn zeromq-%{version}

# remove bundled libraries
rm -rvf foreign/*/*tar*

# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure


%build
%configure \
%if %{with pgm}
            --with-system-pgm \
%endif
            --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la


#%check
#make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS README
%{_libdir}/libzmq.so.*

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*
%{_mandir}/man3/zmq*.3*
%{_mandir}/man7/zmq*.7*


%changelog
* Fri Dec 14 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-2
- add bcond_without pgm macro (Jose Pedro Oliveira, #867182)
- remove bundled pgm
- add zeromq-3 git repository

* Tue Nov 27 2012 Andrew Niemantsverdriet <andrewniemants@gmail.com - 3.2.2-1
- update to 3.2.2

* Wed Oct 17 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.1-0.1.rc2
- update to 3.2.1-rc2 (#867182)

* Fri Oct 12 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.0-0.3.20121009git1ef63bc
- remove defattr and rm -rf buildroot

* Wed Oct 10 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.0-0.2.20121009git1ef63bc
- delete defattr and remove (>el5) macro to only target el6+ and fc17+
- conflict with zeromq-devel
- use proper version

* Wed Oct 10 2012 Thomas  Spura <tomspur@fedoraproject.org> - 3.2.0-0.1
- update to 3.2.0 past rc1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Sat Jan  7 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.11-1
- update to 2.1.11 (as part of rebuilding with gcc-4.7)

* Tue Sep 20 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-1
- update to 2.1.9
- add check section

* Wed Apr  6 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-1
- update to new version (#690199)

* Wed Mar 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.3-1
- update to new version (#690199)
- utils subpackage was removed upstream
  (obsolete it)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Pavel Zhukov <pavel@zhukoff.net> - 2.0.10-1
- update version
- add rpath delete
- change includedir filelist

* Fri Aug 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-1
- update to new version

* Fri Jul 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-4
- upstream VCS changed
- remove buildroot / %%clean
- change descriptions

* Tue Jul 20 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-3
- move binaries to seperate utils package

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-2
- remove BR: libstdc++-devel
- move man3 to the devel package
- change group to System Environment/Libraries

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-1
- initial package (based on upstreams example one)
