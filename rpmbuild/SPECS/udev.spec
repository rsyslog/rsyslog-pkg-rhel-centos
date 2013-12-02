Summary:        A rule-based device node and kernel event manager
Name:           udev
Version:        182
Release:        3%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Source:         ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.xz
URL:            http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gperf
BuildRequires:  libselinux-devel libsepol-devel
BuildRequires:  glib2-devel
BuildRequires:  hwdata
BuildRequires:  gobject-introspection-devel >= 0.6.2
BuildRequires:  usbutils >= 0.82
BuildRequires:  kmod-devel >= 5
BuildRequires:  libblkid-devel >= 2.20
Requires(pre):  fileutils
Requires(pre):  /usr/bin/getent /usr/sbin/groupadd
Requires:       hwdata
Requires:       systemd-units
Requires:       util-linux >= 2.15.1
Conflicts:      systemd < 39
Conflicts:      dracut < 013-93
Conflicts:      filesystem < 3-2

Patch1: udev-rules-Limit-USB-autosuspend-on-USB-HID-devices.patch

%ifarch s390 s390x
# Require s390utils-base, because it's essential on s390
Requires:       s390utils-base
%endif

%description
udev is a collection of tools and a daemon to manage events received
from the kernel and deal with them in user-space. Primarily this
involves managing permissions, and creating and removing meaningful
symlinks to device nodes in /dev when hardware is discovered or
removed from the system.

%package -n libudev
Summary:        Dynamic library to access udev device information
Group:          System Environment/Libraries
Requires:       udev = %{version}-%{release}
Conflicts:      filesystem < 3
License:        LGPLv2+

%description -n libudev
This package contains the dynamic library libudev, which provides access
to udev device information, and an interface to search devices in sysfs.

%package -n libudev-devel
Summary:        Development files for libudev
Group:          Development/Libraries
Requires:       libudev = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+

%description -n libudev-devel
This package contains the development files for the library libudev, a
dynamic library, which provides access to udev device information.

%package -n libgudev1
Summary:        Libraries for adding libudev support to applications that use glib
Group:          Development/Libraries
Requires:       libudev = %{version}-%{release}
Conflicts:      filesystem < 3
License:        LGPLv2+

%description -n libgudev1
This package contains the libraries that make it easier to use libudev
functionality from applications that use glib.

%package -n libgudev1-devel
Summary:        Header files for adding libudev support to applications that use glib
Group:          Development/Libraries
Requires:       libgudev1 = %{version}-%{release}
License:        LGPLv2+

%description -n libgudev1-devel
This package contains the header and pkg-config files for developing
glib-based applications using libudev functionality.

%prep
%setup -q
%patch1 -p1

%build
# prevent man pages from re-building (xsltproc)
find . -name "*.[1-8]" -exec touch '{}' \;
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS -fPIE -DPIE -pie -Wl,-z,relro -Wl,-z,now"
export V=1
%configure \
 --prefix=%{_prefix} \
 --sysconfdir=%{_sysconfdir} \
 --libexecdir=%{_prefix}/lib \
 --with-selinux \
 --with-systemdsystemunitdir=%{_prefix}/lib/systemd/system
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -fr $RPM_BUILD_ROOT%{_docdir}/udev
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
mkdir -p -m 0755 $RPM_BUILD_ROOT%{_prefix}/lib/firmware
mkdir -p -m 0755 $RPM_BUILD_ROOT%{_prefix}/lib/firmware/updates
mkdir -p -m 0755 $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../bin/udevadm $RPM_BUILD_ROOT%{_sbindir}/udevadm

%pre
getent group cdrom >/dev/null || /usr/sbin/groupadd -g 11 cdrom || :
getent group tape >/dev/null || /usr/sbin/groupadd -g 33 tape || :
getent group dialout >/dev/null || /usr/sbin/groupadd -g 18 dialout || :
getent group floppy >/dev/null || /usr/sbin/groupadd -g 19 floppy || :
systemctl stop udev.service udev-control.socket udev-kernel.socket >/dev/null 2>&1 || :

%post
systemctl daemon-reload >/dev/null 2>&1 || :
systemctl start udev.service >/dev/null 2>&1 || :

%postun
systemctl daemon-reload >/dev/null 2>&1 || :

%post -n libudev -p /sbin/ldconfig
%postun -n libudev -p /sbin/ldconfig

%post -n libgudev1 -p /sbin/ldconfig
%postun -n libgudev1 -p /sbin/ldconfig

