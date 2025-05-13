%global date 20250508
%global commit 1a884d5124dc149af4a645aa1493873bf796d677
%global shortcommit %{sub %{commit} 1 7}

%global debug_package %{nil}
%global dkms_name ipu6

Name:       dkms-%{dkms_name}
Version:    0.1~%{date}git%{shortcommit}
Release:    4%{?dist}
Summary:    Kernel drivers for the IPU 6 and sensors
License:    GPLv3
URL:        https://github.com/intel/ipu6-drivers
BuildArch:  noarch

Source0:    %{url}/archive/%{commit}.tar.gz#/ipu6-drivers-%{shortcommit}.tar.gz
Source2:    %{name}.conf

Provides:   %{dkms_name}-kmod = %{version}
Requires:   dkms

%description
Kernel drivers for the IPU 6 and sensors. It supports MIPI cameras through the
IPU6 on Intel platforms.

%prep
%autosetup -p1 -n ipu6-drivers-%{commit}
# Pre-apply patch listed in dkms.conf:
patch -p1 -i patches/*.patch
rm -fr patch* .github

cp -f %{SOURCE2} dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

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

%changelog
* Tue May 13 2025 Simone Caronni <negativo17@gmail.com> - 0.1~20250508git1a884d5-4
- Switch again to intel tree, now that is up to date.
- Do not bunlde usbio-drivers.
- Patch original dkms.conf file and pre-apply patch.

* Sat Feb 15 2025 Simone Caronni <negativo17@gmail.com> - 0.0^20250215git40f5283-3
- Update to latest snapshot.

* Fri Feb 07 2025 Simone Caronni <negativo17@gmail.com> - 0.0^20250205git032c59c-2
- Update to latest snapshot.
- Simplify DKMS configuration.

* Tue Jan 21 2025 Simone Caronni <negativo17@gmail.com> - 0.0^20250119gitf2a1b54-1
- Use recent packaging guidelines for snapshots.
- Switch again to jwrdegoede's fork.

* Mon Nov 11 2024 Simone Caronni <negativo17@gmail.com> - 0-6.20241030git19c1ded
- Update to latest snapshot.

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
