%define amversion 1.13

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake
Version:	1.13.1
Release:	2
License:	GPLv2+
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz
Source100:	fix-old-automake-files
# Automatically invoke fix-old-automake-files from aclocal
Patch0:		automake-1.13.1-automatically-fix-old-files.patch
URL:		http://sources.redhat.com/automake/
BuildArch:	noarch

Requires:	autoconf sed
BuildRequires:	autoconf
BuildRequires:	texinfo
Conflicts:	automake1.5
Provides:	automake1.9 = %{version}-%{release}
Obsoletes:	automake1.9
Provides:	automake1.8 = %{version}-%{release}
Obsoletes:	automake1.8
Requires(post):	update-alternatives
Requires(preun): update-alternatives

# tests need these
%if %{docheck}
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
%setup -q
%apply_patches

%build
%configure2_5x
%make

%check
%if %{docheck}
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
%__sed -e 's/reqd2.test//g' -i tests/Makefile
%__make check	# VERBOSE=1
%endif

%install
%__rm -rf %{buildroot}
%makeinstall_std

# provide -1.x symlinks
for i in 8 9 11 12; do
	%__ln_s automake-%{amversion} %{buildroot}%{_bindir}/automake-1.$i
	%__ln_s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-1.$i
done

%__rm -f %{buildroot}/%{_infodir}/*
%__install -m 644 doc/%{name}.info* %{buildroot}/%{_infodir}/
%__install -c -m 755 %SOURCE100 %buildroot%_bindir/

%__mkdir_p %{buildroot}%{_datadir}/aclocal

%clean
%__rm -rf %{buildroot}

%pre
if [ "$1" = 1 ]; then
  update-alternatives --remove automake %{_bindir}/automake-1.8
  update-alternatives --remove automake %{_bindir}/automake-1.9
  update-alternatives --remove automake %{_bindir}/automake-1.11
  update-alternatives --remove automake %{_bindir}/automake-1.12
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/automake
%{_bindir}/aclocal
%{_bindir}/automake-%{amversion}
%{_bindir}/aclocal-%{amversion}
%{_bindir}/automake-1.8
%{_bindir}/aclocal-1.8
%{_bindir}/automake-1.9
%{_bindir}/aclocal-1.9
%{_bindir}/automake-1.11
%{_bindir}/aclocal-1.11
%{_bindir}/automake-1.12
%{_bindir}/aclocal-1.12
%{_bindir}/fix-old-automake-files
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*
%{_mandir}/man1/aclocal-%{amversion}*
%{_mandir}/man1/aclocal.1*
%{_mandir}/man1/automake-%{amversion}*
%{_mandir}/man1/automake.1*