%files
%doc NEWS COPYING README TODO ChangeLog  src/keymap/README.keymap.txt
%{_bindir}/udevadm
%{_sbindir}/udevadm
%{_prefix}/lib/udev
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/udev/udev.conf
%attr(0755,root,root) %dir %{_sysconfdir}/udev/
%attr(0755,root,root) %dir %{_sysconfdir}/udev/rules.d/
%attr(0644,root,root) %{_mandir}/man7/*.7*
%attr(0644,root,root) %{_mandir}/man8/*.8*
%{_datadir}/pkgconfig/udev.pc
%dir %attr(0755,root,root) %{_prefix}/lib/firmware
%dir %attr(0755,root,root) %{_prefix}/lib/firmware/updates
%attr(0644,root,root) %{_prefix}/lib/systemd/system/*.service
%attr(0644,root,root) %{_prefix}/lib/systemd/system/*.socket
%{_prefix}/lib/systemd/system/basic.target.wants/*.service
%{_prefix}/lib/systemd/system/sockets.target.wants/*.socket

%files -n libudev
%doc src/COPYING
%attr(0755,root,root) %{_libdir}/libudev.so.*

%files -n libudev-devel
%doc src/docs/html/*
%{_includedir}/libudev.h
%{_libdir}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/gtk-doc/html/libudev/*

%files -n libgudev1
%doc src/gudev/COPYING
%attr(0755,root,root) %{_libdir}/libgudev-1.0.so.*
%attr(0644,root,root) %{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files -n libgudev1-devel
%doc src/gudev/docs/html/*
%attr(0755,root,root) %{_libdir}/libgudev-1.0.so
%dir %attr(0755,root,root) %{_includedir}/gudev-1.0
%dir %attr(0755,root,root) %{_includedir}/gudev-1.0/gudev
%attr(0644,root,root) %{_includedir}/gudev-1.0/gudev/*.h
%attr(0644,root,root) %{_datadir}/gir-1.0/GUdev-1.0.gir
%dir %{_datadir}/gtk-doc/html/gudev
%attr(0644,root,root) %{_datadir}/gtk-doc/html/gudev/*
%attr(0644,root,root) %{_libdir}/pkgconfig/gudev-1.0*

%changelog
* Thu May 31 2012 Josh Boyer <jwboyer@redhat.com> 182-3
- Limit USB autosuspend on USB HID devices (brc#825284)

* Tue Mar 27 2012 Harald Hoyer <harald@redhat.com> 182-2
- removed s390 rules

* Sun Mar 18 2012 Kay Sievers <kay@redhat.com> - 182-1
- version 182
  - enable USB sutosuspend for some built-in HID devices
  - do not create /dev/disk/by-path/ for 'ATA transport class' devices
  - do not create /dev/disk/by-id/scsi-* for pure ATA devices
  - let rules file in /etc override rules with the same name in /run

* Thu Feb 09 2012 Kay Sievers <kay@redhat.com> - 181-2
- rebuild with fixed binutils
- remove 'dev' package dependency handling

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> 181-1
- version 181
  - require kmod 5
  - provide /dev/cdrom for /dev/sr0

* Fri Feb  3 2012 Kay Sievers <kay@redhat.com> 180-3
- require an newer filesystem (repo test rebuild)

* Sun Jan 29 2012 Kay Sievers <kay@redhat.com> 180-2
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sun Jan 29 2012 Kay Sievers <kay@redhat.com> 180-1
- version 180
  - fix rule execution (brc#785148)
  - ID_PART_* export for udisks2
- temporarily revert 'install everything in /usr' to be
  able to update teh current rawhide package without the
  dependency on the /usr-move converted filessytem

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> 179-3
- use %{_sbindir}

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> 179-2
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> 179-1
- version 179
  - devtmpfs is mandatory now
  - /run is mandatory now
  - modules are loaded with 'libkmod'
  - blkid is built-in now

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 175-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Kay Sievers <kay@redhat.com> 175-1
- version 175
  - bug fix release

* Sat Oct 22 2011 Kay Sievers <kay@redhat.com> 174-2
- ignore entire rule when a key is unknown (brc#748082)

* Thu Oct 20 2011 Kay Sievers <kay@redhat.com> 174-1
- version 174
  - path_id, usb_id, input_id tools are built-in commands
  - fusectl is mounted by systemd
  - SYSFS=, ID=, BUS= are removed
  - udevadm trigger --type=failed is removed
  - udev control socket is now in /run/udev/control
  - disable persistent net and cdrom rule generator
- remove obsolete rpm dependencies
- remove SYSV init script controls

* Mon Aug 29 2011 Kay Sievers <kay@redhat.com> 173-3
- fix bluetooth input device handling (brc#733862)

* Mon Aug 29 2011 Daniel Drake <dsd@laptop.org> 173-2
- Update OLPC XO keymap

* Mon Aug 01 2011 Harald Hoyer <harald@redhat.com> 173-1
- version 173
- udev-acl functionality is in systemd

* Wed Jul 20 2011 Harald Hoyer <harald@redhat.com> 172-2
- removed loop devices (should be compiled in the kernel)
- removed deprecated directories
- removed scsi_id symlink
- cleanup of requirements

* Mon Jul 11 2011 Harald Hoyer <harald@redhat.com> 172-1
- version 172

* Mon Jun 20 2011 Harald Hoyer <harald@redhat.com> 171-2
- build without introspection
- removed unused dirs
- added ConsoleKit dirs

* Fri May 27 2011 Harald Hoyer <harald@redhat.com> 171-1
- version 171

* Fri May 20 2011 Harald Hoyer <harald@redhat.com> 170-1
- version 170
- removed /sbin/start_udev

* Mon Apr 11 2011 Harald Hoyer <harald@redhat.com> 167-4
- more selinux fixes

* Thu Apr 7 2011 Adam Williamson <awilliam@redhat.com> - 167-3
- selinux_label.patch: from upstream, don't label files outside of /dev

* Thu Mar 31 2011 Harald Hoyer <harald@redhat.com> 167-2
- fixed udev-trigger.service

* Wed Mar 30 2011 Harald Hoyer <harald@redhat.com> 167-1
- version 167

* Wed Mar 23 2011 Harald Hoyer <harald@redhat.com> 166-2
- add ACLs for harmony remote controls
Resolves: rhbz#559412
- fixed CDROM profile handling

* Wed Feb 16 2011 Harald Hoyer <harald@redhat.com> 166-1
- renamed udev-post initscript to udev-retry to match 
  upstream systemd service name
- version 166

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 164-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Harald Hoyer <harald@redhat.com> 164-8
- fixed: network device renaming 2-step exceeds IFNAMSIZ
Resolves: rhbz#673675
- removed v4l version 1

* Fri Jan 21 2011 Harald Hoyer <harald@redhat.com> 164-7
- removed unnecessary devices from /lib/udev/devices

* Mon Dec 06 2010 Harald Hoyer <harald@redhat.com> 164-6
- removed MAKEDEV symlink
Resolves: rhbz#660091
- fixed kill loop
Resolves: rhbz#657651

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 164-5
- Add patches to fix touchpad toggle key handling

* Fri Nov 12 2010 Harald Hoyer <harald@redhat.com> 164-4
- add ACLs for PDA devices
Resolves: rhbz#642435

* Fri Nov 12 2010 Harald Hoyer <harald@redhat.com> 164-3
- enlarged the import buffer to fix the ressize bugs
Resolves: rhbz#652318

* Fri Nov 12 2010 Harald Hoyer <harald@redhat.com> 164-2
- do not create mount point dirs in /dev

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 164-1
- version 164
- skip start_udev with systemd

* Wed Sep 29 2010 jkeating - 161-4
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@rdhat.com> 161-3
- Rebuild against newer gobject-introspection

* Wed Sep 01 2010 Harald Hoyer <harald@redhat.com> 161-2
- bugfixes for systemd service files
- bugfix for selinux labeling
- bugfixes for cdrom_id

* Tue Aug 17 2010 Harald Hoyer <harald@redhat.com> 161-1
- udev-161 with an upstream quirk for the qemu cdrom and
  more cdrom handling bugfixes
Resolves: rhbz#609049 rhbz#624286
- added floppy group
Resolves: rhbz#620814

* Fri Aug 06 2010 Harald Hoyer <harald@redhat.com> 160-9
- added quirk to cdrom_id, to boot from qemu
Resolves: rhbz#609049
- fix console switching and ACLs
Resolves: rhbz#608712
- minor bugfixes

* Tue Jul 20 2010 Harald Hoyer <harald@redhat.com> 160-8
- make loop block device again 

* Tue Jul 20 2010 Harald Hoyer <harald@redhat.com> 160-7
- turn off hotplug in /sys/kernel/uevent_helper or /proc/sys/kernel/hotplug

* Thu Jul 15 2010 Harald Hoyer <harald@redhat.com> 160-6
- add versioned requires for libudev to udev

* Wed Jul 14 2010 Dan Horák <dan[at]danny.cz> 160-5
- update paths to arch-specific rules

* Tue Jul 13 2010 Lennart Poettering <lennart@poettering.net> - 160-4
- Comment systemd-install for now as long as sysinit is not split into pieces

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 160-3
- Update systemd-install lines to use --realize instead of --start (which got renamed in systemd)

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 160-2
- Don't require systemd .pc file, to break build dependency cycle

* Tue Jul 13 2010 Harald Hoyer <harald@redhat.com> 160-1
- version 160
- add systemd service files
- fixed COPYRIGHT files

* Fri Jun 25 2010 Harald Hoyer <harald@redhat.com> 158-2
- moved udev pkgconfig to base file on authors request
- specfile cleanups

* Thu Jun 24 2010 Harald Hoyer <harald@redhat.com> 158-1
- version 158

* Thu May 27 2010 Harald Hoyer <harald@redhat.com> 156-2
- cleaned up start_udev and udev-post initscript
- removed redhat specific rules
- removed all the makedev.d stuff, udevd now natively supports
  /lib/udev/devices
- added basic devices in /lib/udev/devices

* Tue May 25 2010 Harald Hoyer <harald@redhat.com> 156-1
- version 156

* Tue May 25 2010 Harald Hoyer <harald@redhat.com> 155-1
- version 155

* Wed May 12 2010 Harald Hoyer <harald@redhat.com> 154-1
- version 154

* Tue Apr 27 2010 Harald Hoyer <harald@redhat.com> 153-1.20100427git
- version 153

* Tue Apr 13 2010 Harald Hoyer <harald@redhat.com> 152-0.1.20100413git
- pre release of version 152

* Mon Mar 22 2010 Harald Hoyer <harald@redhat.com> 151-8
- only correct the timestamp, if UTC=="no"

* Mon Mar 22 2010 Harald Hoyer <harald@redhat.com> 151-7
- touch with "--no-create", will not use open() 
  and trigger devs/watchdogs (bug #575417)

* Mon Mar 22 2010 Harald Hoyer <harald@redhat.com> 151-6
- fixed return code of touching the device nodes [FAIL] -> [OK]

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 151-5
- add "-D" to gperf call

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 151-4
- add patch for virtio-ports (#569700)
- own libgudev dirs (#561319)
- minor udev startup script improvements (#549518)
- create /dev/hugepages subdir in start_udev (#541998)
- remove GPL COPYING file from LGPL subpackages (#536843)
- removed symlinks to udevadm
- touch all device nodes after udev settled for the timezone
  timestamp (#569335)
- add some upstream bugfixes

* Sun Feb 07 2010 Kyle McMartin <kyle@redhat.com> 151-3
- udev-86a7a2f-fix-missing-firmware.patch: fix hang when loading
  microcode (since microcode_intel tries to probe firmware which does
  not exist. *sigh*)

* Fri Jan 29 2010 Harald Hoyer <harald@redhat.com> 151-2
- fixed rules and startup script (#559844)

* Wed Jan 27 2010 Harald Hoyer <harald@redhat.com> 151-1
- version 151
- fixed udev-post initscript
- only require s390utils-base, rather than s390utils (#553156)

* Tue Nov 24 2009 Harald Hoyer <harald@redhat.com> 147-2
- require s390utils, because it's essential on s390

* Thu Nov 12 2009 Harald Hoyer <harald@redhat.com> 147-1
- version 147
- Fix upgrade from Fedora 11 with bluez installed (#533925)
- obsolete DeviceKit and DeviceKit-devel (#532961)
- fixed udev-post exit codes (#523976)
- own directory /lib/udev/keymaps (#521801)
- no more floppy modaliases (#514329)
- added one more modems to modem-modeswitch.rules (#515349)
- add NEWS file to the doc section
- automatically turn on hotplugged CPUs (rhbz#523127)
- recognize a devtmpfs on /dev (bug #528488)

* Fri Oct 09 2009 Harald Hoyer <harald@redhat.com> 147-0.1.gitdf3e07d
- pre 147 
- database format changed
- lots of potential buffer overflow fixes

* Tue Sep 29 2009 Harald Hoyer <harald@redhat.com> 145-10
- add ConsoleKit patch for ConsoleKit 0.4.1

* Fri Sep 25 2009 harald@redhat.com 145-9
- add patches to fix cdrom_id
- add patch to fix the inotify bug (bug #524752)

* Wed Sep 23 2009 harald@redhat.com 145-8
- obsolete libgudev and libgudev-devel (bug #523569)

* Mon Aug 24 2009 Karsten Hopp <karsten@redhat.com> 145-7
- drop ifnarch s390x for usbutils, as we now have usbutils for s390x

* Mon Aug 24 2009 Harald Hoyer <harald@redhat.com> 145-6
- ifnarch s390 for usbutils

* Tue Aug 04 2009 Harald Hoyer <harald@redhat.com> 145-5
- do not make extra nodes in parallel
- restorecon on /dev

* Tue Aug 04 2009 Harald Hoyer <harald@redhat.com> 145-4
- --enable-debug 
- add patch for timestamps in debugging output

* Wed Jul 29 2009 Harald Hoyer <harald@redhat.com> 145-3
- add patch from upstream git to fix bug #514086
- add version to usbutils build requirement

* Fri Jul 24 2009 Harald Hoyer <harald@redhat.com> 145-2
- fix file permissions
- remove rpath
- chkconfig --add for udev-post
- fix summaries
- add "Required-Stop" to udev-post

* Tue Jul 14 2009 Harald Hoyer <harald@redhat.com> 145-1
- version 145
- add "udevlog" kernel command line option to redirect the
  output of udevd to /dev/.udev/udev.log

* Fri Jul 03 2009 Harald Hoyer <harald@redhat.com> 143-2
- add acpi floppy modalias
- add retrigger of failed events in udev-post.init
- killall pids of udev in %%pre

* Fri Jun 19 2009 Harald Hoyer <harald@redhat.com> 143-1
- version 143

* Thu Jun 08 2009 Harald Hoyer <harald@redhat.com> 142-4
- git fix: udevadm: settle - fix timeout
- git fix: OWNER/GROUP: fix if logic
- git fix: rule-generator: cd - skip by-path links if we create by-id links
- git fix: fix possible endless loop for GOTO to non-existent LABEL
- git fix: cdrom_id: suppress ID_CDROM_MEDIA_STATE=blank for plain non-writable 
                CDROM media

* Thu Jun 08 2009 Harald Hoyer <harald@redhat.com> 142-3
- delay device-mapper changes

* Fri Jun 05 2009 Bastien Nocera <bnocera@redhat.com> 142-2
- Rebuild in dist-f12

* Fri May 15 2009 Harald Hoyer <harald@redhat.com> 142-1
- version 142
- no more libvolume_id and vol_id

* Fri Apr 17 2009 Harald Hoyer <harald@redhat.com> 141-3
- added /dev/fuse creation to start_udev

* Thu Apr 16 2009 Harald Hoyer <harald@redhat.com> 141-2
- fixed post and pre

* Tue Apr 14 2009 Harald Hoyer <harald@redhat.com> 141-1
- version 141

* Wed Apr 01 2009 Harald Hoyer <harald@redhat.com> 139-4
- double the IMPORT buffer (bug #488554)
- Resolves: rhbz#488554

* Wed Apr 01 2009 Harald Hoyer <harald@redhat.com> 139-3
- renamed modprobe /etc/modprobe.d/floppy-pnp to
  /etc/modprobe.d/floppy-pnp.conf (bug #492732 #488768)
- Resolves: rhbz#492732

* Tue Mar 03 2009 Harald Hoyer <harald@redhat.com> 139-2
- speedup of start_udev by doing make_extra_nodes in parallel to 
  the daemon start

* Fri Feb 27 2009 Harald Hoyer <harald@redhat.com> 139-1
- version 139

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 137-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Harald Hoyer <harald@redhat.com> 137-4
- fixed md change/remove event handling

* Thu Feb 05 2009 Harald Hoyer <harald@redhat.com> 137-3
- added 5 second sleep for "modprobedebug" to catch bad modules

* Fri Jan 30 2009 Harald Hoyer <harald@redhat.com> 137-2
- moved groupadd to pre section (bug #483089)

* Thu Jan 29 2009 Harald Hoyer <harald@redhat.com> 137-1
- version 137
- add vol_id patches from kzak
- dialout group has gid 18 now

* Tue Jan 20 2009 Harald Hoyer <harald@redhat.com> 136-2
- added some rule fixes, which will be in udev-137

* Tue Jan 20 2009 Harald Hoyer <harald@redhat.com> 136-1
- test for restorecon in start_udev before it is used (bug #480608)
- added groups video audio cdrom tape dialout in post
  (might be moved to MAKEDEV)
- version 136

* Tue Dec 16 2008 Harald Hoyer <harald@redhat.com> 135-3
- added sepol patch

* Tue Dec 16 2008 Harald Hoyer <harald@redhat.com> 135-2
- changed udevsettle -> udevadm settle
- added doc to libudev-devel
- added more attr and defattr
- various rpmlint fixes

* Tue Dec 02 2008 Harald Hoyer <harald@redhat.com> 135-1
- version 135

* Wed Nov 19 2008 Harald Hoyer <harald@redhat.com> 133-1
- version 133

* Mon Nov 10 2008 Harald Hoyer <harald@redhat.com> 132-1
- version 132
- added memory stick rules (bug #470096)

* Thu Oct 16 2008 Harald Hoyer <harald@redhat.com> 127-2
- added 2 patches for md raid vol_id 

* Mon Sep 01 2008 Harald Hoyer <harald@redhat.com> 127-1
- version 127

* Fri Aug 08 2008 Harald Hoyer <harald@redhat.com> 126-1
- version 126
- fixed udevadm syntax in start_udev (credits B.J.W. Polman)
- removed some manually created devices from makedev (bug #457125)

* Tue Jun 17 2008 Harald Hoyer <harald@redhat.com> 124-1.1
- readded udevcontrol, udevtrigger symlinks for Fedora 9,
  which are needed by live-cd-tools

* Thu Jun 12 2008 Harald Hoyer <harald@redhat.com> 124-1
- version 124
- removed udevcontrol, udevtrigger symlinks (use udevadm now)

* Tue Jun  3 2008 Jeremy Katz <katzj@redhat.com> - 121-2.20080516git
- Add lost F9 change to remove /dev/.udev in start_udev (#442827)

* Fri May 16 2008 Harald Hoyer <harald@redhat.com> 121-1.20080516git
- version 121 + latest git fixes

* Thu May 07 2008 Harald Hoyer <harald@redhat.com> 120-6.20080421git
- added input/hp_ilo_mouse symlink

* Tue May 06 2008 Harald Hoyer <harald@redhat.com> 120-5.20080421git
- remove /dev/.udev in start_udev (bug #442827)

* Mon Apr 21 2008 Harald Hoyer <harald@redhat.com> 120-4.20080421git
- added patches from git:
- persistent device naming: also read unpartitioned media
- scsi_id: initialize serial strings
- logging: add trailing newline to all strings
- path_id: remove subsystem whitelist
- allow setting of MODE="0000"
- selinux: more context settings
- rules_generator: net rules - always add KERNEL== match to generated rules
- cdrom_id: replace with version which also exports media properties
- vol_id: add --offset option
- udevinfo: do not replace chars when printing ATTR== matches
- Resolves: rhbz#440568

* Fri Apr 11 2008 Harald Hoyer <harald@redhat.com> 120-3
- fixed pre/preun scriptlets (bug #441941)
- removed fedora specific patch for selinux symlink handling

* Sat Apr 05 2008 Harald Hoyer <harald@redhat.com> 120-2
- removed warning about deprecated /lib/udev/devices (rhbz#440961)
- replaced /usr/bin/find with shell find function (rhbz#440961)

* Fri Apr 04 2008 Harald Hoyer <harald@redhat.com> 120-1
- version 120

* Mon Mar 17 2008 Harald Hoyer <harald@redhat.com> 118-11
- removed /var/lib/udev/rules.d again

* Fri Mar 14 2008 Harald Hoyer <harald@redhat.com> 118-10
- turned off MAKEDEV cache, until the generated shell scripts 
  create new directories

* Thu Mar 13 2008 Harald Hoyer <harald@redhat.com> 118-9
- added more support for the "modprobedebug" kernel command 
  line option, to debug hanging kernel modules

* Thu Mar 13 2008 Harald Hoyer <harald@redhat.com> 118-8
- added /etc/sysconfig/udev to configure some speedups
- added "udevnopersist" as a kernel command line, to disable
  persistent storage symlink generation

* Thu Mar 13 2008 Harald Hoyer <harald@redhat.com> 118-7
- files from /var/lib/udev/rules.d are copied to /dev/.udev/rules.d 
  at startup and back at shutdown
- persistent cd and net rules generate the files in 
  /dev/.udev/rules.d now
- added post section to symlink 70-persistent-cd.rules 70-persistent-net.rules
  from /etc/udev/rules.d to /dev/.udev/rules.d

* Thu Mar 13 2008 Harald Hoyer <harald@redhat.com> 118-6
- moved all generated files to /var/lib/udev 
  (also 70-persistent-cd.rules 70-persistent-net.rules)
- added a caching mechanism for MAKEDEV (saves some seconds on startup)
- added trigger for selinux-policy and MAKEDEV to remove the udev cache files

* Wed Feb 20 2008 Harald Hoyer <harald@redhat.com> 118-4
- made symlinks relative (rhbz#432878)
- removed the backgrounding of node creation (rhbz#381461)
- do not change sg group ownership to disk for scanners (rhbz#432602)
- attempt to fix selinux symlink bug (rhbz#345071)
- fixed URL
- made rpmlint mostly happy
- disabled static version (no static selinux lib)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 118-3
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Harald Hoyer <harald@redhat.com> 118-2
- reenabled static version

* Tue Jan 08 2008 Harald Hoyer <harald@redhat.com> 118-1
- version 118
- removed old USB compat rule (rhbz#424331)
- disabled static version

* Thu Oct 18 2007 Harald Hoyer <harald@redhat.com> 116-3
- fixed preun chkconfig
- added /sbin path to chkconfig in post section 
- patch: do not generate net rules for type > 256
- fixes glitches appearing in bz#323991

* Tue Oct 16 2007 Dennis Gilmore <dennis@ausil.us> 116-2
- sparc64 requires -fPIE not -fpie

* Mon Oct 15 2007 Harald Hoyer <harald@redhat.com> 116-1
- version 116

* Fri Oct 12 2007 Harald Hoyer <harald@redhat.com> 115-5.20071012git
- added upstream patch for rhbz#328691
- moved floppy module loading to pnp-alias in /etc/modprobe.d/floppy-pnp

* Wed Oct 10 2007 Harald Hoyer <harald@redhat.com> 115-5.20070921git
- better modprobe options for the kernel command line 'modprobedebug' option

* Fri Sep 21 2007 Harald Hoyer <harald@redhat.com> - 115-4
- more upstream fixes from git

* Thu Sep 20 2007 Harald Hoyer <harald@redhat.com> - 115-3
- some upstream fixes from git
- removed last_rule for loop rules
- added "udevinfo udevtrace" kernel command line options for better debugging

* Fri Sep 07 2007 Harald Hoyer <harald@redhat.com> - 115-2
- some upstream fixes from git
- last_rule for loop rules (speedup for live-cds/qemu with 128 loop devices)

* Thu Aug 24 2007 Harald Hoyer <harald@redhat.com> - 115-1
- version 115

* Fri Aug 24 2007 Harald Hoyer <harald@redhat.com> - 113-12
- removed /dev/tape symlink, because it's now a directory
  (bug #251755)

* Thu Aug 23 2007 Harald Hoyer <harald@redhat.com> - 114-4
- added patch to prevent persistent net rules for virtual network interfaces,
  like vmware and vlans

* Thu Aug 23 2007 Harald Hoyer <harald@redhat.com> - 114-3
- changed license tag
- changed to latest upstream rule ordering

* Thu Aug 16 2007 Harald Hoyer <harald@redhat.com> - 113-11
- readded firmware rule (#252983)

* Wed Aug 15 2007 Harald Hoyer <harald@redhat.com> - 113-10
- do not run vol_id on non-partition block devices (bug #251401)
- read all multiline pnp modaliases again

* Mon Aug 13 2007 Harald Hoyer <harald@redhat.com> - 114-2
- fixed isapnp rule (bug #251815)
- fix for nikon cameras (bug #251401)

* Fri Aug 10 2007 Harald Hoyer <harald@redhat.com> - 114-1
- version 114
- big rule unification and cleanup
- added persistent names for network and cdrom devices over reboot

* Wed Aug 08 2007 Harald Hoyer <harald@redhat.com> - 113-9
- added lp* to 50-udev.nodes (#251272)

* Mon Jul 30 2007 Harald Hoyer <harald@redhat.com> - 113-8
- removed "noreplace" config tag from rules (#250043)

* Fri Jul 27 2007 Harald Hoyer <harald@redhat.com> - 113-7
- major rule cleanup
- removed persistent rules from 50 and included upstream rules
- removed skip_wait from modprobe

* Fri Jul 20 2007 Harald Hoyer <harald@redhat.com> - 113-6
- kernel does not provide usb_device anymore,
  corrected the rules (#248916)

* Thu Jul 19 2007 Harald Hoyer <harald@redhat.com> - 113-5
- corrected the rule for usb devices (#248916)

* Sat Jul 14 2007 Harald Hoyer <harald@redhat.com> - 113-4
- do not collect modprobes (bug #222542), because firmware
  loading seems to depend on it.

* Mon Jul  9 2007 Harald Hoyer <harald@redhat.com> - 113-3
- speedup things a little bit

* Wed Jun 27 2007 Harald Hoyer <harald@redhat.com> - 113-2
- added more firewire symlinks (#240770)
- minor rule patches

* Tue Jun 26 2007 Harald Hoyer <harald@redhat.com> - 113-1
- version 113
- added rule for SD cards in a TI FlashMedia slot (#217070)

* Tue Jun 26 2007 Harald Hoyer <harald@redhat.com> - 106-4.1
- fixed modprobedebug option
- removed snd-powermac from the default modules (#200585)

* Wed May 02 2007 Harald Hoyer <harald@redhat.com> - 106-4
- do not skip all events on modprobe (#238385)
- Resolves: rhbz#238385

* Fri Apr 27 2007 Harald Hoyer <harald@redhat.com> - 106-3
- modprobe only on modalias (bug #238140)
- make startup messages visible again
- speedup boot process by not executing pam_console_apply while booting
- Resolves: rhbz#238140

* Wed Apr 11 2007 Harald Hoyer <harald@redhat.com> - 106-2
- create floppy device nodes with the correct selinux context (bug #235953)
- Resolves: rhbz#235953

* Wed Mar  7 2007 Harald Hoyer <harald@redhat.com> - 106-1
- version 106
- specfile cleanup
- removed pilot rule
- removed dasd_id and dasd_id rule
- provide static versions in a subpackage

* Wed Feb 21 2007 Harald Hoyer <harald@redhat.com> - 105-1
- version 105

* Tue Feb  6 2007 Harald Hoyer <harald@redhat.com> - 104-2
- moved uinput to input subdirectory (rhbz#213854)
- added USB floppy symlinks (rhbz#185171)
- fixed ZIP drive handling (rhbz#223016)
- Resolves: rhbz#213854,rhbz#185171,rhbz#223016

* Tue Jan 23 2007 Harald Hoyer <harald@redhat.com> - 104-1
- version 104
- merged changes from RHEL

* Wed Dec  6 2006 Harald Hoyer <harald@redhat.com> - 103-3
- changed DRIVER to DRIVERS 
- Resolves: rhbz#218160

* Fri Nov 10 2006 Harald Hoyer <harald@redhat.com> - 103-2
- changed SYSFS to new ATTR rules
- Resolves: rhbz#214898

* Fri Nov 10 2006 Harald Hoyer <harald@redhat.com> - 103-1
- Removed 51-hotplug.rules
- Resolves: rhbz#214277

* Wed Oct 11 2006 Harald Hoyer <harald@redhat.com> - 095-14
- skip persistent block for gnbd devices (bug #210227)

* Wed Oct  4 2006 Harald Hoyer <harald@redhat.com> - 095-13
- fixed path_id script (bug #207139)

* Tue Oct  3 2006 Jeremy Katz <katzj@redhat.com> - 095-12
- autoload mmc_block (#171687)

* Wed Sep 27 2006 Harald Hoyer <harald@redhat.com> - 095-10
- typo in xpram/slram rule (bug #205563)

* Mon Sep 25 2006 Harald Hoyer <harald@redhat.com> - 095-9
- improved error msg for firmware_helper (bug #206944)
- added xpram symlink to slram device nodes (bug #205563)
- removed infiniband rules (bug #206224)
- use newest path_id script (bug #207139)

* Tue Aug 29 2006 Harald Hoyer <harald@redhat.com> - 095-8
- fixed bug #204157

* Wed Aug 16 2006 Harald Hoyer <harald@redhat.com> - 095-7
- added udevtimeout=<timeout in seconds>
  kernel command line parameters for start_udev 
  (default is to wait forever)

* Wed Aug 16 2006 Harald Hoyer <harald@redhat.com> - 095-6
- new speedup patch for selinux (bug #202673)

* Thu Aug 10 2006 Harald Hoyer <harald@redhat.com> - 095-5
- allow long comments (bug #200244)

* Mon Aug  7 2006 Harald Hoyer <harald@redhat.com> - 095-4
- fixed CAPI device nodes (bug #139321)
- fixed bug #201422

* Wed Jul 12 2006 Harald Hoyer <harald@redhat.com> - 095-3
- more infiniband rules (bug #198501)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 095-2.1
- rebuild

* Thu Jul  6 2006 Harald Hoyer <harald@redhat.com> - 095-2
- added option to debug udev with kernel cmdline option "udevdebug"

* Wed Jul  5 2006 Harald Hoyer <harald@redhat.com> - 095-1
- version 095

* Wed Jun 14 2006 Harald Hoyer <harald@redhat.com> - 094-1
- version 094

* Sun May 21 2006 Peter Jones <pjones@redhat.com> - 092-2
- Fix typo in pam-console rule

* Wed May 18 2006 Harald Hoyer <harald@redhat.com> - 092-1
- version 092
- corrected some rules (bug #192210 #190927)

* Tue May 09 2006 Harald Hoyer <harald@redhat.com> - 091-3
- corrected some rules (bug #190927)

* Wed May 03 2006 Harald Hoyer <harald@redhat.com> - 091-2
- added subpackages libvolume_id and libvolume_id-devel

* Wed May 03 2006 Harald Hoyer <harald@redhat.com> - 091-1
- version 091

* Wed Apr 19 2006 Harald Hoyer <harald@redhat.com> - 090-1
- version 090

* Thu Apr 13 2006 Harald Hoyer <harald@redhat.com> - 089-1
- version 089
- do not force loading of parport_pc (bug #186850)
- manually load snd-powermac (bug #176761)
- added usb floppy symlink (bug #185171)
- start_udev uses udevtrigger now instead of udevstart

* Wed Mar 08 2006 Harald Hoyer <harald@redhat.com> - 084-13
- fixed pam_console rules (#182600)

* Mon Mar 06 2006 Harald Hoyer <harald@redhat.com> - 084-12
- fixed DRI permissions

* Sun Mar 05 2006 Bill Nottingham <notting@redhat.com> - 084-11
- use $ENV{MODALIAS}, not $modalias (#181494)

* Thu Mar 02 2006 Harald Hoyer <harald@redhat.com> - 084-10
- fixed cdrom rule

* Wed Mar 01 2006 Harald Hoyer <harald@redhat.com> - 084-9
- create non-enum device (cdrom, floppy, scanner, changer)
  for compatibility (random device wins)
  e.g. /dev/cdrom -> hdd /dev/cdrom-hdc -> hdc /dev/cdrom-hdd -> hdd

* Wed Mar 01 2006 Harald Hoyer <harald@redhat.com> - 084-8
- fixed ZIP drive thrashing (bz #181041 #182601)
- fixed enumeration (%%e does not work anymore) (bz #183288)

* Fri Feb 24 2006 Peter Jones <pjones@redhat.com> - 084-7
- Don't start udevd in %%post unless it's already running
- Stop udevd before chkconfig --del in %%preun

* Fri Feb 24 2006 Harald Hoyer <harald@redhat.com> - 084-6
- put back original WAIT_FOR_SYSFS rule

* Fri Feb 24 2006 Harald Hoyer <harald@redhat.com> - 084-5
- removed WAIT_FOR_SYSFS rule

* Wed Feb 22 2006 Harald Hoyer <harald@redhat.com> - 084-4
- fixed group issue with vol_id (bz #181432)
- fixed dvb permissions (bz #179993)
- added support for scsi media changer (bz #181911)
- fixed pktcdvd device creation (bz #161268)

* Tue Feb 21 2006 Florian La Roche <laroche@redhat.com> - 084-3
- also output the additional space char as part of the startup message

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 084-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Harald Hoyer <harald@redhat.com> - 084-1
- version 084

* Mon Feb 06 2006 Harald Hoyer <harald@redhat.com> - 078-9
- closed fd leak (bug #179980)

* Thu Jan 26 2006 Harald Hoyer <harald@redhat.com> - 078-8
- changed usb device naming

* Tue Jan 24 2006 Harald Hoyer <harald@redhat.com> - 078-7
- put WAIT_FOR_SYSFS rules in 05-udev-early.rules

* Mon Jan 23 2006 Harald Hoyer <harald@redhat.com> - 078-6
- added some WAIT_FOR_SYSFS rules
- removed warning message, if udev_db is not available

* Sun Jan 22 2006 Kristian Høgsberg <krh@redhat.com> 078-5
- Drop udev dependency (#178621).

* Tue Jan 11 2006 Harald Hoyer <harald@redhat.com> - 078-4
- removed group "video" from the rules
- fixed specfile
- load nvram, floppy, parport and lp modules in
  /etc/sysconfig/modules/udev-stw.modules until there 
  is a better solution
- fixed more floppy module loading

* Fri Dec 23 2005 Harald Hoyer <harald@redhat.com> - 078-3
- fixed floppy module loading
- added monitor socket
- fixed typo in dvb rule

* Wed Dec 21 2005 Bill Nottingham <notting@redhat.com> - 078-2
- udevstart change: allow greylisting of certain modaliases (usb, firewire)

* Wed Dec 21 2005 Harald Hoyer <harald@redhat.com> - 078-1
- version 078
- fixed symlink to pam_console.dev

* Thu Dec 15 2005 Harald Hoyer <harald@redhat.com> - 077-2
- switched back to udevstart and use active /dev/.udev/queue waiting 
  in start_udev
- removed support for old kernels
- refined some udev.rules

* Mon Dec 13 2005 Harald Hoyer <harald@redhat.com> - 077-1
- version 077
- patch to include udevstart2 in udevd and delay daemonize until queue is empty

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec 06 2005 Harald Hoyer <harald@redhat.com> - 076-1
- speedup udevd with selinux by calling matchpathcon_init_prefix()
- version 076

* Mon Nov 21 2005 Harald Hoyer <harald@redhat.com> - 075-4
- speedup udev event replay with udevstart2 

* Fri Nov 18 2005 Harald Hoyer <harald@redhat.com> - 075-3
- refined start_udev for old kernels

* Fri Nov 11 2005 Harald Hoyer <harald@redhat.com> - 075-2
- moved /etc/udev/scripts to /lib/udev
- moved /etc/udev/devices to /lib/udev/devices
- added new event replay for kernel >= 2.6.15
- added usb devices
- renamed cpu device to cpuid (bug #161538)
- changed vendor string "Onstream" to "On[sS]tream" (bug #173043)
- compiled all *_id programs statically

* Fri Nov 11 2005 Harald Hoyer <harald@redhat.com> - 075-1
- version 075

* Tue Oct 25 2005 Harald Hoyer <harald@redhat.com> - 071-1
- version 071

* Mon Oct 10 2005 Harald Hoyer <harald@redhat.com> - 069-10
- removed group usb

* Mon Oct 10 2005 Harald Hoyer <harald@redhat.com> - 069-9
- added libsepol-devel BuildReq
- refined persistent rules

* Mon Oct 10 2005 Harald Hoyer <harald@redhat.com> - 069-8
- corrected c&p edd_id rule, symlink for js devices
- added -lsepol

* Thu Oct 06 2005 Harald Hoyer <harald@redhat.com> - 069-7
- added edd_id

* Fri Sep 30 2005 Harald Hoyer <harald@redhat.com> - 069-6
- special handling of IEEE1394 firewire devices (bug #168093)

* Fri Sep 23 2005 Harald Hoyer <harald@redhat.com> - 069-5
- added missing path_id

* Wed Sep 21 2005 Harald Hoyer <harald@redhat.com> - 069-4
- readded volume_id now known as vol_id, bug #168883

* Thu Sep 15 2005 Bill Nottingham <notting@redhat.com> - 069-3
- fix firmware loading

* Wed Sep 14 2005 Bill Nottingham <notting@redhat.com> - 069-2
- own /lib/firmware (#167016)

* Wed Sep 14 2005 Harald Hoyer <harald@redhat.com> - 069-1
- version 069

* Thu Aug 04 2005 Harald Hoyer <harald@redhat.com> - 063-6
- compile with pie .. again... (#158935)
- fixed typo in echo (#138509)

* Tue Aug 02 2005 Harald Hoyer <harald@redhat.com> - 063-5
- fixed scsi hotplug replay

* Tue Aug 02 2005 Bill Nottingham <notting@redhat.com> - 063-5
- add rule to allow function id matching for pcmcia after loading
  modules (#164665)

* Tue Aug 02 2005 Harald Hoyer <harald@redhat.com> - 063-4
- fixed typo for tape devices and changed mode to 0660

* Thu Jul 28 2005 Harald Hoyer <harald@redhat.com> - 063-3
- changed "SYMLINK=" to "SYMLINK+="

* Sun Jul 24 2005 Bill Nottingham <notting@redhat.com> - 063-2
- don't set SEQNUM for scsi replay events (#163729)

* Tue Jul 19 2005 Bill Nottingham <notting@redhat.com> - 063-1
- update to 063
- handle the hotplug events for ieee1394, scsi, firmware

* Fri Jul 08 2005 Bill Nottingham <notting@redhat.com> - 062-2
- update to 062
- use included ata_id, build usb_id
- load modules for pci, usb, pcmcia
- ship RELEASE-NOTES in %%doc

* Thu Jul 07 2005 Harald Hoyer <harald@redhat.com> - 058-2
- compile with pie

* Fri May 20 2005 Bill Nottingham <notting@redhat.com> - 058-1
- update to 058, fixes conflict with newer kernels (#158371)

* Thu May 12 2005 Harald Hoyer <harald@redhat.com> - 057-6
- polished persistent scripts

* Thu May  5 2005 Bill Nottingham <notting@redhat.com> - 057-5
- rebuild

* Thu May  5 2005 Bill Nottingham <notting@redhat.com> - 057-4
- better check for mounted tmpfs on /dev (#156862)

* Wed Apr 27 2005 Peter Jones <pjones@redhat.com> - 057-3
- use udevstart rather than udev for udevstart.static 

* Thu Apr 21 2005 Harald Hoyer <harald@redhat.com> - 057-2
- added Inifiniband devices (bug #147035)
- fixed pam_console.dev (bug #153250)

* Mon Apr 18 2005 Harald Hoyer <harald@redhat.com> - 057-1
- version 057

* Fri Apr 15 2005 Dan Walsh <dwalsh@redhat.com> - 056-2
- Fix SELinux during creation of Symlinks

* Mon Apr 11 2005 Harald Hoyer <harald@redhat.com> - 056-1
- updated to version 056
- merged permissions in the rules file
- added udevpermconv.sh to convert old permission files

* Mon Mar 28 2005 Warren Togami <wtogami@redhat.com> - 050-10
- own default and net dirs (#151368 Hans de Goede)

* Mon Mar 07 2005 Warren Togami <wtogami@redhat.com> - 050-9
- fixed rh#150462 (udev DRI permissions)

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> - 050-8
- fixed rh#144598

* Fri Feb 18 2005 Harald Hoyer <harald@redhat.com> - 050-6
- introducing /etc/udev/makedev.d/50-udev.nodes
- glibcstatic patch modified to let gcc4 compile udev

* Thu Feb 10 2005 Harald Hoyer <harald@redhat.com> - 050-5
- doh, reverted the start_udev devel version, which slipped in

* Thu Feb 10 2005 Harald Hoyer <harald@redhat.com> - 050-3
- fixed forgotten " in udev.rules

* Tue Jan 11 2005 Harald Hoyer <harald@redhat.com> - 050-2
- removed /dev/microcode, /dev/cpu/microcode is now the real node
- cleaned up start_udev

* Tue Jan 11 2005 Harald Hoyer <harald@redhat.com> - 050-1
- version 050
- /dev/cpu/0/microcode -> /dev/cpu/microcode

* Tue Dec 21 2004 Dan Walsh <dwalsh@redhat.com> - 048-4
- Call selinux_restore to fix labeling problem in selinux
- Fixes rh#142817

* Tue Dec 21 2004 Harald Hoyer <harald@redhat.com> - 048-3
- maybe fixed bug rh#143367

* Thu Dec 16 2004 Harald Hoyer <harald@redhat.com> - 048-2
- fixed a case where reading /proc/ide/hd?/media returns EIO
  (bug rh#142713)
- changed all device node permissions of group "disk" to 0640 
  (bug rh#110197)
- remove $udev_db with -fr in case of a directory (bug rh#142962)

* Mon Dec 13 2004 Harald Hoyer <harald@redhat.com> - 048-1
- version 048
- major specfile cleanup

* Thu Nov 04 2004 Harald Hoyer <harald@redhat.com> - 042-1
- version 042

* Thu Nov 04 2004 Harald Hoyer <harald@redhat.com> - 039-10
- speed improvement, scripts in rules are now executed only once,
  instead of four times

* Thu Nov 04 2004 Harald Hoyer <harald@redhat.com> - 039-9
- removed wrong SIG_IGN for SIGCHLD
- moved ide media check to script to wait for the procfs

* Wed Nov  3 2004 Jeremy Katz <katzj@redhat.com> - 039-8.FC3
- recreate lvm device nodes if needed in the trigger (#137807)

* Wed Nov 03 2004 Harald Hoyer <harald@redhat.com> - 039-6.FC3.2
- replace udev.conf by default
- LANG=C for fgrep in start_udev; turn grep into fgrep

* Tue Nov 02 2004 Harald Hoyer <harald@redhat.com> - 039-6.FC3.1
- speed up pam_console.dev
- mount pts and shm, in case of the dev trigger
- increased timeout for udevstart
- removed syslog() from signal handler (caused vmware locks)
- turned off logging, which speeds up the boot process

* Thu Oct 21 2004 Harald Hoyer <harald@redhat.com> - 039-6
- fixed typo

* Thu Oct 21 2004 Harald Hoyer <harald@redhat.com> - 039-5
- added udev-039-norm.patch, which prevents removal of hd* devices,
  because the kernel sends remove/add events, if an IDE removable device
  is close(2)ed. mke2fs, e.g. would fail in this case.

* Wed Oct 20 2004 Harald Hoyer <harald@redhat.com> - 039-4
- do not call dev.d scripts, if network interface hasn't changed 
  the name
- correct wait for dummy network devices
- removed NONBLOCK from volume-id
- do not log in udev.static, which should fix bug 136005 

* Mon Oct 18 2004 Harald Hoyer <harald@redhat.com> - 039-3
- refined wait_for_sysfs for udev.static

* Mon Oct 18 2004 Harald Hoyer <harald@redhat.com> - 039-2
- improved wait_for_sysfs for virtual consoles with Kay Siever's patch
- wait for ppp class
- wait for LVM dm- devices
- integrate wait_for_sys in udev.static for the initrd

* Mon Oct 18 2004 Harald Hoyer <harald@redhat.com> - 039-1
- version 039, fixes also manpage bug 135996 
- fixed glibc issue for static version (getgrnam, getpwnam) (bug 136005)
- close the syslog in every app

* Fri Oct 15 2004 Harald Hoyer <harald@redhat.com> - 038-2
- par[0-9] is now a symlink to lp
- MAKEDEV the parport devices
- now conflicts with older initscripts

* Thu Oct 14 2004 Harald Hoyer <harald@redhat.com> - 038-1
- raw device nodes are now created in directory raw
- version 038

* Wed Oct 13 2004 Harald Hoyer <harald@redhat.com> - 036-1
- better wait_for_sysfs warning messages

* Wed Oct 13 2004 Harald Hoyer <harald@redhat.com> - 035-2
- fixed double bug in start_udev (bug 135405)

* Tue Oct 12 2004 Harald Hoyer <harald@redhat.com> - 035-1
- version 035, which only improves wait_for_sysfs
- load ide modules in start_udev, until a hotplug script is available
  (bug 135260)

* Mon Oct 11 2004 Harald Hoyer <harald@redhat.com> - 034-3
- removed scary error messages from wait_for_sysfs
- symlink from nst? -> tape?
- kill udevd on update

* Fri Oct  8 2004 Harald Hoyer <harald@redhat.com> - 034-2
- check for /proc/sys/dev/cdrom/info existence in check-cdrom.sh

* Fri Oct  8 2004 Harald Hoyer <harald@redhat.com> - 034-1
- new version udev-034
- removed patches, which went upstream
- pam_console.dev link renamed to 05-pam_console.dev
- MAKEDEV.dev links renamed to 10-MAKEDEV.dev

* Thu Oct 07 2004 Harald Hoyer <harald@redhat.com> - 032-10
- added floppy madness (bug 134830)
- replay scsi events in start_udev for the devices on the adapter (bug 130746)

* Wed Oct 06 2004 Harald Hoyer <harald@redhat.com> - 032-9
- obsoleted $UDEV_LOG, use udev_log
- correct SYMLINK handling in pam_console.dev
- specfile cleanup
- added check-cdrom.sh for nice cdrom symlinks

* Mon Oct 04 2004 Harald Hoyer <harald@redhat.com> - 032-8
- added patches from Féliciano Matias for multiple symlinks (bug 134477 and 134478)
- corrected some permissions with a missing leading 0
- added z90crypt to the permissions file (bug 134448)
- corrected requires and conflicts tags
- removed /dev/log from MAKEDEV creation

* Fri Oct 01 2004 Harald Hoyer <harald@redhat.com> - 032-7
- more device nodes for those without initrd

* Thu Sep 30 2004 Harald Hoyer <harald@redhat.com> - 032-6
- prevent error message from device copying
- use already translated starting strings

* Wed Sep 29 2004 Harald Hoyer <harald@redhat.com> - 032-5
- add "fi" to start_udev
- do not create floppy devices manually (bug 133838)

* Tue Sep 28 2004 Harald Hoyer <harald@redhat.com> - 032-4
- made /etc/udev/devices/ for manual device nodes
- refined SELINUX check, if /dev is not yet mounted in start_dev

* Mon Sep 27 2004 Harald Hoyer <harald@redhat.com> - 032-3
- corrected permissions for /dev/rtc (bug 133636)
- renamed device-mapper to mapper/control (bug 133688)

* Wed Sep 22 2004 Harald Hoyer <harald@redhat.com> - 032-2
- removed option to turn off udev
- udevstart.static now symling to udev.static

* Tue Sep 21 2004 Harald Hoyer <harald@redhat.com> - 032-1
- version 032

* Mon Sep 20 2004 Harald Hoyer <harald@redhat.com> - 030-27
- simplified udev.conf
- refined close_on_exec patch
- added pam_console supply for symlinks, now gives correct permissions,
  for e.g. later plugged in cdroms
- renamed sr? to scd? (see devices.txt; k3b likes that :)

* Mon Sep 13 2004 Jeremy Katz <katzj@redhat.com> - 030-26
- require a 2.6 kernel
- prereq instead of requires MAKEDEV
- obsolete and provide dev
- add a trigger for the removal of /dev so that we set things up 

* Fri Sep 10 2004 Dan Walsh <dwalsh@redhat.com> - 030-25
- Use matchmediacon

* Fri Sep 10 2004 Harald Hoyer <harald@redhat.com> - 030-24
- check if SELINUX is not disabled before executing setfiles (bug 132099)

* Wed Sep  8 2004 Harald Hoyer <harald@redhat.com> - 030-23
- mount tmpfs with mode 0755 in start_udev

* Tue Sep  7 2004 Harald Hoyer <harald@redhat.com> - 030-22
- applied rules from David Zeuthen which read /proc directly without 
  shellscript

* Tue Sep  7 2004 Harald Hoyer <harald@redhat.com> - 030-21
- applied enumeration patch from David Zeuthen for cdrom symlinks (bug 131532)
- create /dev/ppp in start_udev (bug 131114)
- removed nvidia devices from start_udev
- check for restorecon presence in start_udev (bug 131904)

* Fri Sep  3 2004 Harald Hoyer <harald@redhat.com> - 030-20
- due to -x added to MAKEDEV specify the par and lp numbers

* Fri Sep  3 2004 Harald Hoyer <harald@redhat.com> - 030-19
- added udev-030-rhsec.patch (bug 130351)

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 030-18
- make the exact device in start_udev (and thus, require new MAKEDEV)

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 030-17
- make sure file contexts of everything in the tmpfs /dev are set right 
  when start_udev runs

* Thu Sep 02 2004 Harald Hoyer <harald@redhat.com> - 030-16
- moved %%{_sysconfdir}/hotplug.d/default/udev.hotplug to %%{_sysconfdir}/hotplug.d/default/10-udev.hotplug

* Thu Sep 02 2004 Harald Hoyer <harald@redhat.com> - 030-15
- added nvidia devices to start_udev
- added UDEV_RAMFS for backwards compat to udev.conf
- changed Group (bug 131488)
- added libselinux-devel to build requirements

* Wed Sep  1 2004 Jeremy Katz <katzj@redhat.com> - 030-14
- require MAKEDEV

* Wed Sep 1 2004 Dan Walsh <dwalsh@redhat.com> - 030-13
- Change to setfilecon if directory exists.

* Wed Sep 01 2004 Harald Hoyer <harald@redhat.com> - 030-12
- fixed start_udev

* Tue Aug 31 2004 Jeremy Katz <katzj@redhat.com> - 030-11
- use tmpfs instead of ramfs (it has xattr support now)
- change variables appropriately to TMPFS intead of RAMFS in udev.conf
- create loopN, not just loop in start_udev

* Fri Aug 27 2004 Dan Walsh <dwalsh@redhat.com> - 030-10
- Fix Patch

* Thu Aug 26 2004 Dan Walsh <dwalsh@redhat.com> - 030-9
- Cleaned up selinux patch

* Tue Aug 24 2004 Harald Hoyer <harald@redhat.com> - 030-8
- changed defaults not to remove device nodes
- added rule for net/tun
- extended start_udev to create devices, which can trigger module autoloading
- refined cloexec patch, to redirect stdin,out,err of /dev.d execed apps to /dev/null

* Mon Aug 23 2004 Harald Hoyer <harald@redhat.com> - 030-7
- removed usage of /usr/bin/seq in start_udev
- set correct permissions in start_udev
- extended the cloexec patch
- removed udev-persistent package (define with_persistent==0)
- check for /var/run/console/console.lock before calling /sbin/pam_console_setowner
- linked pam_console_setowner statically against libglib-2.0.a

* Fri Aug 20 2004 Harald Hoyer <harald@redhat.com> - 030-5
- use correct console.lock file now in pam_console_setowner

* Wed Aug 18 2004 Harald Hoyer <harald@redhat.com> - 030-4
- added the selinux patch

* Fri Jul 23 2004 Harald Hoyer <harald@redhat.com> - 030-3
- extended the cloexec patch

* Wed Jul 21 2004 Dan Walsh <dwalsh@redhat.com> - 030-2
- Close Database fd in exec processes using FD_CLOSEXEC

* Wed Jul 14 2004 Harald Hoyer <harald@redhat.com> - 030-1
- version 030

* Wed Jul 14 2004 Harald Hoyer <harald@redhat.com> - 029-4
- added udevstart.static 

* Wed Jul 14 2004 Harald Hoyer <harald@redhat.com> - 029-3
- put /etc/sysconfig/udev in /etc/udev/udev.conf and removed it
- made only udev.static static
- make our defaults the default values
- removed /udev

* Tue Jul  6 2004 Harald Hoyer <harald@redhat.com> - 029-1
- version 029, added udev_remove and udev_owner to udev.conf

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Harald Hoyer <harald@redhat.com> - 026-3
- fixed UDEV_REMOVE=no

* Tue Jun  8 2004 Harald Hoyer <harald@redhat.com> - 026-2
- udev-026
- preserve ownership of device nodes, which already exist
- do not remove device nodes if UDEV_REMOVE="no"
- added volume_id
- build with klibc

* Wed May 26 2004 Harald Hoyer <harald@redhat.com> - 025-1
- udev-025
- added ata_identify
- build nearly all with dietlibc

* Mon May 10 2004 Elliot Lee <sopwith@redhat.com> 024-6
- Turn off udevd by default for FC2

* Tue Apr 20 2004 Harald Hoyer <harald@redhat.com> - 024-5
- fixed permission for /dev/tty (FC2)

* Thu Apr 15 2004 Harald Hoyer <harald@redhat.com> - 024-4
- moved the 00- files to 50-, to let the use place his files in front

* Thu Apr 15 2004 Harald Hoyer <harald@redhat.com> - 024-3
- set UDEV_SELINUX to yes
- added UDEV_LOG

* Thu Apr 15 2004 Harald Hoyer <harald@redhat.com> - 024-2
- added /udev to filelist

* Wed Apr 14 2004 Harald Hoyer <harald@redhat.com> - 024-1
- update to 024
- added /etc/sysconfig/udev
- added selinux, pam_console, dbus support

* Fri Mar 26 2004 Harald Hoyer <harald@redhat.com> - 023-1
- update to 023

* Wed Mar 24 2004 Bill Nottingham <notting@redhat.com> 022-1
- update to 022

* Sun Mar 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- really move initscript

* Sun Feb 29 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- move chkconv to preun
- nicer url

* Wed Feb 25 2004 Harald Hoyer <harald@redhat.com> - 018-1
- changes permissions and rules

* Mon Feb 23 2004 Dan Walsh <dwalsh@redhat.com>
- Add selinux support

* Thu Feb 19 2004 Greg Kroah-Hartman <greg@kroah.com>
- add some more files to the documentation directory
- add ability to build scsi_id and make it the default

* Mon Feb 16 2004 Greg Kroah-Hartman <greg@kroah.com>
- fix up udevd build, as it's no longer needed to be build seperatly
- add udevtest to list of files
- more Red Hat sync ups.

* Thu Feb 12 2004 Greg Kroah-Hartman <greg@kroah.com>
- add some changes from the latest Fedora udev release.

* Mon Feb 2 2004 Greg Kroah-Hartman <greg@kroah.com>
- add udevsend, and udevd to the files
- add ability to build udevd with glibc after the rest is build with klibc

* Mon Jan 26 2004 Greg Kroah-Hartman <greg@kroah.com>
- added udevinfo to rpm
- added URL to spec file
- added udevinfo's man page

* Mon Jan 05 2004 Rolf Eike Beer <eike-hotplug@sf-tec.de>
- add defines to choose the init script (Redhat or LSB)

* Tue Dec 16 2003 Robert Love <rml@ximian.com>
- install the initscript and run chkconfig on it

* Tue Nov 2 2003 Greg Kroah-Hartman <greg@kroah.com>
- changes due to config file name changes

* Fri Oct 17 2003 Robert Love <rml@tech9.net>
- Make work without a build root
- Correctly install the right files
- Pass the RPM_OPT_FLAGS to gcc so we can build per the build policy
- Put some prereqs in
- Install the hotplug symlink to udev

* Mon Jul 28 2003 Paul Mundt <lethal@linux-sh.org>
- Initial spec file for udev-0.2.
