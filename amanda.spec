Summary:	A network-capable tape backup solution
Summary(pl):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	2.4.1p1
Release:	5
Copyright:      distributable
Group:          Networking/Utilities
Group(pl):      Sieciowe/Narzêdzia
Source0:	ftp://ftp.amanda.org/pub/amanda/%{name}-%{version}.tar.gz
Source1:	amanda-srv.crontab
Source2:	amanda.inetd
Source3:	amandaidx.inetd
Source4:	amidxtape.inetd
Source5:	amanda.conf
Patch:		amanda-DESTDIR.patch
BuildRequires:	flex
BuildRequires:	dump
BuildRequires:	tar
BuildRequires:	cpio
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel >= 4.1
Prereq:		/sbin/ldconfig
URL:		http://www.amanda.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc
%define		_localstatedir	/var
%define		_libexecdir	%{_libdir}/amanda

%description 
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a backup
system that allows the administrator of a LAN to set up a single master
backup server to back up multiple hosts to a single large capacity tape
drive. AMANDA uses native dump and/or GNU tar facilities and can back up a
large number of workstations running multiple versions of Unix. Newer
versions of AMANDA (including this version) can use SAMBA to back up
Microsoft(TM) Windows95/NT hosts. The amanda package contains the core
AMANDA programs and will need to be installed on both AMANDA clients and
AMANDA servers. Note that you will have to install the amanda-client and
amanda-server packages as well.

%description -l pl
AMANDA jest sieciowo zorientowanym systemem tworzenia kopii
zapasowych. Umo¿liwia administratorowi sieci tworzenie
kopii z wilku hostów na jednej maszynie wyposa¿onej w pojemny
dysk lub streamer. Nowsze wersje programu umo¿liwiaj± zabezpieczanie
zasobów Microsoft Windows 95/98/NT/2000 przy u¿yciu protoko³u Samba.
Ten pakiet zawiera podstawowe pliki programu i powinien byæ zainstalowany
zarówno na serwerze jak i na kliencie. Pamiêtaj tak¿e o instalacji
pakietów amanda-client i amanda-server!

%package libs
Summary:	Amanda shared libraries
Summary(pl):	Biblioteki wspó³dzielone pakietu amanda
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia

%description libs
Amanda shared libraries.

%description -l pl libs
Biblioteki wspó³dzielone pakietu amanda.

%package client
Summary:	The client side of Amanda
Summary(pl):	Klient Amandy
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Prereq:		/sbin/ldconfig
Prereq:		%{name}-libs = %{version}

%description client
The Amanda-client package should be installed on any machine that will be
backed up by AMANDA (including the server if it also needs to be backed up).
You will also need to install the amanda package to each AMANDA client.

%description -l pl client
Ten pakiet powinien byæ zainstalowany ma maszynach, z których
zawarto¶ci bêd± tworzone kopie zapasowe.

%package server
Summary:	The server side of Amanda
Summary(pl):	Serwer Amandy
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Prereq:		rc-inetd
Prereq:		/sbin/ldconfig
Requires:	gnuplot
Requires:	tar
Requires:	cpio
Requires:	dump
Requires:	crondaemon
Requires:	/etc/cron.d
Prereq:		%{name}-libs = %{version}

%description server
The amanda-server package should be installed on the AMANDA server, the
machine attached to the device (such as a tape drive) where backups will be
written. You will also need to install the amanda package to the AMANDA
server. And, if the server is also to be backed up, the server also needs to
have the amanda-client package installed.

%description -l pl server
Ten pakiet powinien byæ zainstalowanych na maszynach, na których
bêd± magazynowane kopie zapasowe (lub do których podpiête s±
urz±dzenia typu streamer).

%prep
%setup -q
%patch -p1

%build
touch COPYING
automake
LDFLAGS="-s"; export LDFLAGS
%configure \
	--disable-static \
	--with-index-server=localhost \
	--with-user=amanda \
	--with-group=amanda \
	--with-samba-user=amanda \
	--with-tape-device=/dev/null \
	--with-ftape-rawdevice=/dev/null \
	--with-changer-device=/dev/null \
	--with-fqdn \
	--with-smbclient=%{_bindir}/smbclient \
	--with-bsd-security \
	--with-buffered-dump \
	--with-amandahosts \
        --with-debugging=%{_localstatedir}/amanda/debug

