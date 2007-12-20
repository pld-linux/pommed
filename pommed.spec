# Conditional build
%bcond_without	gpomme	# don't build gpomme client

Summary:	pommed
Summary(pl.UTF-8):	pommed
Name:		pommed
Version:	1.14
Release:	0.4
License:	GPL v2
Group:		Applications
Source0:	http://alioth.debian.org/frs/download.php/2223/%{name}-%{version}.tar.gz
# Source0-md5:	1b54269bbadb6b43bd9e45566dd1b6ef
Source1:	%{name}.init
URL:		http://www.technologeek.org/projects/pommed/
BuildRequires:	dbus-devel
BuildRequires:	libconfuse-devel
BuildRequires:	libsmbios-devel
BuildRequires:	pciutils-devel
BuildRequires:	rpmbuild(macros) >= 1.228
%if %{with gpomme}
BuildRequires:	gtk+2-devel
BuildRequires:	libglade2-devel
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	alsa-lib
Requires:	eject
Requires:	pomme-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n gpomme
Summary:	gpomme
Summary(pl.UTF-8):	gpomme
Group:		X11/Applications
Requires:	%{name} = %{version}
Provides:	pomme-client

%description -n gpomme

%description -n gpomme -l pl.UTF-8

%package -n wmpomme
Summary:	wmpomme
Summary(pl.UTF-8):	wmpomme
Group:		X11/Applications
Requires:	%{name} = %{version}
Provides:	pomme-client

%description -n wmpomme

%description -n wmpomme -l pl.UTF-8

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_datadir}/%{name},%{_sysconfdir}/dbus-1/system.d}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

install pommed/pommed $RPM_BUILD_ROOT%{_sbindir}
install pommed/data/* $RPM_BUILD_ROOT%{_datadir}/%{name}
install pommed.conf.{mactel,pmac} $RPM_BUILD_ROOT%{_sysconfdir}
install dbus-policy.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/pommed.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pommed
%if %{with gpomme}
install -d $RPM_BUILD_ROOT{%{_datadir}/gpomme/themes,%{_desktopdir}}
install gpomme/gpomme $RPM_BUILD_ROOT%{_bindir}
cp -R gpomme/themes/* $RPM_BUILD_ROOT%{_datadir}/gpomme/themes
install gpomme/gpomme*.desktop $RPM_BUILD_ROOT%{_desktopdir}
install gpomme/gpomme.glade $RPM_BUILD_ROOT%{_datadir}/gpomme
%endif
install wmpomme/wmpomme $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service pommed restart

%preun
if [ "$1" = "0" ]; then
%service pommed stop
/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_sbindir}/pommed
%{_datadir}/%{name}
%{_sysconfdir}/pommed.conf.*
%{_sysconfdir}/dbus-1/system.d/pommed.conf
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/pommed

%if %{with gpomme}
%files -n gpomme
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpomme
%{_datadir}/gpomme
%{_desktopdir}/gpomme*.desktop
%endif

%files -n wmpomme
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wmpomme
