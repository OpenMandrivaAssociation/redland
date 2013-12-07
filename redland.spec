%define major   0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		redland
Version:	1.0.16
Release:	3
License:	LGPLv2.1+ ASL 2.0
Summary:	RDF Application Framework
Group:		Development/Other
Source0:	http://download.librdf.org/source/%{name}-%{version}.tar.gz
URL:		http://librdf.org/
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(raptor2)
BuildRequires:	pkgconfig(rasqal)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	db-devel >= 5.2
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	gmp-devel
Conflicts:	%{develname} < 1.0.13
Requires:	rasqal
Requires:	raptor2

%description
Redland is a library that provides a high-level interface for RDF
(Resource Description Framework) implemented in an object-based API.
It is modular and supports different RDF/XML parsers, storage
mechanisms and other elements. Redland is designed for applications
developers to provide RDF support in their applications as well as
for RDF developers to experiment with the technology.

%package -n	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n	%{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
%rename		%{name}-devel
Obsoletes:	%{mklibname -d %{name} 0} < 1.0.15

%description -n	%{develname}
Libraries and includes files for developing programs based on %{name}.

%track
prog %name = {
	url = http://librdf.org/
	regex = %name-(__VER__)\.tar\.gz
	version = %version
}

%prep
%setup -q
# hack to nuke rpaths
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
./autogen.sh
%configure2_5x	--disable-static \
		--without-included-ltdl \
    		--with-mysql \
    		--with-postgresql \
    		--enable-gtk-doc

%make

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/redland-config

%files
%doc AUTHORS ChangeLog README NEWS
%doc *.html
%{_bindir}/redland-db-upgrade
%{_bindir}/rdfproc
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%{_libdir}/librdf.so.%{major}*

%files -n %{develname}
%{multiarch_bindir}/redland-config
%{_bindir}/redland-config
%{_libdir}/*.so
%{_includedir}/redland.h
%{_includedir}/librdf.h
%{_includedir}/rdf_*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/*/*



%changelog
* Sun Mar 04 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.0.15-1
+ Revision: 782084
- Update to 1.0.15
- Build to pick up db-5.2 -> db-5.3 update

* Sat Nov 26 2011 Zé <ze@mandriva.org> 1.0.14-3
+ Revision: 733582
- readd rename (seams im needing glasses...)

* Sat Nov 26 2011 Zé <ze@mandriva.org> 1.0.14-2
+ Revision: 733573
- set gtk-doc pkg

* Sat Nov 26 2011 Zé <ze@mandriva.org> 1.0.14-1
+ Revision: 733571
- remove rename thats done by default
- add missing buildrequire for glib2
- clean build conflict since iurt doesnt need it
- 1.0.14
- build with latest db and a specific db
- hack rpaths
- clean .la files

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.13-7
+ Revision: 661749
- multiarch fixes

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.13-6
+ Revision: 649256
- add buildconflicts on db1-devel
- drop 'lib%%{name}-devel' provides to make NEVR unique
- use %%rename macro
- correctify license and drop including the docs for those
- drop redundant, default %%defattr's
- run autogen.sh in %%prep rather than %%build
- cosmetics
- drop buildroot, %%clean, %%mkrel etc. now deprecated with rpm5
- drop ancient ldconfig scriptlets

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.13-5
+ Revision: 645757
- relink against libmysqlclient.so.18

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 1.0.13-4
+ Revision: 640216
- rebuild to obsolete old packages

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - build against db 5.x (db 5.1 currently..)

* Sat Feb 12 2011 Frank Kober <emuse@mandriva.org> 1.0.13-3
+ Revision: 637389
- fix devel conflicts making devel install impossible

* Wed Feb 09 2011 Funda Wang <fwang@mandriva.org> 1.0.13-2
+ Revision: 636988
- fix requires

* Wed Feb 09 2011 Funda Wang <fwang@mandriva.org> 1.0.13-1
+ Revision: 636987
- new version 1.0.13

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.12-5mdv2011.0
+ Revision: 627008
- rebuilt against mysql-5.5.8 libs, again

* Mon Dec 27 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.12-4mdv2011.0
+ Revision: 625429
- rebuilt against mysql-5.5.8 libs

* Sun Oct 17 2010 Frank Kober <emuse@mandriva.org> 1.0.12-3mdv2011.0
+ Revision: 586370
- fix rasqal.h location

* Sun Oct 17 2010 Frank Kober <emuse@mandriva.org> 1.0.12-2mdv2011.0
+ Revision: 586307
+ rebuild (emptylog)

* Sun Oct 17 2010 Frank Kober <emuse@mandriva.org> 1.0.12-1mdv2011.0
+ Revision: 586263
- new version 1.0.12 fixing rasqal_world declaration in rdf_init.h

* Sun Sep 26 2010 Funda Wang <fwang@mandriva.org> 1.0.11-1mdv2011.0
+ Revision: 581082
- update to new version 1.0.11

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.10-2mdv2010.1
+ Revision: 507042
- rebuild

* Fri Jan 01 2010 Emmanuel Andry <eandry@mandriva.org> 1.0.10-1mdv2010.1
+ Revision: 484728
- New version 1.0.10
- drop patches (applied upstream)
- fix URL

* Wed Dec 30 2009 Funda Wang <fwang@mandriva.org> 1.0.9-7mdv2010.1
+ Revision: 484132
- rebuild for db4.8

* Wed Nov 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-5mdv2010.1
+ Revision: 467227
- fix deps
- link against system libltdl.so.7

* Mon Aug 31 2009 Helio Chissini de Castro <helio@mandriva.com> 1.0.9-4mdv2010.0
+ Revision: 423010
- Fix mess of link when modules are dynamically parsed

* Mon Aug 17 2009 Helio Chissini de Castro <helio@mandriva.com> 1.0.9-3mdv2010.0
+ Revision: 417261
- Rebuild to fix mysql missing symbol

* Sun Aug 02 2009 Funda Wang <fwang@mandriva.org> 1.0.9-2mdv2010.0
+ Revision: 407508
- there is no more file conflcits

* Wed Jul 29 2009 Emmanuel Andry <eandry@mandriva.org> 1.0.9-1mdv2010.0
+ Revision: 404097
- New version 1.0.9
- update files list

  + Oden Eriksson <oeriksson@mandriva.com>
    - use lowercase mysql-devel

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-3mdv2009.1
+ Revision: 311206
- rebuilt against mysql-5.1.30 libs

* Thu Jul 10 2008 Funda Wang <fwang@mandriva.org> 1.0.8-2mdv2009.0
+ Revision: 233254
- New devel package policy

* Thu Jul 10 2008 Funda Wang <fwang@mandriva.org> 1.0.8-1mdv2009.0
+ Revision: 233243
- Bump BR version

  + Austin Acton <austin@mandriva.org>
    - new version

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.0.7-2mdv2009.0
+ Revision: 225315
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 28 2007 Austin Acton <austin@mandriva.org> 1.0.7-1mdv2008.1
+ Revision: 138743
- new version
- fix buildrequires

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu May 10 2007 Austin Acton <austin@mandriva.org> 1.0.6-1mdv2008.0
+ Revision: 26055
- new version


* Wed Jan 03 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-2mdv2007.0
+ Revision: 103794
- Import redland

* Wed Jan 03 2007 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.4-2mdv2007.1
- rebuild for new ncurses
- fix file list

* Wed May 10 2006 Lenny Cartier <lenny@mandriva.com> 1.0.4-1mdk
- 1.0.4

* Wed Feb 22 2006 Austin Acton <austin@mandriva.org> 1.0.3-1mdk
- New release 1.0.3

* Wed Nov 30 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.0.2-3mdk
- rebuild against openssl-0.9.8

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdk
- rebuilt against MySQL-5.0.15

* Fri Aug 26 2005 Austin Acton <austin@mandriva.org> 1.0.2-1mdk
- New release 1.0.2

* Fri Jun 10 2005 Austin Acton <austin@mandriva.org> 1.0.1-1mdk
- New release 1.0.1

* Sat Apr 30 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.0-2mdk
- rebuild for new sqlite
- add multiarch support

* Sun Feb 06 2005 Austin Acton <austin@mandrake.org> 1.0.0-1mdk
- 1.0.0
- fix requires

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.19-3mdk
- rebuilt against MySQL-4.1.x system libs

* Sat Jan 22 2005 Stefan van der Eijk <stefan@mandrake.org> 0.9.19-2mdk
- rebuild

* Mon Nov 08 2004 Austin Acton <austin@mandrake.org> 0.9.19-1mdk
- 0.9.19
- move bindings to separate SRPM

* Sat Jul 03 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.9.16-3mdk
- Rebuild for new curl

* Fri Jun 11 2004 Austin Acton <austin@mandrake.org> 0.9.16-2mdk
- bring back libtoolize
- configure 2.5
- add missing headers
- remove dependencies on libname

* Thu May 20 2004 Austin Acton <austin@mandrake.org> 0.9.16-1mdk
- 0.9.16

* Mon Feb 02 2004 Austin Acton <austin@mandrake.org> 0.9.15-1mdk
- 0.9.15
- libtoolize
- enable mysql
- buildrequires php-devel

