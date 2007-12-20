
Summary:	pommed
Summary(pl.UTF-8):	pommed
Name:		pommed
Version:	1.14
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://alioth.debian.org/frs/download.php/2223/%{name}-%{version}.tar.gz
# Source0-md5:	1b54269bbadb6b43bd9e45566dd1b6ef
URL:		http://www.technologeek.org/projects/pommed/
BuildRequires:	libconfuse-devel
BuildRequires:	libsmbios-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}

install pommed/pommed $RPM_BUILD_ROOT/%{_sbindir}
install gpomme/gpomme $RPM_BUILD_ROOT/%{_bindir}
install wmpomme/wmpomme $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/*pomme
%attr(755,root,root) %{_sbindir}/pommed
