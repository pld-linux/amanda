Summary:	A network-capable tape backup solution
Summary(pl):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	2.4.2p2
Release:	11
License:	BSD
Group:		Networking/Utilities
Source0:	http://prdownloads.sourceforge.net/amanda/%{name}-%{version}.tar.gz
Source1:	%{name}-srv.crontab
Source2:	%{name}.inetd
Source3:	%{name}idx.inetd
Source4:	amidxtape.inetd
Source5:	%{name}.conf
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-am_fixes.patch
Patch2:		%{name}-bug18322.patch
Patch3:		%{name}-build_tapetype.patch
Patch4:		%{name}-no_private_libtool.m4.patch
Patch5:		%{name}-ac25x.patch
Patch6:		%{name}-chg-zd-mtx-sh.patch
URL:		http://www.amanda.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cpio
BuildRequires:	dump
BuildRequires:	flex
BuildRequires:	gnuplot
BuildRequires:	libtool
BuildRequires:	readline-devel >= 4.2
BuildRequires:	tar
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc
%define		_localstatedir	/var/lib
%define		_libexecdir	%{_libdir}/amanda

%description
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a
single master backup server to back up multiple hosts to a single
large capacity tape drive. AMANDA uses native dump and/or GNU tar
facilities and can back up a large number of workstations running
multiple versions of Unix. Newer versions of AMANDA (including this
version) can use SAMBA to back up Microsoft(TM) Windows95/NT hosts.
The amanda package contains the core AMANDA programs and will need to
be installed on both AMANDA clients and AMANDA servers. Note that you
will have to install the amanda-client and amanda-server packages as
well.

%description -l pl
AMANDA jest sieciowo zorientowanym systemem tworzenia kopii
zapasowych. Umo¿liwia administratorowi sieci tworzenie kopii z kilku
hostów na jednej maszynie wyposa¿onej w pojemny dysk lub streamer.
Nowsze wersje programu umo¿liwiaj± zabezpieczanie zasobów Microsoft
Windows 95/98/NT/2000 przy u¿yciu protoko³u Samba. Ten pakiet zawiera
podstawowe pliki programu i powinien byæ zainstalowany zarówno na
serwerze jak i na kliencie. Pamiêtaj tak¿e o instalacji pakietów
amanda-client i amanda-server!

%package libs
Summary:	Amanda shared libraries
Summary(pl):	Biblioteki wspó³dzielone pakietu amanda
Group:		Networking/Utilities
Prereq:		/usr/bin/getgid
Prereq:		/bin/id
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/useradd
Prereq:		/usr/sbin/groupdel
Prereq:		/usr/sbin/userdel

%description libs
Amanda shared libraries.

%description libs -l pl
Biblioteki wspó³dzielone pakietu amanda.

%package client
Summary:	The client side of Amanda
Summary(pl):	Klient Amandy
Group:		Networking/Utilities
Prereq:		/sbin/ldconfig
Prereq:		rc-inetd
Prereq:		%{name}-libs = %{version}

%description client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up). You will also need to install the amanda package to each
AMANDA client. It requires at least one of dump and GNU tar installed.

%description client -l pl
Ten pakiet powinien byæ zainstalowany ma maszynach, z których
zawarto¶ci bêd± tworzone kopie zapasowe. Wymaga zainstalowanego co
najmniej jednego z pakietów dump i GNU tar.

%package server
Summary:	The server side of Amanda
Summary(pl):	Serwer Amandy
Group:		Networking/Utilities
Prereq:		rc-inetd
Prereq:		/sbin/ldconfig
Requires:	gnuplot
Requires:	crondaemon
Requires:	/etc/cron.d
Requires:	mt-st
Requires:	mtx
Prereq:		rc-inetd
Prereq:		%{name}-libs = %{version}

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device (such as a tape drive) where
backups will be written. You will also need to install the amanda
package to the AMANDA server. And, if the server is also to be backed
up, the server also needs to have the amanda-client package installed.

