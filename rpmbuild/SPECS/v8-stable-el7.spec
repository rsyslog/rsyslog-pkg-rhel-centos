%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/%{name}-%{version}
%if 0%{?rhel} >= 7
%global want_hiredis 0
%global want_mongodb 0
%global want_rabbitmq 0
%else
%global want_hiredis 1
%global want_mongodb 1
%global want_rabbitmq 1
%endif

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.39.0
Release: 2%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: http://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{version}.tar.gz
Source2: rsyslog.conf
Source3: rsyslog.sysconfig
Source4: rsyslog.log

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: bison
BuildRequires: flex
BuildRequires: libfastjson4-devel >= 0.99.8
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
# it depens on rhbz#1419228
BuildRequires: systemd-devel >= 219-39
BuildRequires: zlib-devel

Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires: libestr >= 0.1.11
Requires: libfastjson4 >= 0.99.8
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: syslog
Obsoletes: sysklogd < 1.5-11
Obsoletes: rsyslog-mmutf8fix

# Patches
Patch0: rsyslog-systemd-centos7.patch

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libgcrypt-devel

%package doc
Summary: HTML Documentation for rsyslog
Group: Documentation

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel libuuid-devel

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel >= 0.13.1
%endif

%package mmfields
Summary: mmfields support 
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: liblognorm5 >= 2.0.4
BuildRequires: liblognorm5-devel >= 2.0.4

%package mmjsonparse
Summary: mmjsonparse support 
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: liblognorm5 >= 2.0.4
BuildRequires: liblognorm5-devel >= 2.0.4

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libee-devel liblognorm5-devel >= 2.0.4

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmrm1stspace
Summary: mmrm1stspace support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql >= 4.0
BuildRequires: mysql-devel >= 4.0

%if %{want_mongodb}
%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%package pmciscoios
Summary: pmciscoios support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package pmnormalize
Summary: Log normalization parser for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm5-devel >= 2.0.4

%if %{want_rabbitmq}
%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2
%endif

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.2.17
BuildRequires: librelp-devel >= 1.2.17
BuildRequires: libgcrypt-devel

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel

%package openssl
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: openssl-devel
BuildRequires: libgcrypt-devel

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

%package kafka
Summary: Kafka output support 
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: lz4
BuildRequires: adisconbuild-librdkafka-devel >= 0.11.6
BuildRequires: lz4-devel
BuildRequires: cyrus-sasl-devel

%package ksi-ls12
Summary: KSI signature support 
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: libksi >= 3.13.0
BuildRequires: libksi-devel

%package omfile-hardened
Summary: omfile-hardened support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmkubernetes
Summary: mmkubernetes support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package fmhttp
Summary: fmhttp support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%package fmhash
Summary: fmhash support 
Group: System Environment/Daemons
Requires: %name = %version-%release

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%description doc
This subpackage contains documentation for rsyslog.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmfields
Parse all fields of the message into structured data inside the JSON tree.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%if %{want_mongodb}
%description mongodb
The rsyslog-mongodb package contains a dynamic shared object that will add
MongoDB database support to rsyslog.
%endif

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%if %{want_rabbitmq}
%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.
%endif

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description openssl
The rsyslog-openssl package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%description mmrm1stspace
Removes leading space (mmrm1stspace).
The mmrm1stspace module is used to remove the leading space character of the msg
property. It is basically for cleaning up this unneeded character to make 
subsequent message parsing less error-prone.

%description pmciscoios
Parser module which supports various Cisco IOS formats.

%description pmnormalize
Parser module based on liblognorm.

%description kafka
librdkafka is a C library implementation of the Apache Kafka protocol, 
containing both Producer and Consumer support. It was designed with message delivery 
reliability and high performance in mind, current figures exceed 800000 msgs/second 
for the producer and 3 million msgs/second for the consumer.

%description ksi-ls12
The KSI-LS12 signature plugin provides access to the Keyless Signature Infrastructure 
globally distributed by Guardtime. 

