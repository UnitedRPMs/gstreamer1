
%global         majorminor      1.0

%global commit0 6fa03dd1515ff980f3d06e4c0b92555d47b34c40
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define _legacy_common_support 1


%global         _glib2                  2.32.0
%global         _libxml2                2.4.0
%global         _gobject_introspection  1.31.1

%global debug_package %{nil}

Name:           gstreamer1
Version:        1.19.1
Release:        7%{?gver}%{dist}
Summary:        GStreamer streaming media framework runtime

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0: 	https://github.com/GStreamer/gstreamer/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  gobject-introspection-devel 
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  m4
BuildRequires:  check-devel
BuildRequires:  gtk-doc >= 1.3
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:	make
BuildRequires:	ninja-build

BuildRequires:  chrpath

### documentation requirements
#BuildRequires:  python2
BuildRequires:  openjade
#BuildRequires:  jadetex
BuildRequires:  libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  transfig
BuildRequires:  netpbm-progs
#BuildRequires:  tetex-dvips
BuildRequires:  ghostscript
BuildRequires:	gettext-devel
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
%if !0%{?rhel}
BuildRequires:  xfig
%endif
# New
BuildRequires: meson
BuildRequires: libunwind-devel
BuildRequires: cmake
BuildRequires: pkgconfig(libdw)
BuildRequires: bash-completion
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: libcap-devel 
BuildRequires: gmp-devel 
BuildRequires: valgrind-devel 
BuildRequires: gsl-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.


%package devel
Summary:        Libraries/include files for GStreamer streaming media framework
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel >= %{_glib2}
Requires:       libxml2-devel >= %{_libxml2}
Requires:       check-devel


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package devel-docs
Summary:         Developer documentation for GStreamer streaming media framework
Requires:        %{name} = %{version}-%{release}
BuildArch:       noarch


%description devel-docs
This %{name}-devel-docs contains developer documentation for the
GStreamer streaming media framework.


%prep
%autosetup -n gstreamer-%{commit0}  -p1
rm -rf common && git clone git://anongit.freedesktop.org/gstreamer/common 

sed -i "s/^executable('gst-plugin-scanner',/executable('gst-plugin-scanner-%{_target_cpu}',/" libs/gst/helpers/meson.build
sed -i "s/gst-plugin-scanner/gst-plugin-scanner-%{_target_cpu}/" meson.build

%build

export LIBS=-lcxa

%meson -D ptp-helper-permissions=capabilities \
    -D dbghelp=disabled \
    -D examples=disabled \
    -D benchmarks=disabled \
    -D tests=disabled \
    -D doc=disabled \
    -D gobject-cast-checks=disabled \
    -D package-name="UnitedRPMs GStreamer package" \
    -D package-origin="https://unitedrpms.github.io/"

%meson_build 

%install
%meson_install 

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstbase-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcheck-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcontroller-1.0.so.* 
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstnet-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gstreamer-%{majorminor}/gst-ptp-helper
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-inspect-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-launch-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-typefind-1.0

%find_lang gstreamer-%{majorminor}
# Clean out files that should not be part of the rpm.
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

# Mangling fix
#sed -i '1 i\#!/usr/bin/python2' $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/%{_lib}/libgstreamer*-gdb.py
#sed -i '1 i\#!/usr/bin/python2' $RPM_BUILD_ROOT%{_datadir}/gstreamer-1.0/gdb/glib_gobject_helper.py
#sed -i '1 i\#!/usr/bin/python2' $RPM_BUILD_ROOT%{_datadir}/gstreamer-1.0/gdb/gst_gdb.py
#sed -i 's|/usr/bin/env python|/usr/bin/python3|g' $RPM_BUILD_ROOT/usr/libexec/gstreamer-1.0/gst-plugins-doc-cache-generator

%files -f gstreamer-%{majorminor}.lang
%license COPYING
%doc AUTHORS NEWS README RELEASE
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcheck-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*

%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so

%{_libdir}/girepository-1.0/Gst-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstBase-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstController-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstNet-%{majorminor}.typelib

%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_bindir}/gst-stats-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoretracers.so


%{_datadir}/gdb/auto-load/usr/%{_lib}/libgstreamer*-gdb.py
%{_datadir}/gstreamer-1.0/gdb/glib_gobject_helper.py
%{_datadir}/gstreamer-1.0/gdb/gst_gdb.py


%doc %{_mandir}/man1/gst-inspect-%{majorminor}.*
%doc %{_mandir}/man1/gst-launch-%{majorminor}.*
%doc %{_mandir}/man1/gst-typefind-%{majorminor}.*
%doc %{_mandir}/man1/gst-stats-%{majorminor}.*


%{_datadir}/bash-completion/completions/gst-inspect-1.0
%{_datadir}/bash-completion/completions/gst-launch-1.0
%{_datadir}/bash-completion/helpers/gst
# {_datadir}/bash-completion/helpers/gst-completion-helper-1.0

