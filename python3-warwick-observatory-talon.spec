Name:      python3-warwick-observatory-talon
Version:   20210723
Release:   0
License:   GPL3
Summary:   Common code for the Warwick one-metre and SuperWASP talon daemon
Url:       https://github.com/warwick-one-metre/teld
BuildArch: noarch
Requires:  python3, python3-warwick-observatory-common

%description
Part of the observatory software for the Warwick one-meter and SuperWASP telescope.

python3-warwick-observatory-talon holds the common telescope code.

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog