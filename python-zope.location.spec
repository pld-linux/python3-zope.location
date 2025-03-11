#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (circular dependencies)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.location
Summary:	Zope location module
Summary(pl.UTF-8):	Moduł Zope location
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.3
Release:	3
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.location/zope.location-%{version}.tar.gz
# Source0-md5:	cde53eb5cb53e55aaa45c1405a4b0fea
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.component >= 4.0.1
BuildRequires:	python-zope.configuration
BuildRequires:	python-zope.copy >= 4.0
BuildRequires:	python-zope.interface >= 4.0.2
BuildRequires:	python-zope.proxy >= 4.0.1
BuildRequires:	python-zope.schema >= 4.2.2
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.component >= 4.0.1
BuildRequires:	python3-zope.configuration
BuildRequires:	python3-zope.copy >= 4.0
BuildRequires:	python3-zope.interface >= 4.0.2
BuildRequires:	python3-zope.proxy >= 4.0.1
BuildRequires:	python3-zope.schema >= 4.2.2
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
In Zope, "locations" are special objects that have a structural
location, indicated with __name__ and __parent__ attributes.

%description -l pl.UTF-8
W Zope obiekty "location" to specjalne obiekty, mające położenie
strukturalne, określane przez atrybuty __name__ i __parent__.

%package -n python3-%{module}
Summary:	Zope location module
Summary(pl.UTF-8):	Moduł Zope location
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
In Zope, "locations" are special objects that have a structural
location, indicated with __name__ and __parent__ attributes.

%description -n python3-%{module} -l pl.UTF-8
W Zope obiekty "location" to specjalne obiekty, mające położenie
strukturalne, określane przez atrybuty __name__ i __parent__.

%package apidocs
Summary:	API documentation for Python zope.location module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.location
Group:		Documentation

%description apidocs
API documentation for Python zope.location module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.location.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/location/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/location/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/zope/location
%{py_sitescriptdir}/zope.location-%{version}-py*.egg-info
%{py_sitescriptdir}/zope.location-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/location
%{py3_sitescriptdir}/zope.location-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.location-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
