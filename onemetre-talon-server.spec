Name:      onemetre-talon-server
Version:   20220726
Release:   0
Url:       https://github.com/warwick-one-metre/teld
Summary:   Telescope daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-astropy, python3-Pyro4, python3-sysv_ipc, python3-warwick-observatory-common, python3-warwick-observatory-talon, %{?systemd_requires}
Requires:  onemetre-talon

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/teld/

%{__install} %{_sourcedir}/teld %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/teld@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/teld/

%files
%defattr(0755,root,root,-)
%{_bindir}/teld
%defattr(0644,root,root,-)
%{_unitdir}/teld@.service
%{_sysconfdir}/teld/onemetre.json

%changelog
