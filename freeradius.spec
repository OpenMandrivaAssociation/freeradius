%define _disable_ld_no_undefined 1

Summary: High-performance and highly configurable free RADIUS server
Name: freeradius
Version: 3.2.7
Release: 1
License: GPL-2.0-or-later AND LGPL-2.0-or-later
URL: http://www.freeradius.org/

%global dist_base freeradius-server-%{version}

Source0: ftp://ftp.freeradius.org/pub/radius/%{dist_base}.tar.bz2
Source100: radiusd.service
Source102: freeradius-logrotate
Source103: freeradius-pam-conf
Source104: freeradius-tmpfiles.conf
Source105: freeradius.sysusers

Patch1: freeradius-Adjust-configuration-to-fit-Red-Hat-specifics.patch
Patch2: freeradius-Use-system-crypto-policy-by-default.patch
Patch3: freeradius-bootstrap-create-only.patch
Patch4: freeradius-no-buildtime-cert-gen.patch
Patch5: freeradius-bootstrap-make-permissions.patch
Patch6: freeradius-ldap-infinite-timeout-on-starttls.patch
Patch7: freeradius-ease-openssl-version-check.patch
Patch8: freeradius-configure-c99.patch
Patch9: freeradius-openssl-no-engine.patch
Patch10: freeradius-no-sqlippool-tool.patch

%global docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

BuildRequires: autoconf
BuildRequires: make
BuildRequires: gdbm-devel
BuildRequires: openssl
BuildRequires: net-snmp-devel
BuildRequires: net-snmp-utils
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(readline)
BuildRequires: pkgconfig(libpcap)
BuildRequires: pkgconfig(libxcrypt)
BuildRequires: pkgconfig(libmemcached)
BuildRequires: pkgconfig(talloc)
BuildRequires: pkgconfig(pam)
BuildRequires: pkgconfig(zlib)
BuildRequires: systemd
BuildRequires: chrpath
BuildRequires: systemd-rpm-macros
# radlast gets built only if `last` is available at build time
BuildRequires: util-linux

BuildRequires: libyubikey-devel
BuildRequires: ykclient-devel

# Require OpenSSL version we built with, or newer, to avoid startup failures
# due to runtime OpenSSL version checks.
Requires: openssl >= %(rpm -q --queryformat '%%{VERSION}' openssl)
# Needed for certificate generation as upstream bootstrap script isn't
# compatible with Makefile equivalent.
Requires: make

%description
The FreeRADIUS Server Project is a high performance and highly configurable
GPL'd free RADIUS server. The server is similar in some respects to
Livingston's 2.0 server.  While FreeRADIUS started as a variant of the
Cistron RADIUS server, they don't share a lot in common any more. It now has
many more features than Cistron or Livingston, and is much more configurable.

FreeRADIUS is an Internet authentication daemon, which implements the RADIUS
protocol, as defined in RFC 2865 (and others). It allows Network Access
Servers (NAS boxes) to perform authentication for dial-up users. There are
also RADIUS clients available for Web servers, firewalls, Unix logins, and
more.  Using RADIUS allows authentication and authorization for a network to
be centralized, and minimizes the amount of re-configuration which has to be
done when adding or deleting new users.

%package doc
Summary: FreeRADIUS documentation

%description doc
All documentation supplied by the FreeRADIUS project is included
in this package.

%package utils
Summary: FreeRADIUS utilities
Requires: %{name} = %{version}-%{release}

%description utils
The FreeRADIUS server has a number of features found in other servers,
and additional features not found in any other server. Rather than
doing a feature by feature comparison, we will simply list the features
of the server, and let you decide if they satisfy your needs.

Support for RFC and VSA Attributes Additional server configuration
attributes Selecting a particular configuration Authentication methods

%package devel
Summary: FreeRADIUS development files
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and libraries for FreeRADIUS.

%package ldap
Summary: LDAP support for freeradius
Requires: %{name} = %{version}-%{release}
BuildRequires: pkgconfig(ldap)

%description ldap
This plugin provides the LDAP support for the FreeRADIUS server project.

%package krb5
Summary: Kerberos 5 support for freeradius
Requires: %{name} = %{version}-%{release}
BuildRequires: krb5-devel

%description krb5
This plugin provides the Kerberos 5 support for the FreeRADIUS server project.

%package perl
Summary: Perl support for freeradius
Requires: %{name} = %{version}-%{release}
%{?fedora:BuildRequires: perl-devel}
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::Embed)

%description perl
This plugin provides the Perl support for the FreeRADIUS server project.

