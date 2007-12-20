# Conditional build
%bcond_without	gpomme	# don't build gpomme client

Summary:	pommed
Summary(pl.UTF-8):	pommed
Name:		pommed
Version:	1.14
Release:	0.3
License:	GPL v2
Group:		Applications
Source0:	http://alioth.debian.org/frs/download.php/2223/%{name}-%{version}.tar.gz
# Source0-md5:	1b54269bbadb6b43bd9e45566dd1b6ef
URL:		http://www.technologeek.org/projects/pommed/
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	dbus-devel
BuildRequires:	libconfuse-devel
BuildRequires:	libsmbios-devel
BuildRequires:	pciutils-devel
%if %{with gpomme}
BuildRequires:	gtk+2-devel
BuildRequires:	libglade2-devel
%endif
Requires:	alsa-lib
Requires:	eject
Requires:	pomme-client
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n gpomme
Summary:	gpomme
Summary(pl.UTF-8):	gpomme
Group:		X11/Applications
Provides:	pomme-client
Requires:	%{name} = %{version}

%description -n gpomme

%description -n gpomme -l pl.UTF-8

%package -n wmpomme
Summary:        wmpomme
Summary(pl.UTF-8):      wmpomme
Group:          X11/Applications
Provides:       pomme-client
Requires:       %{name} = %{version}

%description -n wmpomme

%description -n wmpomme -l pl.UTF-8

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_datadir}/%{name},%{_sysconfdir}}

install pommed/pommed $RPM_BUILD_ROOT%{_sbindir}
install pommed/data/* $RPM_BUILD_ROOT%{_datadir}/%{name}
install pommed.conf.{mactel,pmac} $RPM_BUILD_ROOT%{_sysconfdir}
%if %{with gpomme}
install -d $RPM_BUILD_ROOT%{_datadir}/gpomme/themes
install gpomme/gpomme $RPM_BUILD_ROOT%{_bindir}
cp -R gpomme/themes/* $RPM_BUILD_ROOT%{_datadir}/gpomme/themes
%endif
install wmpomme/wmpomme $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_sbindir}/pommed
%{_datadir}/%{name}
%{_sysconfdir}/pommed.conf.*

%if %{with gpomme}
%files -n gpomme
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpomme
%{_datadir}/gpomme
%endif

%files -n wmpomme
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wmpomme