%files devel
%dir %{_includedir}/gstreamer-%{majorminor}
%dir %{_includedir}/gstreamer-%{majorminor}/gst
%dir %{_includedir}/gstreamer-%{majorminor}/gst/base
%dir %{_includedir}/gstreamer-%{majorminor}/gst/check
%dir %{_includedir}/gstreamer-%{majorminor}/gst/controller
%dir %{_includedir}/gstreamer-%{majorminor}/gst/net
%{_includedir}/gstreamer-%{majorminor}/gst/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/base/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/check/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/controller/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/net/*.h

%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so

%{_datadir}/gir-1.0/Gst-%{majorminor}.gir
%{_datadir}/gir-1.0/GstBase-%{majorminor}.gir
%{_datadir}/gir-1.0/GstCheck-%{majorminor}.gir
%{_datadir}/gir-1.0/GstController-%{majorminor}.gir
%{_datadir}/gir-1.0/GstNet-%{majorminor}.gir

%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4

%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc

%files devel-docs
%doc AUTHORS ChangeLog NEWS README RELEASE


%changelog

* Sun Jun 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.1-7.git6fa03dd
- Updated to 1.19.1

* Mon Apr 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.4-7.giteacb7aa
- Updated to 1.18.4

* Mon Jan 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.3-7.gita42fe47
- Updated to 1.18.3

* Mon Dec 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.2-7.git6a62351
- Updated to 1.18.2

* Thu Oct 29 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-7.git29a8099
- Updated to 1.18.1

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.0-7.git96148da
- Updated to 1.18.0

* Sun Sep 06 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-8.gite97c520
- Rebuilt

* Tue Aug 25 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-7.gite97c520
- Updated to 1.17.90

* Fri Jul 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.2-7.git61ed49f
- Updated to 1.17.2

* Sun Mar 22 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-8.git1294936
- Migration to meson

* Wed Dec 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-7.git1294936
- Updated to 1.16.2-7.git1294936

* Wed Sep 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.1-7.gitde0a7c4
- Updated to 1.16.1-7.gitde0a7c4

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-7.git89c221a
- Updated to 1.16.0-7.git89c221a

* Tue Apr 16 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.90-7.gitcd7075d
- Updated to 1.15.90-7.gitcd7075d

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-7.git0dd0a29
- Updated to 1.15.2-7.git0dd0a29

* Thu Jan 17 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.1-7.git6ea4380
- Updated to 1.15.1-7.git6ea4380

* Wed Oct 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.4-7.git3c586de
- Updated to 1.14.4-7.git3c586de

* Mon Sep 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-7.git86a4803
- Updated to 1.14.3-7.gita86a4803

* Fri Jul 20 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.2-7.gitafb3d1b
- Updated to 1.14.2-7.gitafb3d1b

* Mon May 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.1-7.gitcba2c7d 
- Updated to 1.14.1-7.gitcba2c7d

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.0-7.git80e0e90 
- Updated to 1.14.0-7.git80e0e90

* Fri Mar 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.91-7.gitbc431c2  
- Updated to 1.13.91-7.gitbc431c2

* Sun Mar 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.90-7.git87be91a  
- Updated to 1.13.90-7.git87be91a

* Fri Dec 8 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.4-7.git505a24f  
- Updated to 1.12.4-7.git505a24f

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.3-7.gita6653b6  
- Updated to 1.12.3-7.gita6653b6  

* Fri Aug 25 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.12.2-5.gitdca812c  
- Automatic Mass Rebuild

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-2.gitdca812c
- Updated 1.12.2-2.gitdca812c

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.1-2.gitab3f333
- Updated to 1.12.1-2.gitab3f333

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> 1.12.0-2.git7854a65
- Updated to 1.12.0-2.git7854a65

* Sat Apr 29 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.91-2.gita0d2f0a
- Updated to 1.11.91-2.gita0d2f0a

* Thu Apr 20 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.90-2.20170420git4704799
- Updated to 1.11.90-2.20170420git4704799

* Fri Jan 27 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-1.20170224gite4a7200
- Updated to 1.11.2-1.20170224gite4a7200

* Fri Jan 27 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.1-1.20170202git4b7a521
- Updated to 1.11.1-1.20170202git4b7a521

* Sat Oct 15 2016 David Vásquez <davidva AT tutanota DOT com> 1.9.90-1
- Updated to 1.9.90

* Thu Oct 06 2016 David Vásquez <davidva AT tutanota DOT com> 1.9.2-1
- Updated to 1.9.2

* Fri Jul 08 2016 David Vásquez <davidva AT tutanota DOT com> 1.9.1-1
- Updated to 1.9.1

* Thu Jun 23 2016 David Vásquez <davidva AT tutanota DOT com> 1.8.2-1
- Updated

* Wed Apr 20 2016 David Vásquez <davidva AT tutanota DOT com> 1.8.1-1
- Updated to 1.8.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-2
- Remove lib64 rpaths from newly added binaries

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Use license macro for COPYING

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- add new bash-completion scripts
- gstconfig.h got moved

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4.5-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91

* Mon Jun 30 2014 Richard Hughes <rhughes@redhat.com> - 1.3.90-1
- Update to 1.3.90

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4.

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com>
- Tweak BRs for RHEL

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Remove BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Sep  8 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Add patch to gst-inspect to generate RPM provides
- Add RPM find-provides script

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Bump minimum version of glib2 needed.

* Fri Aug  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Use %%global instead of %%define.
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.

