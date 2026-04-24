#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Frontend/Backend Communication Libraries for the Common Print Dialog Backends
Summary(pl.UTF-8):	Biblioteki komunikacji frontendu/backendu dla CPDB (wspólnych okien dialogowych drukowania)
Name:		cpdb-libs
Version:	2.0
%define	subver	b8
%define	rel	1
Release:	0.%{subver}.%{rel}
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/OpenPrinting/cpdb-libs/releases
Source0:	https://github.com/OpenPrinting/cpdb-libs/archive/%{version}%{subver}/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	160cd609b921a47484f0bc7fc6942881
Patch0:		%{name}-link.patch
URL:		https://github.com/OpenPrinting/cpdb-libs
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	gettext-tools >= 0.21
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Obsoletes:	cpdb-backend-file < 2.0-0.b6
Obsoletes:	cpdb-backend-gcp < 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the frontend and backend libraries for the
Common Printing Dialog Backends (CPDB) project. These libraries allow
the CPDB frontends (the print dialogs) and backends (the modules
communicating with the different printing systems) too communicate
with each other via D-Bus.

The frontend library also provides some extra functionality to deal
with Printers, Settings, etc. in a high level manner.

%description -l pl.UTF-8
Ten pakiet zawiera biblioteki frontendu i backendu projektu CPDB
(Common Printing Dialog Backends - wspólnych backendów okien
dialogowych drukowania). Biblioteki te pozwalają na komunikację
pomiędzy frontendami CPDB (oknami dialogowymi drukowania) a backendami
(modułami komunikującymi się z różnymi systemami drukowania) poprzez
szynę D-Bus.

Biblioteka frontendu zapewnia też trochę dodatkowej funkcjonalności
do wysokopoziomowej obsługi drukarek, ustawień itp.

%package devel
Summary:	Header files for CPDB libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek CPDB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0

%description devel
Header files for CPDB libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek CPDB.

%package static
Summary:	Static CPDB libraries
Summary(pl.UTF-8):	Statyczne biblioteki CPDB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CPDB libraries.

%description static -l pl.UTF-8
Statyczne biblioteki CPDB.

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch -P0 -p1

# allow gettextize
%{__sed} -i -e 's,po/Makefile\.in,,' configure.ac

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/print-backends

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcpdb*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_bindir}/cpdb-pickle-print
%attr(755,root,root) %{_bindir}/cpdb-text-frontend
%{_libdir}/libcpdb.so.*.*.*
%ghost %{_libdir}/libcpdb.so.3
%{_libdir}/libcpdb-frontend.so.*.*.*
%ghost %{_libdir}/libcpdb-frontend.so.3
%dir %{_libdir}/print-backends

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcpdb.so
%{_libdir}/libcpdb-frontend.so
%{_includedir}/cpdb
%{_pkgconfigdir}/cpdb.pc
%{_pkgconfigdir}/cpdb-backend.pc
%{_pkgconfigdir}/cpdb-frontend.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcpdb.a
%{_libdir}/libcpdb-frontend.a
%endif
