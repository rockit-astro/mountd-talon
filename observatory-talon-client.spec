Name:      observatory-talon-client
Version:   20220726
Release:   0
Url:       https://github.com/warwick-one-metre/teld
Summary:   Talon telescope client.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwick-observatory-common, python3-warwick-observatory-talon

%description

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
