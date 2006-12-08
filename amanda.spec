#
# Conditional build:
%bcond_without	xfs	# without (possible) support for xfsdump
%bcond_without	client	# without client package
%bcond_without	server	# without server package
#
Summary:	A network-capable tape backup solution
Summary(pl):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	2.5.1p2
Release:	0.8
License:	BSD
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/amanda/%{name}-%{version}.tar.gz
# Source0-md5:	6811f8a296650a6c0f64766b6e6abbe1
Source1:	%{name}-srv.crontab
Source2:	%{name}.inetd
Source3:	%{name}idx.inetd
Source4:	amidxtape.inetd
Source5:	%{name}.conf
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-ac25x.patch
Patch2:		%{name}-chg-zd-mtx-sh.patch
Patch3:		%{name}-tar.patch
URL:		http://www.amanda.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	dump
BuildRequires:	flex
BuildRequires:	libxslt-progs
BuildRequires:	libtool
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_xfs:BuildRequires:	xfsdump}
Conflicts:	shadow < 1:4.0.4.1-4
Conflicts:	pwdutils < 3.1.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
zapasowych. Umo�liwia administratorowi sieci tworzenie kopii z kilku
host�w na jednej maszynie wyposa�onej w pojemny dysk lub streamer.
Nowsze wersje programu umo�liwiaj� zabezpieczanie zasob�w Microsoft
Windows 95/98/NT/2000 przy u�yciu protoko�u Samba. Ten pakiet zawiera
podstawowe pliki programu i powinien by� zainstalowany zar�wno na
serwerze jak i na kliencie. Pami�taj tak�e o instalacji pakiet�w
amanda-client i amanda-server!

%package libs
Summary:	Amanda shared libraries
Summary(pl):	Biblioteki wsp�dzielone pakietu amanda
Group:		Networking/Utilities
Requires(postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/chsh
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(amanda)
Provides:	user(amanda)

%description libs
Amanda shared libraries.

%description libs -l pl
Biblioteki wsp�dzielone pakietu amanda.

%package client
Summary:	The client side of Amanda
Summary(pl):	Klient Amandy
Group:		Networking/Utilities
Requires(post,postun):	/sbin/ldconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-inetd
Conflicts:	tar < 1.13

%description client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up). You will also need to install the amanda package to each
AMANDA client. It requires at least one of dump and GNU tar installed.

%description client -l pl
Ten pakiet powinien by� zainstalowany ma maszynach, z kt�rych
zawarto�ci b�d� tworzone kopie zapasowe. Wymaga zainstalowanego co
najmniej jednego z pakiet�w dump i GNU tar.

%package server
Summary:	The server side of Amanda
Summary(pl):	Serwer Amandy
Group:		Networking/Utilities
Requires(post,postun):	/sbin/ldconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/etc/cron.d
Requires:	crondaemon
Requires:	gnuplot
Requires:	mt-st
Requires:	mtx
Requires:	rc-inetd
Obsoletes:	amanda

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device (such as a tape drive) where
backups will be written. You will also need to install the amanda
package to the AMANDA server. And, if the server is also to be backed
up, the server also needs to have the amanda-client package installed.

