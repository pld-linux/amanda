Summary:	A network-capable tape backup solution
Name:		amanda
Version:	2.4.1
Release:	2d
Source:		ftp://ftp.amanda.org/pub/amanda/%{name}-%{version}.tar.gz
Copyright:	distributable
Group:		Networking/Utilities 
Group(pl):	Sieciowe/Narz�dzia
URL:		http://www.amanda.org/
BuildRoot: 	/tmp/%{name}-%{version}-root

%description 
A network-capable tape backup solution.

%package client
Summary:	The client side of Amanda
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narz�dzia

%description client
This package should be installed on machines that are to be backed
up by Amanda.  (Including, the server if it should be backed up.)

%package server
Summary:	The server side of Amanda
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narz�dzia
Requires:	gnuplot

%description server
This package should be installed on the machine that has the device
(such as a tape drive) where backups will be written.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=/usr \
	--sysconfdir=/etc \
	--libexecdir=\${exec_prefix}/lib/amanda \
	--with-index-server=localhost \
	--with-amandahosts \
	--with-user=operator \
	--with-group=disk
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_OPT_FLAGS/etc 

%clean 
rm -rf $RPM_BUILD_ROOT

%post 		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig
%post client	-p /sbin/ldconfig
%postun client	-p /sbin/ldconfig
%post server	-p /sbin/ldconfig
%postun server	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
/usr/lib/libamanda*
/usr/lib/libamtape*
/usr/lib/amanda/amidxtaped
%attr(755,root,root) /usr/sbin/amrestore
%attr(644,root, man) /usr/man/man8/amrestore.8*

%files server
/usr/lib/libamserver*
/usr/lib/amanda/amindexd
/usr/lib/amanda/amtrmidx
/usr/lib/amanda/driver
/usr/lib/amanda/dumper
/usr/lib/amanda/getconf
/usr/lib/amanda/planner
#/usr/lib/amanda/reporter
/usr/lib/amanda/taper
/usr/lib/amanda/chg-chio
/usr/lib/amanda/chg-manual
/usr/lib/amanda/chg-multi
/usr/lib/amanda/chg-mtx
/usr/lib/amanda/chg-rth
/usr/lib/amanda/chg-chs
/usr/lib/amanda/amcat.awk
/usr/lib/amanda/amplot.awk
/usr/lib/amanda/amplot.g
/usr/lib/amanda/amplot.gp
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
%attr(644,root, man) /usr/man/man8/amadmin.8*
%attr(644,root, man) /usr/man/man8/amrmtape.8*
%attr(644,root, man) /usr/man/man8/amtape.8*
%attr(644,root, man) /usr/man/man8/amtoc.8*
%attr(644,root, man) /usr/man/man8/amanda.8*
%attr(644,root, man) /usr/man/man8/amcheck.8*
%attr(644,root, man) /usr/man/man8/amcleanup.8*
%attr(644,root, man) /usr/man/man8/amdump.8*
%attr(644,root, man) /usr/man/man8/amflush.8*
%attr(644,root, man) /usr/man/man8/amlabel.8*
%attr(644,root, man) /usr/man/man8/amplot.8*
%attr(644,root, man) /usr/man/man8/amreport.8*
%attr(644,root, man) /usr/man/man8/amstatus.8*

%files client
/usr/lib/libamclient*
/usr/lib/amanda/versionsuffix
/usr/lib/amanda/amandad
/usr/lib/amanda/calcsize
/usr/lib/amanda/rundump
/usr/lib/amanda/runtar
/usr/lib/amanda/selfcheck
/usr/lib/amanda/sendbackup
/usr/lib/amanda/sendsize
/usr/lib/amanda/patch-system
/usr/lib/amanda/killpgrp
/usr/sbin/amrecover
%attr(644,root, man) /usr/man/man8/amrecover.8*

%changelog
* Sat Jan 30 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
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
