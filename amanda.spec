Summary:	A network-capable tape backup solution
Name:		amanda
Version:	2.4.1p1
Release:	3
Source:		ftp://ftp.amanda.org/pub/amanda/%{name}-%{version}.tar.gz
Copyright:	distributable
Group:		Networking/Utilities 
Group(pl):	Sieciowe/Narzêdzia
URL:		http://www.amanda.org/
BuildRoot: 	/tmp/%{name}-%{version}-root

%description 
A network-capable tape backup solution.

%package client
Summary:	The client side of Amanda
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia

%description client
This package should be installed on machines that are to be backed
up by Amanda.  (Including, the server if it should be backed up.)

%package server
Summary:	The server side of Amanda
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Requires:	gnuplot

%description server
This package should be installed on the machine that has the device
(such as a tape drive) where backups will be written.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target} \
	--prefix=/usr \
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
	sysconfdir=$RPM_BUILD_ROOT/etc \
	libexecdir=$RPM_BUILD_ROOT/usr/sbin \
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
%{_libdir}/libamanda*
%{_libdir}/libamtape*
%{_libdir}/amanda/amidxtaped
%attr(755,root,root) /usr/sbin/amrestore
%{_mandir}/man8/amrestore.8*

%files server
%{_libdir}/libamserver*
/usr/sbin/amindexd
/usr/sbin/amtrmidx
/usr/sbin/driver
/usr/sbin/dumper
/usr/sbin/getconf
/usr/sbin/planner
#/usr/sbin/reporter
/usr/sbin/taper
/usr/sbin/chg-chio
/usr/sbin/chg-manual
/usr/sbin/chg-multi
/usr/sbin/chg-mtx
/usr/sbin/chg-rth
/usr/sbin/chg-chs
/usr/sbin/amcat.awk
/usr/sbin/amplot.awk
/usr/sbin/amplot.g
/usr/sbin/amplot.gp
/usr/sbin/amadmin
/usr/sbin/amcheck
/usr/sbin/amflush
/usr/sbin/amlabel
/usr/sbin/amtape
/usr/sbin/amcheckdb
/usr/sbin/amcleanup
/usr/sbin/amdump
/usr/sbin/amoverview
/usr/sbin/amrmtape
/usr/sbin/amtoc
/usr/sbin/amverify
/usr/sbin/amplot
/usr/sbin/amreport
/usr/sbin/amstatus
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
/usr/sbin/versionsuffix
/usr/sbin/amandad
/usr/sbin/calcsize
/usr/sbin/rundump
/usr/sbin/runtar
/usr/sbin/selfcheck
/usr/sbin/sendbackup
/usr/sbin/sendsize
/usr/sbin/patch-system
/usr/sbin/killpgrp
/usr/sbin/amrecover
%{_mandir}/man8/amrecover.8*

%changelog
* Sat Jan 30 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.4.1-2d]
- added -q %setup parameter,
- added gzipping man pages,
- added Group(pl),
- added LDFLAGS="-s" to ./configure enviroment,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- added stripping shared libraries,
- added %attr and %defattr macros in %files (allows build package from
  non-root account).

* Tue Oct 27 1998 Cristian Gafton <gafton@redhat.com>
- version 2.4.1

* Tue May 19 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to full 2.4.0 release

* Thu Feb 19 1998 Otto Hammersmith <otto@redhat.com>
- fixed group for -client and -server packages (Network->Networking)

* Wed Feb 11 1998 Otto Hammersmith <otto@redhat.com>
- updated to 2.4.0b6, fixes security hole among other things
  (as well as finally got the glibc patch in the main source.)
 
* Tue Jan 27 1998 Otto Hammersmith <otto@redhat.com>
- moved versionsuffix to client package to remove dependency of amanda on amanda-client

* Mon Jan 26 1998 Otto Hammersmith <otto@redhat.com>
- fixed libexec garbage.

* Wed Jan 21 1998 Otto Hammersmith <otto@redhat.com>
- split into three packages amanda, amanda-client, and amanda-server

* Fri Jan  9 1998 Otto Hammersmith <otto@redhat.com>
- updated to latest beta... builds much cleaner now.

* Thu Jan  8 1998 Otto Hammersmith <otto@redhat.com>
- created the package