%package -n python-freeradius
Summary: Python support for freeradius
Requires: %{name} = %{version}-%{release}
BuildRequires: pkgconfig(python3)

%description -n python-freeradius
This plugin provides the Python 3 support for the FreeRADIUS server project.

%package mariadb
Summary: MariaDB support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: pkgconfig(mariadb)

%description mariadb
This plugin provides the MariaDB support for the FreeRADIUS server project.

%package postgresql
Summary: Postgresql support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: pkgconfig(libpq)

%description postgresql
This plugin provides the postgresql support for the FreeRADIUS server project.

%package sqlite
Summary: SQLite support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: pkgconfig(sqlite3)

%description sqlite
This plugin provides the SQLite support for the FreeRADIUS server project.

%package freetds
Summary: FreeTDS support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: freetds-devel

%description freetds
This plugin provides the FreeTDS support for the FreeRADIUS server project.


%package unixODBC
Summary: Unix ODBC support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: unixODBC-devel

%description unixODBC
This plugin provides the unixODBC support for the FreeRADIUS server project.

%package rest
Summary: REST support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: pkgconfig(libcurl)
BuildRequires: json-c-devel

%description rest
This plugin provides the REST support for the FreeRADIUS server project.

%package redis
Summary: Redis support for freeradius
Requires: %{name} = %{EVRD}
BuildRequires: pkgconfig(hiredis)

%description redis
This plugin provides Redis support for the FreeRADIUS server project.

%package memcached
Summary: Memcached support for freeradius
Requires: %{name} = %{EVRD}

%description memcached
This plugin provides Memcached support for the FreeRADIUS server project.

%prep
%setup -q -n %{dist_base}
# Note: We explicitly do not make patch backup files because 'make install'
# mistakenly includes the backup files, especially problematic for raddb config files.
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1

%build
# Force compile/link options, extra security for network facing daemon
%global _hardened_build 1

%global build_ldflags %{build_ldflags} $(python3-config --embed --libs)
export PY3_LIB_DIR="$(python3-config --configdir)"
export PY3_INC_DIR="$(python3 -c 'import sysconfig; print(sysconfig.get_config_var("INCLUDEPY"))')"

%configure \
        --libdir=%{_libdir}/freeradius \
        --enable-reproducible-builds \
        --disable-openssl-version-check \
        --with-openssl \
        --with-udpfromto \
        --with-threads \
        --with-docdir=%{docdir} \
        --with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
        --with-rlm-sql-postgresql-lib-dir=%{_libdir} \
        --with-rlm-sql_mysql-include-dir=/usr/include/mysql \
        --with-mysql-lib-dir=%{_libdir}/mariadb \
        --with-unixodbc-lib-dir=%{_libdir} \
        --with-rlm-dbm-lib-dir=%{_libdir} \
        --with-rlm-krb5-include-dir=/usr/kerberos/include \
        --with-rlm_python3 \
        --with-rlm-python3-lib-dir=$PY3_LIB_DIR \
        --with-rlm-python3-include-dir=$PY3_INC_DIR \
        --without-rlm_python \
        --without-rlm_eap_ikev2 \
        --without-rlm_eap_tnc \
        --with-rlm_sql_iodbc \
        --with-rlm_sql_firebird \
        --without-rlm_sql_db2 \
        --without-rlm_sql_oracle \
        --without-rlm_unbound \
        --with-rlm_redis \
        --with-rlm_rediswho \
        --with-rlm_cache_memcached

# Build fast, but get better errors if we fail
make %{?_smp_mflags} || make -j1

%install
mkdir -p %{buildroot}/%{_localstatedir}/lib/radiusd
make install R=%{buildroot}

# logs
mkdir -p %{buildroot}/var/log/radius/radacct
touch %{buildroot}/var/log/radius/{radutmp,radius.log}

install -D -m 644 %{SOURCE100} %{buildroot}/%{_unitdir}/radiusd.service
install -D -m 644 %{SOURCE102} %{buildroot}/%{_sysconfdir}/logrotate.d/radiusd
install -D -m 644 %{SOURCE103} %{buildroot}/%{_sysconfdir}/pam.d/radiusd

mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/radiusd/
install -d -m 0700 %{buildroot}%{_localstatedir}/run/radiusd/tmp
install -m 0644 %{SOURCE104} %{buildroot}%{_tmpfilesdir}/radiusd.conf
install -p -D -m 0644 %{SOURCE105} %{buildroot}%{_sysusersdir}/freeradius.conf

