Summary:	A network-capable tape backup solution
Summary(pl):	Sieciowo zorientowany system tworzenia kopii zapasowych
Name:		amanda
Version:	2.4.1
Release:	1
Source:		ftp://ftp.amanda.org/pub/amanda/%{name}-%{version}.tar.gz
Copyright:	distributable
Group:		Networking/Utilities 
Group(pl):	Sieciowe/Narzêdzia
URL:		http://www.amanda.org/
BuildRoot:	/tmp/%{name}-%{version}-root

%description 
A network-capable tape backup solution.

%description -l pl
Sieciowo zorientowany system tworzenia kopii zapasowych

%package client
Summary:	The client side of Amanda
Summary(pl):	Klient Amandy
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia

%description client
This package should be installed on machines that are to be backed
up by Amanda.  (Including, the server if it should be backed up.)

%description -l pl client
Ten pakiet powinien byæ zainstalowany ma maszynach, z których
zawarto¶ci bêd± tworzone kopie zapasowe.


%package server
Summary:	The server side of Amanda
Summary(pl):	Serwer Amandy
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Requires:	gnuplot

%description server
This package should be installed on the machine that has the device
(such as a tape drive) where backups will be written.

%description -l pl server
Ten pakiet powinien byæ zainstalowanych na maszynach, na których
bêd± magazynowane kopie zapasowe (lub do których podpiête s±
urz±dzenia typu streamer).

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=/usr \
	--mandir=%{_mandir} \
	--sysconfdir=/etc \
	--localstatedir=/var \
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
        --with-debugging=/var/amanda/debug

make

%install
rm -rf $RPM_BUILD_ROOT
make install \
	prefix=$RPM_BUILD_ROOT/usr \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	sysconfdir=$RPM_BUILD_ROOT/etc \
	libexecdir=$RPM_BUILD_ROOT%{_sbindir} \
	SETUID_GROUP=`id -g`

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%post 		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig
%post   client	-p /sbin/ldconfig
%postun client	-p /sbin/ldconfig
%post   server	-p /sbin/ldconfig
%postun server	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_sbindir}/amidxtaped
%{_libdir}/libamanda*
%{_libdir}/libamtape*
%attr(755,root,root) %{_sbindir}/amrestore
%{_mandir}/man8/amrestore.8*

%files server
%{_libdir}/libamserver*
%{_sbindir}/amindexd
%{_sbindir}/amtrmidx
%{_sbindir}/driver
%{_sbindir}/dumper
%{_sbindir}/getconf
%{_sbindir}/planner
#%{_sbindir}/reporter
%{_sbindir}/taper
%{_sbindir}/chg-chio
%{_sbindir}/chg-manual
%{_sbindir}/chg-multi
%{_sbindir}/chg-mtx
%{_sbindir}/chg-rth
%{_sbindir}/chg-chs
#%{_sbindir}/amcat.awk
#%{_sbindir}/amplot.awk
#%{_sbindir}/amplot.g
#%{_sbindir}/amplot.gp
%{_sbindir}/amadmin
%{_sbindir}/amcheck
%{_sbindir}/amflush
%{_sbindir}/amlabel
%{_sbindir}/amtape
%{_sbindir}/amcheckdb
%{_sbindir}/amcleanup
%{_sbindir}/amdump
%{_sbindir}/amoverview
%{_sbindir}/amrmtape
%{_sbindir}/amtoc
%{_sbindir}/amverify
#%{_sbindir}/amplot
%{_sbindir}/amreport
%{_sbindir}/amstatus
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
%{_libdir}/libamclient*
%{_sbindir}/versionsuffix
%{_sbindir}/amandad
%{_sbindir}/calcsize
%{_sbindir}/rundump
%{_sbindir}/runtar
%{_sbindir}/selfcheck
%{_sbindir}/sendbackup
%{_sbindir}/sendsize
%{_sbindir}/patch-system
%{_sbindir}/killpgrp
%{_sbindir}/amrecover
%{_mandir}/man8/amrecover.8*
