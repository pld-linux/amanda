#
# Conditional build:
%bcond_without	xfs	# without (possible) support for xfsdump
%bcond_without	samba	# without smbclient support
%bcond_without	client	# without client package
%bcond_without	server	# without server package

%include	/usr/lib/rpm/macros.perl
Summary:	A network-capable tape backup solution
Summary(pl.UTF-8):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	3.3.2
Release:	5
License:	BSD
Group:		Networking/Utilities
Source0:	http://downloads.sourceforge.net/amanda/%{name}-%{version}.tar.gz
# Source0-md5:	1a6cfe47eaee121f22540ac5fa58c366
Source1:	%{name}-srv.crontab
Source2:	%{name}.inetd
Source3:	%{name}idx.inetd
Source4:	amidxtape.inetd
Source5:	k5%{name}.inet
# http://amanda.svn.sourceforge.net/viewvc/amanda/amanda/branches/3_2/contrib/convert-zd-mtx-to-robot.sh
Source6:	convert-zd-mtx-to-robot.sh
Source7:	%{name}-ssh_config
# https://github.com/janekr/amlvm-snapshot
Source8:	amlvm-snapshot.conf
Source9:	amlvm-snapshot.pl
Source10:	amlvm-snapshot.README
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-chg-zd-mtx-sh.patch
Patch2:		%{name}-tar.patch
Patch3:		%{name}-common.patch
Patch4:		%{name}-as_needed.patch
Patch5:		%{name}-tapetypes.patch
Patch6:		%{name}-FHS.patch
Patch7:		%{name}-no-buildtime-ipv6.patch
Patch8:		%{name}-heimdal.patch
Patch9:		%{name}-ac.patch
Patch11:	%{name}-amstar-exclude-fix.patch
Patch12:	%{name}-krb5-auth.patch
Patch13:	%{name}-stdio.patch
Patch14:	%{name}-amstar-device.patch
URL:		http://www.amanda.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.10.0
BuildRequires:	dump
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	gnuplot
BuildRequires:	rpmbuild(macros) >= 1.654
# curl is broken, see curl-config --libs
BuildRequires:	heimdal-devel
BuildRequires:	keyutils-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
BuildRequires:	openssh-clients
BuildRequires:	openssl-devel
BuildRequires:	perl-devel >= 5.6.0
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.654
%{?with_samba:BuildRequires:	samba-client}
BuildRequires:	swig
%{?with_xfs:BuildRequires:	xfsdump}
Conflicts:	pwdutils < 3.1.2-2
Conflicts:	shadow < 1:4.0.4.1-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# for some unknown reason those get detected in R but not in P (Tie::StdHash comes from perl)
%define		_noautoreq_perl	Tie::StdHash Amanda::Recovery::Clerk::Feedback Amanda::Taper::Scribe::Feedback

%define		_ulibdir	%{_prefix}/lib

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

%package common
Summary:	Amanda common files
Summary(pl.UTF-8):	Wspólne pliki pakietu amanda
Group:		Networking/Utilities
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/chsh
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
%requires_ge	glib2
Requires:	setup >= 2.6.1-1
Provides:	group(amanda)
Provides:	user(amanda)
Obsoletes:	amanda-libs
Obsoletes:	amanda-perl

%description common
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

Amanda common files.

%description common -l pl.UTF-8
AMANDA jest sieciowo zorientowanym systemem tworzenia kopii
zapasowych. Umożliwia administratorowi sieci tworzenie kopii z kilku
hostów na jednej maszynie wyposażonej w pojemny dysk lub streamer.
Nowsze wersje programu umożliwiają zabezpieczanie zasobów Microsoft
Windows 95/98/NT/2000 przy użyciu protokołu Samba. Ten pakiet zawiera
podstawowe pliki programu i powinien być zainstalowany zarówno na
serwerze jak i na kliencie. Pamiętaj także o instalacji pakietów
amanda-client i amanda-server!

Wspólne pliki pakietu amanda.

