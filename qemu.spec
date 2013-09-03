# build-time settings that support --with or --without:
#
# = kvmonly =
# Build only KVM-enabled QEMU targets, on KVM-enabled architectures.
#
# Disabled by default.
#
# = exclusive_x86_64 =
# ExclusiveArch: x86_64
#
# Disabled by default, except on RHEL.  Only makes sense with kvmonly.
#
# = rbd =
# Enable rbd support.
#
# Enable by default, except on RHEL.
#
# = separate_kvm =
# Do not build and install stuff that would colide with separately packaged KVM.
#
# Disabled by default, except on EPEL.

%if 0%{?rhel}
# RHEL-specific defaults:
%bcond_without kvmonly          # enabled
%bcond_without exclusive_x86_64 # enabled
%bcond_with    rbd              # disabled
%bcond_without spice            # enabled
%bcond_without seccomp          # enabled
%bcond_with    xfsprogs         # disabled
%bcond_with    separate_kvm     # disabled - for EPEL
%else
# General defaults:
%bcond_with    kvmonly          # disabled
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without spice            # enabled
%bcond_without seccomp          # enabled
%bcond_without xfsprogs         # enabled
%bcond_with    separate_kvm     # disabled
%endif

%global SLOF_gittagdate 20121018

%if %{without separate_kvm}
%global kvm_archs %{ix86} x86_64 ppc64 s390x
%else
%global kvm_archs %{ix86} ppc64 s390x
%endif
%if %{with exclusive_x86_64}
%global kvm_archs x86_64
%endif


%global have_usbredir 1

%ifarch %{ix86} x86_64
%if %{with seccomp}
%global have_seccomp 1
%endif
%if %{with spice}
%global have_spice   1
%endif
%else
%if 0%{?rhel}
%global have_usbredir 0
%endif
%endif

%global need_qemu_kvm %{with kvmonly}
%global need_kvm_modfile 0

# These values for system_xyz are overridden below for non-kvmonly builds.
# Instead, these values for kvm_package are overridden below for kvmonly builds.
# Somewhat confusing, but avoids complicated nested conditionals.

%ifarch %{ix86}
%global system_x86    kvm
%global kvm_package   system-x86
%global kvm_target    i386
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global system_x86    kvm
%global kvm_package   system-x86
%global kvm_target    x86_64
%global need_qemu_kvm 1
%endif
%ifarch ppc64
%global system_ppc    kvm
%global kvm_package   system-ppc
%global kvm_target    ppc64
%global need_kvm_modfile 1
%endif
%ifarch s390x
%global system_s390x  kvm
%global kvm_package   system-s390x
%global kvm_target    s390x
%global need_kvm_modfile 1
%endif

%if %{with kvmonly}
# If kvmonly, put the qemu-kvm binary in the qemu-kvm package
%global kvm_package   kvm
%else
# If not kvmonly, build all packages and give them normal names. qemu-kvm
# is a simple wrapper package and is only build for archs that support KVM.
%global user          user
%global system_alpha  system-alpha
%global system_arm    system-arm
%global system_cris   system-cris
%global system_lm32   system-lm32
%global system_m68k   system-m68k
%global system_microblaze   system-microblaze
%global system_mips   system-mips
%global system_or32   system-or32
%global system_ppc    system-ppc
%global system_s390x  system-s390x
%global system_sh4    system-sh4
%global system_sparc  system-sparc
%global system_x86    system-x86
%global system_xtensa   system-xtensa
%global system_unicore32   system-unicore32
%endif

# libfdt is only needed to build ARM, Microblaze or PPC emulators
%if 0%{?system_arm:1}%{?system_microblaze:1}%{?system_ppc:1}
%global need_fdt      1
%endif

Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 1.4.2
Release: 8%{?dist}
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
# RHEL will build Qemu only on x86_64:
%if %{with kvmonly}
ExclusiveArch: %{kvm_archs}
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%define _smp_mflags %{nil}
%endif

Source0: http://wiki.qemu-project.org/download/%{name}-%{version}.tar.bz2


Source1: qemu.binfmt

# Loads kvm kernel modules at boot
Source2: kvm.modules

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules
Source12: bridge.conf

# qemu-kvm back compat wrapper
Source13: qemu-kvm.sh

# Flow control series
Patch0001: 0001-char-Split-out-tcp-socket-close-code-in-a-separate-f.patch
Patch0002: 0002-char-Add-a-QemuChrHandlers-struct-to-initialise-char.patch
Patch0003: 0003-iohandlers-Add-enable-disable_write_fd_handler-funct.patch
Patch0004: 0004-char-Add-framework-for-a-write-unblocked-callback.patch
Patch0005: 0005-char-Update-send_all-to-handle-nonblocking-chardev-w.patch
Patch0006: 0006-char-Equip-the-unix-tcp-backend-to-handle-nonblockin.patch
Patch0007: 0007-virtio-console-Enable-port-throttling-when-chardev-i.patch
Patch0008: 0008-spice-qemu-char.c-add-throttling.patch
Patch0009: 0009-spice-qemu-char.c-remove-intermediate-buffer.patch
Patch0010: 0010-usb-redir-Add-flow-control-support.patch
Patch0011: 0011-char-Disable-write-callback-if-throttled-chardev-is-.patch
Patch0012: 0012-hw-virtio-serial-bus-replay-guest-open-on-destinatio.patch

