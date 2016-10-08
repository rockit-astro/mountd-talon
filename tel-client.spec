Name:      onemetre-tel-client
Version:   1.16
Release:   0
Url:       https://github.com/warwick-one-metre/teld
Summary:   Telescope client for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4

%description
Part of the observatory software for the Warwick one-meter telescope.

tel is a commandline utility for controlling the telescope.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/tel %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/tel %{buildroot}/etc/bash_completion.d/tel

%files
%defattr(0755,root,root,-)
%{_bindir}/tel
/etc/bash_completion.d/tel

%changelog