%description server -l pl
Ten pakiet powinien by� zainstalowany na maszynach, na kt�rych b�d�
magazynowane kopie zapasowe (lub do kt�rych podpi�te s� urz�dzenia
typu streamer).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# kill libtool.m4 copy
head -n 1147 acinclude.m4 > acinc.tmp
mv -f acinc.tmp acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	GNUPLOT=/usr/bin/gnuplot \
	MAILER=/bin/mail \
	PRINT=/usr/bin/lpr \
	DUMP=/sbin/dump \
	RESTORE=/sbin/restore \
	%{?with_xfs:XFSDUMP=/sbin/xfsdump} \
	%{?with_xfs:XFSRESTORE=/sbin/xfsrestore} \
	--disable-static \
	--enable-shared \
	%{!?with_server:--without-server} \
	%{!?with_client:--without-client} \
	--with-index-server=localhost \
	--with-user=amanda \
	--with-group=amanda \
	--with-tape-device=/dev/null \
	--with-ftape-rawdevice=/dev/null \
	--with-changer-device=/dev/null \
	--with-fqdn \
	--with-smbclient=%{_bindir}/smbclient \
	--with-bsd-security \
	--with-ssh-security \
	--with-buffered-dump \
	--with-amandahosts \
	--with-debugging=%{_localstatedir}/amanda/debug \
	--with-gnutar-listdir=%{_localstatedir}/amanda/gnutar-lists \
	--with-tmpdir=/var/tmp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{amanda,cron.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_localstatedir}/amanda/gnutar-lists \
	$RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SETUID_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/amanda-srv
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE2} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amanda
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE3} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amandaidx
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE4} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amidxtape

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/amanda
install example/*.ps $RPM_BUILD_ROOT%{_localstatedir}/amanda
touch $RPM_BUILD_ROOT%{_localstatedir}/amanda/.amandahosts

> $RPM_BUILD_ROOT%{_sysconfdir}/amandates

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun libs -- %{name}-libs < 2.5.1p2-1
echo "Adding amanda to disk and backup groups"
/usr/sbin/usermod -G disk,backup amanda
echo "Setting amanda shell to /bin/sh"
/usr/bin/chsh -s /bin/sh amanda

%pre libs
%groupadd -P %{name}-libs -g 80 amanda
%useradd -P %{name}-libs -u 80 -G disk,backup -d /var/lib/amanda -s /bin/sh -c "Amanda Backup user" -g amanda amanda

%post	libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove amanda
	%groupremove amanda
fi

%post client
/sbin/ldconfig
%service -q rc-inetd reload

%postun client
/sbin/ldconfig
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post server
/sbin/ldconfig
%service -q rc-inetd reload
if [ "$1" = "1" ]; then
	echo "Don't forget to edit /etc/cron.d/amanda-srv." 1>&2
fi

%postun server
/sbin/ldconfig
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libamanda*.so
%dir %{_libexecdir}
%attr(770,root,amanda) %dir %{_localstatedir}/amanda
%attr(600,amanda,amanda) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/amanda/.amandahosts

%if %{with server}
%files server
%defattr(644,root,root,755)
%doc docs/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amidxtape
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amandaidx

%attr(750,root,amanda) %dir %{_sysconfdir}/amanda
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,amanda) %{_sysconfdir}/amanda/*

%attr(664,root,amanda) %{_localstatedir}/amanda/*.ps

%config(noreplace) %attr(640,root,root) /etc/cron.d/amanda-srv

%attr(755,root,root) %{_libdir}/libamserver*.so
%attr(755,root,root) %{_libdir}/libamtape*.so
%attr(755,root,root) %{_libdir}/librestore*.so

%attr(755,root,root) %{_libexecdir}/amcat.awk
%attr(755,root,root) %{_libexecdir}/amcleanupdisk
%attr(755,root,root) %{_libexecdir}/amidxtaped
%attr(755,root,root) %{_libexecdir}/amindexd
%attr(755,root,root) %{_libexecdir}/amlogroll
%attr(755,root,root) %{_libexecdir}/amplot.awk
%attr(755,root,root) %{_libexecdir}/amplot.g
%attr(755,root,root) %{_libexecdir}/amplot.gp
%attr(755,root,root) %{_libexecdir}/amtrmidx
%attr(755,root,root) %{_libexecdir}/amtrmlog
%attr(755,root,root) %{_libexecdir}/chg-chio
%attr(755,root,root) %{_libexecdir}/chg-chs
%attr(755,root,root) %{_libexecdir}/chg-disk
%attr(755,root,root) %{_libexecdir}/chg-iomega
%attr(755,root,root) %{_libexecdir}/chg-juke
%attr(755,root,root) %{_libexecdir}/chg-manual
%attr(755,root,root) %{_libexecdir}/chg-mcutil
%attr(755,root,root) %{_libexecdir}/chg-mtx
%attr(755,root,root) %{_libexecdir}/chg-multi
%attr(755,root,root) %{_libexecdir}/chg-null
%attr(755,root,root) %{_libexecdir}/chg-rait
%attr(755,root,root) %{_libexecdir}/chg-rth
%attr(755,root,root) %{_libexecdir}/chg-scsi
%attr(755,root,root) %{_libexecdir}/chg-zd-mtx
%attr(755,root,root) %{_libexecdir}/chunker
%attr(755,root,root) %{_libexecdir}/driver
%attr(4754,root,amanda) %{_libexecdir}/dumper
%attr(4754,root,amanda) %{_libexecdir}/planner
%attr(755,root,root) %{_libexecdir}/taper

%attr(755,root,root) %{_sbindir}/amadmin
%attr(755,root,root) %{_sbindir}/amaespipe
%attr(4754,root,amanda) %{_sbindir}/amcheck
%attr(755,root,root) %{_sbindir}/amcheckdb
%attr(755,root,root) %{_sbindir}/amcleanup
%attr(755,root,root) %{_sbindir}/amcrypt*
%attr(755,root,root) %{_sbindir}/amdd
%attr(755,root,root) %{_sbindir}/amdump
%attr(755,root,root) %{_sbindir}/amfetchdump
%attr(755,root,root) %{_sbindir}/amflush
%attr(755,root,root) %{_sbindir}/amgetconf
%attr(755,root,root) %{_sbindir}/amlabel
%attr(755,root,root) %{_sbindir}/ammt
%attr(755,root,root) %{_sbindir}/amoverview
%attr(755,root,root) %{_sbindir}/amplot
%attr(755,root,root) %{_sbindir}/amreport
%attr(755,root,root) %{_sbindir}/amrestore
%attr(755,root,root) %{_sbindir}/amrmtape
%attr(755,root,root) %{_sbindir}/amstatus
%attr(755,root,root) %{_sbindir}/amtape
%attr(755,root,root) %{_sbindir}/amtapetype
%attr(755,root,root) %{_sbindir}/amtoc
%attr(755,root,root) %{_sbindir}/amverify
%attr(755,root,root) %{_sbindir}/amverifyrun
%{_mandir}/man5/amanda.conf.5*
%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amaespipe.8*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amcheckdb.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amcrypt*.8*
%{_mandir}/man8/amdd.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amfetchdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amgetconf.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/ammt.8*
%{_mandir}/man8/amoverview.8*
%{_mandir}/man8/amplot.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amrestore.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amstatus.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtapetype.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amverify.8*
%{_mandir}/man8/amverifyrun.8*
%endif

%if %{with client}
%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amanda
%attr(664,root,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amandates
%attr(755,root,root) %{_libdir}/libamclient*.so
%attr(755,root,root) %{_libexecdir}/amandad
%attr(755,root,root) %{_libexecdir}/noop
%attr(755,root,root) %{_libexecdir}/patch-system
%attr(755,root,root) %{_libexecdir}/sendbackup
%attr(755,root,root) %{_libexecdir}/sendsize
%attr(755,root,root) %{_libexecdir}/versionsuffix
%attr(4754,root,amanda) %{_libexecdir}/calcsize
%attr(4754,root,amanda) %{_libexecdir}/killpgrp
%attr(4754,root,amanda) %{_libexecdir}/rundump
%attr(4754,root,amanda) %{_libexecdir}/runtar
%attr(4754,root,amanda) %{_libexecdir}/selfcheck
%attr(755,root,root) %{_sbindir}/amoldrecover
%attr(755,root,root) %{_sbindir}/amrecover
%attr(770,root,amanda) %dir %{_localstatedir}/amanda/gnutar-lists
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amrecover.8*
%endif
