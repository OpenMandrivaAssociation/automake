%define version 1.11.1
%define release %mkrel 3

%define amversion 1.11

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
# Adds 'make dist-xz' target, backport from git
URL:		http://sources.redhat.com/automake/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch

Requires:	autoconf >= 1:2.58
BuildRequires:	autoconf >= 1:2.59-4mdk
BuildRequires:	texinfo
Conflicts:	automake1.5
Provides:	automake1.9 = %{version}-%{release}
Obsoletes:	automake1.9
Provides:	automake1.8 = %{version}-%{release}
Obsoletes:	automake1.8
Requires(post):	info-install
Requires(preun): info-install
Requires(post):	update-alternatives
Requires(preun): update-alternatives

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

%build
# (Abel) config* don't understand noarch-mandriva-linux-gnu arch
%configure2_5x --build=i586-%{_target_vendor}-%{_target_os}%{?_gnu}
%make

%check
%if %docheck
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
sed -e 's/reqd2.test//g' -i tests/Makefile
make check	# VERBOSE=1
%endif

%install
rm -rf %{buildroot}
%makeinstall_std

# provide -1.8 symlinks
ln -s automake-%{amversion} %{buildroot}%{_bindir}/automake-1.8
ln -s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-1.8

# provide -1.9 symlinks
ln -s automake-%{amversion} %{buildroot}%{_bindir}/automake-1.9
ln -s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-1.9

rm -f %{buildroot}/%{_infodir}/*
install -m 644 doc/%{name}.info* %{buildroot}/%{_infodir}/

mkdir -p %{buildroot}%{_datadir}/aclocal

%clean
rm -rf %{buildroot}

%pre
if [ "$1" = 1 ]; then
  update-alternatives --remove automake %{_bindir}/automake-1.8
  update-alternatives --remove automake %{_bindir}/automake-1.9
fi

%post
%_install_info %name.info

%preun
%_remove_install_info %name.info

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/automake
%{_bindir}/aclocal
%{_bindir}/automake-%{amversion}
%{_bindir}/aclocal-%{amversion}
%{_bindir}/automake-1.8
%{_bindir}/aclocal-1.8
%{_bindir}/automake-1.9
%{_bindir}/aclocal-1.9
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*
%{_mandir}/man1/aclocal-1.11.1*
%{_mandir}/man1/aclocal.1*
%{_mandir}/man1/automake-1.11.1*
%{_mandir}/man1/automake.1*