# Fix migration crash with spice (bz #962954)
Patch0101: 0101-vnc-tls-Fix-compilation-with-newer-versions-of-GNU-T.patch
Patch0102: 0102-migration-change-initial-value-of-expected_downtime.patch
Patch0103: 0103-migration-calculate-end-time-after-we-have-sent-the-.patch
Patch0104: 0104-migration-don-t-account-sleep-time-for-calculating-b.patch
Patch0105: 0105-migration-calculate-expected_downtime.patch
Patch0106: 0106-migration-simplify-while-loop.patch
Patch0107: 0107-migration-always-use-vm_stop_force_state.patch
Patch0108: 0108-migration-move-more-error-handling-to-migrate_fd_cle.patch
Patch0109: 0109-migration-push-qemu_savevm_state_cancel-out-of-qemu_.patch
Patch0110: 0110-block-migration-remove-useless-calls-to-blk_mig_clea.patch
Patch0111: 0111-qemu-file-pass-errno-from-qemu_fflush-via-f-last_err.patch
Patch0112: 0112-migration-use-qemu_file_set_error-to-pass-error-code.patch
Patch0113: 0113-qemu-file-temporarily-expose-qemu_file_set_error-and.patch
Patch0114: 0114-migration-flush-all-data-to-fd-when-buffered_flush-i.patch
Patch0115: 0115-migration-use-qemu_file_set_error.patch
Patch0116: 0116-migration-simplify-error-handling.patch
Patch0117: 0117-migration-do-not-nest-flushing-of-device-data.patch
Patch0118: 0118-migration-add-migrate_set_state-tracepoint.patch
Patch0119: 0119-migration-prepare-to-access-s-state-outside-critical.patch
Patch0120: 0120-migration-cleanup-migration-including-thread-in-the-.patch
Patch0121: 0121-block-migration-remove-variables-that-are-never-read.patch
Patch0122: 0122-block-migration-small-preparatory-changes-for-lockin.patch
Patch0123: 0123-block-migration-document-usage-of-state-across-threa.patch
Patch0124: 0124-block-migration-add-lock.patch
Patch0125: 0125-migration-reorder-SaveVMHandlers-members.patch
Patch0126: 0126-migration-run-pending-iterate-callbacks-out-of-big-l.patch
Patch0127: 0127-migration-run-setup-callbacks-out-of-big-lock.patch
Patch0128: 0128-migration-yay-buffering-is-gone.patch
Patch0129: 0129-Rename-buffered_-to-migration_.patch
Patch0130: 0130-qemu-file-make-qemu_fflush-and-qemu_file_set_error-p.patch
Patch0131: 0131-migration-eliminate-last_round.patch
Patch0132: 0132-migration-detect-error-before-sleeping.patch
Patch0133: 0133-migration-remove-useless-qemu_file_get_error-check.patch
Patch0134: 0134-migration-use-qemu_file_rate_limit-consistently.patch
Patch0135: 0135-migration-merge-qemu_popen_cmd-with-qemu_popen.patch
Patch0136: 0136-qemu-file-fsync-a-writable-stdio-QEMUFile.patch
Patch0137: 0137-qemu-file-check-exit-status-when-closing-a-pipe-QEMU.patch
Patch0138: 0138-qemu-file-add-writable-socket-QEMUFile.patch
Patch0139: 0139-qemu-file-simplify-and-export-qemu_ftell.patch
Patch0140: 0140-migration-use-QEMUFile-for-migration-channel-lifetim.patch
Patch0141: 0141-migration-use-QEMUFile-for-writing-outgoing-migratio.patch
Patch0142: 0142-migration-use-qemu_ftell-to-compute-bandwidth.patch
Patch0143: 0143-migration-small-changes-around-rate-limiting.patch
Patch0144: 0144-migration-move-rate-limiting-to-QEMUFile.patch
Patch0145: 0145-migration-move-contents-of-migration_close-to-migrat.patch
Patch0146: 0146-migration-eliminate-s-migration_file.patch
Patch0147: 0147-migration-inline-migrate_fd_close.patch
Patch0148: 0148-Revert-migration-don-t-account-sleep-time-for-calcul.patch

# 917860 libcacard and qemu/hw/ccid windows 7 smartcard support.
Patch0201: 0201-configure-Add-enable-migration-from-qemu-kvm.patch
Patch0202: 0202-acpi_piix4-Drop-minimum_version_id-to-handle-qemu-kv.patch
Patch0203: 0203-i8254-Fix-migration-from-qemu-kvm-1.1.patch
Patch0204: 0204-pc_piix-Add-compat-handling-for-qemu-kvm-VGA-mem-siz.patch
Patch0205: 0205-qxl-Add-rom_size-compat-property-fix-migration-from-.patch
Patch0206: 0206-rtl8139-flush-queued-packets-when-RxBufPtr-is-writte.patch
Patch0207: 0207-spice-qemu-char-vmc_write-Don-t-write-more-bytes-the.patch
Patch0208: 0208-configure-dtc-Probe-for-libfdt_env.h.patch
Patch0209: 0209-Fix-usage-of-USB_DEV_FLAG_IS_HOST-flag.patch
Patch0210: 0210-qxl-Fix-QXLRam-initialisation.patch
Patch0211: 0211-qemu-socket-Make-socket_optslist-public.patch
Patch0212: 0212-libcacard-correct-T0-historical-bytes-size.patch
Patch0213: 0213-ccid-card-emul-do-not-crash-if-backend-is-not-provid.patch
Patch0214: 0214-ccid-make-backend_enum_table-static-const-and-adjust.patch
Patch0215: 0215-ccid-declare-DEFAULT_ATR-table-to-be-static-const.patch
Patch0216: 0216-libcacard-use-system-config-directory-for-nss-db-on-.patch
Patch0217: 0217-util-move-socket_init-to-osdep.c.patch
Patch0218: 0218-build-sys-must-link-with-fstack-protector.patch
Patch0219: 0219-libcacard-fix-mingw64-cross-compilation.patch
Patch0220: 0220-libcacard-split-vscclient-main-from-socket-reading.patch
Patch0221: 0221-libcacard-vscclient-to-use-QemuThread-for-portabilit.patch
Patch0222: 0222-libcacard-teach-vscclient-to-use-GMainLoop-for-porta.patch
Patch0223: 0223-libcacard-remove-sql-prefix.patch
Patch0224: 0224-libcacard-remove-default-libcoolkey-loading.patch
Patch0225: 0225-dev-smartcard-reader-white-space-fixes.patch
Patch0226: 0226-dev-smartcard-reader-nicer-debug-messages.patch
Patch0227: 0227-dev-smartcard-reader-remove-aborts-never-triggered-b.patch
Patch0228: 0228-dev-smartcard-reader-support-windows-guest.patch
Patch0229: 0229-dev-smartcard-reader-reuse-usb.h-definitions.patch
Patch0230: 0230-libcacard-change-default-ATR.patch
Patch0231: 0231-ccid-card-passthru-add-atr-check.patch

# qemu-kvm migration compat (posted upstream)
Patch0301: 0301-ccid-card-passthru-dev-smartcard-reader-add-debug-en.patch
Patch0302: 0302-dev-smartcard-reader-define-structs-for-CCID_Paramet.patch
Patch0303: 0303-dev-smartcard-reader-change-default-protocol-to-T-0.patch
Patch0304: 0304-dev-smartcard-reader-copy-atr-protocol-to-ccid-param.patch
Patch0305: 0305-libcacard-vreader-add-debugging-messages-for-apdu.patch
# Fix rtl8139 + windows 7 + large transfers (bz #970240)
Patch0306: 0306-libcacard-move-atr-setting-from-macro-to-function.patch
# Fix crash on large drag and drop file transfer w/ spice (bz #969109)
Patch0307: 0307-dev-smartcard-reader-empty-implementation-for-Mechan.patch
# Fix build with latest libfdt
Patch0308: 0308-libcacard-cac-change-big-switch-functions-to-single-.patch
# Fix usb_handle_packet assertions (bz #981459)
Patch0309: 0309-libcacard-vscclient-fix-leakage-of-socket-on-error-p.patch
# Fix crash when adding spice vdagent channel in the guest (bz #969084)
Patch0310: 0310-libcacard-Fix-cppcheck-warning-and-remove-unneeded-c.patch
# Fix crash with -M isapc -cpu Haswell (bz #986790)
Patch0311: 0311-isapc-disable-kvmvapic.patch
# Fix crash in lsi_soft_reset (bz #1000947)
# Patches posted upstream
Patch0312: 0312-pci-do-not-export-pci_bus_reset.patch
Patch0313: 0313-qdev-allow-both-pre-and-post-order-vists-in-qdev-wal.patch
Patch0314: 0314-qdev-switch-reset-to-post-order.patch
# Fix crash in scsi_dma_complete (bz #1001617)
Patch0315: 0315-scsi-avoid-assertion-failure-on-VERIFY-command.patch

