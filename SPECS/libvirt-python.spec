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
Version: 8.0.0
Release: 2%{?dist}%{?extra_release}
Source0: https://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: https://libvirt.org
License: LGPLv2+
BuildRequires: git
BuildRequires: libvirt-devel >= 8.0.0-9
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-lxml
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
* Thu Jun 30 2022 Jiri Denemark <jdenemar@redhat.com> - 8.0.0-2
- [RFE] RFE backport allow enabling ZEROCOPY live migration to libvirt-python on RHEL8 to be consumed by VDSM (rhbz#2092756)

* Fri Jan 14 2022 Jiri Denemark <jdenemar@redhat.com> - 8.0.0-1
- Rebased to libvirt-python-8.0.0 (rhbz#2012806)

* Fri Dec  3 2021 Jiri Denemark <jdenemar@redhat.com> - 7.10.0-1
- Rebased to libvirt-python-7.10.0 (rhbz#2012806)

* Thu Nov  4 2021 Jiri Denemark <jdenemar@redhat.com> - 7.9.0-1
- Rebased to libvirt-python-7.9.0 (rhbz#2012806)

* Wed Oct 20 2021 Jiri Denemark <jdenemar@redhat.com> - 7.8.0-1
- Rebased to libvirt-python-7.8.0 (rhbz#2012806)

* Thu Sep 2 2021 Danilo C. L. de Paula <ddepaula@redhat.com> - 7.6.0-1.el8
- Resolves: bz#2000225
  (Rebase virt:rhel module:stream based on AV-8.6)

* Mon Apr 27 2020 Danilo C. L. de Paula <ddepaula@redhat.com> - 6.0.0
- Resolves: bz#1810193
  (Upgrade components in virt:rhel module:stream for RHEL-8.3 release)

* Fri Jun 28 2019 Danilo de Paula <ddepaula@redhat.com> - 4.5.0-2
- Rebuild all virt packages to fix RHEL's upgrade path
- Resolves: rhbz#1695587
  (Ensure modular RPM upgrade path)

* Tue Jul  3 2018 Jiri Denemark <jdenemar@redhat.com> - 4.5.0-1
- Rebased to libvirt-python-4.5.0

* Fri May 25 2018 Jiri Denemark <jdenemar@redhat.com> - 4.3.0-1
- Rebased to libvirt-python-4.3.0

* Mon Mar  5 2018 Daniel P. Berrange <berrange@redhat.com> - 4.1.0-1
- Update to 4.1.0 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Daniel P. Berrange <berrange@redhat.com> - 4.0.0-1
- Update to 4.0.0 release

* Tue Dec  5 2017 Daniel P. Berrange <berrange@redhat.com> - 3.10.0-1
- Update to 3.10.0 release

* Fri Nov  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.9.0-1
- Update to 3.9.0 release

* Wed Oct  4 2017 Daniel P. Berrange <berrange@redhat.com> - 3.8.0-1
- Update to 3.8.0 release

* Mon Sep  4 2017 Daniel P. Berrange <berrange@redhat.com> - 3.7.0-1
- Update to 3.7.0 release

* Fri Aug 11 2017 Daniel P. Berrange <berrange@redhat.com> - 3.6.0-2
- Rename sub-RPMs to python2-libvirt & python3-libvirt
- Re-add py3 conditionals for benefit of RHEL/CentOS builds

* Thu Aug 10 2017 Daniel P. Berrange <berrange@redhat.com> - 3.6.0-1
- Update to 3.6.0 release
- Always build py3 package

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.5.0-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul  6 2017 Daniel P. Berrange <berrange@redhat.com> - 3.5.0-1
- Update to 3.5.0 release

* Mon Jun  5 2017 Daniel P. Berrange <berrange@redhat.com> - 3.4.0-1
- Update to 3.4.0 release

* Mon May  8 2017 Daniel P. Berrange <berrange@redhat.com> - 3.3.0-1
- Update to 3.3.0 release

* Mon Apr  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-1
- Update to 3.2.0 release

* Fri Mar  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-1
- Update to 3.1.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Daniel P. Berrange <berrange@redhat.com> - 3.0.0-1
- Update to 3.0.0 release
