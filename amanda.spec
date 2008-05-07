#
# Conditional build:
%bcond_without	xfs	# without (possible) support for xfsdump
%bcond_without	samba	# without smbclient support
%bcond_without	client	# without client package
%bcond_without	server	# without server package
#
Summary:	A network-capable tape backup solution
Summary(pl.UTF-8):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	2.6.0
Release:	0.1
License:	BSD
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/amanda/%{name}-%{version}.tar.gz
# Source0-md5:	c347c1e573c33018f234750ac6435156
Source1:	%{name}-srv.crontab
Source2:	%{name}.inetd
Source3:	%{name}idx.inetd
Source4:	amidxtape.inetd
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-chg-zd-mtx-sh.patch
Patch2:		%{name}-tar.patch
Patch3:		%{name}-bashizm.patch
Patch4:		%{name}-as_needed.patch
URL:		http://www.amanda.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	dump
BuildRequires:	flex
BuildRequires:	glib2-devel
# curl is broken, see curl-config --libs
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel >= 1.6-4
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
BuildRequires:	openssh-clients
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_samba:BuildRequires:	samba-client}
BuildRequires:	swig
%{?with_xfs:BuildRequires:	xfsdump}
Conflicts:	shadow < 1:4.0.4.1-4
Conflicts:	pwdutils < 3.1.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
AMANDA jest sieciowo zorientowanym systemem tworzenia kopii
zapasowych. Umożliwia administratorowi sieci tworzenie kopii z kilku
hostów na jednej maszynie wyposażonej w pojemny dysk lub streamer.
Nowsze wersje programu umożliwiają zabezpieczanie zasobów Microsoft
Windows 95/98/NT/2000 przy użyciu protokołu Samba. Ten pakiet zawiera
podstawowe pliki programu i powinien być zainstalowany zarówno na
serwerze jak i na kliencie. Pamiętaj także o instalacji pakietów
amanda-client i amanda-server!

%package libs
Summary:	Amanda shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone pakietu amanda
Group:		Networking/Utilities
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

%description libs -l pl.UTF-8
Biblioteki współdzielone pakietu amanda.

%package client
Summary:	The client side of Amanda
Summary(pl.UTF-8):	Klient Amandy
Group:		Networking/Utilities
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-inetd
Conflicts:	tar < 1.13

%description client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up). You will also need to install the amanda package to each
AMANDA client. It requires at least one of dump and GNU tar installed.

%description client -l pl.UTF-8
Ten pakiet powinien być zainstalowany ma maszynach, z których
zawartości będą tworzone kopie zapasowe. Wymaga zainstalowanego co
najmniej jednego z pakietów dump i GNU tar.

%package server
Summary:	The server side of Amanda
Summary(pl.UTF-8):	Serwer Amandy
Group:		Networking/Utilities
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

%description server -l pl.UTF-8
Ten pakiet powinien być zainstalowany na maszynach, na których będą
magazynowane kopie zapasowe (lub do których podpięte są urządzenia
typu streamer).

%package perl
Summary:	Perl stuff
Summary(pl.UTF-8):	Serwer Amandy
Group:		Networking/Utilities
Requires:	%{name}-libs = %{version}-%{release}

%description perl

%description perl -l pl.UTF-8

%package perl-server
Summary:	Perl stuff
Summary(pl.UTF-8):	Serwer Amandy
Group:		Networking/Utilities
Requires:	%{name}-perl = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}

%description perl-server

%description perl-server -l pl.UTF-8

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal} -I config -I config/gettext-macros -I config/gnulib -I config/amanda -I config/macro-archive
%{__autoconf}
%{__automake}
%configure \
	MT=/bin/mt \
	MTX=/usr/sbin/mtx \
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
	%{?with_samba:--with-smbclient=%{_bindir}/smbclient} \
	--with-bsd-security \
	--with-ssh-security \
	--with-krb5-security \
	--without-krb4-security \
	--with-buffered-dump \
	--with-amandahosts \
	--with-gnutar-listdir=%{_sharedstatedir}/gnutar-lists \
	--with-amandates=%{_sharedstatedir}/amanda/amandates \
	--with-debugging=%{_sharedstatedir}/amanda/debug \
	--with-tmpdir=/var/tmp \
	--with-amperldir=%{perl_vendorarch} \
	--disable-installperms

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{amanda,cron.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_sharedstatedir}/amanda/gnutar-lists

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/amanda-srv
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE2} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amanda
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE3} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amandaidx
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE4} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amidxtape

install example/amanda.conf $RPM_BUILD_ROOT%{_sysconfdir}/amanda
touch $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.amandahosts

> $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/amandates

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun libs -- %{name}-libs < 2.5.1p2-1
echo "Adding amanda to disk and backup groups"
/usr/sbin/usermod -G disk,backup amanda
echo "Setting amanda shell to /bin/sh"
/usr/bin/chsh -s /bin/sh amanda
if [ -f %{_sharedstatedir}/amanda/.amandahosts ]; then
	echo "Fixing permissions of %{_sharedstatedir}/amanda/.amandahosts file"
	chown amanda:amanda %{_sharedstatedir}/amanda/.amandahosts
	chmod 600 %{_sharedstatedir}/amanda/.amandahosts
fi

%pre libs
%groupadd -P %{name}-libs -g 80 amanda
%useradd -P %{name}-libs -u 80 -G disk,backup -d /var/lib/amanda -s /bin/sh -c "Amanda Backup user" -g amanda amanda

%postun libs
if [ "$1" = "0" ]; then
	%userremove amanda
	%groupremove amanda
fi

%post client
%service -q rc-inetd reload

%postun client
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post server
%service -q rc-inetd reload
if [ "$1" = "1" ]; then
	echo "Don't forget to edit /etc/cron.d/amanda-srv." 1>&2
fi