# install SNMP MIB files
mkdir -p %{buildroot}%{_datadir}/snmp/mibs/
install -m 644 mibs/*RADIUS*.mib %{buildroot}%{_datadir}/snmp/mibs/

# remove rpath where needed
chrpath --delete %{buildroot}%{_libdir}/freeradius/*.so
for f in %{buildroot}/usr/sbin/*; do chrpath --delete $f || true; done
for f in %{buildroot}/usr/bin/*; do chrpath --delete $f || true; done

# update ld with freeradius libs
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/freeradius" > %{buildroot}/%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# remove unneeded stuff
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.crt
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.crl
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.csr
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.der
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.key
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.pem
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/*.p12
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/index.*
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/serial*
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/dh
rm -f %{buildroot}/%{_sysconfdir}/raddb/certs/random

rm -f %{buildroot}/usr/sbin/rc.radiusd
rm -f %{buildroot}/usr/bin/rbmonkey
rm -rf %{buildroot}/%{_libdir}/freeradius/*.a
rm -rf %{buildroot}/%{_libdir}/freeradius/*.la

rm -rf %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/main/mssql

rm -rf %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/ippool/oracle
rm -rf %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/ippool/mssql
rm -rf %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/oracle
rm -rf %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/main/oracle
rm -r %{buildroot}%{_sysconfdir}/raddb/mods-config/sql/moonshot-targeted-ids

rm %{buildroot}/%{_sysconfdir}/raddb/mods-available/unbound
rm %{buildroot}/%{_sysconfdir}/raddb/mods-config/unbound/default.conf
rm %{buildroot}/%{_sysconfdir}/raddb/mods-available/couchbase
rm %{buildroot}/%{_sysconfdir}/raddb/mods-available/abfab*
rm %{buildroot}/%{_sysconfdir}/raddb/mods-available/moonshot-targeted-ids
rm %{buildroot}/%{_sysconfdir}/raddb/policy.d/abfab*
rm %{buildroot}/%{_sysconfdir}/raddb/policy.d/moonshot-targeted-ids
rm %{buildroot}/%{_sysconfdir}/raddb/sites-available/abfab*

rm %{buildroot}/%{_libdir}/freeradius/rlm_test.so

# remove unsupported config files
rm -f %{buildroot}/%{_sysconfdir}/raddb/experimental.conf

# Mongo will never be supported on Fedora or RHEL
rm -f %{buildroot}/%{_sysconfdir}/raddb/mods-config/sql/ippool/mongo/queries.conf
rm -f %{buildroot}/%{_sysconfdir}/raddb/mods-config/sql/main/mongo/queries.conf

# install doc files omitted by standard install
for f in COPYRIGHT CREDITS INSTALL.rst README.rst VERSION; do
    cp $f %{buildroot}/%{docdir}
done
cp LICENSE %{buildroot}/%{docdir}/LICENSE.gpl
cp src/lib/LICENSE %{buildroot}/%{docdir}/LICENSE.lgpl
cp src/LICENSE.openssl %{buildroot}/%{docdir}/LICENSE.openssl

%files
# doc
%license %{docdir}/LICENSE.gpl
%license %{docdir}/LICENSE.lgpl
%license %{docdir}/LICENSE.openssl

# system
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_unitdir}/radiusd.service
%{_tmpfilesdir}/radiusd.conf
%{_sysusersdir}/freeradius.conf
%dir %attr(710,radiusd,radiusd) %{_localstatedir}/run/radiusd
%dir %attr(700,radiusd,radiusd) %{_localstatedir}/run/radiusd/tmp
%dir %attr(755,radiusd,radiusd) %{_localstatedir}/lib/radiusd

# configs (raddb)
%dir %attr(755,root,radiusd) %{_sysconfdir}/raddb
%defattr(-,root,radiusd)
%{_sysconfdir}/raddb/README.rst
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/panic.gdb

%attr(644,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/dictionary
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/clients.conf

%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/templates.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/trigger.conf

# symlink: %{_sysconfdir}/raddb/hints -> ./mods-config/preprocess/hints
%config %{_sysconfdir}/raddb/hints

# symlink: %{_sysconfdir}/raddb/huntgroups -> ./mods-config/preprocess/huntgroups
%config %{_sysconfdir}/raddb/huntgroups

%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/proxy.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/radiusd.conf

# symlink: %{_sysconfdir}/raddb/users -> ./mods-config/files/authorize
%config(noreplace) %{_sysconfdir}/raddb/users

# certs
%dir %attr(770,root,radiusd) %{_sysconfdir}/raddb/certs
%config(noreplace) %{_sysconfdir}/raddb/certs/Makefile
%config(noreplace) %{_sysconfdir}/raddb/certs/passwords.mk
%{_sysconfdir}/raddb/certs/README.md
%{_sysconfdir}/raddb/certs/realms/README.md
%config(noreplace) %{_sysconfdir}/raddb/certs/xpextensions
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/certs/*.cnf
%attr(750,root,radiusd) %{_sysconfdir}/raddb/certs/bootstrap

# mods-config
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config
%{_sysconfdir}/raddb/mods-config/README.rst
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/attr_filter
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/attr_filter/*
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/files
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/files/*
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/preprocess
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/preprocess/*
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/realm/freeradius-naptr-to-home-server.sh

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/counter
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/cui
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main

# sites-available
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/sites-available
%{_sysconfdir}/raddb/sites-available/README
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/aws-nlb
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/resource-check
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/control-socket
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/decoupled-accounting
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/robust-proxy-accounting
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/soh
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/coa
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/coa-relay
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/example
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/inner-tunnel
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/dhcp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/check-eap-tls
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/status
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/dhcp.relay
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/virtual.example.com
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/originate-coa
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/vmps
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/default
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/proxy-inner-tunnel
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/dynamic-clients
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/copy-acct-to-home-server
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/buffered-sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/tls
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/totp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/channel_bindings
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/challenge
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/google-ldap-auth
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/sites-available/tls-cache

# sites-enabled
# symlink: %{_sysconfdir}/raddb/sites-enabled/xxx -> ../sites-available/xxx
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/sites-enabled
%config(missingok) %{_sysconfdir}/raddb/sites-enabled/inner-tunnel
%config(missingok) %{_sysconfdir}/raddb/sites-enabled/default

# mods-available
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-available
%{_sysconfdir}/raddb/mods-available/README.rst
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/always
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/attr_filter
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/cache
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/cache_auth
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/chap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/counter
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/cui
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/date
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/detail
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/detail.example.com
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/detail.log
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dhcp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dhcp_files
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dhcp_passwd
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dhcp_sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dhcp_sqlippool
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/digest
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dynamic_clients
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/eap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/echo
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/etc_group
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/exec
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/expiration
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/expr
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/files
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/idn
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/inner-eap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/ippool
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/json
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/ldap_google
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/linelog
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/logintime
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/mac2ip
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/mac2vlan
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/mschap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/ntlm_auth
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/opendirectory
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/pam
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/pap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/passwd
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/preprocess
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/python
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/python3
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/radutmp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/realm
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/redis
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/rediswho
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/replicate
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/smbpasswd
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/smsotp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/soh
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sometimes
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sql_map
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sqlcounter
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sqlippool
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/sradutmp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/totp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/unix
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/unpack
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/utf8
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/wimax
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/yubikey
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/dpsk
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/proxy_rate_limit

# mods-enabled
# symlink: %{_sysconfdir}/raddb/mods-enabled/xxx -> ../mods-available/xxx
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-enabled
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/always
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/attr_filter
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/chap
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/date
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/detail
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/detail.log
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/digest
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/dynamic_clients
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/eap
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/echo
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/exec
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/expiration
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/expr
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/files
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/linelog
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/logintime
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/mschap
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/ntlm_auth
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/pap
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/passwd
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/preprocess
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/radutmp
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/realm
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/replicate
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/soh
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/sradutmp
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/totp
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/unix
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/unpack
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/utf8
%config(missingok) %{_sysconfdir}/raddb/mods-enabled/proxy_rate_limit

# policy
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/policy.d
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/accounting
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/canonicalization
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/control
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/cui
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/debug
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/dhcp
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/eap
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/filter
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/operator-name
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/policy.d/rfc7542


# binaries
%defattr(-,root,root)
%{_bindir}/checkrad
%{_bindir}/raddebug
%{_bindir}/radiusd
%{_bindir}/radmin

# dictionaries
%dir %attr(755,root,root) /usr/share/freeradius
/usr/share/freeradius/*

# logs
%dir %attr(700,radiusd,radiusd) /var/log/radius/
%dir %attr(700,radiusd,radiusd) /var/log/radius/radacct/
%ghost %attr(644,radiusd,radiusd) /var/log/radius/radutmp
%ghost %attr(600,radiusd,radiusd) /var/log/radius/radius.log

# libs
%attr(755,root,root) %{_libdir}/freeradius/lib*.so*

# loadable modules
%dir %attr(755,root,root) %{_libdir}/freeradius
%{_libdir}/freeradius/proto_dhcp.so
%{_libdir}/freeradius/proto_vmps.so
%{_libdir}/freeradius/rlm_always.so
%{_libdir}/freeradius/rlm_attr_filter.so
%{_libdir}/freeradius/rlm_cache.so
%{_libdir}/freeradius/rlm_cache_rbtree.so
%{_libdir}/freeradius/rlm_chap.so
%{_libdir}/freeradius/rlm_counter.so
%{_libdir}/freeradius/rlm_date.so
%{_libdir}/freeradius/rlm_detail.so
%{_libdir}/freeradius/rlm_dhcp.so
%{_libdir}/freeradius/rlm_digest.so
%{_libdir}/freeradius/rlm_dynamic_clients.so
%{_libdir}/freeradius/rlm_eap.so
%{_libdir}/freeradius/rlm_eap_fast.so
%{_libdir}/freeradius/rlm_eap_gtc.so
%{_libdir}/freeradius/rlm_eap_md5.so
%{_libdir}/freeradius/rlm_eap_mschapv2.so
%{_libdir}/freeradius/rlm_eap_peap.so
%{_libdir}/freeradius/rlm_eap_pwd.so
%{_libdir}/freeradius/rlm_eap_sim.so
%{_libdir}/freeradius/rlm_eap_tls.so
%{_libdir}/freeradius/rlm_eap_ttls.so
%{_libdir}/freeradius/rlm_exec.so
%{_libdir}/freeradius/rlm_expiration.so
%{_libdir}/freeradius/rlm_expr.so
%{_libdir}/freeradius/rlm_files.so
%{_libdir}/freeradius/rlm_ippool.so
%{_libdir}/freeradius/rlm_json.so
%{_libdir}/freeradius/rlm_linelog.so
%{_libdir}/freeradius/rlm_logintime.so
%{_libdir}/freeradius/rlm_mschap.so
%{_libdir}/freeradius/rlm_pam.so
%{_libdir}/freeradius/rlm_pap.so
%{_libdir}/freeradius/rlm_passwd.so
%{_libdir}/freeradius/rlm_preprocess.so
%{_libdir}/freeradius/rlm_radutmp.so
%{_libdir}/freeradius/rlm_realm.so
%{_libdir}/freeradius/rlm_replicate.so
%{_libdir}/freeradius/rlm_soh.so
%{_libdir}/freeradius/rlm_sometimes.so
%{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sqlcounter.so
%{_libdir}/freeradius/rlm_sqlippool.so
%{_libdir}/freeradius/rlm_sql_map.so
%{_libdir}/freeradius/rlm_sql_null.so
%{_libdir}/freeradius/rlm_totp.so
%{_libdir}/freeradius/rlm_unix.so
%{_libdir}/freeradius/rlm_unpack.so
%{_libdir}/freeradius/rlm_utf8.so
%{_libdir}/freeradius/rlm_wimax.so
%{_libdir}/freeradius/rlm_yubikey.so
%{_libdir}/freeradius/rlm_dpsk.so
%{_libdir}/freeradius/rlm_eap_teap.so
%{_libdir}/freeradius/rlm_proxy_rate_limit.so

# main man pages
%doc %{_mandir}/man5/clients.conf.5*
%doc %{_mandir}/man5/dictionary.5*
%doc %{_mandir}/man5/radiusd.conf.5*
%doc %{_mandir}/man5/radrelay.conf.5*
%doc %{_mandir}/man5/rlm_always.5*
%doc %{_mandir}/man5/rlm_attr_filter.5*
%doc %{_mandir}/man5/rlm_chap.5*
%doc %{_mandir}/man5/rlm_counter.5*
%doc %{_mandir}/man5/rlm_detail.5*
%doc %{_mandir}/man5/rlm_digest.5*
%doc %{_mandir}/man5/rlm_expr.5*
%doc %{_mandir}/man5/rlm_files.5*
%doc %{_mandir}/man5/rlm_idn.5*
%doc %{_mandir}/man5/rlm_mschap.5*
%doc %{_mandir}/man5/rlm_pap.5*
%doc %{_mandir}/man5/rlm_passwd.5*
%doc %{_mandir}/man5/rlm_realm.5*
%doc %{_mandir}/man5/rlm_sql.5*
%doc %{_mandir}/man5/rlm_unbound.5*
%doc %{_mandir}/man5/rlm_unix.5*
%doc %{_mandir}/man5/unlang.5*
%doc %{_mandir}/man5/users.5*
%doc %{_mandir}/man8/raddebug.8*
%doc %{_mandir}/man8/radiusd.8*
%doc %{_mandir}/man8/radmin.8*
%doc %{_mandir}/man8/radrelay.8*
%doc %{_mandir}/man8/rlm_sqlippool_tool.8*

# MIB files
%{_datadir}/snmp/mibs/*RADIUS*.mib

%files doc

%doc %{docdir}/


%files utils
%{_bindir}/*

# utils man pages
%doc %{_mandir}/man1/radclient.1*
%doc %{_mandir}/man1/radeapclient.1*
%doc %{_mandir}/man1/radlast.1*
%doc %{_mandir}/man1/radtest.1*
%doc %{_mandir}/man1/radwho.1*
%doc %{_mandir}/man1/radzap.1*
%doc %{_mandir}/man1/rad_counter.1*
%doc %{_mandir}/man1/smbencrypt.1*
%doc %{_mandir}/man1/dhcpclient.1*
%doc %{_mandir}/man5/checkrad.5*
%doc %{_mandir}/man8/radcrypt.8*
%doc %{_mandir}/man8/radsniff.8*
%doc %{_mandir}/man8/radsqlrelay.8*
%doc %{_mandir}/man8/rlm_ippool_tool.8*

%files devel
%{_includedir}/freeradius

%files krb5
%{_libdir}/freeradius/rlm_krb5.so
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/krb5

%files perl
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/perl

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/perl
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/perl/example.pl

%{_libdir}/freeradius/rlm_perl.so

%files -n python-freeradius
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/python3
%{_sysconfdir}/raddb/mods-config/python3/example.py*
%{_sysconfdir}/raddb/mods-config/python3/radiusd.py*
%{_libdir}/freeradius/rlm_python3.so

%files mariadb
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/mysql/noresetcounter.conf

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/cui/mysql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/mysql/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mssql
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mssql/queries.conf
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mssql/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mysql
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mysql/queries.conf
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mysql/schema.sql
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/mysql/setup.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/oracle
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/oracle/queries.conf
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/oracle/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/postgresql
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/postgresql/queries.conf
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/postgresql/schema.sql
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/postgresql/setup.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/sqlite
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/sqlite/queries.conf
%attr(640,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/dhcp/sqlite/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool/mysql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/mysql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/mysql/procedure-no-skip-locked.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mysql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mysql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mysql/procedure-no-skip-locked.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mssql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mssql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mssql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/mssql/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/postgresql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/postgresql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/postgresql/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/mysql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/setup.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/process-radacct.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/extras
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/extras/wimax
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/extras/wimax/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/mysql/extras/wimax/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/ndb
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/ndb/setup.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/ndb/schema.sql
%{_sysconfdir}/raddb/mods-config/sql/main/ndb/README

%{_libdir}/freeradius/rlm_sql_mysql.so

%files postgresql
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/postgresql/noresetcounter.conf

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/cui/postgresql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/postgresql/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool/postgresql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/postgresql/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/postgresql/procedure.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/setup.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/process-radacct.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/extras
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/extras/voip-postpaid.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/postgresql/extras/cisco_h323_db_schema.sql

%{_libdir}/freeradius/rlm_sql_postgresql.so

%files sqlite
%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/counter/sqlite/noresetcounter.conf

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/cui/sqlite
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/cui/sqlite/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool/sqlite
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool/sqlite/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/sqlite
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp/sqlite/schema.sql

%dir %attr(750,root,radiusd) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite/schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite/process-radacct-schema.sql
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite/process-radacct-close-after-reload.pl
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-config/sql/main/sqlite/process-radacct-new-data-usage-period.sh

%{_libdir}/freeradius/rlm_sql_sqlite.so

%files ldap
%{_libdir}/freeradius/rlm_ldap.so
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/ldap

%files unixODBC
%{_libdir}/freeradius/rlm_sql_unixodbc.so

%files freetds
%{_libdir}/freeradius/rlm_sql_freetds.so

%files redis
%{_libdir}/freeradius/rlm_cache_redis.so
%{_libdir}/freeradius/rlm_redis.so
%{_libdir}/freeradius/rlm_rediswho.so

%files memcached
%{_libdir}/freeradius/rlm_cache_memcached.so

%files rest
%{_libdir}/freeradius/rlm_rest.so
%attr(640,root,radiusd) %config(noreplace) %{_sysconfdir}/raddb/mods-available/rest