make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{amanda,cron.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_localstatedir}/state/amanda

make install \
	DESTDIR=$RPM_BUILD_ROOT \
	SETUID_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/amanda-srv
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amanda
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amandaidx
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amidxtape

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/amanda
install example/*.ps $RPM_BUILD_ROOT%{_localstatedir}/state/amanda

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%pre libs
/usr/sbin/groupadd -g 80 -r -f amanda
/usr/sbin/useradd -u 80 -r -d /var/state/amanda -s /bin/false -c "Amanda Backup user" -g amanda amanda

%post   libs -p /sbin/ldconfig

%preun libs
/sbin/ldconfig
if [ "$1" = "0" ]; then
	/usr/sbin/groupdel amanda
	/usr/sbin/userdel amanda
fi

%post client
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
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
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun server
/sbin/ldconfig
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libamanda*.so.*.*
%attr(755,root,root) %{_libdir}/libamtape*.so.*.*
%attr(770,root,amanda) %dir %{_libexecdir}

%files server
%defattr(644,root,root,755)
%config(noreplace) /etc/sysconfig/rc-inetd/amidxtape
%config(noreplace) /etc/sysconfig/rc-inetd/amandaidx
%attr(755,root,root) %{_libexecdir}/amidxtaped

%dir %{_sysconfdir}/amanda
%attr(640,root,amanda) %{_sysconfdir}/amanda/*

%attr(660,amanda,amanda) %dir %{_localstatedir}/state/amanda
%{_localstatedir}/state/amanda/*

%attr(640,root,root) /etc/cron.d/amanda-srv

%attr(755,root,root) %{_libdir}/libamserver*.so.*.*
%attr(755,root,root) %{_libexecdir}/amindexd
%attr(755,root,root) %{_libexecdir}/amtrmidx
%attr(755,root,root) %{_libexecdir}/driver
%attr(4754,root,amanda) %{_libexecdir}/dumper
%attr(755,root,root) %{_libexecdir}/getconf
%attr(4754,root,amanda) %{_libexecdir}/planner
%attr(755,root,root) %{_libexecdir}/taper
%attr(755,root,root) %{_libexecdir}/chg-chio
%attr(755,root,root) %{_libexecdir}/chg-manual
%attr(755,root,root) %{_libexecdir}/chg-multi
%attr(755,root,root) %{_libexecdir}/chg-mtx
%attr(755,root,root) %{_libexecdir}/chg-rth
%attr(755,root,root) %{_libexecdir}/chg-chs
%attr(755,root,root) %{_sbindir}/amadmin
%attr(755,root,root) %{_sbindir}/amcheck
%attr(755,root,root) %{_sbindir}/amflush
%attr(755,root,root) %{_sbindir}/amlabel
%attr(755,root,root) %{_sbindir}/amtape
%attr(755,root,root) %{_sbindir}/amcheckdb
%attr(755,root,root) %{_sbindir}/amcleanup
%attr(755,root,root) %{_sbindir}/amdump
%attr(755,root,root) %{_sbindir}/amoverview
%attr(755,root,root) %{_sbindir}/amrmtape
%attr(755,root,root) %{_sbindir}/amtoc
%attr(755,root,root) %{_sbindir}/amverify
#%attr(755,root,root) %{_sbindir}/amplot
%attr(755,root,root) %{_sbindir}/amreport
%attr(755,root,root) %{_sbindir}/amstatus
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

%attr(755,root,root) %{_libdir}/libamclient*.so.*.*
%attr(755,root,root) %{_libexecdir}/versionsuffix
%attr(755,root,root) %{_libexecdir}/amandad
%attr(4754,root,amanda) %{_libexecdir}/calcsize
%attr(755,root,root) %{_libexecdir}/rundump
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