%postun server
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT ChangeLog NEWS README ReleaseNotes UPGRADING
%attr(755,root,root) %{_libdir}/amanda/libamanda*.so
%dir %{_libdir}/amanda
%attr(770,root,amanda) %dir %{_sharedstatedir}/amanda
%attr(600,amanda,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/amanda/.amandahosts

%if %{with server}
%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amidxtape
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amandaidx

%attr(750,root,amanda) %dir %{_sysconfdir}/amanda
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,amanda) %{_sysconfdir}/amanda/*

#%attr(664,root,amanda) %{_sharedstatedir}/amanda/*.ps
%{_sharedstatedir}/amanda/example
%{_sharedstatedir}/amanda/template.d

%config(noreplace) %attr(640,root,root) /etc/cron.d/amanda-srv

%dir %{_libdir}/amanda/application
%attr(755,root,root) %{_libdir}/amanda/application/amgtar
%attr(644,root,root) %{_libdir}/amanda/application/generic-dumper

%attr(755,root,root) %{_libdir}/amanda/libamdevice*.so
%attr(755,root,root) %{_libdir}/amanda/libamserver*.so
%attr(755,root,root) %{_libdir}/amanda/libamtape*.so
%attr(755,root,root) %{_libdir}/amanda/librestore*.so

%attr(755,root,root) %{_libdir}/amanda/amcat.awk
%attr(755,root,root) %{_libdir}/amanda/amcleanupdisk
%attr(755,root,root) %{_libdir}/amanda/amidxtaped
%attr(755,root,root) %{_libdir}/amanda/amindexd
%attr(755,root,root) %{_libdir}/amanda/amlogroll
%attr(755,root,root) %{_libdir}/amanda/amplot.awk
%attr(755,root,root) %{_libdir}/amanda/amplot.g
%attr(755,root,root) %{_libdir}/amanda/amplot.gp
%attr(755,root,root) %{_libdir}/amanda/amtrmidx
%attr(755,root,root) %{_libdir}/amanda/amtrmlog
%attr(755,root,root) %{_libdir}/amanda/chg-chio
%attr(755,root,root) %{_libdir}/amanda/chg-chs
%attr(755,root,root) %{_libdir}/amanda/chg-disk
%attr(755,root,root) %{_libdir}/amanda/chg-iomega
%attr(755,root,root) %{_libdir}/amanda/chg-juke
%attr(755,root,root) %{_libdir}/amanda/chg-lib.sh
%attr(755,root,root) %{_libdir}/amanda/chg-manual
%attr(755,root,root) %{_libdir}/amanda/chg-mcutil
%attr(755,root,root) %{_libdir}/amanda/chg-mtx
%attr(755,root,root) %{_libdir}/amanda/chg-multi
%attr(755,root,root) %{_libdir}/amanda/chg-null
%attr(755,root,root) %{_libdir}/amanda/chg-rait
%attr(755,root,root) %{_libdir}/amanda/chg-rth
%attr(755,root,root) %{_libdir}/amanda/chg-scsi
%attr(755,root,root) %{_libdir}/amanda/chg-zd-mtx
%attr(755,root,root) %{_libdir}/amanda/chunker
%attr(755,root,root) %{_libdir}/amanda/driver
%attr(4750,root,amanda) %{_libdir}/amanda/dumper
%attr(4750,root,amanda) %{_libdir}/amanda/planner
%attr(755,root,root) %{_libdir}/amanda/taper

%attr(755,root,root) %{_sbindir}/amadmin
%attr(755,root,root) %{_sbindir}/amaespipe
%attr(4750,root,amanda) %{_sbindir}/amcheck
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
%attr(664,root,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/amanda/amandates
%attr(755,root,root) %{_libdir}/amanda/libamclient*.so
%attr(755,root,root) %{_libdir}/amanda/amandad
%attr(755,root,root) %{_libdir}/amanda/noop
%attr(755,root,root) %{_libdir}/amanda/patch-system
%attr(755,root,root) %{_libdir}/amanda/sendbackup
%attr(755,root,root) %{_libdir}/amanda/sendsize
%attr(755,root,root) %{_libdir}/amanda/versionsuffix
%attr(4750,root,amanda) %{_libdir}/amanda/calcsize
%attr(4750,root,amanda) %{_libdir}/amanda/killpgrp
%attr(4750,root,amanda) %{_libdir}/amanda/rundump
%attr(4750,root,amanda) %{_libdir}/amanda/runtar
%attr(755,root,root) %{_libdir}/amanda/selfcheck
%attr(755,root,root) %{_sbindir}/amoldrecover
%attr(755,root,root) %{_sbindir}/amrecover
%attr(770,root,amanda) %dir %{_sharedstatedir}/amanda/gnutar-lists
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amrecover.8*
%endif

%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/amanda/libamglue*.so
%dir %{perl_vendorarch}/Amanda
%{perl_vendorarch}/Amanda/Config.pm
%{perl_vendorarch}/Amanda/Debug.pm
%{perl_vendorarch}/Amanda/Paths.pm
%{perl_vendorarch}/Amanda/Types.pm
%{perl_vendorarch}/Amanda/Util.pm
%dir %{perl_vendorarch}/auto/Amanda
%dir %{perl_vendorarch}/auto/Amanda/Config
%dir %{perl_vendorarch}/auto/Amanda/Debug
%dir %{perl_vendorarch}/auto/Amanda/Types
%dir %{perl_vendorarch}/auto/Amanda/Util
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Config/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Debug/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Types/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Util/*.so

%files perl-server
%defattr(644,root,root,755)
%{perl_vendorarch}/Amanda/Changer.pm
%{perl_vendorarch}/Amanda/Cmdline.pm
%{perl_vendorarch}/Amanda/Device.pm
%{perl_vendorarch}/Amanda/Logfile.pm
%{perl_vendorarch}/Amanda/Tapefile.pm
%dir %{perl_vendorarch}/auto/Amanda/Cmdline
%dir %{perl_vendorarch}/auto/Amanda/Device
%dir %{perl_vendorarch}/auto/Amanda/Logfile
%dir %{perl_vendorarch}/auto/Amanda/Tapefile
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Cmdline/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Device/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Logfile/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Tapefile/*.so
