%define dir /usr/libexec/argo/probes/archiver

Name:          argo-probe-archiver
Summary:       Probe for checking freshness of ams-consumer data
Version:       0.1.1
Release:       1%{?dist}
License:       ASL 2.0
Source0:       %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Group:         Network/Monitoring
BuildArch:     noarch
BuildRequires: python3-devel

%description
This package includes probe that check ams-consumer component.

%prep
%setup -q

%build
%{py3_build}

%install
%{py3_install "--record=INSTALLED_FILES" }

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%{python3_sitelib}/argo_probe_archiver
%{dir}


%changelog
* Wed Mar 6 2024 Daniel Vrcic <daniel.vrcic@gmail.com> - 0.1.0-1%{?dist}
- initial spec
