%define amversion 1.14

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake
Version:	1.14.1
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
for i in 8 9 11 12 13; do
	%__ln_s automake-%{amversion} %{buildroot}%{_bindir}/automake-1.$i
	%__ln_s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-1.$i
done

%__rm -f %{buildroot}/%{_infodir}/*
%__install -m 644 doc/%{name}.info* %{buildroot}/%{_infodir}/
%__install -c -m 755 %SOURCE100 %buildroot%_bindir/

%__mkdir_p %{buildroot}%{_datadir}/aclocal

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
%{_bindir}/automake-1.13
%{_bindir}/aclocal-1.13
%{_bindir}/fix-old-automake-files
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*
%{_mandir}/man1/aclocal-%{amversion}*
%{_mandir}/man1/aclocal.1*
%{_mandir}/man1/automake-%{amversion}*
%{_mandir}/man1/automake.1*

%changelog
* Tue Feb 18 2014 Bernhard Rosenkraenzer <bero@lindev.ch> 1.14.1-2
+ Revision: b8825f0
- Add some more configure.in renaming magic to fix-old-automake-files

* Thu Dec 26 2013 Bernhard Rosenkränzer <bero@lindev.ch> 1.14.1-1
+ Revision: 67093c2
- Update to 1.14.1

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.4-5
+ Revision: 9bb89b7
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.4-4
+ Revision: f520e88
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.4-3
+ Revision: 801c5da
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.4-2
+ Revision: 5a47767
- MassBuild#289: Increase release tag

* Sat Jun 15 2013 Bernhard Rosenkränzer <bero@lindev.ch> 1.13.4-1
+ Revision: 700beb1
- 1.13.4

* Thu Jun 06 2013 Bernhard Rosenkraenzer <Bernhard.Rosenkranzer@linaro.org> 1.13.3-1
+ Revision: d3de7d4
- 1.13.3

* Thu May 16 2013 Bernhard Rosenkränzer <bero@lindev.ch> 1.13.2-1
+ Revision: 8270b67
- 1.13.2, some updates to fix-old-automake-files

* Tue Apr 23 2013 Bernhard Rosenkränzer <bero@lindev.ch> 1.13.1-2
+ Revision: 0a206e0
- Automatically fix old syntax (AM_CONFIG_HEADERS etc.) when running aclocal

* Tue Jan 01 2013 Bernhard Rosenkränzer <bero@lindev.ch> 1.13.1-1
+ Revision: 5fd9d3d
- Update to 1.13.1

* Sat Dec 29 2012 Bernhard Rosenkränzer <bero@lindev.ch> 1.13-1
+ Revision: 7d59186
- Update to 1.13

* Sun Dec 16 2012 Bernhard Rosenkränzer <bero@bero.eu> 1.12.6-1
+ Revision: 1a78dec
- Update to 1.12.6

* Thu Jul 12 2012 bero <bero@mandriva.org> 1.12.2-1
+ Revision: 25d7266
- Update to 1.12.2
- SILENT: svn-revision: 808964

* Sun Jun 03 2012 bero <bero@mandriva.org> 1.12.1-1
+ Revision: 693265d
- Update to 1.12.1
- SILENT: svn-revision: 802167

* Fri Apr 27 2012 bero <bero@mandriva.org> 1.12-1
+ Revision: 03199d4
- Update to 1.12
- SILENT: svn-revision: 793944

* Sat Apr 14 2012 bero <bero@mandriva.org> 1.11.5-1
+ Revision: 1d8f6eb
- Update to 1.11.5
- SILENT: svn-revision: 790967

* Tue Apr 03 2012 bero <bero@mandriva.org> 1.11.4-1
+ Revision: 345d73d
- Update to 1.11.4
- - Fix build in current environment (rpmlint)
- SILENT: svn-revision: 789044

* Mon Feb 13 2012 abondrov <abondrov@mandriva.org> 1.11.3-1
+ Revision: df66b25
- New version 1.11.3, drop BuildRoot definition from spec
- SILENT: svn-revision: 773760

* Mon Jan 09 2012 abondrov <abondrov@mandriva.org> 1.11.2-1
+ Revision: 7a57974
- New version 1.11.2
- SILENT: svn-revision: 758764

* Thu Dec 01 2011 oden <oden@mandriva.org> 1.11.1-3
+ Revision: 3e138ac
- - SILENT: RPM_BUILD_ROOT was removed
- SILENT: svn-revision: 736128

* Mon May 02 2011 oden <oden@mandriva.org> 1.11.1-3
+ Revision: e9cc9d8
- - mass rebuild
- SILENT: svn-revision: 662898

* Tue Nov 30 2010 oden <oden@mandriva.org> 1.11.1-2
+ Revision: 7c6966e
- - rebuild
- SILENT: svn-revision: 603484

* Tue Dec 08 2009 oden <oden@mandriva.org> 1.11.1-1
+ Revision: 4bc610d
- - 1.11.1
- SILENT: svn-revision: 475202

* Mon May 18 2009 fhimpe <fhimpe@mandriva.org> 1.11-2
+ Revision: 27600e6
- - Update to new version 1.11
- - Remove xz patch (integrated upstream)
- SILENT: svn-revision: 377328

* Thu Feb 26 2009 peroyvind <peroyvind@mandriva.org> 1.10.2-2
+ Revision: b2d9ec4
- sed is lighter and all and preferred over perl :o)
- SILENT: svn-revision: 345225

* Thu Feb 26 2009 peroyvind <peroyvind@mandriva.org> 1.10.2-2
+ Revision: 53eff5e
- add 'make dist-xz' target (P0, backported from git)
- SILENT: svn-revision: 345141

* Thu Nov 27 2008 fwang <fwang@mandriva.org> 1.10.2-1
+ Revision: 3745455
- fix license
- SILENT: svn-revision: 307220

* Thu Nov 27 2008 fwang <fwang@mandriva.org> 1.10.2-1
+ Revision: 566db93
- New version 1.10.2
- SILENT: svn-revision: 307192


