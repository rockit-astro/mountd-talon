Name:      rockit-mount-talon
Version:   %{_version}
Release:   1
Summary:   Talon mount control
Url:       https://github.com/rockit-astro/mountd-talon
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/mountd/

%{__install} %{_sourcedir}/tel %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/talon_mountd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/talon_mountd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/tel %{buildroot}/etc/bash_completion.d/tel

%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/mountd/
%{__install} %{_sourcedir}/ngts_m06.json %{buildroot}%{_sysconfdir}/mountd/

%package server
Summary:  Talon mount server
Group:    Unspecified
Requires: python3-rockit-mount-talon python3-astropy python3-sysv_ipc rockit-talon
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/talon_mountd
%defattr(0644,root,root,-)
%{_unitdir}/talon_mountd@.service

%package client
Summary:  Talon mount client
Group:    Unspecified
Requires: python3-rockit-mount-talon python3-astropy
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/tel
/etc/bash_completion.d/tel

%package data-onemetre
Summary: Talon mount configuration for the W1m telescope
Group:   Unspecified
%description data-onemetre

%files data-onemetre
%defattr(0644,root,root,-)
%{_sysconfdir}/mountd/onemetre.json

%package data-ngts-m06
Summary: Talon mount configuration for NGTS M06
Group:   Unspecified
%description data-ngts-m06

%files data-ngts-m06
%defattr(0644,root,root,-)
%{_sysconfdir}/mountd/ngts_m06.json

%changelog