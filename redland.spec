%define major   0
%define libname %mklibname rdf %{major}
%define devname %mklibname -d rdf

Summary:	RDF Application Framework
Name:		redland
Version:	1.0.17
Release:	4
License:	LGPLv2.1+ ASL 2.0
Group:		Development/Other
Url:		http://librdf.org/
Source0:	http://download.librdf.org/source/%{name}-%{version}.tar.gz
BuildRequires:	db-devel >= 6.0
BuildRequires:	gmp-devel
BuildRequires:	libtool-devel
BuildRequires:	mariadb-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(raptor2)
BuildRequires:	pkgconfig(rasqal)
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
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}redland0 < 1.0.17-1

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n	%{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}redland-devel < 1.0.17-1
Conflicts:	redland < 1.0.17-1

%description -n	%{devname}
Libraries and includes files for developing programs based on %{name}.

%track
prog %{name} = {
	url = http://librdf.org/
	regex = %{name}-(__VER__)\.tar\.gz
	version = %{version}
}

%prep
%setup -q
# hack to nuke rpaths
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

./autogen.sh

%build
%configure2_5x \
	--disable-static \
	--without-included-ltdl \
    	--with-mysql \
    	--with-postgresql \
    	--enable-gtk-doc \
	--with-bdb-dbname=db-6.0 \
	--with-bdb-lib=%{_libdir}

%make

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/redland-config

%files
%doc AUTHORS ChangeLog README NEWS
%doc *.html
%{_bindir}/rdfproc
%{_bindir}/redland-db-upgrade
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/rdfproc.1*
%{_mandir}/man1/redland-db-upgrade.1*

%files -n %{libname}
%{_libdir}/librdf.so.%{major}*

%files -n %{devname}
%{multiarch_bindir}/redland-config
%{_bindir}/redland-config
%{_includedir}/redland.h
%{_includedir}/librdf.h
%{_includedir}/rdf_*.h
%{_datadir}/gtk-doc/*/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/librdf.so
%{_mandir}/man1/redland-config.1*
%{_mandir}/man3/*