%description omfile-hardened
Duplicate of the omfile module with settings to harden the output 
against failure.

%description mmkubernetes
Message modification module to add Kubernetes metadata to a messages.

%description fmhttp
Function module for rainerscript function http_request.

%description fmhash
Function module for rainerscript function hash.

%prep
# set up rsyslog-doc sources
%setup -q -a 1 -T -c
#%patch0 -p1
rm -r LICENSE README.md source build/objects.inv
mv build doc

# set up rsyslog sources
%setup -q -D
%patch0 -p1

autoreconf 

%build
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS=-L%{_libdir}
%endif
%configure \
	--prefix=/usr \
	--disable-static \
	--disable-testbench \
	--disable-liblogging-stdlog \
	--enable-elasticsearch \
	--enable-generate-man-pages \
	--enable-gnutls \
	--enable-openssl \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp \
	--enable-libdbi \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mmutf8fix \
	--enable-mysql \
%if %{want_hiredis}
	--enable-omhiredis \
%endif
	--enable-omjournal \
%if %{want_mongodb}
	--enable-ommongodb \
%endif
	--enable-omprog \
%if %{want_rabbitmq}
	--enable-omrabbitmq \
%endif
	--enable-omruleset \
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmnormalize \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \
	--enable-uuid \
        --enable-omkafka \
	--enable-imkafka \
	--enable-kafka-static \
	--enable-ksi-ls12 \
	--enable-mmfields \
	--enable-mmpstrucdata \
	--enable-mmsequence \
	--enable-mmrm1stspace \
	--enable-pmciscoios \
	--enable-omfile-hardened \
	--enable-mmkubernetes \
	--enable-pmnull

#	--enable-pmrfc3164sd \


make

%install
make DESTDIR=%{buildroot} install

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -d -m 700 %{buildroot}%{rsyslog_statedir}
install -d -m 700 %{buildroot}%{rsyslog_pkidir}
install -d -m 755 %{buildroot}%{rsyslog_docdir}/html

