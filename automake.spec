%define amversion 1.16

%bcond_with	check
# remove bogus Automake perl dependencies and provides
%global __requires_exclude perl\\(Automake::.*\\)
%global __provides_exclude perl\\(Automake::.*\\)

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake
Version:	1.16.1
Release:	4
License:	GPLv2+
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz
Source100:	fix-old-automake-files
# Automatically invoke fix-old-automake-files from aclocal
Patch0:		automake-1.13.4-automatically-fix-old-files.patch
# Something changed in Perl 5.18 and the testsuite started to fail because
# of random looping in hashes items.  Upstream will probably start sorting of
# hash items by default for this failing case ~> we just don't resist on its
# order for now (only testsuite change).
# ~> Downstream
# ~> http://lists.gnu.org/archive/html/bug-automake/2013-07/msg00022.html
Patch1:		automake-1.13.4-hash-order-workaround.patch
URL:		http://sources.redhat.com/automake/
BuildArch:	noarch

Requires:	autoconf
Requires:	sed
BuildRequires:	autoconf
BuildRequires:	texinfo
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Thread::Queue)
BuildRequires:	perl(threads)
Conflicts:	automake1.5
%rename		automake1.9
%rename		automake1.8

# tests need these
%if %{with check}
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
%autosetup -p1

%build
%define _disable_rebuild_configure 1
%configure
%make_build

%if %{with check}
%check
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
sed -e 's/reqd2.test//g' -i tests/Makefile
make check VERBOSE=1
%endif

%install
%make_install

# provide -1.x symlinks
for i in 8 9 11 12 13 14 15; do
	ln -s automake-%{amversion} %{buildroot}%{_bindir}/automake-1.$i
	ln -s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-1.$i
done

rm %{buildroot}%{_infodir}/*
install -m644 doc/%{name}.info* %{buildroot}%{_infodir}/
install -m755 %{SOURCE100} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/aclocal

%files
%doc AUTHORS NEWS README THANKS
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
%{_bindir}/automake-1.13
%{_bindir}/aclocal-1.13
%{_bindir}/automake-1.14
%{_bindir}/aclocal-1.14
%{_bindir}/automake-1.15
%{_bindir}/aclocal-1.15
%{_bindir}/fix-old-automake-files
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*
%{_mandir}/man1/aclocal-%{amversion}*
%{_mandir}/man1/aclocal.1*
%{_mandir}/man1/automake-%{amversion}*
%{_mandir}/man1/automake.1*
%doc %{_docdir}/automake
