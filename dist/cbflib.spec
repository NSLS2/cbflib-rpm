# Stop generation of debug rpms
%global debug_package %{nil}

%global cqrlib_version 1.1.4

Name:           cbflib
Version:        0.9.8
Release:        1%{?dist}
Summary:        Library for accessing Crystallographic Binary Files (CBF/imgCIF)

License:        GPL-2.0-or-later OR LGPL-2.1-or-later
URL:            https://github.com/NSLS2/cbflib-rpm
Source0:        https://github.com/dials/cbflib/archive/refs/tags/CBFlib-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/yayahjb/cqrlib/archive/refs/tags/CQRlib-%{cqrlib_version}.tar.gz#/cqrlib-%{cqrlib_version}.tar.gz

BuildRequires:  cmake >= 3.18
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pkgconfig
BuildRequires:  hdf5
BuildRequires:  hdf5-devel
BuildRequires:  libtiff-devel

# CQRlib is fetched and built in-tree by the upstream CMake build
Provides:       bundled(cqrlib) = %{cqrlib_version}

ExclusiveArch:      x86_64

%description
CBFlib is a library of ANSI-C functions providing a simple mechanism for
accessing Crystallographic Binary Files (CBF files) and Image-supporting
CIF (imgCIF) files, along with NeXus/HDF5 conversion utilities.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hdf5-devel

%description devel
This package contains the header files, unversioned shared libraries
(e.g., .so files), and other resources needed for developing applications
that use %{name}.

%prep
%autosetup -n cbflib-CBFlib-%{version}
mkdir cqrlib
tar -xzf %{SOURCE1} -C cqrlib --strip-components=1
patch -d cqrlib -p1 -t < patches/cqrlib-%{cqrlib_version}.patch
# Append to, rather than overwrite, the distribution compiler flags
sed -i 's|set(CMAKE_C_FLAGS "-Wall|set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall|' CMakeLists.txt
# Fix non-literal format string (rejected by -Werror=format-security)
sed -i 's|xstrlen-chars_used:0),sep);|xstrlen-chars_used:0),"%%s",sep);|' examples/tif_sprint.c

%build
# Use system HDF5/LibTIFF and libc regex, provide CQRlib locally, and point
# the test data at a dummy location so that no network access is required.
%cmake \
    -DCBF_ENABLE_FORTRAN=OFF \
    -DCBF_WITH_HDF5=OFF \
    -DCBF_WITH_LIBTIFF=OFF \
    -DCBF_WITH_PCRE=OFF \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_CQRLIB=$PWD/cqrlib \
    -DCBF_DATA_INPUT=$PWD/testdata-unavailable \
    -DCBF_DATA_OUTPUT=$PWD/testdata-unavailable
%cmake_build

%install
%cmake_install

# Upstream hardcodes "lib" as the install destination for its libraries
if [ "%{_prefix}/lib" != "%{_libdir}" ] && [ -d %{buildroot}%{_prefix}/lib ]; then
    mkdir -p %{buildroot}%{_libdir}
    mv %{buildroot}%{_prefix}/lib/lib* %{buildroot}%{_libdir}/
    rmdir %{buildroot}%{_prefix}/lib
fi

# Only the bundled CQRlib runtime library is shipped
rm -f %{buildroot}%{_includedir}/cqrlib.h
rm -f %{buildroot}%{_libdir}/libCQRlib.so
rm -rf %{buildroot}%{_libdir}/cmake/CQRlib

%files
%license gpl.txt lgpl.txt CBFlib_NOTICES.txt
%doc README.md ChangeLog.md
%{_bindir}/*
%{_libdir}/libcbf.so.*
%{_libdir}/libCQRlib.so.*

%files devel
%license gpl.txt lgpl.txt CBFlib_NOTICES.txt
%{_libdir}/libcbf.so
%{_libdir}/libimg.so
%{_includedir}/cbflib/

%changelog

* Thu Oct 15 2026 Jakub Wlodek <jwlodek@bnl.gov> - 0.9.8-1
- Initial release of cbflib as an RPM.
