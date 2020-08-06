Name:      onemetre-telescope-server
Version:   2.1.2
Release:   0
Url:       https://github.com/warwick-one-metre/teld
Summary:   Telescope daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-sysv_ipc, python3-pyephem, python3-warwick-observatory-common
Requires:  observatory-log-client, %{?systemd_requires}
Requires: onemetre-talon

%description
Part of the observatory software for the Warwick one-meter telescope.

teld interfaces with and wraps the low-level talon daemons and exposes a
coherant telescope control interface via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/teld %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/teld.service %{buildroot}%{_unitdir}

%post
%systemd_post teld.service

%preun
%systemd_preun teld.service

%postun
%systemd_postun_with_restart teld.service

%files
%defattr(0755,root,root,-)
%{_bindir}/teld
%defattr(0644,root,root,-)
%{_unitdir}/teld.service

%changelog
