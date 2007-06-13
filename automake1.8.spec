%define version 1.9.6
%define release %mkrel 4

%define amversion 1.9
%define pkgamversion 1.8

%define docheck 1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake%{pkgamversion}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.9.4-infofiles.patch
URL:		http://sources.redhat.com/automake/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch

Requires:	autoconf >= 1:2.58
BuildRequires:	autoconf >= 1:2.59-4mdk
BuildRequires:	texinfo
Provides:	automake = %{version}-%{release}
Conflicts:	automake1.5
Conflicts:	automake < 1.4-22.p6.mdk
Provides:	automake1.9 = %{version}-%{release}
Obsoletes:	automake1.9
Requires(post):	/sbin/install-info
Requires(preun): /sbin/install-info
Requires(post):	/usr/sbin/update-alternatives
Requires(preun): /usr/sbin/update-alternatives

# tests need these
%if %docheck
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	tetex-latex
BuildRequires:	emacs
BuildRequires:	dejagnu
BuildRequires:	gcc-java
BuildRequires:	python
%endif

%description
Automake is a tool for automatically generating Makefiles compliant with
the GNU Coding Standards.

You should install Automake if you are developing software and would like
to use its capabilities of automatically generating GNU standard
Makefiles. If you install Automake, you will also need to install GNU's
Autoconf package.

%prep
%setup -q -n automake-%{version}
%patch0 -p1 -b .parallel

%build
# (Abel) config* don't understand noarch-mandrake-linux-gnu arch
%define _target_platform i586-mandrake-linux-gnu

%configure2_5x
%make

%if %docheck
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
make check	# VERBOSE=1
%endif

# (Abel) forcefully modify info filename, otherwise info page will refer to
# old automake
pushd doc
makeinfo -I . -o %{name}.info automake.texi
popd

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f $RPM_BUILD_ROOT/%{_bindir}/{automake,aclocal}

# provide -1.8 symlinks
ln -s automake-%{amversion} $RPM_BUILD_ROOT%{_bindir}/automake-%{pkgamversion}
ln -s aclocal-%{amversion} $RPM_BUILD_ROOT%{_bindir}/aclocal-%{pkgamversion}

rm -f $RPM_BUILD_ROOT/%{_infodir}/*
install -m 644 doc/%{name}.info* $RPM_BUILD_ROOT/%{_infodir}/

perl -p -i -e 's|\(automake\)Extending aclocal|(%{name})Extending aclocal|' \
  $RPM_BUILD_ROOT/%{_bindir}/aclocal-%{amversion}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %name.info
update-alternatives \
	--install %{_bindir}/automake automake %{_bindir}/automake-%{amversion} 30 \
	--slave   %{_bindir}/aclocal  aclocal  %{_bindir}/aclocal-%{amversion}

%preun
%_remove_install_info %name.info
if [ $1 = 0 ]; then
	update-alternatives --remove automake %{_bindir}/automake-%{amversion}
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*