%package client
Summary:	The client side of Amanda
Summary(pl.UTF-8):	Klient Amandy
Group:		Networking/Utilities
Requires(post):	/bin/hostname
Requires(post):	/usr/bin/ssh-keygen
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-inetd
Suggests:	gzip
Suggests:	openssh-clients
Suggests:	openssh-server
Suggests:	star
Suggests:	tar
Conflicts:	tar < 1.15

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
Requires(post):	/bin/hostname
Requires(post):	/usr/bin/ssh-keygen
Requires:	%{name}-common = %{version}-%{release}
Requires:	/etc/cron.d
Requires:	crondaemon
Requires:	gnuplot
Requires:	mt-st
Requires:	mtx
Requires:	rc-inetd
Suggests:	openssh-clients
Suggests:	openssh-server
Obsoletes:	amanda
Obsoletes:	amanda-perl-server

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
cp -a %{SOURCE10} .

%build
%{__aclocal} -I config -I config/gettext-macros -I config/gnulib -I config/amanda -I config/macro-archive
%{__autoconf}
%{__automake}
%configure \
	DUMP=/sbin/dump \
	GZIP=/bin/gzip \
	MAILER=/bin/mail \
	MT=/bin/mt \
	MTX=/usr/sbin/mtx \
	PRINT=/usr/bin/lpr \
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
	--with-fqdn \
	%{?with_samba:--with-smbclient=%{_bindir}/smbclient} \
	--with-star=%{_bindir}/star \
	--with-gnuplot=%{_bindir}/gnuplot \
	--with-bsd-security \
	--with-bsdtcp-security \
	--with-ssh-security \
	--with-krb5-security \
	--with-buffered-dump \
	--with-amandahosts \
	--with-configdir=%{_sysconfdir}/amanda \
	--with-gnutar-listdir=%{_sharedstatedir}/amanda/gnutar-lists \
	--with-amandates=%{_sharedstatedir}/amanda/amandates \
	--with-debugging=%{_sharedstatedir}/amanda/debug \
	--with-tmpdir=/var/tmp/amanda \
	--with-amperldir=%{perl_vendorarch} \
	--with-ipv6 \
	--with-readline \
	--disable-installperms

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{amanda,cron.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_sharedstatedir}/amanda/{.gnupg,.ssh,gnutar-lists} \
	$RPM_BUILD_ROOT%{_sharedstatedir}/amanda/debug/{amandad,client,server}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/amanda-srv
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE2} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amanda
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE3} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amandaidx
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE4} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/amidxtape
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE5} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/k5amanda

install example/amanda.conf $RPM_BUILD_ROOT%{_sysconfdir}/amanda
install example/amanda-client.conf $RPM_BUILD_ROOT%{_sysconfdir}/amanda
touch $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.amandahosts

install %{SOURCE6} $RPM_BUILD_ROOT%{_sbindir}/amconvert-zd-mtx-to-robot.sh

install %{SOURCE7} $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.ssh/config
touch $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.ssh/{,client_}authorized_keys
touch $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.ssh/id_rsa_amdump{,.pub}
touch $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/.ssh/id_rsa_amrecover{,.pub}

%if %{with server}
install -p %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/amanda/lvm-snapshot.conf
%endif

%if %{with client}
sed -e 's|@@PERL_VENDORARCH@@|%{perl_vendorarch}|' %{SOURCE9} >$RPM_BUILD_ROOT%{_libdir}/amanda/application/amlvm-snapshot
%endif

> $RPM_BUILD_ROOT%{_sharedstatedir}/amanda/amandates

# Amanda tools generate ssh keys with embeded commands pointing to /usr/lib
# Tools can't be "fixed" because keys generated on server are to be used on client
if [ "%{_lib}" != "lib" ] ; then
	install -d $RPM_BUILD_ROOT%{_ulibdir}
	ln -s %{_libdir}/amanda $RPM_BUILD_ROOT%{_ulibdir}/amanda
