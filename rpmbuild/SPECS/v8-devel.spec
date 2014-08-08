%global _exec_prefix %{nil}
%global _libdir %{_exec_prefix}/%{_lib}
%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog

# Set PIDFILE Variable!
%if 0%{?rhel} >= 6
	%define Pidfile syslogd.pid
	%define rsysloginit rsyslog.init.epel6
	%define rsysloglog rsyslog.log.epel6
%else
	%define Pidfile rsyslogd.pid
	%define rsysloginit rsyslog.init.epel5
	%define rsysloglog rsyslog.log.epel5
%endif

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.3.5
Release: 1%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: %{rsysloginit}
Source2: rsyslog_v7.conf
Source3: rsyslog.sysconfig
Source4: %{rsysloglog}
Requires: libgt
BuildRequires: libestr-devel
BuildRequires: libee-devel
BuildRequires: json-c-devel
BuildRequires: curl-devel
BuildRequires: libgt-devel
BuildRequires: python-docutils
BuildRequires: jemalloc-devel
BuildRequires: liblogging-devel

# json-c.i686
# tweak the upstream service file to honour configuration from /etc/sysconfig/rsyslog
# NOT NEEDED ANYMORE Patch0: Patch0: rsyslog-7.1.0-systemd.patch
# already patched 
# Patch1: rsyslog-5.8.7-sysklogd-compat-1-template.patch
# Patch2: rsyslog-5.8.7-sysklogd-compat-2-option.patch

BuildRequires: zlib-devel
Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
Provides: syslog
Obsoletes: sysklogd < 1.5-11
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# %package sysvinit
# Summary: SysV init script for rsyslog
# Group: System Environment/Daemons
# Requires: %name = %version-%release
# Requires(post): /sbin/chkconfig

%package libdbi
Summary: libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql-devel >= 4.0

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

# bugged 
#%package gssapi
#Summary: GSSAPI authentication and encryption support for rsyslog
#Group: System Environment/Daemons
#Requires: %name = %version-%release
#BuildRequires: krb5-devel 

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.1.1
BuildRequires: librelp-devel 

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel

%package mmjsonparse
Summary: mmjsonparse support 
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package mmnormalize
Summary: mmnormalize support 
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package mmfields
Summary: mmfields support 
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package mmanon
Summary: mmanon support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package ommail
Summary: Mail support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package pmciscoios
Summary: pmciscoios support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%if 0%{?rhel} >= 6
%package elasticsearch
Summary: Provides the omelasticsearch module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libuuid-devel
BuildRequires: libcurl-devel

# Package BUGGED!
#%package zmq3
#Summary: zmq3 support
#Group: System Environment/Daemons
#Requires: %name = %version-%release
#BuildRequires: czmq-devel

%package mongodb
Summary: MongoDB output support 
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mongodb-devel
BuildRequires: libmongo-client-devel
%endif

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

#%description sysvinit
#SysV style init script for rsyslog. It needs to be installed only if systemd
#is not used as the system init process.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

# bugged 
#%description gssapi
#The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI 
#authentication and secure connections. GSSAPI is commonly used for Kerberos 
#authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol. 

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%description mmjsonparse
The rsyslog-mmjsonparse package provides mmjsonparse filter support. 

%description mmnormalize
The rsyslog-mmnormalize package provides log normalization 
by using the liblognorm and it's Rulebase format. 

%description mmfields
Parse all fields of the message into structured data inside the JSON tree.

%description mmanon
IP Address Anonimization Module (mmanon).
It is a message modification module that actually changes the IP address 
inside the message, so after calling mmanon, the original message can 
no longer be obtained. Note that anonymization will break digital 
signatures on the message, if they exist.

%description pmciscoios
Parser module which supports various Cisco IOS formats.

%description ommail
Mail Output Module.
This module supports sending syslog messages via mail. Each syslog message 
is sent via its own mail. The ommail plugin is primarily meant for alerting users. 
As such, it is assume that mails will only be sent in an extremely 
limited number of cases.

%if 0%{?rhel} >= 6
%description elasticsearch
The rsyslog-elasticsearch package provides omelasticsearch module support. 

