# Stop generation of debug rpms
%global debug_package %{nil}

Name:           cbflib
Version:        0.9.8
Release:        1%{?dist}
Summary:        Library for accessing Crystallographic Binary Files (CBF/imgCIF)

License:        LicenseRef-Callaway-MIT
URL:            https://github.com/NSLS2/cbflib-rpm
Source0:        https://github.com/NSLS2/cbflib-rpm/archive/refs/tags/%{version}.tar.gz

#BuildRequires:
#Requires:
#Recommends:

ExclusiveArch:      x86_64

# Prevent rpmbuild from smart-generating dependencies list
#AutoReq:        no

%description
Library for accessing Crystallographic Binary Files (CBF/imgCIF)

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_includedirisa} = %{version}-%{release}

%description devel
This package contains the header files, unversioned shared libraries
(e.g., .so files), and other resources needed for developing applications
that use %{name}.

%prep

%autosetup

%build

%install

%files
%license LICENSE

%files devel
%license LICENSE

%changelog

* Fri Oct 30 2026 Jakub Wlodek <jwlodek@bnl.gov> - 0.9.8-1
- Initial release of cbflib as an RPM.
