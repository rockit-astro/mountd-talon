Name:      onemetre-telescope-server
Version:   2.0.0
Release:   0
Url:       https://github.com/warwick-one-metre/teld
Summary:   Telescope daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
#Requires: onemetre-talon
Requires: python34-Pyro4, python34-sysv_ipc, python34-pyephem, python34-warwick-observatory-common, observatory-log-client
%if 0%{?suse_version}
Requires:  python3, %{?systemd_requires}
BuildRequires: systemd-rpm-macros
%endif
%if 0%{?centos_ver}
Requires:  python34, %{?systemd_requires}
%endif

%description
Part of the observatory software for the Warwick one-meter telescope.

teld interfaces with and wraps the low-level talon daemons and exposes a
coherant telescope control interface via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/teld %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/teld.service %{buildroot}%{_unitdir}

%pre
%if 0%{?suse_version}
%service_add_pre teld.service
%endif

%post
%if 0%{?suse_version}
%service_add_post teld.service
%endif
%if 0%{?centos_ver}
%systemd_post teld.service
%endif

%preun
%if 0%{?suse_version}
%stop_on_removal teld.service
%service_del_preun teld.service
%endif
%if 0%{?centos_ver}
%systemd_preun teld.service
%endif

%postun
%if 0%{?suse_version}
%restart_on_update teld.service
%service_del_postun teld.service
%endif
%if 0%{?centos_ver}
%systemd_postun_with_restart teld.service
%endif

%files
%defattr(0755,root,root,-)
%{_bindir}/teld
%defattr(0644,root,root,-)
%{_unitdir}/teld.service

%changelog
