Name:		simh
Version:	3.8.1
Release:	5%{?dist}
Summary:	A highly portable, multi-system emulator

Group:		Applications/Emulators
#The licensing is mostly MIT, but there is also some GPL+ (literally, v1+) code
#in there, notably in AltairZ80/.
#(each target is compiled into its own binary, so only AltairZ80 is GPL+)
License:	MIT and GPL+

URL:		http://simh.trailing-edge.com/
Source0:	simh-%{version}-noroms.tar.gz
# we use
# this script to remove the roms binary and patented code before shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./simh-generate-tarball.sh 3.8.1
Source1:	simh-generate-tarball.sh

# prefer default gnu89 (ISO C90) as C99 is not fully supported by cc
# and add fedora optflags
Patch0:		simh-3.8.0-gcc.patch
Patch1:		simh-3.8.1-altair-segfault.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libpcap-devel, dos2unix
#Requires:

%description
SIMH is a historical computer simulation system. It consists of simulators
for many different computers, all written around a common user
interface package and set of supporting libraries.
SIMH can be used to simulate any computer system for which sufficient detail
is available, but the focus to date has been on simulating computer systems
of historic interest.

SIMH implements simulators for:

* Data General Nova, Eclipse
* Digital Equipment Corporation PDP-1, PDP-4, PDP-7, PDP-8, PDP-9, PDP-10,
  PDP-11, PDP-15, VAX
* GRI Corporation GRI-909, GRI-99
* IBM 1401, 1620, 7090/7094, System 3
* Interdata (Perkin-Elmer) 16b and 32b systems
* Hewlett-Packard 2114, 2115, 2116, 2100, 21MX, 1000
* Honeywell H316/H516
* MITS Altair 8800, with both 8080 and Z80
* Royal-Mcbee LGP-30, LGP-21
* Scientific Data Systems SDS 940

%prep
%setup -qn %{name}-%{version}
%patch0 -p1 -b .gcc
%patch1 -p1 -b .altair-segfault


%build
mkdir -p BIN
make %{?_smp_mflags} -e OPT="%{optflags}" USE_NETWORK=1


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in `ls BIN/`; do
	install -p -m 755 BIN/$i $RPM_BUILD_ROOT%{_bindir}/simh-$i
done
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
for i in `find -iname "*.txt"`; do dos2unix -k $i; done

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc ALTAIR/altair.txt NOVA/eclipse.txt 0readme_38.txt 0readme_ethernet.txt
%doc HP2100/hp2100_diag.txt I7094/i7094_bug_history.txt Interdata/id_diag.txt
%doc PDP1/pdp1_diag.txt PDP10/pdp10_bug_history.txt PDP18B/pdp18b_diag.txt
%doc S3/haltguide.txt S3/readme_s3.txt S3/system3.txt SDS/sds_diag.txt
%doc VAX/vax780_bug_history.txt


%changelog
* Sat Jan 09 2010 Lucian Langa <cooly@gnome.eu.org> - 3.8.1-5
- fix altair segfault

* Tue Nov 17 2009 Lucian Langa <cooly@gnome.eu.org> - 3.8.1-4
- add correct source

* Fri Nov 13 2009 Lucian Langa <cooly@gnome.eu.org> - 3.8.1-3
- update description

* Sun Nov 08 2009 Lucian Langa <cooly@gnome.eu.org> - 3.8.1-2
- add correct generate script

* Wed Oct 08 2009 Lucian Langa <cooly@gnome.eu.org> - 3.8.1-1
- remove separate docs
- misc cleanups
- new upstream release

* Wed Dec 24 2008 Lucian Langa <cooly@gnome.eu.org> - 3.8.0-1
- initial spec file

