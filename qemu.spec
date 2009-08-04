Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 0.10.6
Release: 1%{?dist}
# Epoch because we pushed a qemu-1.0 package
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/

Source0: http://downloads.sourceforge.net/sourceforge/kvm/qemu-kvm-%{version}.tar.gz
Source1: qemu.init
Source2: kvm.modules

Patch1: 01-tls-handshake-fix.patch
Patch2: 02-vnc-monitor-info.patch
Patch3: 03-display-keymaps.patch
Patch4: 04-vnc-struct.patch
Patch5: 05-vnc-tls-vencrypt.patch
Patch6: 06-vnc-sasl.patch
Patch7: 07-vnc-monitor-authinfo.patch
Patch8: 08-vnc-acl-mgmt.patch

Patch9: kvm-upstream-ppc.patch
Patch10: qemu-fix-debuginfo.patch
Patch11: qemu-roms-more-room.patch
Patch12: qemu-roms-more-room-fix-vga-align.patch
Patch13: qemu-bios-bigger-roms.patch
Patch14: qemu-kvm-fix-kerneldir-includes.patch
Patch15: qemu-avoid-harmless-msr-warnings.patch
Patch16: qemu-ppc-on-ppc.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: SDL-devel zlib-devel which texi2html gnutls-devel cyrus-sasl-devel
BuildRequires: rsync dev86 iasl
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}

%define qemudocdir %{_docdir}/%{name}-%{version}

%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
%ifarch %{ix86} x86_64
Requires: qemu-system-x86 = %{epoch}:%{version}-%{release}
%endif
%ifarch ppc ppc64
Requires: qemu-system-ppc = %{epoch}:%{version}-%{release}
%endif

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
%description img
QEMU is a generic and open source processor emulator which achieves a good 
emulation speed by using dynamic translation.

This package provides the command line tool for manipulating disk images

%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service
%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets

%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: etherboot-zroms-kvm
Requires: vgabios
Requires: bochs-bios >= 2.3.8-0.5
Provides: kvm = 85
Obsoletes: kvm < 85

%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-ppc
Summary: QEMU system emulator for ppc
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios-ppc
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ppc

%package system-sparc
Summary: QEMU system emulator for sparc
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for sparc

%package system-arm
Summary: QEMU system emulator for arm
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for arm

%package system-mips
Summary: QEMU system emulator for mips
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for mips

%package system-cris
Summary: QEMU system emulator for cris
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for cris

%package system-m68k
Summary: QEMU system emulator for m68k
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for m68k

%package system-sh4
Summary: QEMU system emulator for sh4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for sh4

%ifarch %{ix86} x86_64
%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvmtrace and kvm_stat.
%endif

%prep
%setup -q -n qemu-kvm-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%build
# systems like rhel build system does not have a recent enough linker so
# --build-id works. this option is used fedora 8 onwards for giving info
# to the debug packages.

build_id_available() {
 echo "int main () { return 0; }" | gcc -x c -Wl,--build-id - 2>/dev/null
}

if build_id_available; then
 extraldflags="-Wl,--build-id";
 buildldflags="VL_LDFLAGS=-Wl,--build-id"
else
 extraldflags=""
 buildldflags=""
fi

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (#495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --audio-drv-list=pa,sdl,alsa,oss \
            --disable-strip \
            --extra-ldflags=$extraldflags \
            --extra-cflags="$RPM_OPT_FLAGS"

make V=1 %{?_smp_mflags} $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean

make -C kvm/extboot extboot.bin

cd kvm/user
./configure --prefix=%{_prefix} --kerneldir=$(pwd)/../kernel/
make kvmtrace
cd ../../
%endif

./configure \
    --target-list="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
                mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu ppc-softmmu \
                ppcemb-softmmu ppc64-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu \
                i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
                armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
                mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
                sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
                sparc32plus-linux-user" \
    --prefix=%{_prefix} \
    --interp-prefix=%{_prefix}/qemu-%%M \
    --audio-drv-list=pa,sdl,alsa,oss \
    --disable-kvm \
    --disable-strip \
    --extra-ldflags=$extraldflags \
    --extra-cflags="$RPM_OPT_FLAGS"

make V=1 %{?_smp_mflags} $buildldflags

%install
rm -rf $RPM_BUILD_ROOT

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/extboot/extboot.bin $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 0755 kvm/user/kvmtrace $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/user/kvmtrace_format $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
%endif

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" install
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/qemu
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}/%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64

