%define name    redland
%define version 1.0.9
%define release %mkrel 1

%define major	0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary:   	Redland RDF Application Framework
Name:      	%{name}
Version:   	%{version}
Release:   	%{release}
License: 	LGPL
Group:     	Development/Other
Source:    	http://librdf.org/dist/source/%{name}-%{version}.tar.gz
URL:       	http://www.redland.opensource.ac.uk/
BuildRequires: 	libxml2-devel db-devel
BuildRequires:	w3c-libwww-devel swig mysql-devel
BuildRequires:	rasqal-devel >= 0.9.16
BuildRequires:	raptor-devel
Requires:  	rasqal raptor
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Redland is a library that provides a high-level interface for RDF
(Resource Description Framework) implemented in an object-based API.
It is modular and supports different RDF/XML parsers, storage
mechanisms and other elements. Redland is designed for applications
developers to provide RDF support in their applications as well as
for RDF developers to experiment with the technology.

%package -n %{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n %{develname}
Summary: Header files and static libraries from %name
Group: Development/Other
Requires: %{libname} >= %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release} 
Obsoletes: %name-devel
Obsoletes: %{mklibname -d %name 0}

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x --with-mysql --with-raptor=system --with-rasqal=system
%make

%install
rm -rf %{buildroot}
# fix install command
perl -p -i -e 's/install\ -c/install\ -D/g' `find -name Makefile`
%makeinstall_std
#cp -f librdf/*.h %{buildroot}/%_includedir/

# don't include files from raptor or rasqal
cd %{buildroot}
rm -f `find -name '*rapper*'` `find -name '*raptor*'` `find -name 'ntriples.h'`
rm -f `find -name '*rasqal*'` `find -name 'roqet'`

# shouldn't be needing this?
rm -rf `find -name '*win32*'`

%multiarch_binaries %{buildroot}%{_bindir}/redland-config

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.LIB ChangeLog
%doc README NEWS LICENSE.txt
%doc *.html
%_bindir/redland-db-upgrade
%_bindir/rdfproc
%_datadir/%name
%_mandir/man1/*
%_mandir/man3/*

%files -n %libname
%defattr(-,root,root)
%_libdir/librdf.so.%{major}*

%files -n %develname
%defattr(-, root, root)
%multiarch %{multiarch_bindir}/redland-config
%_bindir/redland-config
%_libdir/*.a
%_libdir/*.la
%_libdir/*.so
%_libdir/%{name}/*.a
%_libdir/%{name}/*.la
%_libdir/%{name}/*.so
%_includedir/redland.h
%_includedir/librdf.h 
%_includedir/rdf_*.h
%_libdir/pkgconfig/*.pc
%_datadir/gtk-doc/*/*

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif
