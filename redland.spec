%define major   0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		redland
Version:	1.0.13
Release:	6
License:	LGPLv2.1+ ASL 2.0
Summary:	Redland RDF Application Framework
Group:		Development/Other
Source0:	http://librdf.org/dist/source/%{name}-%{version}.tar.gz
URL:		http://librdf.org/
BuildRequires:	db5-devel
BuildConflicts:	db1-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite3-devel
BuildRequires:	rasqal-devel >= 0.9.22
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
Requires:	%{libname} >= %{version}
%rename		%{name}-devel
Obsoletes:	%{mklibname -d %{name} 0}

%description -n	%{develname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
sh ./autogen.sh

%build
%configure2_5x	--disable-static \
		--without-included-ltdl \
    		--with-mysql \
    		--with-postgresql \
    		--enable-gtk-doc

%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/%{name}/*.la

%multiarch_binaries %{buildroot}%{_bindir}/redland-config

%files
%doc AUTHORS ChangeLog README NEWS
%doc *.html
%{_bindir}/redland-db-upgrade
%{_bindir}/rdfproc
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_datadir}/%name
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%{_libdir}/librdf.so.%{major}*

%files -n %{develname}
%multiarch %{multiarch_bindir}/redland-config
%{_bindir}/redland-config
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/redland.h
%{_includedir}/librdf.h
%{_includedir}/rdf_*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/*/*