BuildRequires: SDL-devel
BuildRequires: zlib-devel
BuildRequires: which
BuildRequires: texi2html
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libiscsi-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
%if 0%{?have_usbredir:1}
BuildRequires: usbredir-devel >= 0.5.2
%endif
BuildRequires: texinfo
# for /usr/bin/pod2man
%if 0%{?fedora} > 18
BuildRequires: perl-podlators
%endif
%if 0%{?have_spice:1}
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
BuildRequires: libseccomp-devel >= 1.0.0
%endif
# For network block driver
BuildRequires: libcurl-devel
%if %{with rbd}
# For rbd block driver
BuildRequires: ceph-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
%if %{with xfsprogs}
BuildRequires: xfsprogs-devel
%endif
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
%if 0%{?need_fdt:1}
# For FDT device tree support
BuildRequires: libfdt-devel
%endif
# For test suite
BuildRequires: check-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
%if 0%{?fedora} > 18
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
%endif

%if 0%{?user:1}
Requires: %{name}-%{user} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_alpha:1}
Requires: %{name}-%{system_alpha} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_arm:1}
Requires: %{name}-%{system_arm} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_cris:1}
Requires: %{name}-%{system_cris} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_lm32:1}
Requires: %{name}-%{system_lm32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_m68k:1}
Requires: %{name}-%{system_m68k} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_microblaze:1}
Requires: %{name}-%{system_microblaze} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_mips:1}
Requires: %{name}-%{system_mips} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_or32:1}
Requires: %{name}-%{system_or32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_ppc:1}
Requires: %{name}-%{system_ppc} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_s390x:1}
Requires: %{name}-%{system_s390x} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_sh4:1}
Requires: %{name}-%{system_sh4} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_sparc:1}
Requires: %{name}-%{system_sparc} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_unicore32:1}
Requires: %{name}-%{system_unicore32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_x86:1}
Requires: %{name}-%{system_x86} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_xtensa:1}
Requires: %{name}-%{system_xtensa} = %{epoch}:%{version}-%{release}
%endif
%if %{without separate_kvm}
Requires: %{name}-img = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-img
%endif

%define qemudocdir %{_docdir}/%{name}

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

%if %{without kvmonly}
%ifarch %{kvm_archs}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86
%endif
%endif

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description img
This package provides a command line tool for manipulating disk images

%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%package guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post guest-agent
%systemd_post qemu-guest-agent.service

%preun guest-agent
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%package -n ksm
Summary: Kernel Samepage Merging services
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.


%if 0%{?user:1}
%package %{user}
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description %{user}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets
%endif

%if 0%{?system_x86:1}
%package %{system_x86}
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Provides: kvm = 85
Obsoletes: kvm < 85
Requires: seavgabios-bin
Requires: seabios-bin >= 0.6.0-2
Requires: sgabios-bin
Requires: ipxe-roms-qemu
%if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
%endif

%description %{system_x86}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.
%endif

%if 0%{?system_alpha:1}
%package %{system_alpha}
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_alpha}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.
%endif

%if 0%{?system_arm:1}
%package %{system_arm}
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_arm}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.
%endif

%if 0%{?system_mips:1}
%package %{system_mips}
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_mips}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.
%endif

%if 0%{?system_cris:1}
%package %{system_cris}
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_cris}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.
%endif

%if 0%{?system_lm32:1}
%package %{system_lm32}
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_lm32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.
%endif

%if 0%{?system_m68k:1}
%package %{system_m68k}
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_m68k}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.
%endif

%if 0%{?system_microblaze:1}
%package %{system_microblaze}
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_microblaze}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.
%endif

%if 0%{?system_or32:1}
%package %{system_or32}
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_or32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.
%endif

%if 0%{?system_s390x:1}
%package %{system_s390x}
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_s390x}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.
%endif

%if 0%{?system_sh4:1}
%package %{system_sh4}
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_sh4}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.
%endif

%if 0%{?system_sparc:1}
%package %{system_sparc}
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description %{system_sparc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.
%endif

%if 0%{?system_ppc:1}
%package %{system_ppc}
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF = 0.1.git%{SLOF_gittagdate}
%description %{system_ppc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.
%endif

%if 0%{?system_xtensa:1}
%package %{system_xtensa}
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_xtensa}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.
%endif

%if 0%{?system_unicore32:1}
%package %{system_unicore32}
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_unicore32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.
%endif

%ifarch %{kvm_archs}
%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif

%if %{without separate_kvm}
%package -n libcacard
Summary:        Common Access Card (CAC) Emulation
Group:          Development/Libraries

%description -n libcacard
Common Access Card (CAC) emulation library.

%package -n libcacard-tools
Summary:        CAC Emulation tools
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-tools
CAC emulation tools.

%package -n libcacard-devel
Summary:        CAC Emulation devel
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-devel
CAC emulation development files.
%endif

%prep
%setup -q

# Flow control series
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1

# Fix migration crash with spice (bz #962954)
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1
%patch0133 -p1
%patch0134 -p1
%patch0135 -p1
%patch0136 -p1
%patch0137 -p1
%patch0138 -p1
%patch0139 -p1
%patch0140 -p1
%patch0141 -p1
%patch0142 -p1
%patch0143 -p1
%patch0144 -p1
%patch0145 -p1
%patch0146 -p1
%patch0147 -p1
%patch0148 -p1

# 917860 libcacard and qemu/hw/ccid windows 7 smartcard support.
%patch0201 -p1
%patch0202 -p1
%patch0203 -p1
%patch0204 -p1
%patch0205 -p1
%patch0206 -p1
%patch0207 -p1
%patch0208 -p1
%patch0209 -p1
%patch0210 -p1
%patch0211 -p1
%patch0212 -p1
%patch0213 -p1
%patch0214 -p1
%patch0215 -p1
%patch0216 -p1
%patch0217 -p1
%patch0218 -p1
%patch0219 -p1
%patch0220 -p1
%patch0221 -p1
%patch0222 -p1
%patch0223 -p1
%patch0224 -p1
%patch0225 -p1
%patch0226 -p1
%patch0227 -p1
%patch0228 -p1
%patch0229 -p1
%patch0230 -p1
%patch0231 -p1

# qemu-kvm migration compat (posted upstream)
%patch0301 -p1
%patch0302 -p1
%patch0303 -p1
%patch0304 -p1
%patch0305 -p1
# Fix rtl8139 + windows 7 + large transfers (bz #970240)
%patch0306 -p1
# Fix crash on large drag and drop file transfer w/ spice (bz #969109)
%patch0307 -p1
# Fix build with latest libfdt
%patch0308 -p1
# Fix usb_handle_packet assertions (bz #981459)
%patch0309 -p1
# Fix crash when adding spice vdagent channel in the guest (bz #969084)
%patch0310 -p1
# Fix crash with -M isapc -cpu Haswell (bz #986790)
%patch0311 -p1
# Fix crash in lsi_soft_reset (bz #1000947)
# Patches posted upstream
%patch0312 -p1
%patch0313 -p1
%patch0314 -p1
# Fix crash in scsi_dma_complete (bz #1001617)
%patch0315 -p1

%build
%if %{with kvmonly}
    buildarch="%{kvm_target}-softmmu"
%else
    buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu \
    cris-softmmu lm32-softmmu m68k-softmmu microblaze-softmmu \
    microblazeel-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
    mips64el-softmmu or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
    s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
    xtensa-softmmu xtensaeb-softmmu unicore32-softmmu \
    i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
    armeb-linux-user cris-linux-user m68k-linux-user \
    microblaze-linux-user microblazeel-linux-user mips-linux-user \
    mipsel-linux-user or32-linux-user ppc-linux-user ppc64-linux-user \
    ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
    sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
    unicore32-linux-user"
%endif

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif


dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,sdl,alsa,oss \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --disable-strip \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
        --enable-mixemu \
        --enable-trace-backend=dtrace \
        --disable-werror \
        --disable-xen \
        --enable-kvm \
        --enable-migration-from-qemu-kvm \
%if 0%{?have_spice:1}
        --enable-spice \
%endif
%if 0%{?have_seccomp:1}
        --enable-seccomp \
%endif
%if %{without rbd}
        --disable-rbd \
%endif
%if 0%{?need_fdt:1}
        --enable-fdt \
%else
        --disable-fdt \
%endif
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
}