install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -p -m 644 plugins/ommysql/createDB.sql %{buildroot}%{rsyslog_docdir}/mysql-createDB.sql
install -p -m 644 plugins/ompgsql/createDB.sql %{buildroot}%{rsyslog_docdir}/pgsql-createDB.sql
# extract documentation
cp -r doc/* %{buildroot}%{rsyslog_docdir}/html
# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# get rid of socket activation by default
sed -i '/^Alias/s/^/;/;/^Requires=syslog.socket/s/^/;/' %{buildroot}%{_unitdir}/rsyslog.service

# convert line endings from "\r\n" to "\n"
cat tools/recover_qi.pl | tr -d '\r' > %{buildroot}%{_bindir}/rsyslog-recover-qi.pl

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog
%exclude %{rsyslog_docdir}/html
%exclude %{rsyslog_docdir}/mysql-createDB.sql
%exclude %{rsyslog_docdir}/pgsql-createDB.sql
%dir %{_libdir}/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_sbindir}/rsyslogd
%attr(755,root,root) %{_bindir}/rsyslog-recover-qi.pl
%{_mandir}/man5/rsyslog.conf.5.gz
%{_mandir}/man8/rsyslogd.8.gz
%{_unitdir}/rsyslog.service
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
# plugins
%{_libdir}/rsyslog/imdiag.so
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imjournal.so
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
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/mmutf8fix.so
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmcisconames.so
%{_libdir}/rsyslog/pmlastmsg.so
#%{_libdir}/rsyslog/pmrfc3164sd.so
%{_libdir}/rsyslog/pmsnare.so
%{_libdir}/rsyslog/lmcry_gcry.so
%{_libdir}/rsyslog/mmpstrucdata.so
%{_libdir}/rsyslog/mmsequence.so
%{_libdir}/rsyslog/pmnull.so

%files crypto
%defattr(-,root,root)
%{_bindir}/rscryutil
%{_mandir}/man1/rscryutil.1.gz
%{_libdir}/rsyslog/lmcry_gcry.so

%files doc
%defattr(-,root,root)
%doc %{rsyslog_docdir}/html

%files elasticsearch
%defattr(-,root,root)
%{_libdir}/rsyslog/omelasticsearch.so

%if %{want_hiredis}
%files hiredis
%defattr(-,root,root)
%{_libdir}/rsyslog/omhiredis.so
%endif

%files libdbi
%defattr(-,root,root)
%{_libdir}/rsyslog/omlibdbi.so

%files mmaudit
%defattr(-,root,root)
%{_libdir}/rsyslog/mmaudit.so

%files mmjsonparse
%defattr(-,root,root)
%{_libdir}/rsyslog/mmjsonparse.so

%files mmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/mmnormalize.so

%files mmsnmptrapd
%defattr(-,root,root)
%{_libdir}/rsyslog/mmsnmptrapd.so

%files mysql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/mysql-createDB.sql
%{_libdir}/rsyslog/ommysql.so

%if %{want_mongodb}
%files mongodb
%defattr(-,root,root)
%{_bindir}/logctl
%{_libdir}/rsyslog/ommongodb.so
%endif

%files pgsql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/pgsql-createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%if %{want_rabbitmq}
%files rabbitmq
%defattr(-,root,root)
%{_libdir}/rsyslog/omrabbitmq.so
%endif

%files gssapi
%defattr(-,root,root)
%{_libdir}/rsyslog/lmgssutil.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/omgssapi.so

%files relp
%defattr(-,root,root)
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files gnutls
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_gtls.so

%files openssl
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_ossl.so

%files snmp
%defattr(-,root,root)
%{_libdir}/rsyslog/omsnmp.so

%files udpspoof
%defattr(-,root,root)
%{_libdir}/rsyslog/omudpspoof.so

%files mmfields
%defattr(-,root,root)
%{_libdir}/rsyslog/mmfields.so

%files pmciscoios
%defattr(-,root,root)
%{_libdir}/rsyslog/pmciscoios.so

%files pmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/pmnormalize.so

%files mmrm1stspace 
%defattr(-,root,root)
%{_libdir}/rsyslog/mmrm1stspace.so

%files kafka
%defattr(-,root,root)
%{_libdir}/rsyslog/omkafka.so
%{_libdir}/rsyslog/imkafka.so

%files ksi-ls12
%defattr(-,root,root)
%{_libdir}/rsyslog/lmsig_ksi_ls12.so

%files omfile-hardened
%defattr(-,root,root)
%{_libdir}/rsyslog/omfile-hardened.so

%files mmkubernetes
%defattr(-,root,root)
%{_libdir}/rsyslog/mmkubernetes.so

%files fmhttp
%defattr(-,root,root)
%{_libdir}/rsyslog/fmhttp.so

%files fmhash
%defattr(-,root,root)
%{_libdir}/rsyslog/fmhash.so

%changelog
* Fri Nov 02 2018 Julien Thomas - 8.39.0-3
- Add pmnormalize subpackage

* Wed Oct 31 2018 Florian Riedl - 8.39.0-2
- Rebuild for fixed Kafka dependency

* Tue Oct 30 2018 Florian Riedl - 8.39.0-1
- Release build for 8.39.0

* Tue Sep 18 2018 Florian Riedl - 8.38.0-1
- Release build for 8.38.0

* Tue Aug 07 2018 Florian Riedl - 8.37.0-1
- Release build for 8.37.0

* Thu Aug 02 2018 Florian Riedl - 8.36.0-3
- Rebuild for new kafka support library
- Updated librelp 1.2.17 dependency

* Wed Jun 27 2018 Florian Riedl - 8.36.0-2
- Rebuild
- Added module pmnull to base RPM

* Tue Jun 26 2018 Florian Riedl - 8.36.0-1
- Release build for 8.36.0
- Removed imrelp patch

* Tue Jun 12 2018 Florian Riedl - 8.35.0-3
- Added patch to remove -iNone directive in service file
  and add sysconfig path back for custom options

* Thu May 17 2018 Florian Riedl - 8.35.0-2
- Rebuild for librelp 1.2.16 dependency
- Added patch for imrelp: #2712
- Removed old patch definitions
- Changed logrotate script to use systemctl command for HUP

* Tue May 15 2018 Florian Riedl - 8.35.0-1
- Release build for 8.35.0
- Added RPM rsyslog-fmhash

* Tue Apr 03 2018 Florian Riedl - 8.34.0-1
- Release build for 8.34.0
- Added RPM rsyslog-omfile-hardened
- Added RPM rsyslog-mmkubernetes
- Added RPM rsyslog-fmhttp

* Wed Mar 21 2018 Florian Riedl - 8.33.1-2
- Rebuild for librelp 1.2.15 dependency

* Tue Mar 06 2018 Florian Riedl - 8.33.1-1
- Release build for 8.33.1
- Added obsolete function rsyslog-mmutf8fix

* Tue Feb 20 2018 Florian Riedl - 8.33.0-1
- Release build for 8.33.0
- Disabled previous patches

* Fri Jan 19 2018 Florian Riedl - 8.32.0-4
- Added patch for external cmd parser
  ref https://github.com/rsyslog/rsyslog/pull/2410

* Wed Jan 17 2018 Florian Riedl - 8.32.0-3
- Added patches for json processing in rainerscript
  and jsonmesg
  fixes: https://github.com/rsyslog/rsyslog/issues/2391
  fixes: https://github.com/rsyslog/rsyslog/issues/2396

* Tue Jan 09 2018 Florian Riedl - 8.32.0-2
- Fixed missing packages and modules
- Dependency fixes

* Tue Jan 09 2018 Florian Riedl - 8.32.0-1
- Used spec file from base repository RPM for new build
  fixes: https://github.com/rsyslog/rsyslog/issues/2134
- Disabled most patches
- Added module packages for modules previously built:
  kafka, ksi-ls12, mmfields, mmrm1stspace, pmciscoios
- Module packages no longer built, because modules in base RPM:
  mmanon, mmutf8fix, mail, pmaixforwardedfrom
- Added BuildRequires/Requires for libfastjson >= 0.99.8

* Wed May 10 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-12
- added BuildRequires for systemd >= 219-39 depents on rhbz#1419228

* Tue May 09 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-11
RHEL 7.4 ERRATUM
- added new patch that backports num2ipv4 due to rhbz#1427821
  resolves: rhbz#1427821
- enable pmrfc3164sd module
  resolves: rhbz#1431616

* Wed May 03 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-10
RHEL 7.4 ERRATUM
- edited patches Patch19 and Patch21
  resolves: rhbz#1419228(coverity scan problems)
  resolves: rhbz#1056548(failed QA, coverity scan problems)

* Tue May 02 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-9
RHEL 7.4 ERRATUM
- added autoreconf call
- added patch to replace gethostbyname with getaddrinfo call
  resolves: rhbz#1056548(failed QA)

* Wed Apr 19 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-8
RHEL 7.4 ERRATUM
- added dependency automake autoconf libtool due to yum-builddep
- reenable omruleset module
  resolves: rhbz#1431615
  resolves: rhbz#1428403
  resolves: rhbz#1427821(fix regression, failed QA)
  resolves: rhbz#1432069
- resolves: rhbz#1165236
  resolves: rhbz#1419228
  resolves: rhbz#1431616 
  resolves: rhbz#1196230(failed QA)

* Thu Mar 02 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-7
- reverted logrotate file that was added by mistake

* Wed Mar 01 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-6
- RHEL 7.4 ERRATUM
- rsyslog rebase to 8.24
- added patch to prevent segfault while setting aclResolveHostname
  config options
  resolves: rhbz#1422414
- added patch to check config variable names at startup
  resolves: rhbz#1427828
- added patch for str2num to handle empty strings
  resolves: rhbz#1427821
- fixed typo in added-chdir patch
  resolves: rhbz#1422789
- added patch to log source process when beginning rate-limiting
  resolves: rhbz#1196230
- added patch to chdir after chroot
  resolves: rhbz#1422789
- added patch to remove "inputname" imudp module parameter 
  deprecation warnings
  resolves: rhbz#1403907
- added patch which resolves situation when time goes backwards
  and statefile is invalid
  resolves rhbz#1088021
- added a patch to bring back deprecated cmd-line switches and
  remove associated warnings
  resolves: rhbz#1403831
- added documentation recover_qi.pl
  resolves: rhbz#1286707
- add another setup for doc package
- add --enable-generate-man-pages to configure parameters;
  the rscryutil man page isn't generated without it
  https://github.com/rsyslog/rsyslog/pull/469
- enable mmcount, mmexternal modules
- remove omruleset and pmrfc3164sd modules

* Thu Jul 14 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-16
- add a patch to prevent races in libjson-c calls
  resolves: rhbz#1222746

* Sun Jul 10 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-15
- add a patch to make state file handling in imjournal more robust
  resolves: rhbz#1245194
- add a patch to support wildcards in imfile
  resolves: rhbz#1303617

* Fri May 20 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-14
- add a patch to prevent loss of partial messages
  resolves: rhbz#1312459
- add a patch to allow multiple rulesets in imrelp
  resolves: rhbz#1223566
- add a patch to fix a race condition during shutdown
  resolves: rhbz#1295798
- add a patch to backport the mmutf8fix plugin
  resolves: rhbz#1146237
- add a patch to order service startup after the network
  resolves: rhbz#1263853

* Mon May 16 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-13
- add a patch to prevent crashes when using multiple rulesets
  resolves: rhbz#1224336
- add a patch to keep the imjournal state file updated
  resolves: rhbz#1216957
- add a patch to fix an undefined behavior caused by the maxMessageSize directive
  resolves: rhbz#1214257
- add a patch to prevent crashes when using rulesets with a parser
  resolves: rhbz#1282687

* Fri Aug 28 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-12
- amend the patch for rhbz#1151041
  resolves: rhbz#1257150

* Tue Aug 18 2015 Radovan Sroka <rsroka@redhat.com> 7.4.7-11
- add patch that resolves config.guess system-recognition on ppc64le architecture
  resolves: rhbz:1254511

* Mon Aug 03 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-10
- add a patch to prevent field truncation in imjournal
  resolves: rhbz#1101602
- add a patch to enable setting a default TAG
  resolves: rhbz#1188503
- add a patch to fix a nonfunction hostname setting in imuxsock
  resolves: rhbz#1184402

* Mon Jul 20 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-9
- update the patch fixing a race condition in directory creation
  resolves: rhbz#1202489
- improve provided documentation
  - move documentation from all subpackages under a single directory
  - add missing images
  - remove doc files without content
  - add a patch making various corrections to the HTML documentation
  resolves: rhbz#1238713
- add a patch to prevent division-by-zero errors
  resolves: rhbz#1078878
- add a patch to clarify usage of the SysSock.Use option
  resolves: rhbz#1143846
- add a patch to support arbitrary number of listeners in imuxsock
  - drop patch for rhbz#1053669 as it has been merged into this one
  resolves: rhbz#1151041

* Fri Jul 03 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-8
- modify the service file to automatically restart rsyslog on failure
  resolves: rhbz#1061322
- add explicitly versioned dependencies on libraries which do not have
  correctly versioned sonames
  resolves: rhbz#1107839
- make logrotate tolerate missing log files
  resolves: rhbz#1144465
- backport the mmcount plugin
  resolves: rhbz#1151037
- set the default service umask to 0066
  resolves: rhbz#1228192
- add a patch to make imjournal sanitize messages as imuxsock does it
  resolves: rhbz#743890
- add a patch to fix a bug preventing certain imuxsock directives from
  taking effect
  resolves: rhbz#1184410
- add a patch to fix a race condition in directory creation
  resolves: rhbz#1202489

* Tue Oct 07 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-7
- fix CVE-2014-3634
  resolves: #1149153

* Wed Mar 26 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-6
- disable the imklog plugin by default
  the patch for rhbz#1038136 caused duplication of kernel messages since the
  messages read by the imklog plugin were now also pulled in from journald
  resolves: #1078654

* Wed Feb 19 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-5
- move the rscryutil man page to the crypto subpackage
  resolves: #1056565
- add a patch to prevent message loss in imjournal
  rsyslog-7.4.7-bz1038136-imjournal-message-loss.patch
  resolves: #1038136

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 7.4.7-4
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-3
- replace rsyslog-7.3.15-imuxsock-warning.patch
  with rsyslog-7.4.7-bz1053669-imuxsock-wrn.patch
  resolves: #1053669
- add rsyslog-7.4.7-bz1052266-dont-link-libee.patch to prevent
  linking the main binary with libee
  resolves: #1052266
- add rsyslog-7.4.7-bz1054171-omjournal-warning.patch to fix
  a condition for issuing a warning in omjournal
  resolves: #1054171
- drop the "v5" string from the conf file as it's misleading
  resolves: #1040036

* Wed Jan 15 2014 Honza Horak <hhorak@redhat.com> - 7.4.7-2
- Rebuild for mariadb-libs
  Related: #1045013

* Mon Jan 06 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-1
- rebase to 7.4.7
  add requirement on libestr >= 0.1.9
  resolves: #836485
  resolves: #1020854
  resolves: #1040036
- drop patch 4; not needed anymore
  rsyslog-7.4.2-imuxsock-rfc3339.patch
- install the rsyslog-recover-qi.pl tool
- fix a typo in a package description
- add missing defattr directives
- add a patch to remove references to Google ads in the html docs
  rsyslog-7.4.7-bz1030044-remove-ads.patch
  Resolves: #1030043
- add a patch to allow numeric specification of UIDs/GUIDs
  rsyslog-7.4.7-numeric-uid.patch
  resolves: #1032198
- change the installation prefix to "/usr"
  resolves: #1032223
- fix a bad date in the changelog
  resolves: #1043622
- resolve a build issue with missing mysql_config by adding
  additional BuildRequires for the mysql package
- add a patch to resolve build issue on ppc
  rsyslog-7.4.7-omelasticsearch-atomic-inst.patch

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.4.2-5
- Mass rebuild 2013-12-27

* Wed Nov 06 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-4
- add a patch to fix issues with rfc 3339 timestamp parsing
  resolves: #1020826

* Fri Jul 12 2013 Jan Safranek <jsafrane@redhat.com> - 7.4.2-3
- Rebuilt for new net-snmp

* Wed Jul 10 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-2
- make compilation of the rabbitmq plugin optional
  resolves: #978919

* Tue Jul 09 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-1
- rebase to 7.4.2
  most importantly, this release fixes a potential vulnerability,
  see http://www.lsexperts.de/advisories/lse-2013-07-03.txt
  the impact should be low as only those using the omelasticsearch
  plugin with a specific configuration are exposed

* Mon Jun 17 2013 Tomas Heinrich <theinric@redhat.com> 7.4.1-1
- rebase to 7.4.1
  this release adds code that somewhat mitigates damage in cases
  where large amounts of messages are received from systemd
  journal (see rhbz#974132)
- regenerate patch 0
- drop patches merged upstream: 4..8
- add a dependency on the version of systemd which resolves the bug
  mentioned above
- update option name in rsyslog.conf

* Wed Jun 12 2013 Tomas Heinrich <theinric@redhat.com> 7.4.0-1
- rebase to 7.4.0
- drop autoconf automake libtool from BuildRequires
- depends on systemd >= 201 because of the sd_journal_get_events() api
- add a patch to prevent a segfault in imjournal caused by a bug in
  systemd journal
- add a patch to prevent an endless loop in the ratelimiter
- add a patch to prevent another endless loop in the ratelimiter
- add a patch to prevent a segfault in imjournal for undefined state file
- add a patch to correctly reset state in the ratelimiter

* Tue Jun 04 2013 Tomas Heinrich <theinric@redhat.com> 7.3.15-1.20130604git6e72fa6
- rebase to an upstream snapshot, effectively version 7.3.15
  plus several more changes
- drop patches 3, 4 - merged upstream
- add a patch to silence warnings emitted by the imuxsock module
- drop the imkmsg plugin
- enable compilation of additional modules
  imjournal, mmanon, omjournal, omrabbitmq
- new subpackages: crypto, rabbitmq
- add python-docutils and autoconf to global BuildRequires
- drop the option for backwards compatibility from the
  sysconfig file - it is no longer supported
- call autoreconf to prepare the snapshot for building
- switch the local message source from imuxsock to imjournal
  the imuxsock module is left enabled so it is easy to swich back to
  it and because systemd drops a file into /etc/rsyslog.d which only
  imuxsock can parse

* Wed Apr 10 2013 Tomas Heinrich <theinric@redhat.com> 7.3.10-1
- rebase to 7.3.10
- add a patch to resolve #950088 - ratelimiter segfault, merged upstream
  rsyslog-7.3.10-ratelimit-segv.patch
- add a patch to correct a default value, merged upstream
  rsyslog-7.3.10-correct-def-val.patch
- drop patch 5 - fixed upstream

* Thu Apr 04 2013 Tomas Heinrich <theinric@redhat.com> 7.3.9-1
- rebase to 7.3.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Tomas Heinrich <theinric@redhat.com> 7.2.5-2
- update a line in rsyslog.conf for the new syntax

* Sun Jan 13 2013 Tomas Heinrich <theinric@redhat.com> 7.2.5-1
- upgrade to upstream version 7.2.5
- update the compatibility mode in sysconfig file

* Mon Dec 17 2012 Tomas Heinrich <theinric@redhat.com> 7.2.4-2
- add a condition to disable several subpackages

* Mon Dec 10 2012 Tomas Heinrich <theinric@redhat.com> 7.2.4-1
- upgrade to upstream version 7.2.4
- remove trailing whitespace

* Tue Nov 20 2012 Tomas Heinrich <theinric@redhat.com> 7.2.2-1
- upgrade to upstream version 7.2.2
  update BuildRequires
- remove patches merged upstream
  rsyslog-5.8.7-sysklogd-compat-1-template.patch
  rsyslog-5.8.7-sysklogd-compat-2-option.patch
  rsyslog-5.8.11-close-fd1-when-forking.patch
- add patch from Milan Bartos <mbartos@redhat.com>
  rsyslog-7.2.1-msg_c_nonoverwrite_merge.patch
- remove the rsyslog-sysvinit package
- clean up BuildRequires, Requires
- remove the 'BuildRoot' tag
- split off a doc package
- compile additional modules (some of them in separate packages):
  elasticsearch
  hiredis
  mmjsonparse
  mmnormalize
  mmaudit
  mmsnmptrapd
  mongodb
- correct impossible timestamps in older changelog entries
- correct typos, trailing spaces, etc
- s/RPM_BUILD_ROOT/{buildroot}/
- remove the 'clean' section
- replace post* scriptlets with systemd macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Tomas Heinrich <theinric@redhat.com> 5.8.11-2
- update systemd patch: remove the 'ExecStartPre' option

* Wed May 23 2012 Tomas Heinrich <theinric@redhat.com> 5.8.11-1
- upgrade to new upstream stable version 5.8.11
- add impstats and imptcp modules
- include new license text files
- consider lock file in 'status' action
- add patch to update information on debugging in the man page
- add patch to prevent debug output to stdout after forking
- add patch to support ssl certificates with domain names longer than 128 chars

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> 5.8.7-2
- libnet rebuild.

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

* Tue Sep 06 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-2
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

* Wed Jan 07 2009 Tomas Heinrich <theinric@redhat.com> 3.21.9-2
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

* Tue Mar 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.4-1
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
- add BuildRequires for zlib compression feature

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
