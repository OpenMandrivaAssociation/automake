%define version 1.10
%define release %mkrel 3

%define amversion 1.10

%define docheck 1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
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

%build
# (Abel) config* don't understand noarch-mandrake-linux-gnu arch
%configure2_5x --build=i586-%{_target_vendor}-%{_target_os}%{?_gnu}
%make

%check
%if %docheck
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
make check	# VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# provide -1.8 symlinks
ln -s automake-%{amversion} $RPM_BUILD_ROOT%{_bindir}/automake-1.8
ln -s aclocal-%{amversion} $RPM_BUILD_ROOT%{_bindir}/aclocal-1.8

# provide -1.9 symlinks
ln -s automake-%{amversion} $RPM_BUILD_ROOT%{_bindir}/automake-1.9
ln -s aclocal-%{amversion} $RPM_BUILD_ROOT%{_bindir}/aclocal-1.9

rm -f $RPM_BUILD_ROOT/%{_infodir}/*
install -m 644 doc/%{name}.info* $RPM_BUILD_ROOT/%{_infodir}/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

# %%doc doesn't work
cp AUTHORS COPYING ChangeLog NEWS README THANKS TODO $RPM_BUILD_ROOT%{_datadir}/doc/automake/

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_bindir}/automake
%{_bindir}/aclocal
%{_bindir}/automake-%{version}
%{_bindir}/aclocal-%{version}
%{_bindir}/automake-1.8
%{_bindir}/aclocal-1.8
%{_bindir}/automake-1.9
%{_bindir}/aclocal-1.9
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*
%{_datadir}/doc/automake