#%description zmq3
#zmq3 support for RSyslog. These plugins allows you to push data from 
#and into rsyslog from a zeromq socket.

%description mongodb
MongoDB output plugin for rsyslog. This plugin allows rsyslog to write 
the syslog messages to MongoDB, a scalable, high-performance, 
open source NoSQL database.
%endif

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%build
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DSYSLOGD_PIDNAME=\\\"%{Pidfile}\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"%{Pidfile}\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif
#		--enable-imzmq3 \
#		--enable-omzmq3 \
#		--enable-gssapi-krb5 \	# bugged
%configure	--disable-static \
		--disable-testbench \
%if 0%{?rhel} >= 6
		--enable-uuid \
		--enable-elasticsearch \
		--enable-ommongodb \
	        --enable-usertools \
%else
		--disable-uuid \
		--enable-cached-man-pages \
		--disable-generate-man-pages \
%endif
		--enable-gnutls \
		--enable-imfile \
		--enable-impstats \
		--enable-imptcp \
		--enable-libdbi \
		--enable-mail \
		--enable-mysql \
		--enable-omprog \
		--enable-omudpspoof \
		--enable-omuxsock \
		--enable-pgsql \
		--enable-pmlastmsg \
		--enable-relp \
		--enable-snmp \
		--enable-unlimited-select \
		--enable-mmjsonparse \
		--enable-mmnormalize \
		--enable-mmanon \
		--enable-mail \
		--enable-mmfields \
		--enable-mmpstrucdata \
		--enable-mmsequence \
		--enable-pmciscoios \
		--enable-guardtime \
		--enable-jemalloc

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.d
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_statedir}
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_pkidir}

install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/rsyslog
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/syslog
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.conf

#get rid of *.la
rm $RPM_BUILD_ROOT/%{_libdir}/rsyslog/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rsyslog
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done

%preun
if [ $1 = 0 ]; then
	service rsyslog stop >/dev/null 2>&1 ||:
	/sbin/chkconfig --del rsyslog
fi

%postun
if [ "$1" -ge "1" ]; then
	service rsyslog condrestart > /dev/null 2>&1 ||:
fi 


%triggerun -- rsyslog < 5.7.8-1
## Save the current service runlevel info
## User must manually run systemd-sysv-convert --apply rsyslog
## to migrate them to systemd targets
#%{_bindir}/systemd-sysv-convert --save rsyslog >/dev/null 2>&1 || :
#/bin/systemctl enable rsyslog.service >/dev/null 2>&1 || :
#/sbin/chkconfig --del rsyslog >/dev/null 2>&1 || :
#/bin/systemctl try-restart rsyslog.service >/dev/null 2>&1 || :
# previous versions used a different lock file, which would break condrestart
[ -f /var/lock/subsys/rsyslogd ] || exit 0
mv /var/lock/subsys/rsyslogd /var/lock/subsys/rsyslog
[ -f /var/run/rklogd.pid ] || exit 0
/bin/kill `cat /var/run/rklogd.pid 2> /dev/null` > /dev/null 2>&1 ||:

