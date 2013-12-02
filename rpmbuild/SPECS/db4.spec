# the set of arches on which libgcj provides gcj and libgcj-javac-placeholder.sh
%define java_arches %{ix86} alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x %{arm}
%define __soversion 4.8

Summary: The Berkeley DB database library (version 4) for C
Name: db4
Version: 4.8.30
Release: 10%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
URL: http://www.oracle.com/database/berkeley-db/
License: Sleepycat and BSD
Group: System Environment/Libraries
# unversioned obsoletes are OK here as these BDB versions never occur again
Obsoletes: db1, db2, db3
Conflicts: filesystem < 3
BuildRequires: perl, libtool, ed, util-linux-ng
BuildRequires: tcl-devel >= 8.5.2-3
%ifarch %{java_arches}
BuildRequires: gcc-java
BuildRequires: java-devel >= 1:1.6.0
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Group: System Environment/Libraries

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB (version 4) databases
Group: Applications/Databases
Requires: db4 = %{version}-%{release}
Obsoletes: db1-utils, db2-utils, db3-utils

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Group: Development/Libraries
Requires: db4 = %{version}-%{release}
Requires: db4-cxx = %{version}-%{release}
Obsoletes: db1-devel, db2-devel, db3-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-static
Summary: Berkeley DB (version 4) static libraries
Group: Development/Libraries
Requires: db4-devel = %{version}-%{release}

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require statical linking of
Berkeley DB.

%package tcl
Summary: Development files for using the Berkeley DB (version 4) with tcl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package java
Summary: Development files for using the Berkeley DB (version 4) with Java
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description java
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Java.

%prep
%setup -q -n db-%{version} -a 1

pushd db.1.85/PORT/linux
%patch10 -p0 -b .1.1
popd
pushd db.1.85
%patch11 -p0 -b .1.2
%patch12 -p0 -b .1.3
%patch13 -p0 -b .1.4
%patch20 -p1 -b .errno
popd

%patch22 -p1 -b .185compat
%patch24 -p1 -b .4.5.20.jni

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
	for doc in $@ ; do
		chmod u+w ${doc}
		sed	-e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
			-e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
			-e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
			-e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
			-e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
			-e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
			-e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
			-e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
		touch -r ${doc} ${doc}.new
		cat ${doc}.new > ${doc}
		touch -r ${doc}.new ${doc}
		rm -f ${doc}.new
	done
}

set +x
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x

cd dist
./s_config

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"; export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

build() {
	test -d dist/$1 || mkdir dist/$1
	# Static link db_dump185 with old db-185 libraries.
	/bin/sh libtool --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c db_dump185/db_dump185.c -o dist/$1/db_dump185.lo
	/bin/sh libtool --mode=link	%{__cc} -o dist/$1/db_dump185 dist/$1/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

	pushd dist
	popd
	pushd dist/$1
	ln -sf ../configure .
	# XXX --enable-diagnostic should be disabled for production (but is
	# useful).
	# XXX --enable-debug_{r,w}op should be disabled for production.
	%configure -C \
		--enable-compat185 --enable-dump185 \
		--enable-shared --enable-static \
		--enable-tcl --with-tcl=%{_libdir} \
		--enable-cxx \
%ifarch %{java_arches}
		--enable-java \
%else
		--disable-java \
%endif
		--enable-test \
		--with-tcl=%{_libdir}/tcl8.5 \
		# --enable-diagnostic \
		# --enable-debug --enable-debug_rop --enable-debug_wop \

	# Remove libtool predep_objects and postdep_objects wonkiness so that
	# building without -nostdlib doesn't include them twice.  Because we
	# already link with g++, weird stuff happens if you don't let the
	# compiler handle this.
	perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
	perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
	perl -pi -e 's/-shared -nostdlib/-shared/' libtool

	make %{?_smp_mflags}

	# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
	LDBJ=./.libs/libdb_java-%{__soversion}.la
	if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
		sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
	fi

	popd
}

