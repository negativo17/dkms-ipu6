%global commit0 c6f2924c47e68837404cc7c09f0d75bc2581b87e
%global date 20241012
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global debug_package %{nil}
%global dkms_name ipu6

Name:       dkms-%{dkms_name}
Version:    0
Release:    5.%{date}git%{shortcommit0}%{?dist}
Summary:    Kernel drivers for the IPU 6 and sensors
License:    GPLv3
URL:        https://github.com/intel/ipu6-drivers
BuildArch:  noarch

Source0:    %{url}/archive/%{commit0}.tar.gz#/ipu6-drivers-%{shortcommit0}.tar.gz
Source1:    dkms-no-weak-modules.conf
Patch0:     %{name}-conf.patch

Provides:   %{dkms_name}-kmod = %{version}
Requires:   %{dkms_name}-kmod-common = %{version}
Requires:   dkms

%description
Kernel drivers for the IPU 6 and sensors. It supports MIPI cameras through the
IPU6 on Intel Tiger Lake, Alder Lake, Raptor Lake and Meteor Lake platforms.

%prep
%autosetup -p1 -n ipu6-drivers-%{commit0}

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Sun Oct 27 2024 Simone Caronni <negativo17@gmail.com> - 0-5.20241012gitc6f2924
- Update to latest Intel snapshot.

* Tue Jun 18 2024 Simone Caronni <negativo17@gmail.com> - 0-4.20240618gitbef7b04
- Switch to jwrdegoede's fork for contributions.

* Wed Jun 05 2024 Simone Caronni <negativo17@gmail.com> - 0-3.20240605git404740a
- Update to latest snapshot.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0-2.20240509git6fcc4c5
- Patch 0 merged upstream.

* Mon May 06 2024 Simone Caronni <negativo17@gmail.com> - 0-1.20240418git71e0c69
- First build.