fi

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%{__rm} $RPM_BUILD_ROOT%{_datadir}/amanda/{COPYRIGHT,ChangeLog,NEWS,ReleaseNotes}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/amanda/example/{chg-multi,chg-scsi}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun common -- amanda-libs < 2.6.0p2-3
echo "Adding amanda to disk and tape groups"
/usr/sbin/usermod -G disk,tape amanda
echo "Setting amanda shell to /bin/sh"
/usr/bin/chsh -s /bin/sh amanda
if [ -f %{_sharedstatedir}/amanda/.amandahosts ]; then
	echo "Fixing permissions of %{_sharedstatedir}/amanda/.amandahosts file"
	chown amanda:amanda %{_sharedstatedir}/amanda/.amandahosts
	chmod 600 %{_sharedstatedir}/amanda/.amandahosts
fi

%triggerpostun common -- amanda-common < 3.3
%banner %{name}-common -e << EOF
In amanda 3.3 the default auth has changed to "bsdtcp",
if you are using the default "bsd" then you must add it
to your configuration:

 *   in amanda.conf
 *   in amanda-client.conf
 *   in dumptype/disklist
 *   in inetd (if no '-auth' argument to amandad)
EOF

%pre common
%groupadd -P %{name}-common -g 80 amanda
%useradd -P %{name}-common -u 80 -G disk,tape -d /var/lib/amanda -s /bin/sh -c "Amanda Backup user" -g amanda amanda

%postun common
if [ "$1" = "0" ]; then
	%userremove amanda
	%groupremove amanda
fi

%post client
%service -q rc-inetd reload
if [ ! -e /var/lib/amanda/.ssh/id_rsa_amrecover ] ; then
	HOST="`/bin/hostname`"
	FQDNHOST="`/bin/hostname -f`"
	if [ -z "$HOST" ] ; then
		COMMENT="root@client"
	else
		COMMENT="root@$HOST"
	fi
	/usr/bin/ssh-keygen -t rsa -C $COMMENT -f /var/lib/amanda/.ssh/id_rsa_amrecover -N "" || :
	chown amanda:amanda /var/lib/amanda/.ssh/id_rsa_amrecover{,.pub} || :
	chmod 600 /var/lib/amanda/.ssh/id_rsa_amrecover{,.pub} || :
	if [ -n "$FQDNHOST" ]; then
		echo -n "from=\"$FQDNHOST\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command=\"%{_ulibdir}/amanda/amandad -auth=ssh amindexd amidxtaped\" " >/var/lib/amanda/.ssh/server_authorized_keys
		cat /var/lib/amanda/.ssh/id_rsa_amrecover.pub >>/var/lib/amanda/.ssh/server_authorized_keys

		echo "Remember to copy the contents of /var/lib/amanda/.ssh/server_authorized_keys to"
		echo "/var/lib/amanda/.ssh/authorized_keys on amanda server"
	fi
fi

%postun client
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post server
%service -q rc-inetd reload
if [ ! -e /var/lib/amanda/.ssh/id_rsa_amdump ] ; then
	HOST="`/bin/hostname`"
	if [ -z "$HOST" ] ; then
		COMMENT="amanda@server"
	else
		COMMENT="amanda@$HOST"
	fi
	/usr/bin/ssh-keygen -t rsa -C $COMMENT -f /var/lib/amanda/.ssh/id_rsa_amdump -N "" || :
	chown amanda:amanda /var/lib/amanda/.ssh/id_rsa_amdump{,.pub} || :
	chmod 600 /var/lib/amanda/.ssh/id_rsa_amdump{,.pub} || :
fi
if [ "$1" = "1" ]; then
	echo "Don't forget to edit /etc/cron.d/amanda-srv." 1>&2
fi

%postun server
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%triggerpostun server -- amanda-server < 3.2.0
%banner %{name} -e << EOF
Warning: Tape changer configuration has chaged, please read
%{_docdir}/%{name}-server-%{version}/ReleaseNotes.gz
and %{_docdir}/%{name}-server-%{version}/NEWS.gz for details.
You can use %{_sbindir}/amconvert-zd-mtx-to-robot.sh script
to upgrade to chg-robot.
EOF