build dist-tls

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl.so

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/db4
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/db4/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
for i in db.h db_cxx.h db_185.h; do
	ln -s db4/$i ${RPM_BUILD_ROOT}%{_includedir}
done

%ifarch %{java_arches}
# Move java jar file to the correct place
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/java
mv ${RPM_BUILD_ROOT}%{_libdir}/*.jar ${RPM_BUILD_ROOT}%{_datadir}/java
%endif

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# rename utils so that they won't conflict with libdb (#749293)
pushd ${RPM_BUILD_ROOT}%{_bindir}
for i in `ls | sed s/db_//`; do
  mv db_$i db4_$i;
done
popd

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -p /sbin/ldconfig tcl

%postun -p /sbin/ldconfig tcl

%post -p /sbin/ldconfig java

%postun -p /sbin/ldconfig java

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/libdb-%{__soversion}.so

%files cxx
%defattr(-,root,root)
%{_libdir}/libdb_cxx-%{__soversion}.so

%files utils
%defattr(-,root,root)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_sql
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files devel
%defattr(-,root,root)
%doc	docs/*
%doc	examples_c examples_cxx
%{_libdir}/libdb.so
%{_libdir}/libdb_cxx.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_185.h
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db.h
%{_includedir}/db_185.h
%{_includedir}/db_cxx.h

%files devel-static
%defattr(-,root,root)
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.a
%ifarch %{java_arches}
%{_libdir}/libdb_java-%{__soversion}.a
%endif

%files tcl
%defattr(-,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so

%ifarch %{java_arches}
%files java
%defattr(-,root,root)
%doc docs/java
%doc examples_java
%{_libdir}/libdb_java*.so
%{_datadir}/java/*.jar
%endif

%changelog
* Mon Apr 30 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 4.8.30-10
- Add ARM to list of supported JAVA arches

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 4.8.30-9
- Removed explicit Java 6 requirement

* Mon Feb  6 2012 Tom Callaway <spot@fedoraproject.org> 4.8.30-8
- correct License tag

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 4.8.30-7
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 4.8.30-6
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Jindrich Novy <jnovy@redhat.com> 4.8.30-4
- rename utils so that they won't conflict with libdb (#749293)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Jindrich Novy <jnovy@redhat.com> 4.8.30-2
- add Requires: db4-devel to db4-deve-static
- add Requires: db4-cxx to db4-devel
- enable SHA-256 signatures for BDB packages

* Thu May  6 2010 Jindrich Novy <jnovy@redhat.com> 4.8.30-1
- update to 4.8.30, bugfix release

* Fri Jan  8 2010 Jindrich Novy <jnovy@redhat.com> 4.8.26-1
- update to 4.8.26, bugfix release

* Tue Oct  6 2009 Jindrich Novy <jnovy@redhat.com> 4.8.24-1
- update to 4.8.24

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May  6 2009 Jindrich Novy <jnovy@redhat.com> 4.7.25-12
- fix for Java API __repmgr_send crash where eid=SELF_EID,
  don't update master_id so soon after election (upstream bz#16299)

* Tue May 05 2009 Karsten Hopp <karsten@redhat.com> 4.7.25-11.1
- add s390 and s390x to java_arches

* Fri Feb 27 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.25-11
- build with md5 file digests for now to ensure upgradability of rpm

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-9
- remove dual tcl-devel requirement
- nuke useless libtool hacks

* Mon Dec 22 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-8
- DB_ENV->lock_get may self deadlock if user defined locks
  are used and there is only one lock partition defined
  (upstream bz#16415)
- fix for dd segfaults (upstream bz#16541)
- reorder patches

* Tue Dec  2 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-7
- remove s390 and s390x from java_arches (#474061)
- BR: tcl-devel for the tclConfig.sh change (#474062)

* Sun Nov 16 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-6
- package complete db4 documentation in db4-devel (#471633)
- add fix for the new libtool

* Tue Sep 16 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-5
- build also if db4 is not installed (thanks to Michael A. Peters)

* Wed Sep 10 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-4
- actually apply the .jni patch
- fix permissions in db4-utils package (#225675)

* Tue Aug 19 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-3
- apply upstream patch to allow replication clients to
  opena sequence
- rediff .jni patch

* Wed Jul  9 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-2
- rebuild

* Wed Jul  9 2008 Jindrich Novy <jnovy@redhat.com> 4.7.25-1
- update to 4.7.25 (#449735)
- package static java library only if listed in java_arches
- move to java-1.6.0-openjdk
- fix tcl library path
- drop glibc patch, no more needed

* Sat May 17 2008 Jindrich Novy <jnovy@redhat.com> 4.6.21-6
- fix license, remove .la files (#225675)
- move static libraries to separate package

* Fri Apr  3 2008 Jindrich Novy <jnovy@redhat.com> 4.6.21-5
- add upstream patch to fix a race condition between checkpoint
  and DB->close which can result in the checkpoint thread self-deadlocking

* Mon Mar 10 2008 Jindrich Novy <jnovy@redhat.com> 4.6.21-4
- don't list headers twice in filelist (#436701)

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 4.6.21-3
- manual rebuild because of gcc-4.3 (#434185)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.6.21-2
- Autorebuild for GCC 4.3

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 4.6.21-1
- update to 4.6.21
- own %%{_includedir}/db4 (#274251)

* Mon Sep  3 2007 Jindrich Novy <jnovy@redhat.com> 4.6.19-1
- update to 4.6.19 (#273461)

* Thu Aug 29 2007 Jindrich Novy <jnovy@redhat.com> 4.6.18-2
- rebuild for BuildID
- BR util-linux-ng

* Mon Jul 30 2007 Jindrich Novy <jnovy@redhat.com> 4.6.18-1
- update to 4.6.18
- drop upstream patches for 4.5.20 and gcj patch
- remove nptl-abi-note.S, useless as we are definitely
  running kernel >= 2.4.20 (#245416)
- move C++ stuff to subpackages to reduce dependency bloat (#220484)
- package db_codegen
- correct open() calls so that new db4 compiles with the new glibc

* Sat Mar 24 2007 Thomas Fitzsimmons <fitzsim@redhat.com> 4.5.20-5
- Require java-1.5.0-gcj and java-1.5.0-gcj-devel for build.

* Mon Dec  4 2006 Jindrich Novy <jnovy@redhat.com> 4.5.20-4
- apply upstream patches for 4.5.20
  (Java API <-> core API related fixes)

* Fri Dec  1 2006 Jindrich Novy <jnovy@redhat.com> 4.5.20-3
- temporarily remove ppc64 from java arches

* Sun Nov 26 2006 Jindrich Novy <jnovy@redhat.com> 4.5.20-2
- sync db4 and compat-db licenses to BSD-style as the result of
  consultation with legal department
- fix some rpmlint warnings

* Fri Nov 10 2006 Jindrich Novy <jnovy@redhat.com> 4.5.20-1
- update to db-4.5.20 (#198038)
- fix BuildRoot
- drop .64bit patch
- patch/source URLs now point to correct location

* Tue Sep 12 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-9
- rebuild

* Wed Sep  6 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-8
- revert the previous fix, it crashes OOo help

* Sun Sep  3 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-7.fc6
- fix memleak caused by SET_TXN macro in xa_db.c, when opening
  database created with DB_XA_CREATE flag (#204920)

* Wed Jul 19 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-6
- fix sparc64 build (#199358)

* Mon Jul 17 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-5
- rebuild because of gnu_hash

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.3.29-4.1
- rebuild

* Fri Mar 24 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-4
- drop useless java, lfs patches

* Mon Mar 13 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-3
- apply x86_64 fix from Henrik Nordstrom (#184588)
- don't nuke non-versioned archives twice

* Wed Feb 15 2006 Jindrich Novy <jnovy@redhat.com> 4.3.29-2
- don't package /usr/share/doc/images in the main db4 package
  and move it to db4-devel (#33328)
- make db4 LFS capable (#33849)
- move db4-devel, db4-tcl, db4-java to Development/Libraries
  group instead of System Environment/Libraries (#54320)
- BuildPrereq -> BuildRequires
- don't use RPM_SOURCE_DIR
- Obsoletes db3, db2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3.29-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.3.29-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Oct 07 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.29-1
- New upstream release

* Fri Sep 30 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.28-4
- Re-enable java for ppc64

* Wed Sep 21 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.28-3
- Add fno-strict-aliasing for java (#168965)

* Tue Sep 20 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.28-2
- no java for ppc64 for now (#166657)

* Tue Sep 20 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.28-1
- FC5 is nptl only (derived from jbj's spec)
- upgrade to 4.3.28

* Thu Jul 14 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.27-5
- re-enable db4-java

* Tue May 17 2005 Paul Nasrat <pnasrat@redhat.com> 4.3.27-4
- /usr/lib/tls/ix86 dirs (#151371)

* Mon Apr 25 2005 Bill Nottingham <notting@redhat.com> 4.3.27-3
- add libdb_cxx.so link (#149191)

* Fri Mar  4 2005 Jeff Johnson <jbj@jbj.org> 4.3.27-2
- rebuild with gcc4.

* Sat Jan  1 2005 Jeff Johnson <jbj@jbj.org> 4.3.27-1
- upgrade to 4.3.27.

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 4.3.21-1
- upgrade to 4.3.21, no db4-java for the moment again again.

* Tue Sep 21 2004 Nalin Dahyabhai <nalin@redhat.com> 4.2.52-6
- on %%{ix86} systems, make the availability of an NPTL-requiring libdb match
  the availability of an NPTL libpthread in glibc > 2.3.3-48
- run ldconfig in db4-java's %%post/%%postun
- when building java support, assume that libgcj is equivalent enough to 1.3

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Jeff Johnson <jbj@jbj.org> 4.2.52-4
- remove dangling symlinks (#123721 et al).
- remove db_cxx.so and db_tcl.so symlinks, versioned equivs exist.
- apply 2 patches from sleepycat.
- resurrect db4-java using sun jvm-1.4.2.
- cripple autoconf sufficiently to build db4-java with gcj, without jvm.
- check javac first, gcj34 next, then gcj-ssa, finally gcj.
- add ed build dependency (#125180).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Jeff Johnson <jbj@jbj.org> 4.2.52-2
- fix: automake *.lo wrapper, not elf, files included in *.a (#113572).

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 4.2.52-1
- upgrade to db-4.2.52, no db4-java for the moment.

* Fri Nov 28 2003 Paul Nasrat <pauln@truemesh.com> 4.2.41-0.2
- Add build requires tcl-devel

* Fri Oct 24 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-14
- symlink from %%{_libdir}/tls/libdb-4.1.so to the copy in /%%{_lib}/tls, so
  that the run-time linker can find the right copy for of apps which use an
  RPATH to point at %%{_libdir}/libdb-4.1.so

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-13
- add another section to the ABI note for the TLS libdb so that it's marked as
  not needing an executable stack (from Arjan Van de Ven)

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- build both with and without support for shared mutex locks, which require NPTL
- make behavior wrt where we put libdb the same for all OSs
- revert changes making tcl optional - nesting %%if tcl and %%ifarch nptl
  doesn't work
- fix dangling HREFs in utility docs (pointed to main docs dir, while they're
  actually in the -utils docs dir)
- run ldconfig when installing/removing the -utils subpackage, as it contains
  shared libraries

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-11
- fix multiple-inclusion problem of startup files when building shlibs without
  the -nostdlib flag

* Tue Oct 14 2003 Nalin Dahyabhai <nalin@redhat.com>
- link shared libraries without -nostdlib, which created an unresolvable dep
  on a hidden symbol

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without tcl dependency

* Sat Sep 20 2003 Jeff Johnson <jbj@jbj.org> 4.2.42-0.1
- update to 4.2.42.
- build in build_unix subdir.
- eliminate --enable-dump185, db_dump185.c no longer compiles for libdb*.
- create db4-tcl sub-pkg to isolate libtcl dependencies.

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-9
- rebuild

* Tue Aug 19 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-8
- add missing tcl-devel buildrequires (#101814)

* Tue Jul 15 2003 Joe Orton <jorton@redhat.com> 4.1.25-7
- rebuild

* Fri Jun 27 2003 Jeff Johnson <jbj@redhat.com> 4.1.25-6
- build with libtool-1.5, which can't recognize the .so in libfoo*.so atm.
- whack out libtool predep_objects wonkiness.

* Thu Jun 26 2003 Jeff Johnson <jbj@redhat.com> 4.1.25-5
- rebuild.

* Tue Jun 24 2003 Jeff Johnson <jbj@redhat.com> 4.1.25-4
- hack out O_DIRECT support in db4 for now.

* Tue Jun 24 2003 Nalin Dahyabhai <nalin@redhat.com>
- replace libtool.ac with current libtool.m4 so that running libtoolize doesn't
  cause a mismatch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  4 2003 Nalin Dahyabhai <nalin@redhat.com> 4.1.25-2
- change configure to only warn if JNI includes aren't found, assuming that
  the C compiler can find them
- remove build requirement on jdkgcj -- gcj is sufficient

* Mon May  5 2003 Jeff Johnson <jbj@redhat.com> 4.1.25-1
- upgrade to 4.1.25, crypto version.
- enable posix mutexes using nptl on all arches.

* Mon Mar  3 2003 Thoams Woerner <twoerner@redhat.com> 4.0.14-21
- enabled db4-java for x86_64

* Wed Feb  5 2003 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-20
- add dynamic libdb-4.0.so link back to %%{_libdir} so that dynamically
  linking with -ldb-4.0 will work again

* Tue Feb  4 2003 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-19
- rebuild to use link the shared object with the same libraries we use
  for the bundled utils, should pull in libpthread when needed
- move libdb.so from /%%{_lib} to %%{_libdir} where the linker can find it

* Sun Feb 02 2003 Florian La Roche <Florian.LaRoche@redhat.de> 4.0.14-18
- add java for s390x

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.0.14-17
- rebuilt

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de> 4.0.14-16
- add java for s390

* Tue Oct  8 2002 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-15
- add java bits back in for x86 boxes

* Fri Sep 20 2002 Than Ngo <than@redhat.com> 4.0.14-14.1
- Added better fix for s390/s390x/x86_64

* Thu Sep 05 2002 Arjan van de Ven
- remove java bits for x86-64

* Tue Aug 27 2002 Jeff Johnson <jbj@redhat.com> 4.0.14-14
- include libdb_tcl-4.1.a library.
- obsolete db1 packages.

* Tue Aug 13 2002 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-13
- include patch to avoid db_recover (#70362)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-11
- own %%{_includedir}/%{name}

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 4.0.14-10
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 4.0.14-8
- Add java bindings
- Fix C++ bindings

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  9 2002 Jeff Johnson <jbj@redhat.com>
- re-enable db.h symlink creation, db_util names, and db[23]-devel obsoletes.
- make sure that -ldb is functional.

* Thu Feb 21 2002 Jeff Johnson <jbj@redhat.com>
- avoid db_util name collisions with multiple versions installed.

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-3
- remove relocatability stuffs
- swallow a local copy of db1 and build db185_dump statically with it, to
  remove the build dependency and simplify bootstrapping new arches

* Mon Jan 27 2002 Nalin Dahyabhai <nalin@redhat.com> 4.0.14-2
- have subpackages obsolete their db3 counterparts, because they conflict anyway

* Tue Jan  8 2002 Jeff Johnson <jbj@redhat.com> db4-4.0.14-1
- upgrade to 4.0.14.

* Sun Aug  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix dangling docs symlinks
- fix dangling doc HREFs (#33328)
- apply the two patches listed at http://www.sleepycat.com/update/3.2.9/patch.3.2.9.html

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- turn off --enable-debug

* Thu May 10 2001 Than Ngo <than@redhat.com>
- fixed to build on s390x

* Mon Mar 19 2001 Jeff Johnson <jbj@redhat.com>
- update to 3.2.9.

* Tue Dec 12 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to remove 777 directories.

* Sat Nov 11 2000 Jeff Johnson <jbj@redhat.com>
- don't build with --enable-diagnostic.
- add build prereq on tcl.
- default value for %%_lib macro if not found.

* Tue Oct 17 2000 Jeff Johnson <jbj@redhat.com>
- add /usr/lib/libdb-3.1.so symlink to %%files.
- remove dangling tags symlink from examples.

* Mon Oct  9 2000 Jeff Johnson <jbj@redhat.com>
- rather than hack *.la (see below), create /usr/lib/libdb-3.1.so symlink.
- turn off --enable-diagnostic for performance.

* Fri Sep 29 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.1.17.
- disable posix mutexes Yet Again.

* Tue Sep 26 2000 Jeff Johnson <jbj@redhat.com>
- add c++ and posix mutex support.

* Thu Sep 14 2000 Jakub Jelinek <jakub@redhat.com>
- put nss_db into a separate package

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Wed Aug 23 2000 Jeff Johnson <jbj@redhat.com>
- remove redundant strip of libnss_db* that is nuking symbols.
- change location in /usr/lib/libdb-3.1.la to point to /lib (#16776).

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.
- all of libdb_tcl* (including symlinks) in db3-utils, should be db3->tcl?

* Wed Aug 16 2000 Jakub Jelinek <jakub@redhat.com>
- temporarily build nss_db in this package, should be moved
  into separate nss_db package soon

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.1.14.
- create db3-utils sub-package to hide tcl dependency, enable tcl Yet Again.
- FHS packaging.

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- disable tcl Yet Again, base packages cannot depend on libtcl.so.

* Sat Jun  3 2000 Jeff Johnson <jbj@redhat.com>
- enable tcl, rebuild against tcltk 8.3.1 (w/o pthreads).

* Tue May 30 2000 Matt Wilson <msw@redhat.com>
- include /lib/libdb.so in the devel package

* Wed May 10 2000 Jeff Johnson <jbj@redhat.com>
- put in "System Environment/Libraries" per msw instructions.

* Tue May  9 2000 Jeff Johnson <jbj@redhat.com>
- install shared library in /lib, not /usr/lib.
- move API docs to db3-devel.

* Mon May  8 2000 Jeff Johnson <jbj@redhat.com>
- don't rename db_* to db3_*.

* Tue May  2 2000 Jeff Johnson <jbj@redhat.com>
- disable --enable-test --enable-debug_rop --enable-debug_wop.
- disable --enable-posixmutexes --enable-tcl as well, to avoid glibc-2.1.3
  problems.

* Mon Apr 24 2000 Jeff Johnson <jbj@redhat.com>
- add 3.0.55.1 alignment patch.
- add --enable-posixmutexes (linux threads has not pthread_*attr_setpshared).
- add --enable-tcl (needed -lpthreads).

* Sat Apr  1 2000 Jeff Johnson <jbj@redhat.com>
- add --enable-debug_{r,w}op for now.
- add variable to set shm perms.

* Sat Mar 25 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.0.55

* Tue Dec 29 1998 Jeff Johnson <jbj@redhat.com>
- Add --enable-cxx to configure.

* Thu Jun 18 1998 Jeff Johnson <jbj@redhat.com>
- Create.
