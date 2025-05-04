#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (circular dependencies)

%define module	zope.location
Summary:	Zope location module
Summary(pl.UTF-8):	Moduł Zope location
Name:		python3-%{module}
Version:	5.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.location/zope_location-%{version}.tar.gz
# Source0-md5:	9f25225ed1cd679f5521fc83140b9537
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-devel >= 1:3.9
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
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
In Zope, "locations" are special objects that have a structural
location, indicated with __name__ and __parent__ attributes.

%description -l pl.UTF-8
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
%setup -q -n zope_location-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/location/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/location
%{py3_sitescriptdir}/zope.location-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.location-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