dobuild --target-list="$buildarch"

gcc %{SOURCE6} -O2 -g -o ksmctl


%install

%define _udevdir /lib/udev/rules.d

install -D -p -m 0744 %{SOURCE4} $RPM_BUILD_ROOT/lib/systemd/system/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT/lib/systemd/ksmctl

install -D -p -m 0744 %{SOURCE7} $RPM_BUILD_ROOT/lib/systemd/system/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{kvm_archs}
%if 0%{?need_kvm_modfile}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_udevdir}

install -m 0755 scripts/kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_udevdir}
%endif

make DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?need_qemu_kvm}
install -m 0755 %{SOURCE13} $RPM_BUILD_ROOT%{_bindir}/qemu-kvm
%endif

%if %{with kvmonly}
rm $RPM_BUILD_ROOT%{_bindir}/qemu-system-%{kvm_target}
rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}.stp
%endif

chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE
for emu in $RPM_BUILD_ROOT%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/$(basename $emu).1.gz
done
%if 0%{?need_qemu_kvm}
ln -sf qemu.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/qemu-kvm.1.gz
%endif

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/slof.bin

# Remove possibly unpackaged files.  Unlike others that are removed
# unconditionally, these firmware files are still distributed as a binary
# together with the qemu package.  We should try to move at least s390-zipl.rom
# to a separate package...  Discussed here on the packaging list:
# https://lists.fedoraproject.org/pipermail/packaging/2012-July/008563.html
%if 0%{!?system_alpha:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/palcode-clipper
%endif
%if 0%{!?system_microblaze:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix*.dtb
%endif
%if 0%{!?system_ppc:1}
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/spapr-rtas.bin
%endif
%if 0%{!?system_s390x:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-zipl.rom
%endif

# Provided by package ipxe
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*rom
# Provided by package seavgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
# Provided by package sgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sgabios.bin

%if 0%{?system_x86:1}
# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../sgabios/sgabios.bin sgabios.bin
%endif

%if 0%{?user:1}
mkdir -p $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips
    qemu-mips qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE1} > $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}
%endif

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_udevdir}

# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/qemu
chmod u+s $RPM_BUILD_ROOT%{_libexecdir}/qemu-bridge-helper

find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
find $RPM_BUILD_ROOT -name "libcacard.so*" -exec chmod +x \{\} \;

%if %{with separate_kvm}
rm -f $RPM_BUILD_ROOT%{_bindir}/qemu-kvm
rm -f $RPM_BUILD_ROOT%{_bindir}/qemu-img
rm -f $RPM_BUILD_ROOT%{_bindir}/qemu-io
rm -f $RPM_BUILD_ROOT%{_bindir}/qemu-nbd
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/qemu-img.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/qemu-nbd.8*

rm -f $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
rm -f $RPM_BUILD_ROOT/lib/systemd/ksmctl
rm -f $RPM_BUILD_ROOT/lib/systemd/system/ksm.service
rm -f $RPM_BUILD_ROOT/lib/systemd/system/ksmtuned.service

rm -f $RPM_BUILD_ROOT%{_bindir}/qemu-ga
rm -f $RPM_BUILD_ROOT%{_unitdir}/qemu-guest-agent.service
rm -f $RPM_BUILD_ROOT%{_udevdir}/99-qemu-guest-agent.rules

rm -f $RPM_BUILD_ROOT%{_bindir}/vscclient
rm -f $RPM_BUILD_ROOT%{_libdir}/libcacard*
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libcacard.pc
rm -rf $RPM_BUILD_ROOT%{_includedir}/cacard
%endif

%check
make check

%ifarch %{kvm_archs}
%post %{kvm_package}
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules &> /dev/null || :
setfacl --remove-all /dev/kvm &> /dev/null || :
udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
%endif

%if %{without separate_kvm}
%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%post -n ksm
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun -n ksm
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun -n ksm
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service
%endif


%if 0%{?user:1}
%post %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%global kvm_files \
%if 0%{?need_kvm_modfile} \
%{_sysconfdir}/sysconfig/modules/kvm.modules \
%endif \
%{_udevdir}/80-kvm.rules

%if 0%{?need_qemu_kvm}
%global qemu_kvm_files \
%{_bindir}/qemu-kvm \
%{_mandir}/man1/qemu-kvm.1*
%endif

%files
%defattr(-,root,root)

%ifarch %{kvm_archs}
%files kvm
%defattr(-,root,root)
%endif

%files common
%defattr(-,root,root)
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_bindir}/virtfs-proxy-helper
%{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf

%if %{without separate_kvm}
%files -n ksm
/lib/systemd/system/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
/lib/systemd/system/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%endif

%if %{without separate_kvm}
%files guest-agent
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%endif

%if 0%{?user:1}
%files %{user}
%defattr(-,root,root)
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-unicore32
%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-or32.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-unicore32.stp
%endif

%if 0%{?system_x86:1}
%files %{system_x86}
%defattr(-,root,root)
%if %{without kvmonly}
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%endif
%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/q35-acpi-dsdt.aml
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/qemu-icon.bmp
%config(noreplace) %{_sysconfdir}/qemu/target-x86_64.conf
%if %{without separate_kvm}
%ifarch %{ix86} x86_64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif
%endif

%ifarch %{kvm_archs}
%files kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvm_stat
%endif

%if 0%{?system_alpha:1}
%files %{system_alpha}
%defattr(-,root,root)
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper
%endif

%if 0%{?system_arm:1}
%files %{system_arm}
%defattr(-,root,root)
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%{_mandir}/man1/qemu-system-arm.1*
%endif

%if 0%{?system_mips:1}
%files %{system_mips}
%defattr(-,root,root)
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*
%endif

%if 0%{?system_cris:1}
%files %{system_cris}
%defattr(-,root,root)
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris.stp
%{_mandir}/man1/qemu-system-cris.1*
%endif

%if 0%{?system_lm32:1}
%files %{system_lm32}
%defattr(-,root,root)
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32.stp
%{_mandir}/man1/qemu-system-lm32.1*
%endif

%if 0%{?system_m68k:1}
%files %{system_m68k}
%defattr(-,root,root)
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%{_mandir}/man1/qemu-system-m68k.1*
%endif

%if 0%{?system_microblaze:1}
%files %{system_microblaze}
%defattr(-,root,root)
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb
%endif

%if 0%{?system_or32:1}
%files %{system_or32}
%defattr(-,root,root)
%{_bindir}/qemu-system-or32
%{_datadir}/systemtap/tapset/qemu-system-or32.stp
%{_mandir}/man1/qemu-system-or32.1*
%endif

%if 0%{?system_s390x:1}
%files %{system_s390x}
%defattr(-,root,root)
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-zipl.rom
%ifarch s390x
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_sh4:1}
%files %{system_sh4}
%defattr(-,root,root)
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*
%endif

%if 0%{?system_sparc:1}
%files %{system_sparc}
%defattr(-,root,root)
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%endif

%if 0%{?system_ppc:1}
%files %{system_ppc}
%defattr(-,root,root)
%if %{without kvmonly}
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%endif
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%ifarch ppc64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_unicore32:1}
%files %{system_unicore32}
%defattr(-,root,root)
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32.stp
%{_mandir}/man1/qemu-system-unicore32.1*
%endif

%if 0%{?system_xtensa:1}
%files %{system_xtensa}
%defattr(-,root,root)
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*
%endif

%if %{without separate_kvm}
%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*


%files -n libcacard
%defattr(-,root,root,-)
%{_libdir}/libcacard.so.*

%files -n libcacard-tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%files -n libcacard-devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc
%endif

%changelog
* Tue Sep 03 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-8
- Fix crash with -M isapc -cpu Haswell (bz #986790)
- Fix crash in lsi_soft_reset (bz #1000947)
- Fix crash in scsi_dma_complete (bz #1001617)
- Fix initial /dev/kvm permissions (bz #993491)

* Sun Aug 18 2013 Alon Levy <alevy@redhat.com> - 2:1.4.2-7
- Support windows 7 smartcard using guests and clients - (bz #917860 rhel 6.5)

* Thu Aug 01 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-6
- Fix crash when adding spice vdagent channel in the guest (bz #969084)

* Tue Jul 30 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-5
- Fix usb_handle_packet assertions (bz #981459)

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-4
- Fix build with latest libfdt
- Don't install conflicting binfmt handler on arm (bz #974804)

* Tue Jun 11 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-3
- Fix rtl8139 + windows 7 + large transfers (bz #970240)
- Fix crash on large drag and drop file transfer w/ spice (bz #969109)

* Mon May 27 2013 Dan Horák <dan[at]danny.cz> - 2:1.4.2-2
- Install the qemu-kvm.1 man page only on arches with kvm

* Sat May 25 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.2-1
- Update to qemu stable 1.4.2
- Alias qemu-system-* man page to qemu.1 (bz #907746)
- Drop execute bit on service files (bz #963917)
- Conditionalize KSM service on host virt support (bz #963681)
- Split out KSM package, make it not pulled in by default

* Wed May 22 2013 Alon Levy <alevy@redhat.com> - 2:1.4.1-4
- Backport migration cleanup (bz #962954)

* Thu May 16 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.1-3
- Drop loading of vhost-net module (bz #963198)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.1-2
- Fix crash with usbredir (bz #962826)
- Drop unneeded kvm.modules on x86 (bz #963198)
- Make ksmtuned handle set_progname usage (bz #955230)
- Enable gluster support

* Sat Apr 20 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.1-1
- Rebased to version 1.4.1
- qemu stable release 1.4.1 (bz 952599)
- CVE-2013-1922: qemu-nbd block format auto-detection vulnerability (bz
  952574, bz 923219)

* Thu Apr 04 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.4.0-11
- Rebuild to attempt to fix broken dep on libbrlapi.so.0.5

* Wed Apr 03 2013 Nathaniel McCallum <nathaniel@themccallums.org> - 2:1.4.0-10
- Sorted qemu.binfmt
- Remove mipsn32 / mipsn32el binfmt support (it is broken and can't be fixed)
- Fix binfmt support for mips / mipsel to match what qemu can do
- Add binfmt support for cris
- Add binfmt support for microblaze / microblazeel
- Add binfmt support for sparc64 / sparc32plus
- Add binfmt support for ppc64 / ppc64abi32

* Wed Apr 03 2013 Hans de Goede <hdegoede@redhat.com> - 2:1.4.0-9
- Fix USB-tablet not working with some Linux guests (bz #929068)

* Tue Apr 02 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-8
- Fix dep on seavgabios-bin

* Mon Apr 01 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-7
- Fixes for iscsi dep
- Fix TCG ld/st optimization (lp 1127369)
- Fix possible crash with VNC and qxl (bz #919777)
- Fix kvm module permissions after first install (bz #907215)
- Switch to seavgabios by default

* Sun Mar 31 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.4.0-6
- Fix TCG ld/st optimization. https://bugs.launchpad.net/bugs/1127369

* Thu Mar 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-5
- do not package libcacard in the separate_kvm case
- backport xfsprogs and usbredir flags from el6

* Mon Mar 11 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-4
- Use pkg-config to search for libiscsi

* Mon Mar 11 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-3
- Added libiscsi-devel BuildRequires

* Fri Mar 01 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-2
- Fix test ordering with latest glib

* Tue Feb 19 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-1
- Rebased to version 1.4.0
- block: dataplane for virtio, potentially large performance improvment
- migration: threaded live migration
- usb-tablet: usb 2.0 support, significantly lowering CPU usage
- usb: improved support for pass-through of USB serial devices
- virtio-net: added support supports multiqueue operation

* Sat Feb  2 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2:1.3.0-9
- add BR perl-podlators for pod2man (F19 development)
- fix "bogus date" entries in %%changelog to fix rebuild

* Fri Feb 01 2013 Alon Levy <alevy@redhat.com> - 2:1.3.0-8
- rebuilt, removing the two added Provides & Obsoletes lines, since
  the current EVR already does that by being 1.3.0 > 1.2.2 , and having
  the same package name of "libcacard"

* Tue Jan 29 2013 Alon Levy <alevy@redhat.com> - 2:1.3.0-7
- Bump and rebuild for updated Provides & Obsoletes of libcacard 1.2.2-4

* Mon Jan 28 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.3.0-6
- Bump and rebuild for updated libseccomp.

* Tue Jan 22 2013 Alon Levy <alevy redhat com> - 2:1.3.0-5
- Fix missing error_set symbol in libcacard.so (bz #891552)

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2:1.3.0-4
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Cole Robinson <crobinso@redhat.com> - 2:1.3.0-3
- Fix migration from qemu-kvm
- Fix the test suite on i686
- Use systemd macros in specfile (bz #850285)

* Tue Jan 15 2013 Hans de Goede <hdegoede@redhat.com> - 2:1.3.0-2
- Fix 0110-usb-redir-Add-flow-control-support.patch being mangled on rebase
  to 1.3.0, breaking usbredir support

* Fri Dec 07 2012 Cole Robinson <crobinso@redhat.com> - 2:1.3.0-1
- Switch base tarball from qemu-kvm to qemu
- qemu 1.3 release
- Option to use linux VFIO driver to assign PCI devices
- Many USB3 improvements
- New paravirtualized hardware random number generator device.
- Support for Glusterfs volumes with "gluster://" -drive URI
- Block job commands for live block commit and storage migration

* Wed Nov 28 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-25
* Merge libcacard into qemu, since they both use the same sources now.

* Thu Nov 22 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-24
- Move vscclient to qemu-common, qemu-nbd to qemu-img

* Tue Nov 20 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-23
- Rewrite fix for bz #725965 based on fix for bz #867366
- Resolve bz #867366

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-23
- Backport --with separate_kvm support from EPEL branch

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-22
- Fix previous commit

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-21
- Backport commit 38f419f (configure: Fix CONFIG_QEMU_HELPERDIR generation,
  2012-10-17)

* Thu Nov 15 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-20
- Install qemu-bridge-helper as suid root
- Distribute a sample /etc/qemu/bridge.conf file

* Thu Nov  1 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-19
- Sync spice patches with upstream, minor bugfixes and set the qxl pci
  device revision to 4 by default, so that guests know they can use
  the new features

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-18
- Fix loading arm initrd if kernel is very large (bz #862766)
- Don't use reserved word 'function' in systemtap files (bz #870972)
- Drop assertion that was triggering when pausing guests w/ qxl (bz
  #870972)

* Sun Oct 28 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-17
- Pull patches queued for qemu 1.2.1

* Fri Oct 19 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-16
- add s390x KVM support
- distribute pre-built firmware or device trees for Alpha, Microblaze, S390
- add missing system targets
- add missing linux-user targets
- fix previous commit

* Thu Oct 18 2012 Dan Horák <dan[at]danny.cz> - 2:1.2.0-15
- fix build on non-kvm arches like s390(x)

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-14
- Change SLOF Requires for the new version number

* Thu Oct 11 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-13
- Add ppc support to kvm.modules (original patch by David Gibson)
- Replace x86only build with kvmonly build: add separate defines and
  conditionals for all packages, so that they can be chosen and
  renamed in kvmonly builds and so that qemu has the appropriate requires
- Automatically pick libfdt dependancy
- Add knob to disable spice+seccomp

* Fri Sep 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-12
- Call udevadm on post, fixing bug 860658

* Fri Sep 28 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-11
- Rebuild against latest spice-server and spice-protocol
- Fix non-seamless migration failing with vms with usb-redir devices,
  to allow boxes to load such vms from disk

* Tue Sep 25 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-10
- Sync Spice patchsets with upstream (rhbz#860238)
- Fix building with usbredir >= 0.5.2

* Thu Sep 20 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-9
- Sync USB and Spice patchsets with upstream

* Sun Sep 16 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-8
- Use 'global' instead of 'define', and underscore in definition name,
  n-v-r, and 'dist' tag of SLOF, all to fix RHBZ#855252.

* Fri Sep 14 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-4
- add versioned dependency from qemu-system-ppc to SLOF (BZ#855252)

* Wed Sep 12 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-3
- Fix RHBZ#853408 which causes libguestfs failure.

* Sat Sep  8 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-2
- Fix crash on (seamless) migration
- Sync usbredir live migration patches with upstream

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-1
- New upstream release 1.2.0 final
- Add support for Spice seamless migration
- Add support for Spice dynamic monitors
- Add support for usb-redir live migration

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.2.0-0.5.rc1
- Flip Requires: ceph >= foo to Conflicts: ceph < foo, so we pull in only the
  libraries which we need and not the rest of ceph which we don't.

* Tue Aug 28 2012 Cole Robinson <crobinso@redhat.com> 1.2.0-0.4.rc1
- Update to 1.2.0-rc1

* Mon Aug 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2-0.3.20120806git3e430569
- Backport Bonzini's vhost-net fix (RHBZ#848400).

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.2.20120806git3e430569
- Bump release number, previous build forgot but the dist bump helped us out

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569
- Revive qemu-system-{ppc*, sparc*} (bz 844502)
- Enable KVM support for all targets (bz 844503)

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569.fc18
- Update to git snapshot

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 1.1.1-1
- Upstream stable release 1.1.1
- Fix systemtap tapsets (bz 831763)
- Fix VNC audio tunnelling (bz 840653)
- Don't renable ksm on update (bz 815156)
- Bump usbredir dep (bz 812097)
- Fix RPM install error on non-virt machines (bz 660629)
- Obsolete openbios to fix upgrade dependency issues (bz 694802)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-8
- Re-diff previous patch so that it applies and actually apply it

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-7
- Add patch to fix default machine options.  This fixes libvirt
  detection of qemu.
- Back out patch 1 which conflicts.

* Fri Jul  6 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-5
- Fix qemu crashing (on an assert) whenever USB-2.0 isoc transfers are used

* Thu Jul  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-4
- Disable tests since they hang intermittently.
- Add kvmvapic.bin (replaces vapic.bin).
- Add cpus-x86_64.conf.  qemu now creates /etc/qemu/target-x86_64.conf
  as an empty file.
- Add qemu-icon.bmp.
- Add qemu-bridge-helper.
- Build and include virtfs-proxy-helper + man page (thanks Hans de Goede).

* Wed Jul  4 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-1
- New upstream release 1.1.0
- Drop about a 100 spice + USB patches, which are all upstream

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-17
- Fix install failure due to set -e (rhbz #815272)

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-16
- Fix kvm.modules to exit successfully on non-KVM capable systems (rhbz #814932)

* Thu Apr 19 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-15
- Add a couple of backported QXL/Spice bugfixes
- Add spice volume control patches

* Fri Apr 6 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-12
- Add back PPC and SPARC user emulators
- Update binfmt rules from upstream

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-11
- Some more USB bugfixes from upstream

* Thu Mar 29 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-12
- Fix ExclusiveArch mistake that disabled all non-x86_64 builds on Fedora

* Wed Mar 28 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-11
- Use --with variables for build-time settings

* Wed Mar 28 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-10
- Switch to use iPXE for netboot ROMs

* Thu Mar 22 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-9
- Remove O_NOATIME for 9p filesystems

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-8
- Move udev rules to /lib/udev/rules.d (rhbz #748207)

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-7
- Add a whole bunch of USB bugfixes from upstream

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-6
- Add many more missing BRs for misc QEMU features
- Enable running of test suite during build

* Tue Feb 07 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-5
- Add support for virtio-scsi

* Sun Feb  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.0-4
- Require updated ceph for latest librbd with rbd_flush symbol.

* Tue Jan 24 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-3
- Add support for vPMU
- e1000: bounds packet size against buffer size CVE-2012-0029

* Fri Jan 13 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-2
- Add patches for USB redirect bits
- Remove palcode-clipper, we don't build it

* Wed Jan 11 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Add patches from 1.0.1 queue

* Fri Dec 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Update to qemu 1.0

* Tue Nov 15 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-3
- Enable spice for i686 users as well

* Thu Nov 03 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-2
- Fix POSTIN scriplet failure (#748281)

* Fri Oct 21 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-1
- Require seabios-bin >= 0.6.0-2 (#741992)
- Replace init scripts with systemd units (#741920)
- Update to 0.15.1 stable upstream
  
* Fri Oct 21 2011 Paul Moore <pmoore@redhat.com>
- Enable full relro and PIE (rhbz #738812)

* Wed Oct 12 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-6
- Add BR on ceph-devel to enable RBD block device

* Wed Oct  5 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-5
- Create a qemu-guest-agent sub-RPM for guest installation

* Tue Sep 13 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-4
- Enable DTrace tracing backend for SystemTAP (rhbz #737763)
- Enable build with curl (rhbz #737006)

* Thu Aug 18 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-3
- Add missing BuildRequires: usbredir-devel, so that the usbredir code
  actually gets build

* Thu Aug 18 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.15.0-2
- Add upstream qemu patch 'Allow to leave type on default in -machine'
  (2645c6dcaf6ea2a51a3b6dfa407dd203004e4d11).

* Sun Aug 14 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-1
- Update to 0.15.0 stable release.

* Thu Aug 04 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.3.201108040af4922
- Update to 0.15.0-rc1 as we prepare for 0.15.0 release

* Thu Aug  4 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-0.3.2011072859fadcc
- Fix default accelerator for non-KVM builds (rhbz #724814)

* Thu Jul 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.2011072859fadcc
- Update to 0.15.0-rc0 as we prepare for 0.15.0 release

* Tue Jul 19 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-0.2.20110718525e3df
- Add support usb redirection over the network, see:
  http://fedoraproject.org/wiki/Features/UsbNetworkRedirection
- Restore chardev flow control patches

* Mon Jul 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.20110718525e3df
- Update to git snapshot as we prepare for 0.15.0 release

* Wed Jun 22 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.14.0-9
- Add BR libattr-devel.  This caused the -fstype option to be disabled.
  https://www.redhat.com/archives/libvir-list/2011-June/thread.html#01017

* Mon May  2 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.14.0-8
- Fix a bug in the spice flow control patches which breaks the tcp chardev

* Tue Mar 29 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-7
- Disable qemu-ppc and qemu-sparc packages (#679179)

* Mon Mar 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-6
- Spice fixes for flow control.

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 2:0.14.0-5
- be more careful when removing the -g flag on s390

* Fri Mar 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-4
- Fix thinko on adding the most recent patches.

* Wed Mar 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-3
- Fix migration issue with vhost
- Fix qxl locking issues for spice

* Wed Mar 02 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-2
- Re-enable sparc and cris builds

* Thu Feb 24 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-1
- Update to 0.14.0 release

* Fri Feb 11 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110210git7aa8c46
- Update git snapshot
- Temporarily disable qemu-cris and qemu-sparc due to build errors (to be resolved shorly)

* Tue Feb 08 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110208git3593e6b
- Update to 0.14.0 rc git snapshot
- Add virtio-net to modules

* Wed Nov  3 2010 Daniel P. Berrange <berrange@redhat.com> - 2:0.13.0-2
- Revert previous change
- Make qemu-common own the /etc/qemu directory
- Add /etc/qemu/target-x86_64.conf to qemu-system-x86 regardless
  of host architecture.

* Wed Nov 03 2010 Dan Horák <dan[at]danny.cz> - 2:0.13.0-2
- Remove kvm config file on non-x86 arches (part of #639471)
- Own the /etc/qemu directory

* Mon Oct 18 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-1
- Update to 0.13.0 upstream release
- Fixes for vhost
- Fix mouse in certain guests (#636887)
- Fix issues with WinXP guest install (#579348)
- Resolve build issues with S390 (#639471)
- Fix Windows XP on Raw Devices (#631591)

* Tue Oct 05 2010 jkeating - 2:0.13.0-0.7.rc1.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.7.rc1
- Flip qxl pci id from unstable to stable (#634535)
- KSM Fixes from upstream (#558281)

* Tue Sep 14 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.6.rc1
- Move away from git snapshots as 0.13 is close to release
- Updates for spice 0.6

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.5.20100809git25fdf4a
- Fix typo in e1000 gpxe rom requires.
- Add links to newer vgabios

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.4.20100809git25fdf4a
- Disable spice on 32bit, it is not supported and buildreqs don't exist.

* Mon Aug 9 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.3.20100809git25fdf4a
- Updates from upstream towards 0.13 stable
- Fix requires on gpxe
- enable spice now that buildreqs are in the repository.
- ksmtrace has moved to a separate upstream package

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.2.20100727gitb81fe95
- add texinfo buildreq for manpages.

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.1.20100727gitb81fe95
- Update to 0.13.0 upstream snapshot
- ksm init fixes from upstream

* Tue Jul 20 2010 Dan Horák <dan[at]danny.cz> - 2:0.12.3-8
- Add avoid-llseek patch from upstream needed for building on s390(x)
- Don't use parallel make on s390(x)

* Tue Jun 22 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.3-7
- Add vvfat hardening patch from upstream (#605202)

* Fri Apr 23 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-6
- Change requires to the noarch seabios-bin
- Add ownership of docdir to qemu-common (#572110)
- Fix "Cannot boot from non-existent NIC" error when using virt-install (#577851)

* Thu Apr 15 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-5
- Update virtio console patches from upstream

* Thu Mar 11 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-4
- Detect cdrom via ioctl (#473154)
- re add increased buffer for USB control requests (#546483)

* Wed Mar 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-3
- Migration clear the fd in error cases (#518032)

* Tue Mar 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-2
- Allow builds --with x86only
- Add libaio-devel buildreq for aio support

* Fri Feb 26 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-1
- Update to 0.12.3 upstream
- vhost-net migration/restart fixes
- Add F-13 machine type
- virtio-serial fixes

* Tue Feb 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-6
- Add vhost net support.

* Thu Feb 04 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-5
- Avoid creating too large iovecs in multiwrite merge (#559717)
- Don't try to set max_kernel_pages during ksm init on newer kernels (#558281)
- Add logfile options for ksmtuned debug.

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-4
- Remove build dependency on iasl now that we have seabios

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-3
- Remove source target for 0.12.1.2

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-2
- Add virtio-console patches from upstream for the F13 VirtioSerial feature

* Mon Jan 25 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-1
- Update to 0.12.2 upstream

* Sun Jan 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-3
- Point to seabios instead of bochs, and add a requires for seabios

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-2
- Remove qcow2 virtio backing file patch

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-1
- Update to 0.12.1.2 upstream
- Remove patches included in upstream

* Fri Nov 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-12
- Fix a use-after-free crasher in the slirp code (#539583)
- Fix overflow in the parallels image format support (#533573)

* Wed Nov  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-11
- Temporarily disable preadv/pwritev support to fix data corruption (#526549)

* Tue Nov  3 2009 Justin M. Forbes <jforbes@redhat.com> - 2:0.11.0-10
- Default ksm and ksmtuned services on.

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-9
- Fix dropped packets with non-virtio NICs (#531419)

* Wed Oct 21 2009 Glauber Costa <gcosta@redhat.com> - 2:0.11.0-8
- Properly save kvm time registers (#524229)

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7
- Fix potential segfault from too small MSR_COUNT (#528901)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-6
- Fix fs errors with virtio and qcow2 backing file (#524734)
- Fix ksm initscript errors on kernel missing ksm (#527653)
- Add missing Requires(post): getent, useradd, groupadd (#527087)

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-5
- Add 'retune' verb to ksmtuned init script

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-4
- Use rtl8029 PXE rom for ne2k_pci, not ne (#526777)
- Also, replace the gpxe-roms-qemu pkg requires with file-based requires

* Thu Oct  1 2009 Justin M. Forbes <jmforbes@redhat.com> - 2:0.11.0-3
- Improve error reporting on file access (#524695)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-2
- Fix pci hotplug to not exit if supplied an invalid NIC model (#524022)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-1
- Update to 0.11.0 release
- Drop a couple of upstreamed patches

* Wed Sep 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-5
- Fix issue causing NIC hotplug confusion when no model is specified (#524022)

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-4
- Fix for KSM patch from Justin Forbes

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-3
- Add ksmtuned, also from Dan Kenigsberg
- Use %_initddir macro

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-2
- Add ksm control script from Dan Kenigsberg

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-1
- Update to qemu-kvm-0.11.0-rc2
- Drop upstreamed patches
- extboot install now fixed upstream
- Re-place TCG init fix (#516543) with the one gone upstream

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.10.rc1
- Fix MSI-X error handling on older kernels (#519787)

* Fri Sep  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.9.rc1
- Make pulseaudio the default audio backend (#519540, #495964, #496627)

* Thu Aug 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2:0.10.91-0.8.rc1
- Fix segfault when qemu-kvm is invoked inside a VM (#516543)

* Tue Aug 18 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.7.rc1
- Fix permissions on udev rules (#517571)

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 2:0.10.91-0.6.rc1
- Allow blacklisting of kvm modules (#517866)

* Fri Aug  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.5.rc1
- Fix virtio_net with -net user (#516022)

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.4.rc1
- Update to qemu-kvm-0.11-rc1; no changes from rc1-rc0

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.3.rc1.rc0
- Fix extboot checksum (bug #514899)

* Fri Jul 31 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.2.rc1.rc0
- Add KSM support
- Require bochs-bios >= 2.3.8-0.8 for latest kvm bios updates

* Thu Jul 30 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.1.rc1.rc0
- Update to qemu-kvm-0.11.0-rc1-rc0
- This is a pre-release of the official -rc1
- A vista installer regression is blocking the official -rc1 release
- Drop qemu-prefer-sysfs-for-usb-host-devices.patch
- Drop qemu-fix-build-for-esd-audio.patch
- Drop qemu-slirp-Fix-guestfwd-for-incoming-data.patch
- Add patch to ensure extboot.bin is installed

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.10.50-14.kvm88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-13.kvm88
- Fix bug 513249, -net channel option is broken

* Thu Jul 16 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.10.50-12.kvm88
- Add 'qemu' user and group accounts
- Force disable xen until it can be made to build

* Thu Jul 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-11.kvm88
- Update to kvm-88, see http://www.linux-kvm.org/page/ChangeLog
- Package mutiboot.bin
- Update for how extboot is built
- Fix sf.net source URL
- Drop qemu-fix-ppc-softmmu-kvm-disabled-build.patch
- Drop qemu-fix-pcspk-build-with-kvm-disabled.patch
- Cherry-pick fix for esound support build failure

* Wed Jul 15 2009 Daniel Berrange <berrange@lettuce.camlab.fab.redhat.com> - 2:0.10.50-10.kvm87
- Add udev rules to make /dev/kvm world accessible & group=kvm (rhbz #497341)
- Create a kvm group if it doesn't exist (rhbz #346151)

* Tue Jul 07 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-9.kvm87
- use pxe roms from gpxe, instead of etherboot package.

* Fri Jul  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-8.kvm87
- Prefer sysfs over usbfs for usb passthrough (#508326)

* Sat Jun 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-7.kvm87
- Update to kvm-87
- Drop upstreamed patches
- Cherry-pick new ppc build fix from upstream
- Work around broken linux-user build on ppc
- Fix hw/pcspk.c build with --disable-kvm
- Re-enable preadv()/pwritev() since #497429 is long since fixed
- Kill petalogix-s3adsp1800.dtb, since we don't ship the microblaze target

* Fri Jun  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-6.kvm86
- Fix 'kernel requires an x86-64 CPU' error
- BuildRequires ncurses-devel to enable '-curses' option (#504226)

* Wed Jun  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-5.kvm86
- Prevent locked cdrom eject - fixes hang at end of anaconda installs (#501412)
- Avoid harmless 'unhandled wrmsr' warnings (#499712)

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-4.kvm86
- Update to kvm-86 release
- ChangeLog here: http://marc.info/?l=kvm&m=124282885729710

* Fri May  1 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-3.kvm85
- Really provide qemu-kvm as a metapackage for comps

* Tue Apr 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-2.kvm85
- Provide qemu-kvm as a metapackage for comps

* Mon Apr 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-1.kvm85
- Update to qemu-kvm-devel-85
- kvm-85 is based on qemu development branch, currently version 0.10.50
- Include new qemu-io utility in qemu-img package
- Re-instate -help string for boot=on to fix virtio booting with libvirt
- Drop upstreamed patches
- Fix missing kernel/include/asm symlink in upstream tarball
- Fix target-arm build
- Fix build on ppc
- Disable preadv()/pwritev() until bug #497429 is fixed
- Kill more .kernelrelease uselessness
- Make non-kvm qemu build verbose

* Fri Apr 24 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-15
- Fix source numbering typos caused by make-release addition

* Thu Apr 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-14
- Improve instructions for generating the tarball

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-13
- Enable pulseaudio driver to fix qemu lockup at shutdown (#495964)

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

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Sun May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