%description server -l pl
Ten pakiet powinien byæ zainstalowanych na maszynach, na których bêd±
magazynowane kopie zapasowe (lub do których podpiête s± urz±dzenia
typu streamer).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
libtoolize --copy --force
aclocal
autoconf
touch COPYING
rm -f missing
automake -a -c
%configure \
	--disable-static \
	--enable-shared \
	--with-index-server=localhost \
	--with-user=amanda \
	--with-group=amanda \
	--with-tape-device=/dev/null \
	--with-ftape-rawdevice=/dev/null \
	--with-changer-device=/dev/null \
	--with-fqdn \
	--with-smbclient=%{_bindir}/smbclient \
	--with-bsd-security \
	--with-buffered-dump \
	--with-amandahosts \
        --with-debugging=%{_localstatedir}/amanda/debug \
	--with-gnutar-listdir=%{_localstatedir}/amanda/gnutar-lists \
	--with-tmpdir=/var/tmp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{amanda,cron.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_localstatedir}/amanda

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SETUID_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/amanda-srv
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amanda
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amandaidx
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amidxtape

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/amanda
install example/*.ps $RPM_BUILD_ROOT%{_localstatedir}/amanda

> $RPM_BUILD_ROOT%{_sysconfdir}/amandates

gzip -9nf docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- amanda-libs < 2.4.2p2-3
/usr/sbin/chsh -s /bin/sh amanda

%triggerpostun -- amanda-libs < 2.4.2p2-11
/usr/sbin/usermod -G disk amanda

%pre libs
if [ -n "`/usr/bin/getgid amanda`" ]; then
	if [ "`getgid amanda`" != "80" ]; then
		echo "Warning: group amanda haven't gid=80. Correct this before installing amanda-libs" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 80 -r -f amanda
fi
if [ -n "`/bin/id -u amanda 2>/dev/null`" ]; then
	if [ "`/bin/id -u amanda`" != "80" ]; then
		echo "Warning: user amanda haven't uid=80. Correct this before installing amanda-libs" 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 80 -G disk -r -d /var/lib/amanda -s /bin/sh -c "Amanda Backup user" -g amanda amanda 1>&2
fi

%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig
if [ "$1" = "0" ]; then
	/usr/sbin/userdel amanda
	/usr/sbin/groupdel amanda
fi

%post client
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun client
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%post server
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi
echo "Don't forget to edit /etc/cron.d/amanda-srv" 1>&2

%postun server
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libamanda*.so
%attr(755,root,root) %{_libdir}/libamtape*.so
%attr(770,root,amanda) %dir %{_libexecdir}
%attr(770,root,amanda) %dir %{_localstatedir}/amanda


%files server
%defattr(644,root,root,755)
%doc docs/*.gz
%config(noreplace) /etc/sysconfig/rc-inetd/amidxtape
%config(noreplace) /etc/sysconfig/rc-inetd/amandaidx

%attr(750,root,amanda) %dir %{_sysconfdir}/amanda
%config(noreplace) %attr(640,root,amanda) %{_sysconfdir}/amanda/*

%attr(664,amanda,amanda) %{_localstatedir}/amanda/*

%attr(640,root,root) /etc/cron.d/amanda-srv

%attr(755,root,root) %{_libdir}/libamserver*.so
%attr(755,root,root) %{_libexecdir}/amindexd
%attr(755,root,root) %{_libexecdir}/amtrmidx
%attr(755,root,root) %{_libexecdir}/driver
%attr(4754,root,amanda) %{_libexecdir}/dumper
%attr(4754,root,amanda) %{_libexecdir}/planner
%attr(755,root,root) %{_libexecdir}/amcat.awk
%attr(755,root,root) %{_libexecdir}/amcleanupdisk
%attr(755,root,root) %{_libexecdir}/amidxtaped
%attr(755,root,root) %{_libexecdir}/amlogroll
%attr(755,root,root) %{_libexecdir}/amplot.awk
%attr(755,root,root) %{_libexecdir}/amplot.g
%attr(755,root,root) %{_libexecdir}/amplot.gp
%attr(755,root,root) %{_libexecdir}/amtrmlog
%attr(755,root,root) %{_libexecdir}/chg-chio
%attr(755,root,root) %{_libexecdir}/chg-chs
%attr(755,root,root) %{_libexecdir}/chg-manual
%attr(755,root,root) %{_libexecdir}/chg-mtx
%attr(755,root,root) %{_libexecdir}/chg-multi
%attr(755,root,root) %{_libexecdir}/chg-rth
%attr(755,root,root) %{_libexecdir}/chg-scsi
%attr(755,root,root) %{_libexecdir}/chg-zd-mtx
%attr(755,root,root) %{_libexecdir}/selfcheck
%attr(755,root,root) %{_libexecdir}/taper
%attr(755,root,root) %{_sbindir}/amadmin
%attr(4754,root,amanda) %{_sbindir}/amcheck
%attr(755,root,root) %{_sbindir}/amcheckdb
%attr(755,root,root) %{_sbindir}/amcleanup
%attr(755,root,root) %{_sbindir}/amdump
%attr(755,root,root) %{_sbindir}/amflush
%attr(755,root,root) %{_sbindir}/amgetconf
%attr(755,root,root) %{_sbindir}/amlabel
%attr(755,root,root) %{_sbindir}/amoverview
%attr(755,root,root) %{_sbindir}/amplot
%attr(755,root,root) %{_sbindir}/amrmtape
%attr(755,root,root) %{_sbindir}/amreport
%attr(755,root,root) %{_sbindir}/amstatus
%attr(755,root,root) %{_sbindir}/amtape
%attr(755,root,root) %{_sbindir}/amtoc
%attr(755,root,root) %{_sbindir}/amverify
%attr(755,root,root) %{_sbindir}/tapetype
%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/amplot.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amstatus.8*

%files client
%defattr(644,root,root,755)
%config(noreplace) /etc/sysconfig/rc-inetd/amanda
%attr(664,root,amanda) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/amandates
%attr(755,root,root) %{_libdir}/libamclient*.so
%attr(755,root,root) %{_libexecdir}/versionsuffix
%attr(755,root,root) %{_libexecdir}/amandad
%attr(4754,root,amanda) %{_libexecdir}/calcsize
%attr(4754,root,amanda) %{_libexecdir}/rundump
%attr(4754,root,amanda) %{_libexecdir}/runtar
%attr(4754,root,amanda) %{_libexecdir}/selfcheck
%attr(755,root,root) %{_libexecdir}/sendbackup
%attr(755,root,root) %{_libexecdir}/sendsize
%attr(755,root,root) %{_libexecdir}/patch-system
%attr(4754,root,amanda) %{_libexecdir}/killpgrp
%attr(755,root,root) %{_sbindir}/amrecover
%attr(755,root,root) %{_sbindir}/amrestore
%{_mandir}/man8/amrecover.8*
%{_mandir}/man8/amrestore.8*
