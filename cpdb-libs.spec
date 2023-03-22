#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Frontend/Backend Communication Libraries for the Common Print Dialog Backends
Summary(pl.UTF-8):	Biblioteki komunikacji frontendu/backendu dla CPDB (wspólnych okien dialogowych drukowania)
Name:		cpdb-libs
Version:	1.2.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/OpenPrinting/cpdb-libs/releases
Source0:	https://github.com/OpenPrinting/cpdb-libs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2df7396b3c6ce05a0c001324d82396de
Patch0:		%{name}-link.patch
URL:		https://github.com/OpenPrinting/cpdb-libs
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
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
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/print-backends,%{_datadir}/print-backends}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcpdb-*.la

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_libdir}/libcpdb-libs-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcpdb-libs-common.so.1
%attr(755,root,root) %{_libdir}/libcpdb-libs-frontend.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcpdb-libs-frontend.so.1
%dir %{_libdir}/print-backends
%dir %{_datadir}/print-backends

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpdb-libs-common.so
%attr(755,root,root) %{_libdir}/libcpdb-libs-frontend.so
%{_includedir}/cpd-interface-headers
%{_includedir}/cpdb-libs-backend.h
%{_includedir}/cpdb-libs-frontend.h
%{_pkgconfigdir}/cpdb-libs-backend.pc
%{_pkgconfigdir}/cpdb-libs-common.pc
%{_pkgconfigdir}/cpdb-libs-frontend.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcpdb-libs-common.a
%{_libdir}/libcpdb-libs-frontend.a
%endif