%files common
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT ChangeLog NEWS README ReleaseNotes UPGRADING amlvm-snapshot.README
%attr(755,root,root) %{_libdir}/amanda/libamanda*.so
%attr(755,root,root) %{_libdir}/amanda/libamar*.so
%attr(755,root,root) %{_libdir}/amanda/libamxfer*.so
%attr(755,root,root) %{_libdir}/amanda/libamglue*.so
%attr(755,root,root) %{_libdir}/amanda/libndmjob*.so
%attr(755,root,root) %{_libdir}/amanda/libndmlib*.so
%attr(755,root,root) %{_libdir}/amanda/amndmjob
%attr(755,root,root) %{_libdir}/amanda/ndmjob
%attr(750,amanda,amanda) %dir %{_sysconfdir}/amanda
%dir %{_libdir}/amanda
%if %{_lib} != "lib"
%{_ulibdir}/amanda
%endif
%{_libdir}/amanda/amanda-sh-lib.sh
%attr(755,root,root) %{_sbindir}/amaespipe
%attr(755,root,root) %{_sbindir}/amarchiver
%attr(755,root,root) %{_sbindir}/amcrypt*
%attr(755,root,root) %{_sbindir}/amgetconf
%attr(755,root,root) %{_sbindir}/amgpgcrypt
%attr(750,amanda,amanda) %dir %{_datadir}/amanda
%attr(750,amanda,amanda) %dir %{_datadir}/amanda/example
%attr(750,amanda,amanda) %dir %{_datadir}/amanda/example/label-templates
%attr(640,amanda,amanda) %{_datadir}/amanda/example/*amanda*
%attr(640,amanda,amanda) %{_datadir}/amanda/example/disklist
%attr(640,amanda,amanda) %{_datadir}/amanda/example/label-templates/*.ps
%attr(750,amanda,amanda) %dir %{_datadir}/amanda/template.d
%attr(640,amanda,amanda) %{_datadir}/amanda/template.d/*
%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda
%attr(700,amanda,amanda) %dir %{_sharedstatedir}/amanda/.ssh
%attr(700,amanda,amanda) %dir %{_sharedstatedir}/amanda/.gnupg
%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda/debug
%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda/debug/amandad
%attr(600,amanda,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/amanda/.amandahosts
%attr(600,amanda,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/amanda/.ssh/config
# Commented out so it won't get removed on uninstall
#%attr(600,amanda,amanda) %ghost %{_sharedstatedir}/amanda/.ssh/authorized_keys
%{_mandir}/man5/amanda-archive-format.5*
%{_mandir}/man7/amanda-auth.7*
%{_mandir}/man7/amanda-match.7*
%{_mandir}/man7/amanda-scripts.7*
%{_mandir}/man8/amaespipe.8*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amarchiver.8*
%{_mandir}/man8/amcrypt*.8*
%{_mandir}/man8/amgetconf.8*
%{_mandir}/man8/amgpgcrypt.8*
%{_mandir}/man8/script-email.8*

%dir %{perl_vendorarch}/Amanda
%dir %{perl_vendorarch}/Amanda/Config
%dir %{perl_vendorarch}/Amanda/IPC
%{perl_vendorarch}/Amanda/Archive.pm
%{perl_vendorarch}/Amanda/BigIntCompat.pm
%{perl_vendorarch}/Amanda/ClientService.pm
%{perl_vendorarch}/Amanda/Config.pm
%{perl_vendorarch}/Amanda/Config/FoldingHash.pm
%{perl_vendorarch}/Amanda/Constants.pm
%{perl_vendorarch}/Amanda/Debug.pm
%{perl_vendorarch}/Amanda/Feature.pm
%{perl_vendorarch}/Amanda/Header.pm
%{perl_vendorarch}/Amanda/IPC/Binary.pm
%{perl_vendorarch}/Amanda/IPC/LineProtocol.pm
%{perl_vendorarch}/Amanda/MainLoop.pm
%{perl_vendorarch}/Amanda/NDMP.pm
%{perl_vendorarch}/Amanda/Paths.pm
%{perl_vendorarch}/Amanda/Process.pm
%{perl_vendorarch}/Amanda/Script.pm
%{perl_vendorarch}/Amanda/Script_App.pm
%{perl_vendorarch}/Amanda/Tests.pm
%{perl_vendorarch}/Amanda/Util.pm
%{perl_vendorarch}/Amanda/Xfer.pm
%dir %{perl_vendorarch}/auto/Amanda
%dir %{perl_vendorarch}/auto/Amanda/Archive
%dir %{perl_vendorarch}/auto/Amanda/Config
%dir %{perl_vendorarch}/auto/Amanda/Debug
%dir %{perl_vendorarch}/auto/Amanda/Feature
%dir %{perl_vendorarch}/auto/Amanda/Header
%dir %{perl_vendorarch}/auto/Amanda/IPC
%dir %{perl_vendorarch}/auto/Amanda/IPC/Binary
%dir %{perl_vendorarch}/auto/Amanda/MainLoop
%dir %{perl_vendorarch}/auto/Amanda/NDMP
%dir %{perl_vendorarch}/auto/Amanda/Tests
%dir %{perl_vendorarch}/auto/Amanda/Util
%dir %{perl_vendorarch}/auto/Amanda/Xfer
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Archive/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Config/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Feature/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Header/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/IPC/Binary/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Debug/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/MainLoop/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/NDMP/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Tests/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Util/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Xfer/*.so

%if %{with server}
%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amidxtape
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amandaidx

%config(noreplace) %verify(not md5 mtime size) %attr(640,amanda,amanda) %{_sysconfdir}/amanda/amanda.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,amanda,amanda) %{_sysconfdir}/amanda/lvm-snapshot.conf

# Commented out so it won't get removed on uninstall
#%attr(600,amanda,amanda) %ghost %{_sharedstatedir}/amanda/.ssh/client_authorized_keys
#%attr(600,amanda,amanda) %ghost %{_sharedstatedir}/amanda/.ssh/id_rsa_amdump*

%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda/debug/server

%config(noreplace) %attr(640,root,root) /etc/cron.d/amanda-srv

%attr(755,root,root) %{_libdir}/amanda/libamdevice*.so
%attr(755,root,root) %{_libdir}/amanda/libamserver*.so

%attr(755,root,root) %{_libdir}/amanda/amcat.awk
%attr(755,root,root) %{_libdir}/amanda/amcheck-device
%attr(755,root,root) %{_libdir}/amanda/amdumpd
%attr(755,root,root) %{_libdir}/amanda/amidxtaped
%attr(755,root,root) %{_libdir}/amanda/amindexd
%attr(755,root,root) %{_libdir}/amanda/amlogroll
%attr(755,root,root) %{_libdir}/amanda/amplot.awk
%attr(755,root,root) %{_libdir}/amanda/amplot.g
%attr(755,root,root) %{_libdir}/amanda/amplot.gp
%attr(755,root,root) %{_libdir}/amanda/amtrmidx
%attr(755,root,root) %{_libdir}/amanda/amtrmlog
%attr(755,root,root) %{_libdir}/amanda/chg-disk
%attr(755,root,root) %{_libdir}/amanda/chg-lib.sh
%attr(755,root,root) %{_libdir}/amanda/chg-manual
%attr(755,root,root) %{_libdir}/amanda/chg-multi
%attr(755,root,root) %{_libdir}/amanda/chg-zd-mtx
%attr(755,root,root) %{_libdir}/amanda/chunker
%attr(755,root,root) %{_libdir}/amanda/driver
%attr(4750,root,amanda) %{_libdir}/amanda/dumper
%attr(4750,root,amanda) %{_libdir}/amanda/planner
%attr(755,root,root) %{_libdir}/amanda/taper

%attr(755,root,root) %{_sbindir}/activate-devpay
%attr(755,root,root) %{_sbindir}/amaddclient
%attr(755,root,root) %{_sbindir}/amadmin
%attr(4750,root,amanda) %{_sbindir}/amcheck
%attr(755,root,root) %{_sbindir}/amcheckdb
%attr(755,root,root) %{_sbindir}/amcheckdump
%attr(755,root,root) %{_sbindir}/amcleanup
%attr(755,root,root) %{_sbindir}/amcleanupdisk
%attr(755,root,root) %{_sbindir}/amconvert-zd-mtx-to-robot.sh
%attr(755,root,root) %{_sbindir}/amdevcheck
%attr(755,root,root) %{_sbindir}/amdump
%attr(755,root,root) %{_sbindir}/amfetchdump
%attr(755,root,root) %{_sbindir}/amflush
%attr(755,root,root) %{_sbindir}/amlabel
%attr(755,root,root) %{_sbindir}/amoverview
%attr(755,root,root) %{_sbindir}/amplot
%attr(755,root,root) %{_sbindir}/amreport
%attr(755,root,root) %{_sbindir}/amrestore
%attr(755,root,root) %{_sbindir}/amrmtape
%attr(755,root,root) %{_sbindir}/amserverconfig
%attr(755,root,root) %{_sbindir}/amservice
%attr(755,root,root) %{_sbindir}/amstatus
%attr(755,root,root) %{_sbindir}/amtape
%attr(755,root,root) %{_sbindir}/amtapetype
%attr(755,root,root) %{_sbindir}/amtoc
%attr(755,root,root) %{_sbindir}/amvault
%{_mandir}/man5/amanda.conf.5*
%{_mandir}/man5/disklist.5*
%{_mandir}/man5/tapelist.5*
%{_mandir}/man7/amanda-changers.7*
%{_mandir}/man7/amanda-compatibility.7*
%{_mandir}/man7/amanda-devices.7*
%{_mandir}/man7/amanda-interactivity.7*
%{_mandir}/man7/amanda-taperscan.7*
%{_mandir}/man8/amaddclient.8*
%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amcheckdb.8*
%{_mandir}/man8/amcheckdump.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amcleanupdisk.8*
%{_mandir}/man8/amdevcheck.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amfetchdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/amoverview.8*
%{_mandir}/man8/amplot.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amrestore.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amserverconfig.8*
%{_mandir}/man8/amservice.8*
%{_mandir}/man8/amstatus.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtapetype.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amvault.8*

%{perl_vendorarch}/Amanda/Changer.pm
%dir %{perl_vendorarch}/Amanda/Changer
%{perl_vendorarch}/Amanda/Changer/*.pm
%{perl_vendorarch}/Amanda/Cmdline.pm
%{perl_vendorarch}/Amanda/Curinfo.pm
%dir %{perl_vendorarch}/Amanda/Curinfo
%{perl_vendorarch}/Amanda/Curinfo/*.pm
%dir %{perl_vendorarch}/Amanda/DB
%{perl_vendorarch}/Amanda/DB/*.pm
%{perl_vendorarch}/Amanda/Device.pm
%{perl_vendorarch}/Amanda/Disklist.pm
%{perl_vendorarch}/Amanda/Holding.pm
%{perl_vendorarch}/Amanda/Interactivity.pm
%dir %{perl_vendorarch}/Amanda/Interactivity
%{perl_vendorarch}/Amanda/Interactivity/*.pm
%{perl_vendorarch}/Amanda/Logfile.pm
%dir %{perl_vendorarch}/Amanda/Recovery
%{perl_vendorarch}/Amanda/Recovery/*.pm
%{perl_vendorarch}/Amanda/Report.pm
%dir %{perl_vendorarch}/Amanda/Report
%{perl_vendorarch}/Amanda/Report/*.pm
%{perl_vendorarch}/Amanda/ScanInventory.pm
%{perl_vendorarch}/Amanda/Tapelist.pm
%dir %{perl_vendorarch}/Amanda/Taper
%{perl_vendorarch}/Amanda/Taper/*.pm
%dir %{perl_vendorarch}/Amanda/Taper/Scan
%{perl_vendorarch}/Amanda/Taper/Scan/*.pm
%{perl_vendorarch}/Amanda/XferServer.pm
%dir %{perl_vendorarch}/auto/Amanda/Cmdline
%dir %{perl_vendorarch}/auto/Amanda/Device
%dir %{perl_vendorarch}/auto/Amanda/Disklist
%dir %{perl_vendorarch}/auto/Amanda/Logfile
%dir %{perl_vendorarch}/auto/Amanda/Tapelist
%dir %{perl_vendorarch}/auto/Amanda/XferServer
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Cmdline/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Device/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Disklist/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Logfile/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Tapelist/*.so
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/XferServer/*.so
%endif

%if %{with client}
%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/amanda
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/k5amanda
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,amanda) %{_sysconfdir}/amanda/amanda-client.conf
# Commented out so it won't get removed on uninstall
#%attr(600,amanda,amanda) %ghost %{_sharedstatedir}/amanda/.ssh/id_rsa_amrecover*
%attr(640,amanda,amanda) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/amanda/amandates

%dir %{_libdir}/amanda/application
%attr(4750,root,amanda) %{_libdir}/amanda/application/amgtar
%attr(755,root,root) %{_libdir}/amanda/application/amlog-script
%attr(755,root,root) %{_libdir}/amanda/application/amlvm-snapshot
%attr(755,root,root) %{_libdir}/amanda/application/ampgsql
%attr(755,root,root) %{_libdir}/amanda/application/amraw
%attr(755,root,root) %{_libdir}/amanda/application/amsamba
%attr(4750,root,amanda) %{_libdir}/amanda/application/amstar
%attr(755,root,root) %{_libdir}/amanda/application/amsuntar
%attr(755,root,root) %{_libdir}/amanda/application/amzfs*
%attr(755,root,root) %{_libdir}/amanda/application/script-email

%attr(755,root,root) %{_libdir}/amanda/libamclient*.so
%attr(755,root,root) %{_libdir}/amanda/amandad
%attr(755,root,root) %{_libdir}/amanda/noop
%attr(755,root,root) %{_libdir}/amanda/patch-system
%attr(755,root,root) %{_libdir}/amanda/sendbackup
%attr(755,root,root) %{_libdir}/amanda/sendsize
%attr(755,root,root) %{_libdir}/amanda/teecount
%attr(4750,root,amanda) %{_libdir}/amanda/calcsize
%attr(4750,root,amanda) %{_libdir}/amanda/killpgrp
%attr(4750,root,amanda) %{_libdir}/amanda/rundump
%attr(4750,root,amanda) %{_libdir}/amanda/runtar
%attr(755,root,root) %{_libdir}/amanda/selfcheck
%attr(755,root,root) %{_sbindir}/amdump_client
%attr(755,root,root) %{_sbindir}/amoldrecover
%attr(755,root,root) %{_sbindir}/amrecover
%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda/gnutar-lists
%attr(750,amanda,amanda) %dir %{_sharedstatedir}/amanda/debug/client
%{_mandir}/man7/amanda-applications.7*
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amdump_client.8*
%{_mandir}/man8/amgtar.8*
%{_mandir}/man8/ampgsql.8*
%{_mandir}/man8/amrecover.8*
%{_mandir}/man8/amraw.8*
%{_mandir}/man8/amsamba.8*
%{_mandir}/man8/amstar.8*
%{_mandir}/man8/amsuntar.8*
%{_mandir}/man8/amzfs*.8*

%{perl_vendorarch}/Amanda/Application.pm
%dir %{perl_vendorarch}/Amanda/Application
%{perl_vendorarch}/Amanda/Application/Zfs.pm
%dir %{perl_vendorarch}/auto/Amanda/Application
%attr(755,root,root) %{perl_vendorarch}/auto/Amanda/Application/*.so
%endif