#%triggerpostun -n rsyslog-sysvinit -- rsyslog < 5.8.2-3
#/sbin/chkconfig --add rsyslog >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* NEWS README ChangeLog 
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
# %{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/lmcry_gcry.so
%{_libdir}/rsyslog/lmsig_gt.so
%{_libdir}/rsyslog/mmpstrucdata.so
%{_libdir}/rsyslog/mmsequence.so
%{_libdir}/rsyslog/mmexternal.so
%if 0%{?rhel} >= 6
%{_bindir}/rscryutil
%{_bindir}/rsgtutil
%endif
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_initrddir}/rsyslog
%{_sbindir}/rsyslogd
%{_mandir}/*/*
# removed since 7.3.9 
# %{_libdir}/rsyslog/compat.so
# %{_unitdir}/rsyslog.service

#%files sysvinit
#%attr(0755,root,root) %{_initrddir}/rsyslog

%files libdbi
%defattr(-,root,root)
%{_libdir}/rsyslog/omlibdbi.so

%files mysql
%defattr(-,root,root)
%doc plugins/ommysql/createDB.sql
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%defattr(-,root,root)
%doc plugins/ompgsql/createDB.sql
%{_libdir}/rsyslog/ompgsql.so

# bugged 
#%files gssapi
#%defattr(-,root,root)
#%{_libdir}/rsyslog/lmgssutil.so
#%{_libdir}/rsyslog/imgssapi.so
#%{_libdir}/rsyslog/omgssapi.so

%files relp
%defattr(-,root,root)
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files gnutls
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_gtls.so

%files snmp
%defattr(-,root,root)
%{_libdir}/rsyslog/omsnmp.so

%files udpspoof
%defattr(-,root,root)
%{_libdir}/rsyslog/omudpspoof.so

%files mmjsonparse
%defattr(-,root,root)
%{_libdir}/rsyslog/mmjsonparse.so

%files mmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/mmnormalize.so

%files mmfields
%defattr(-,root,root)
%{_libdir}/rsyslog/mmfields.so

%files mmanon
%defattr(-,root,root)
%{_libdir}/rsyslog/mmanon.so

%files pmciscoios
%defattr(-,root,root)
%{_libdir}/rsyslog/pmciscoios.so

%files ommail
%defattr(-,root,root)
%{_libdir}/rsyslog/ommail.so

%if 0%{?rhel} >= 6
%files elasticsearch
%defattr(-,root,root)
%{_libdir}/rsyslog/omelasticsearch.so

#%files zmq3
#%defattr(-,root,root)
#%{_libdir}/rsyslog/imzmq3.so
#%{_libdir}/rsyslog/omzmq3.so

%files mongodb
%defattr(-,root,root)
%{_libdir}/rsyslog/ommongodb.so
%if 0%{?rhel} >= 6
%{_bindir}/logctl
%endif

%endif

%changelog
* Tue Aug 05 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.5
- Added RPM Package for pmciscoios

* Fri Jul 11 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.4

* Thu Jun 26 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.3

* Fri May 02 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.2

* Thu Apr 24 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.1

* Thu Apr 10 2014 Andre Lorbach
- Created RPM's for RSyslog 8.3.0

* Thu Mar 11 2014 Andre Lorbach
- New build for librelp

* Fri Mar 07 2014 Andre Lorbach 
- new build for CentOS 6

* Thu Feb 20 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.6

* Fri Jan 24 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.5

* Fri Jan 10 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.4

* Fri Dec 06 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.3

* Thu Nov 28 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.2
  Added jemalloc support

* Tue Nov 19 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.1

* Fri Nov 15 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.0

* Thu Nov 07 2013 Andre Lorbach
- Removed unused reload option 
  from INIT script. 

* Wed Oct 30 2013 Andre Lorbach
- Added mmsequence modul into base package

* Tue Oct 29 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.6

* Wed Oct 15 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.5

* Mon Oct 07 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.4

* Wed Sep 11 2013 Andre Lorbach
- Added RPM Package for mmfields
- Created RPM's for RSyslog 7.5.3

* Thu Jul 04 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.2

* Tue Jun 26 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.5.1

* Tue Jun 11 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.5.0

* Tue May 21 2013 Andre Lorbach
- Added new module ommail 

* Wed May 15 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.15

* Wed May 08 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.14

* Thu Apr 25 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.12

* Wed Apr 13 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.10

* Thu Mar 28 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.9

* Fri Mar 22 2013 Andre Lorbach
- Testing RPMs for v7-devel 7.3.9
				 
* Mon Mar 18 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.8

* Thu Mar 14 2013 Andre Lorbach
- Added RPM Package for mmanon

* Wed Mar 13 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.7

* Tue Mar 12 2013 Andre Lorbach
- Added RPM Package for mmnormalize

* Fri Mar 08 2013 Andre Lorbach
- Added RPM Package for MongoDB

* Fri Feb 22 2013 Andre Lorbach
- removed -c option from sysconfig file

* Tue Jan 29 2013 Andre Lorbach
- Added new default configuration which is only 
  V7 compatible. 
- Created new RPMs for v7-devel 7.3.6

* Tue Jan 17 2013 Andre Lorbach
- Added Module for omelasticsearch , 
  thanks to Radu Gheorghe. Support is only available on
  EHEL 6 and higher!
- Added Module for mmjsonparse.

* Wed Dec 19 2012 Andre Lorbach
- Created new RPMs for v7-devel 7.3.5

* Wed Nov 21 2012 Andre Lorbach
- Changed PIDFile back to rsyslog.pid for EPEL5 dist
- removed depencies for libuuid-devel package

* Fri Nov 07 2012 Andre Lorbach
- Created RPMs for v7-devel: 7.3.3

* Fri Oct 19 2012 Andre Lorbach
- Created Specfile and RPMs for v7-devel: 7.3.1

* Wed Oct 17 2012 Andre Lorbach
- created RPMs for RSyslog 7.1.11

* Mon Oct 15 2012 Andre Lorbach
- removed systemd-units dependency  

* Fri Sep 06 2012 Andre Lorbach
- created RPMs for RSyslog 7.1.0 

* Fri Aug 24 2012 Andre Lorbach
- Adapted RPM Specfile for RSyslog 6 and 7

* Thu Aug 23 2012 Andre Lorbach
- created RPMs for 5.8.13, no changes needed

* Wed Jun 20 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-2
- update systemd patch: remove the 'ExecStartPre' option
  Resolves: #833549

* Fri Apr 13 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-1
- upgrade to new upstream stable version 5.8.10
- add impstats and imptcp modules
- include new license text files
- consider lock file in 'status' action

* Mon Jan 23 2012 Tomas Heinrich <theinric@redhat.com> 5.8.7-1
- upgrade to new upstream version 5.8.7
- change license from 'GPLv3+' to '(GPLv3+ and ASL 2.0)'
  http://blog.gerhards.net/2012/01/rsyslog-licensing-update.html
- use a specific version for obsoleting sysklogd
- add patches for better sysklogd compatibility (taken from upstream)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Tomas Heinrich <theinric@redhat.com> 5.8.6-1
- upgrade to new upstream version 5.8.6
- obsolete sysklogd
  Resolves: #748495

* Tue Oct 11 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-3
- modify logrotate configuration to omit boot.log
  Resolves: #745093

* Mon Sep 06 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-2
- add systemd-units to BuildRequires for the _unitdir macro definition

* Mon Sep 05 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-1
- upgrade to new upstream version (CVE-2011-3200)

* Fri Jul 22 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-3
- move the SysV init script into a subpackage
- Resolves: 697533

* Mon Jul 11 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-2
- rebuild for net-snmp-5.7 (soname bump in libnetsnmp)

* Mon Jun 27 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-1
- upgrade to new upstream version 5.8.2

* Mon Jun 13 2011 Tomas Heinrich <theinric@redhat.com> 5.8.1-2
- scriptlet correction
- use macro in unit file's path

* Fri May 20 2011 Tomas Heinrich <theinric@redhat.com> 5.8.1-1
- upgrade to new upstream version
- correct systemd scriptlets (#705829)

* Mon May 16 2011 Bill Nottingham <notting@redhat.com> - 5.7.9-3
- combine triggers (as rpm will only execute one) - fixes upgrades (#699198)

* Tue Apr 05 2011 Tomas Heinrich <theinric@redhat.com> 5.7.10-1
- upgrade to new upstream version 5.7.10

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 5.7.9-2
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Fri Mar 18 2011 Tomas Heinrich <theinric@redhat.com> 5.7.9-1
- upgrade to new upstream version 5.7.9
- enable compilation of several new modules,
  create new subpackages for some of them
- integrate changes from Lennart Poettering
  to add support for systemd
  - add rsyslog-5.7.9-systemd.patch to tweak the upstream
    service file to honour configuration from /etc/sysconfig/rsyslog

* Fri Mar 18 2011 Dennis Gilmore <dennis@ausil.us> - 5.6.2-3
- sparc64 needs big PIE

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Tomas Heinrich <theinric@redhat.com> 5.6.2-1
- upgrade to new upstream stable version 5.6.2
- drop rsyslog-5.5.7-remove_include.patch; applied upstream
- provide omsnmp module
- use correct name for lock file (#659398)
- enable specification of the pid file (#579411)
- init script adjustments

* Wed Oct 06 2010 Tomas Heinrich <theinric@redhat.com> 5.5.7-1
- upgrade to upstream version 5.5.7
- update configuration and init files for the new major version
- add several directories for storing auxiliary data
- add ChangeLog to documentation
- drop unlimited-select.patch; integrated upstream
- add rsyslog-5.5.7-remove_include.patch to fix compilation

* Tue Sep 07 2010 Tomas Heinrich <theinric@redhat.com> 4.6.3-2
- build rsyslog with PIE and RELRO

* Thu Jul 15 2010 Tomas Heinrich <theinric@redhat.com> 4.6.3-1
- upgrade to new upstream stable version 4.6.3

* Wed Apr 07 2010 Tomas Heinrich <theinric@redhat.com> 4.6.2-1
- upgrade to new upstream stable version 4.6.2
- correct the default value of the OMFileFlushOnTXEnd directive

* Thu Feb 11 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-6
- modify rsyslog-4.4.2-unlimited-select.patch so that
  running autoreconf is not needed
- remove autoconf, automake, libtool from BuildRequires
- change exec-prefix to nil

* Wed Feb 10 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-5
- remove '_smp_mflags' make argument as it seems to be
  producing corrupted builds

* Mon Feb 08 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-4
- redefine _libdir as it doesn't use _exec_prefix

* Thu Dec 17 2009 Tomas Heinrich <theinric@redhat.com> 4.4.2-3
- change exec-prefix to /

* Wed Dec 09 2009 Robert Scheck <robert@fedoraproject.org> 4.4.2-2
- run libtoolize to avoid errors due mismatching libtool version

* Thu Dec 03 2009 Tomas Heinrich <theinric@redhat.com> 4.4.2-1
- upgrade to new upstream stable version 4.4.2
- add support for arbitrary number of open file descriptors

* Mon Sep 14 2009 Tomas Heinrich <theinric@redhat.com> 4.4.1-2
- adjust init script according to guidelines (#522071)

* Thu Sep 03 2009 Tomas Heinrich <theinric@redhat.com> 4.4.1-1
- upgrade to new upstream stable version

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.2.0-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Tomas Heinrich <theinric@redhat.com> 4.2.0-1
- upgrade

* Mon Apr 13 2009 Tomas Heinrich <theinric@redhat.com> 3.21.11-1
- upgrade

* Tue Mar 31 2009 Lubomir Rintel <lkundrak@v3.sk> 3.21.10-4
- Backport HUPisRestart option

* Wed Mar 18 2009 Tomas Heinrich <theinric@redhat.com> 3.21.10-3
- fix variables' type conversion in expression-based filters (#485937)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Tomas Heinrich <theinric@redhat.com> 3.21.10-1
- upgrade

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 3.21.9-3
- rebuild for dependencies

* Tue Jan 07 2009 Tomas Heinrich <theinric@redhat.com> 3.21.9-2
- fix several legacy options handling
- fix internal message output (#478612)

* Mon Dec 15 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.9-1
- update is fixing $AllowedSender security issue

* Mon Sep 15 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.3-4
- use RPM_OPT_FLAGS
- use same pid file and logrotate file as syslog-ng (#441664)
- mark config files as noreplace (#428155)

* Mon Sep 01 2008 Tomas Heinrich <theinric@redhat.com> 3.21.3-3
- fix a wrong module name in the rsyslog.conf manual page (#455086)
- expand the rsyslog.conf manual page (#456030)

* Thu Aug 28 2008 Tomas Heinrich <theinric@redhat.com> 3.21.3-2
- fix clock rollback issue (#460230)

* Wed Aug 20 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.3-1
- upgrade to bugfix release

* Wed Jul 23 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.0-1
- upgrade

* Mon Jul 14 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.9-2
- adjust default config file

* Fri Jul 11 2008 Lubomir Rintel <lkundrak@v3.sk> 3.19.9-1
- upgrade

* Wed Jun 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-3
- rebuild because of new gnutls

* Fri Jun 13 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-2
- do not translate Oopses (#450329)

* Fri Jun 13 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-1
- upgrade

* Wed May 28 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.4-1
- upgrade

* Mon May 26 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.3-1
- upgrade to new upstream release

* Wed May 14 2008 Tomas Heinrich <theinric@redhat.com> 3.16.1-1
- upgrade

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-5
- prevent undesired error description in legacy 
  warning messages

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-4
- adjust symbol lookup method to 2.6 kernel 

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-3
- fix segfault of expression based filters

* Mon Apr 07 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-2
- init script fixes (#441170,#440968)

* Fri Apr 04 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-1
- upgrade

* Mon Mar 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.4-1
- upgrade

* Wed Mar 19 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.3-1
- upgrade 
- fix some significant memory leaks

* Tue Mar 11 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.1-2
- init script fixes (#436854)
- fix config file parsing (#436722)

* Thu Mar 06 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.1-1
- upgrade

* Wed Mar 05 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.0-1
- upgrade

* Mon Feb 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.11.5-1
- upgrade

* Fri Feb 01 2008 Peter Vrabec <pvrabec@redhat.com> 3.11.0-1
- upgrade to the latests development release
- provide PostgresSQL support
- provide GSSAPI support

* Mon Jan 21 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-7
- change from requires sysklogd to conflicts sysklogd

* Fri Jan 18 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-6
- change logrotate file
- use rsyslog own pid file

* Thu Jan 17 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-5
- fixing bad descriptor (#428775)

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-4
- rename logrotate file

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-3
- fix post script and init file

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-2
- change pid filename and use logrotata script from sysklogd

* Tue Jan 15 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-1
- upgrade to stable release
- spec file clean up

* Wed Jan 02 2008 Peter Vrabec <pvrabec@redhat.com> 1.21.2-1
- new upstream release

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.19.11-2
- Rebuild for deps

* Thu Nov 29 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.11-1
- new upstream release
- add conflicts (#400671)

* Mon Nov 19 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.10-1
- new upstream release

* Wed Oct 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.6-3
- remove NUL character from recieved messages

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-2
- fix message suppression (303341)

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-1
- upstream bugfix release

* Tue Aug 28 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.2-1
- upstream bugfix release
- support for negative app selector, patch from 
  theinric@redhat.com

* Fri Aug 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.0-1
- new upstream release with MySQL support(as plugin)

* Wed Aug 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.1-1
- upstream bugfix release

* Mon Aug 06 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.0-1
- new upstream release

* Thu Aug 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.6-1
- upstream bugfix release

* Mon Jul 30 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.5-1
- upstream bugfix release
- fix typo in provides 

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 1.17.2-4
- rebuild for toolchain bug

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-3
- take care of sysklogd configuration files in %%post

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-2
- use EVR in provides/obsoletes sysklogd

* Mon Jul 23 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-1
- upstream bug fix release

* Fri Jul 20 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.1-1
- upstream bug fix release
- include html docs (#248712)
- make "-r" option compatible with sysklogd config (248982)

* Tue Jul 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.0-1
- feature rich upstream release

* Thu Jul 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-2
- use obsoletes and hadle old config files

* Wed Jul 11 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-1
- new upstream bugfix release

* Tue Jul 10 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.0-1
- new upstream release introduce capability to generate output 
  file names based on templates

* Tue Jul 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.2-1
- new upstream bugfix release

* Mon Jul 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.1-1
- new upstream release with IPv6 support

* Tue Jun 26 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-3
- add BuildRequires for  zlib compression feature

* Mon Jun 25 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-2
- some spec file adjustments.
- fix syslog init script error codes (#245330)

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-1
- new upstream release

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-2
- some spec file adjustments.

* Mon Jun 18 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-1
- upgrade to new upstream release

* Wed Jun 13 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-2
- DB support off

* Tue Jun 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-1
- new upstream release based on redhat patch

* Fri Jun 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-2
- rsyslog package provides its own kernel log. daemon (rklogd)

* Mon Jun 04 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-1
- Initial rpm build