# the pxe etherboot images will be symlinks to the images on
# /usr/share/etherboot, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../etherboot/$2.zrom %{buildroot}%{_prefix}/share/qemu/pxe-$1.bin
}

pxe_link e1000 e1000-82542
pxe_link ne2k_pci ne
pxe_link pcnet pcnet32
pxe_link rtl8139 rtl8139
pxe_link virtio virtio-net
ln -s ../vgabios/VGABIOS-lgpl-latest.bin  %{buildroot}/%{_datadir}/%{name}/vgabios.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}/%{_datadir}/%{name}/vgabios-cirrus.bin
ln -s ../bochs/BIOS-bochs-kvm %{buildroot}/%{_datadir}/%{name}/bios.bin
ln -s ../openbios/openbios-ppc %{buildroot}/%{_datadir}/%{name}/openbios-ppc
ln -s ../openbios/openbios-sparc32 %{buildroot}/%{_datadir}/%{name}/openbios-sparc32
ln -s ../openbios/openbios-sparc64 %{buildroot}/%{_datadir}/%{name}/openbios-sparc64

%clean
rm -rf $RPM_BUILD_ROOT

%post system-x86
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh /%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

%post user
/sbin/chkconfig --add qemu

%preun user
if [ $1 -eq 0 ]; then
    /sbin/service qemu stop &>/dev/null || :
    /sbin/chkconfig --del qemu
fi

%postun user
if [ $1 -ge 1 ]; then
    /sbin/service qemu condrestart &>/dev/null || :
fi

%files 
%defattr(-,root,root)

%files kvm
%defattr(-,root,root)

%files common
%defattr(-,root,root)
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html 
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/COPYING 
%doc %{qemudocdir}/COPYING.LIB 
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%{_bindir}/qemu-nbd
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%files user
%defattr(-,root,root)
%{_sysconfdir}/rc.d/init.d/qemu
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-sparc32plus
%files system-x86
%defattr(-,root,root)
%{_bindir}/qemu
%{_bindir}/qemu-system-x86_64
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/pxe-e1000.bin
%{_datadir}/%{name}/pxe-virtio.bin
%{_datadir}/%{name}/pxe-pcnet.bin
%{_datadir}/%{name}/pxe-rtl8139.bin
%{_datadir}/%{name}/pxe-ne2k_pci.bin
%ifarch %{ix86} x86_64
%{_datadir}/%{name}/extboot.bin
%{_bindir}/qemu-kvm
%{_sysconfdir}/sysconfig/modules/kvm.modules
%files kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvmtrace
%{_bindir}/kvmtrace_format
%{_bindir}/kvm_stat
%endif
%files system-sparc
%defattr(-,root,root)
%{_bindir}/qemu-system-sparc
%{_datadir}/%{name}/openbios-sparc32
%{_datadir}/%{name}/openbios-sparc64
%files system-arm
%defattr(-,root,root)
%{_bindir}/qemu-system-arm
%files system-mips
%defattr(-,root,root)
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%files system-ppc
%defattr(-,root,root)
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/%{name}/openbios-ppc
%{_datadir}/%{name}/video.x
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%files system-cris
%defattr(-,root,root)
%{_bindir}/qemu-system-cris
%files system-m68k
%defattr(-,root,root)
%{_bindir}/qemu-system-m68k
%files system-sh4
%defattr(-,root,root)
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%changelog
* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.6-1
- Update to qemu-kvm-0.10.6; upstream ChangeLog:
   - merge qemu 0.10.6
      - fix -net socket,listen
      - live migration: don't send gratuitous packets all at once
      - serial: fix lost characters after sysrq
      - Delete io-handler before closing fd after migration
      - Fix qemu_aio_flush
      - i386: fix cpu reset
      - Prevent CD-ROM eject while device is locked
      - Fix migration after hot remove with eepro100
      - Don't start a VM after failed migration if stopped
      - Fix live migration under heavy IO load
      - Honor -S on incoming migration
      - Reset PS2 keyboard/mouse on reset
   - build and install extboot
