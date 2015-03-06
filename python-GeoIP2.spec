#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	GeoIP2
Summary:	GeoIP2 webservice client and database reader
Name:		python-%{module}
Version:	2.1.0
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
Source0:	https://github.com/maxmind/GeoIP2-python/archive/v%{version}.tar.gz
# Source0-md5:	daa61c5cd1b3bc45e03aada0466978aa
URL:		http://geoip2.readthedocs.org/en/latest/
BuildRequires:	libmaxminddb-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_doc:BuildRequires:	sphinx-pdg}
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-httpretty >= 0.6.1
BuildRequires:	python-maxminddb
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-httpretty >= 0.6.1
BuildRequires:	python3-maxminddb
BuildRequires:	python3-modules
%endif
Requires:	python-ipaddr
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides an API for the GeoIP2 web services and
databases. The API also works with MaxMind's free GeoLite2 databases.

%package -n python3-%{module}
Summary:	GeoIP2 webservice client and database reader
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
This package provides an API for the GeoIP2 web services and
databases. The API also works with MaxMind's free GeoLite2 databases.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-python-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py_sitescriptdir}/geoip2
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/geoip2-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py3_sitescriptdir}/geoip2
%{py3_sitescriptdir}/geoip2-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
