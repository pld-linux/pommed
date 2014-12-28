# TODO: optflags
#
# Conditional build
%bcond_without	gpomme	# don't build gpomme client

Summary:	pommed - Apple laptops hotkeys event handler
Summary(pl.UTF-8):	pommed - obsługa zdarzeń klawiszy specjalnych w laptopach Apple'a
Name:		pommed
Version:	1.39
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://alioth.debian.org/frs/download.php/3583/%{name}-%{version}.tar.gz
# Source0-md5:	f36757d180ed4f35fced6c096e1bcbeb
Source1:	%{name}.init
URL:		https://launchpad.net/pommed
BuildRequires:	alsa-lib-devel
BuildRequires:	audiofile-devel
BuildRequires:	dbus-devel
BuildRequires:	gettext-tools
BuildRequires:	libconfuse-devel
BuildRequires:	libsmbios-devel
BuildRequires:	pciutils-devel
BuildRequires:	rpmbuild(macros) >= 1.228
%if %{with gpomme}
BuildRequires:	gtk+2-devel
BuildRequires:	libglade2-devel
%endif
BuildRequires:	xorg-lib-libXpm-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	alsa-lib
Requires:	eject
Requires:	pomme-client
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pommed is a daemon handling the hotkeys found on the Apple laptops,
like the MacBook Pro, MacBook and PowerBook laptops. These hotkeys
control, through pommed, the LCD backlight level, the audio volume,
the keyboard backlight level (only on the MacBook Pro and the latest
PowerBook) and the CD/DVD drive ejection. Additionally, pommed
monitors the ambient light sensors found on the MacBook Pro and the
latest PowerBook to automatically light up the keyboard backlight when
the ambient light level gets too low.

%description -l pl.UTF-8
pommed to demon obsługujący klawisze specjalne w laptopach Apple'a,
takich jak MacBook Pro, MacBook i PowerBook. Klawisze te poprzez
pommeda sterują poziomem podświetlenia LCD, głośnością dźwięku,
poziomem podświetlenia klawiatury (tylko w MacBooku Pro i najnowszych
PowerBookach) oraz wysuwaniem napędu CD/DVD. Ponadto pommed monitoruje
czujnik światła zewnętrznego w MacBookach Pro i najnowszych
PowerBookach w celu automatycznego podświetlania klawiatury kiedy
światło zewnętrzne jest zbyt słabe.

%package -n gpomme
Summary:	gpomme - GTK+ graphical client for use with pommed
Summary(pl.UTF-8):	gpomme - graficzny klient GTK+ dla pommeda
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	pomme-client

%description -n gpomme
gpomme will react to signals sent by pommed over DBus when a key is
pressed, displaying the action taken by pommed and the current state
associated with this action.

%description -n gpomme -l pl.UTF-8
gpomme reaguje na sygnały wysyłane przez pommeda poprzez DBus przy
naciśnięciu klawisza, wyświetlając podejmowaną akcję i aktualny stan
związany z tą akcją.

%package -n wmpomme
Summary:	wmpomme - WindowMaker dockapp for use with pommed
Summary(pl.UTF-8):	wmpomme - aplet doku WindowMakera dla pommeda
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	pomme-client

%description -n wmpomme
wmpomme displays, as a WindowMaker dockapp, the state of the devices
controlled by pommed.

%description -n wmpomme -l pl.UTF-8
wmpomme wyświetla w postaci apletu doku WindowMakera stan urządzeń
sterowanych przez pommeda.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_datadir}/%{name},/etc/{dbus-1/system.d,rc.d/init.d}}

install -p pommed/pommed $RPM_BUILD_ROOT%{_sbindir}
cp -p pommed/data/* $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p pommed.conf.{mactel,pmac} $RPM_BUILD_ROOT%{_sysconfdir}
cp -p dbus-policy.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/pommed.conf
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pommed
%if %{with gpomme}
install -d $RPM_BUILD_ROOT{%{_datadir}/gpomme/themes,%{_desktopdir}}
install -p gpomme/gpomme $RPM_BUILD_ROOT%{_bindir}
cp -a gpomme/themes/* $RPM_BUILD_ROOT%{_datadir}/gpomme/themes
cp -p gpomme/gpomme*.desktop $RPM_BUILD_ROOT%{_desktopdir}
%endif
install -p wmpomme/wmpomme $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service pommed restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	%service pommed stop
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_sbindir}/pommed
%{_datadir}/%{name}
%{_sysconfdir}/pommed.conf.*
/etc/dbus-1/system.d/pommed.conf
%attr(754,root,root) /etc/rc.d/init.d/pommed

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