- Drop upstreamed qemu-prevent-cdrom-media-eject-while-device-is-locked.patch
  and qemu-fix-net-socket-list-init.patch and

* Wed Jun 17 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.5-3
- ppc-on-ppc fix (#504273)
- Fix -kernel regression (#506443)

* Wed Jun  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.5-2
- Prevent locked cdrom eject - fixes hang at end of anaconda installs (#501412)
- Fix crash with '-net socket,listen=...' (#501264)
- Avoid harmless 'unhandled wrmsr' warnings (#499712)

* Sun May 31 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.5-1
- Update to 0.10.5, and remove already upstream patches
    qemu-fix-gcc.patch
    qemu-fix-load-linux.patch
    qemu-dma-aio-cancellation1.patch
    qemu-dma-aio-cancellation2.patch
    qemu-dma-aio-cancellation3.patch
    qemu-dma-aio-cancellation4.patch
    + all cpuid trimming

  Conflicts:
    qemu-roms-more-room.patch

* Mon May 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.4-5
- Backport cpuid trimming from upstream (#499596)

* Thu May 14 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.4-4
- Cherry pick more DMA AIO cancellation fixes from upstream (#497170)

* Wed May 13 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.4-3
- Fix mixup between kvm.modules and the init script (reported by Rich Jones)

* Wed May 13 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.4-2
- Fix -kernel bustage in upstream 0.10.4

* Tue May 12 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.4-1
- Update to 0.10.4
- Fix yet more qcow2 corruption (#498405)
- AIO cancellation fixes (#497170)
- Fix VPC image size overflow (#491981)
- Fix oops with 2.6.25 virtio guest (#470386)
- Enable pulseaudio driver (#495964, #496627)
- Fix cpuid initialization
- Fix HPET emulation
- Fix storage hotplug error handling
- Migration fixes
- Block range checking fixes
- Make PCI config status register read-only
- Handle newer Xorg keymap names
- Don't leak memory on NIC hot-unplug
- Hook up keypad keys for qemu console emulation
- Correctly run on kernels lacking mmu notifiers
- Support DDIM option ROMs
- Fix PCI NIC error handling
- Fix in-kernel LAPIC initialization
- Fix broken e1000 PCI config space
- Drop some patches which have been upstreamed
- Drop the make-release script; we have an official tarball now

* Tue May 12 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-18
- move option rom setup function to the beginning of the file. This
  avoids static vs non-static issues, and is the way upstream does

* Tue May 12 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-17
- fix reboot with -kernel parameter (#499666)

* Fri May  1 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-16
- Really provide qemu-kvm as a metapackage

* Fri Apr 27 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-15
- provide qemu-kvm as a metapackage

* Fri Apr 24 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-14
- Fix source numbering typos caused by make-release addition

* Thu Apr 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-13
- Improve instructions for generating the tarball

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-12
- Another qcow2 image corruption fix (#496642)

* Mon Apr 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-11
- Fix qcow2 image corruption (#496642)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-10
- Run sysconfig.modules from %post on x86_64 too (#494739)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-9
- Align VGA ROM to 4k boundary - fixes 'qemu-kvm -std vga' (#494376)

* Tue Apr  14 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-8
- Provide qemu-kvm conditional on the architecture.

* Thu Apr  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-7
- Add a much cleaner fix for vga segfault (#494002)

* Sun Apr  5 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-6
- Fixed qcow2 segfault creating disks over 2TB. #491943

* Fri Apr  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-5
- Fix vga segfault under kvm-autotest (#494002)
- Kill kernelrelease hack; it's not needed
- Build with "make V=1" for more verbose logs

* Thu Apr 02 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-4
- Support botting gpxe roms.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-2
- added missing patch. love for CVS.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-1
- Include debuginfo for qemu-img
- Do not require qemu-common for qemu-img
- Explicitly own each of the firmware files
- remove firmwares for ppc and sparc. They should be provided by an external package.
  Not that the packages exists for sparc in the secondary arch repo as noarch, but they
  don't automatically get into main repos. Unfortunately it's the best we can do right
  now.
- rollback a bit in time. Snapshot from avi's maint/2.6.30
  - this requires the sasl patches to come back.
  - with-patched-kernel comes back.

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-0.12.kvm20090323git
- BuildRequires pciutils-devel for device assignment (#492076)

* Mon Mar 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.11.kvm20090323git
- Update to snapshot kvm20090323.
- Removed patch2 (upstream).
- use upstream's new split package.
- --with-patched-kernel flag not needed anymore
- Tell how to get the sources.

* Wed Mar 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.10.kvm20090310git
- Added extboot to files list.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.9.kvm20090310git
- Fix wrong reference to bochs bios.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.8.kvm20090310git
- fix Obsolete/Provides pair
- Use kvm bios from bochs-bios package.
- Using RPM_OPT_FLAGS in configure
- Picked back audio-drv-list from kvm package

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.7.kvm20090310git
- modify ppc patch

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.6.kvm20090310git
- updated to kvm20090310git
- removed sasl patches (already in this release)

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.5.kvm20090303git
- kvm.modules were being wrongly mentioned at %%install.
- update description for the x86 system package to include kvm support
- build kvm's own bios. It is still necessary while kvm uses a slightly different
  irq routing mechanism

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.4.kvm20090303git
- seems Epoch does not go into the tags. So start back here.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.1.kvm20090303git
- Use bochs-bios instead of bochs-bios-data
- It's official: upstream set on 0.10

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.9.2-0.2.kvm20090303git
- Added BSD to license list, since many files are covered by BSD

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.9.2-0.1.kvm20090303git
- missing a dot. shame on me

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.92-0.1.kvm20090303git
- Set Epoch to 2
- Set version to 0.92. It seems upstream keep changing minds here, so pick the lowest
- Provides KVM, Obsoletes KVM
- Only install qemu-kvm in ix86 and x86_64
- Remove pkgdesc macros, as they were generating bogus output for rpm -qi.
- fix ppc and ppc64 builds

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.3.kvm20090303git
- only execute post scripts for user package.
- added kvm tools.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.2.kvm20090303git
- put kvm.modules into cvs

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.1.kvm20090303git
- Set Epoch to 1
- Build KVM (basic build, no tools yet)
- Set ppc in ExcludeArch. This is temporary, just to fix one issue at a time.
  ppc users (IBM ? ;-)) please wait a little bit.

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0-0.5.svn6666
- Support VNC SASL authentication protocol
- Fix dep on bochs-bios-data

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.4.svn6666
- use bios from bochs-bios package.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.3.svn6666
- use vgabios from vgabios package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.2.svn6666
- use pxe roms from etherboot package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.1.svn6666
- Updated to tip svn (release 6666). Featuring split packages for qemu.
  Unfortunately, still using binary blobs for the bioses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.9.1-12
- Updated build patch. Closes Red Hat Bugzilla bug #465041.

* Wed Dec 31 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-11
- add sparcv9 and sparc64 support

* Fri Jul 25 2008 Bill Nottingham <notting@redhat.com>
- Fix qemu-img summary (#456344)

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-10.fc10
- Rebuild for GNU TLS ABI change

* Wed Jun 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-9.fc10
- Remove bogus wildcard from files list (rhbz #450701)

* Sat May 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-8
- Register binary handlers also for shared libraries

* Mon May  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-7.fc10
- Fix text console PTYs to be in rawmode

* Sun Apr 27 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.9.1-6
- Register binary handler for SuperH-4 CPU

* Wed Mar 19 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-5.fc9
- Split qemu-img tool into sub-package for smaller footprint installs

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-4.fc9
- Fix block device checks for extendable disk formats (rhbz #435139)

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-3.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-2
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-1.fc9
- Updated to 0.9.1 release
- Fix license tag syntax
- Don't mark init script as a config file

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-5.fc8
- Fix rtl8139 checksum calculation for Vista (rhbz #308201)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-4.fc8
- Fix debuginfo by passing -Wl,--build-id to linker

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-4
- Update licence
- Fix CDROM emulation (#253542)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-3.fc8
- Added backport of VNC password auth, and TLS+x509 cert auth
- Switch to rtl8139 NIC by default for linkstate reporting
- Fix rtl8139 mmio region mappings with multiple NICs

* Sun Apr  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.0-2
- Fix direct loading of a linux kernel with -kernel & -initrd (bz 234681)
- Remove spurious execute bits from manpages (bz 222573)

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-1
- Update to 0.9.0

* Wed Jan 31 2007 David Woodhouse <dwmw2@infradead.org> 0.8.2-5
- Include licences

* Mon Nov 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.2-4
- Backport patch to make FC6 guests work by Kevin Kofler
  <Kevin@tigcc.ticalc.org> (bz 207843).

* Mon Sep 11 2006 David Woodhouse <dwmw2@infradead.org> 0.8.2-3
- Rebuild

* Thu Aug 24 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-2
- Remove the target-list iteration for x86_64 since they all build again.
- Make gcc32 vs. gcc34 conditional on %%{fedora} to share the same spec for
  FC5 and FC6.

* Wed Aug 23 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-1
- Update to 0.8.2 (#200065).
- Drop upstreamed syscall-macros patch2.
- Put correct scriplet dependencies.
- Force install mode for the init script to avoid umask problems.
- Add %%postun condrestart for changes to the init script to be applied if any.
- Update description with the latest "about" from the web page (more current).
- Update URL to qemu.org one like the Source.
- Add which build requirement.
- Don't include texi files in %%doc since we ship them in html.
- Switch to using gcc34 on devel, FC5 still has gcc32.
- Add kernheaders patch to fix linux/compiler.h inclusion.
- Add target-sparc patch to fix compiling on ppc (some int32 to float).

* Thu Jun  8 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-3
- More header abuse in modify_ldt(), change BuildRoot:

* Wed Jun  7 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-2
- Fix up kernel header abuse

* Tue May 30 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-1
- Update to 0.8.1

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-6
- Update linker script for PPC

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-5
- Just drop $RPM_OPT_FLAGS. They're too much of a PITA

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-4
- Disable stack-protector options which gcc 3.2 doesn't like

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-3
- Use -mcpu= instead of -mtune= on x86_64 too
- Disable SPARC targets on x86_64, because dyngen doesn't like fnegs

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-2
- Don't use -mtune=pentium4 on i386. GCC 3.2 doesn't like it

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-1
- Update to 0.8.0
- Resort to using compat-gcc-32
- Enable ALSA

* Mon May 16 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-2
- Proper fix for GCC 4 putting 'blr' or 'ret' in the middle of the function,
  for i386, x86_64 and PPC.

* Sat Apr 30 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-1
- Update to 0.7.0
- Fix dyngen for PPC functions which end in unconditional branch

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Mon May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Thu May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
