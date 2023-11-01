# -*- rpm-spec -*-

# This spec file assumes you are building on a Fedora or RHEL version
# that's still supported by the vendor. It may work on other distros
# or versions, but no effort will be made to ensure that going forward
%define min_rhel 8
%define min_fedora 33

%if (0%{?fedora} && 0%{?fedora} >= %{min_fedora}) || (0%{?rhel} && 0%{?rhel} >= %{min_rhel})
    %define supported_platform 1
%else
    %define supported_platform 0
%endif

Summary: The libvirt virtualization API python3 binding
Name: libvirt-python
Version: 9.0.0
Release: 1%{?dist}%{?extra_release}
Source0: https://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: https://libvirt.org
License: LGPLv2+
BuildRequires: git
BuildRequires: libvirt-devel >= 9.0.0-2
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-lxml
BuildRequires: python3-setuptools
BuildRequires: gcc

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python3_sitearch}/.*\.so}
%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%package -n python3-libvirt
Summary: The libvirt virtualization API python3 binding
Url: http://libvirt.org
License: LGPLv2+
%{?python_provide:%python_provide python3-libvirt}
Provides: libvirt-python3 = %{version}-%{release}
Obsoletes: libvirt-python3 <= 3.6.0-1%{?dist}

%description -n python3-libvirt
The python3-libvirt package contains a module that permits applications
written in the Python 3.x programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%prep
%autosetup -S git_am -N

git config gc.auto 0

%autopatch


# Unset execute bit for example scripts; it can introduce spurious
# RPM dependencies, like /usr/bin/python3
# for the -python3 package
find examples -type f -exec chmod 0644 \{\} \;

%build
%if ! %{supported_platform}
echo "This RPM requires either Fedora >= %{min_fedora} or RHEL >= %{min_rhel}"
exit 1
%endif

%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-libvirt
%doc ChangeLog AUTHORS README COPYING COPYING.LESSER examples/
%{python3_sitearch}/libvirt.py*
%{python3_sitearch}/libvirtaio.py*
%{python3_sitearch}/libvirt_qemu.py*
%{python3_sitearch}/libvirt_lxc.py*
%{python3_sitearch}/__pycache__/libvirt.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_qemu.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_lxc.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirtaio.cpython-*.py*
%{python3_sitearch}/libvirtmod*
%{python3_sitearch}/*egg-info

%changelog
* Wed Feb  1 2023 Jiri Denemark <jdenemar@redhat.com> - 9.0.0-1
- Rebased to libvirt-python-9.0.0 (rhbz#2124467)

* Thu Dec  8 2022 Jiri Denemark <jdenemar@redhat.com> - 8.10.0-1
- Rebased to libvirt-python-8.10.0 (rhbz#2124467)

* Fri Nov  4 2022 Jiri Denemark <jdenemar@redhat.com> - 8.9.0-1
- Rebased to libvirt-python-8.9.0 (rhbz#2124467)

* Mon Sep 26 2022 Jiri Denemark <jdenemar@redhat.com> - 8.7.0-1
- Rebased to libvirt-python-8.7.0 (rhbz#2124467)

* Thu Aug 18 2022 Jiri Denemark <jdenemar@redhat.com> - 8.5.0-2
- Add VIR_DOMAIN_IOTHREAD_THREAD_POOL_{MIN,MAX} macros (rhbz#2117475)

* Wed Jul 13 2022 Jiri Denemark <jdenemar@redhat.com> - 8.5.0-1
- Rebased to libvirt-python-8.5.0 (rhbz#2060316)
- The rebase also fixes the following bugs:
    rhbz#2092752

* Thu Jun  9 2022 Jiri Denemark <jdenemar@redhat.com> - 8.4.0-1
- Rebased to libvirt-python-8.4.0 (rhbz#2060316)

* Thu May 19 2022 Jiri Denemark <jdenemar@redhat.com> - 8.3.0-1
- Rebased to libvirt-python-8.3.0 (rhbz#2060316)

* Fri Apr 15 2022 Jiri Denemark <jdenemar@redhat.com> - 8.2.0-1
- Rebased to libvirt-python-8.2.0 (rhbz#2060316)

* Mon Jan 17 2022 Jiri Denemark <jdenemar@redhat.com> - 8.0.0-1
- Rebased to libvirt-python-8.0.0 (rhbz#2001522)

* Mon Dec 13 2021 Jiri Denemark <jdenemar@redhat.com> - 7.10.0-1
- Rebased to libvirt-python-7.10.0 (rhbz#2001522)

* Thu Nov 11 2021 Jiri Denemark <jdenemar@redhat.com> - 7.9.0-1
- Rebased to libvirt-python-7.9.0 (rhbz#2001522)

* Mon Oct 18 2021 Jiri Denemark <jdenemar@redhat.com> - 7.8.0-1
- Rebased to libvirt-python-7.8.0 (rhbz#2001522)

* Thu Aug 12 2021 Jiri Denemark <jdenemar@redhat.com> - 7.6.0-1
- Rebased to libvirt-python-7.6.0 (rhbz#1950951)

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 7.5.0-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jul 16 2021 Jiri Denemark <jdenemar@redhat.com> - 7.5.0-1
- Rebased to libvirt-python-7.5.0 (rhbz#1950951)

* Wed Jun 16 2021 Jiri Denemark <jdenemar@redhat.com> - 7.4.0-1
- Rebased to libvirt-python-7.4.0 (rhbz#1950951)

* Mon May 31 2021 Jiri Denemark <jdenemar@redhat.com> - 7.3.0-1
- Rebased to libvirt-python-7.3.0 (rhbz#1950951)
- The rebase also fixes the following bugs:
    rhbz#1916800, rhbz#1950603, rhbz#1950951
- RHEL: Add gating.yaml for RHEL9 (rhbz#1950603)

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 7.0.0-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Cole Robinson <crobinso@redhat.com> - 7.0.0-1
- Update to version 7.0.0

* Tue Dec 01 2020 Cole Robinson <crobinso@redhat.com> - 6.10.0-1
- Update to version 6.10.0

* Tue Nov 03 2020 Cole Robinson <crobinso@redhat.com> - 6.9.0-1
- Update to version 6.9.0

* Thu Oct 15 2020 Daniel P. Berrangé <berrange@redhat.com> - 6.8.0-2
- Fix regression with snapshot handling (rhbz #1888709)

* Fri Oct 02 2020 Cole Robinson <crobinso@redhat.com> - 6.8.0-1
- Update to version 6.8.0

* Wed Sep 02 2020 Cole Robinson <crobinso@redhat.com> - 6.7.0-1
- Update to version 6.7.0

* Tue Aug 04 2020 Cole Robinson <crobinso@redhat.com> - 6.6.0-1
- Update to version 6.6.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 2020 Cole Robinson <crobinso@redhat.com> - 6.5.0-1
- Update to version 6.5.0

* Tue Jun 02 2020 Cole Robinson <crobinso@redhat.com> - 6.4.0-1
- Update to version 6.4.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 6.3.0-2
- Rebuilt for Python 3.9

* Tue May 05 2020 Cole Robinson <crobinso@redhat.com> - 6.3.0-1
- Update to version 6.3.0

* Thu Apr 02 2020 Cole Robinson <crobinso@redhat.com> - 6.2.0-1
- Update to version 6.2.0

* Wed Mar 04 2020 Cole Robinson <crobinso@redhat.com> - 6.1.0-1
- Update to version 6.1.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Cole Robinson <crobinso@redhat.com> - 6.0.0-1
- Update to version 6.0.0
