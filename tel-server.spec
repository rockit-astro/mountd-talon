Name:      onemetre-tel-server
Version:   1.9
Release:   1
Url:       https://github.com/warwick-one-metre/teld
Summary:   Telescope daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-sysv_ipc, python3-pyephem, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

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
%service_add_pre teld.service

%post
%service_add_post teld.service
%fillup_and_insserv -f -y teld.service

%preun
%stop_on_removal teld.service
%service_del_preun teld.service

%postun
%restart_on_update teld.service
%service_del_postun teld.service

%files
%defattr(0755,root,root,-)
%{_bindir}/teld
%defattr(-,root,root,-)
%{_unitdir}/teld.service

%changelog
