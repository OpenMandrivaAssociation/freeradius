%define _disable_ld_no_undefined 1
%define __noautoreq 'perl\\(DBI\\)'

%define major 1
%define libname %mklibname freeradius %{major}
%define develname %mklibname -d freeradius

Summary:	High-performance and highly configurable RADIUS server
Name:		freeradius
Version:	2.2.9
Release:	4
License:	GPLv2+
Group:		System/Servers
URL:		https://www.freeradius.org/
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.gz
Source1:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.gz.sig
Source2:	freeradius.pam-0.77
Source3:	freeradius.pam
Source5:	freeradius.logrotate
Source6:	freeradius.sysconfig
Source7:	freeradius.service
Source8:	freeradius.tmpfiles
# http://code.google.com/p/freeradius-yubikey-module/
Source9:	rlm_yubikey.tar.gz
# Fix certificate location
Patch0:		freeradius-2.1.11-ssl-config.patch
Patch1:		freeradius-server-2.1.6-fix-format-errors.patch
Patch4:		freeradius-0.8.1-use-system-com_err.patch
Patch6:		freeradius-server-2.2.0-avoid-version.diff
Patch7:		freeradius-server-2.1.10-version-info.diff
Patch8:		freeradius-2.0.0-samba3.patch
Patch9:		freeradius-server-2.1.8-ltdl_no_la.patch
Patch10:	freeradius-server-linkage_fix.diff
Patch11:	freeradius-server-2.1.7-fix-perl-scripts.patch
Patch12:	freeradius-server-2.2.0-yubico-paths.diff
BuildRequires:	gdbm-devel
BuildRequires:	krb5-devel
BuildRequires:	sasl-devel
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcap-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpm-helper
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
# minimal version for ssl cert generation
Requires(post): openssl
Requires(post,preun,pre,postun):  rpm-helper

%description
The FreeRADIUS Server Project is a high-performance and highly configurable
GPL'd RADIUS server. It is somewhat similar to the Livingston 2.0 RADIUS
server, but has many more features, and is much more configurable.

%package -n	%{name}-krb5
Summary:	The Kerberos module for %{name}
Group:		System/Servers
Requires:	krb5-libs
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-krb5
The FreeRADIUS server can use Kerberos to authenticate users, and this module
is necessary for that.

%package -n	%{name}-ldap
Summary:	The LDAP module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-ldap
The FreeRADIUS server can use LDAP to authenticate users, and this module is
necessary for that.

%package -n	%{name}-postgresql
Summary:	The PostgreSQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-postgresql
The FreeRADIUS server can use PostgreSQL to authenticate users and do
accounting, and this module is necessary for that.

%package -n	%{name}-mysql
Summary:	The MySQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-mysql
The FreeRADIUS server can use MySQL to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-unixODBC
Summary:	The unixODBC module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-unixODBC
The FreeRADIUS server can use unixODBC to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-sqlite
Summary:	The sqlite module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-sqlite
The FreeRADIUS server can use sqlite to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-yubikey
Summary:	The yubikey module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description -n	%{name}-yubikey
The FreeRADIUS server can use yubikey to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
Libraries for %{name}

%package -n	%{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname -d %{name} 1}
Provides:	freeradius-devel = %{version}-%{release}

%description -n	%{develname}
Development headers and libraries for %{name}

%package web
Summary:	Web based administration interface for freeradius
Group:		System/Servers
Requires:	apache-mod_php
Requires:	freeradius
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
Provides:	dialup_admin = %{version}-%{release}

%description web
dialup_admin is a web based administration interface for the freeradius radius
server. It is written in PHP4. It is modular and right now it assumes that user
information is stored in an ldap server or an sql database and accounting in an
sql server.

%prep
%setup -q -n %{name}-server-%{version}

# add the yubikey plugin from http://code.google.com/p/freeradius-yubikey-module/
tar -zxf %{SOURCE9}
mv freeradius-yubikey-module-read-only src/modules/rlm_yubikey

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch0 -p1 -b .config
%patch4 -p1 -b .peroyvind
%patch6 -p1 -b .avoid-version
%patch7 -p1 -b .version-info
%patch8 -p0 -b .samba3
%patch9 -p1 -b .ltdl_no_la
%patch10 -p0 -b .linkage_fix
%patch11 -p1 -b .file-temp
%patch1 -p 1
%patch12 -p0

./autogen.sh

# For pre release only:
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/Makefile
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/rfc/Makefile

# fix path
find . -type f | xargs perl -pi -e "s|/usr/local/bin|%{_bindir}|g"

# move php3 to php
find dialup_admin -name '*.php3' | while read php3; do
    mv $php3 ${php3%%.php3}.php
done

find dialup_admin -type f | xargs perl -pi -e "s|\.php3|\.php|g"
perl -pi -e "s|\\\${bindir}|\\\${bindir}/|g" dialup_admin/Makefile

%build
%serverbuild

export CFLAGS="$CFLAGS -fPIC -DLDAP_DEPRECATED"
export CXXFLAGS="$CXXFLAGS -fPIC -DLDAP_DEPRECATED"
export PYTHONBIN=%{__python2}

%configure2_5x \
    --with-gnu-ld \
    --with-threads \
    --with-thread-pool \
    --with-system-libtool \
    --with-system-libltdl \
    --disable-static \
    --libdir=%{_libdir}/%{name}  \
    --libexecdir=%{_libdir}/%{name} \
    --localstatedir=%{_var} \
    --with-logdir=%{_var}/log/radius \
    --disable-ltdl-install \
    --with-ltdl-lib=%{_libdir} \
    --with-ltdl-include=%{_includedir} \
    --with-radacctdir=%{_var}/log/radius/radacct \
    --with-raddbdir=%{_sysconfdir}/raddb \
    --with-static-modules="" \
    --with-experimental-modules \
    --with-large-files \
    --with-rlm-dbm-lib-dir=%{_libdir} \
    --with-rlm-eap-peap-lib-dir=%{_libdir} \
    --with-openssl-libraries=%{_libdir} \
    --with-rlm-ruby-include-dir=%{_includedir}/ruby \
    --with-rlm-krb5-lib-dir=%{_libdir} \
    --with-rlm-ldap-lib-dir=%{_libdir} \
    --with-rlm-ldap-include-dir=%{_includedir}/ldap \
    --with-mysql-include-dir=%{_includedir}/mysql \
    --with-mysql-lib-dir=%{_libdir}/mysql \
    --with-mysql-dir=%{_prefix} \
    --with-rlm-sql-postgresql-lib-dir=%{_libdir}/mysql \
    --with-rlm-sql-postgresql-include-dir=%{_includedir}/pgsql \
    --with-unixodbc-lib-dir=%{_libdir} \
    --with-unixodbc-dir=%{_prefix} \
    --without-rlm_sql_db2 \
    --without-rlm_sql_firebird \
    --without-rlm_sql_freetds \
    --without-rlm_sql_iodbc \
    --without-rlm_sql_oracle \
    --without-rlm_sql_sybase \
    --without-rlm_ruby \

# enable this one with a hack...
perl -pi \
    -e "s|^TARGET.*|TARGET=rlm_dbm|g;" \
    -e "s|^SRCS.*|SRCS=rlm_dbm.c|g;" \
    -e "s|^RLM_UTILS.*|RLM_UTILS=rlm_dbm_parser rlm_dbm_cat|g;" \
    -e "s|^RLM_CFLAGS.*|RLM_CFLAGS=-I%{_includedir}/gdbm -DHAVE_GDBM_NDBM_H|g;" \
    -e "s|^RLM_LIBS.*|RLM_LIBS=-L%{_libdir} -lgdbm -lgdbm_compat|g;" \
    -e "s|^RLM_INSTALL.*|RLM_INSTALL=rlm_dbm_install|g;" \
    src/modules/rlm_dbm/Makefile

%if "%{_lib}" == "lib64"
    perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

make

%install
make install R=%{buildroot}

install -d %{buildroot}%{_sysconfdir}/raddb/yubico

# fix default configuration file permissions
find %{buildroot}%{_sysconfdir}/raddb -type d | xargs chmod 755
find %{buildroot}%{_sysconfdir}/raddb -type f | xargs chmod 644
chmod 640 \
    %{buildroot}%{_sysconfdir}/raddb/acct_users \
    %{buildroot}%{_sysconfdir}/raddb/acct_users \
    %{buildroot}%{_sysconfdir}/raddb/clients.conf \
    %{buildroot}%{_sysconfdir}/raddb/preproxy_users \
    %{buildroot}%{_sysconfdir}/raddb/users \

# install headers
install -d -m 755 %{buildroot}%{_includedir}/%{name}
install -m 644 src/include/*  %{buildroot}%{_includedir}/%{name}/

# install distribution scripts and stuff...
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/radiusd
install -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/radiusd
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/radiusd
install -D -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/radiusd.service
install -D -m 644 %{SOURCE8} %{buildroot}%{_prefix}/lib/tmpfiles.d/radiusd.conf

# put the mibs in place
install -d -m 755 %{buildroot}%{_datadir}/snmp/mibs
install -m 644 mibs/RADIUS* %{buildroot}%{_datadir}/snmp/mibs/

# fix ghostfiles
touch %{buildroot}%{_localstatedir}/log/radius/radutmp
touch %{buildroot}%{_localstatedir}/log/radius/radwtmp
touch %{buildroot}%{_localstatedir}/log/radius/radius.log

# remove unneeded stuff
rm -f %{buildroot}%{_sbindir}/rc.radiusd
rm -f %{buildroot}%{_includedir}/%{name}/Makefile
rm -f %{buildroot}%{_sysconfdir}/raddb/Makefile
rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/mssql
rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/oracle
rm -f %{buildroot}%{_sysconfdir}/raddb/certs/*

find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/%{name}/*.a

# include more docs
cp src/modules/rlm_sql/README README.sql
cp src/modules/rlm_cram/Readme Readme.cram
cp src/modules/rlm_cram/Standard.draft .
cp src/modules/rlm_cram/dictionary.sandy .
cp src/modules/rlm_smb/README README.smb

# put specific docs and files where they belong (prepare for doc inclusion)
cp doc/rlm_krb5 .
cp doc/RADIUS*.schema .
cp doc/rlm_ldap .

%multiarch_includes %{buildroot}%{_includedir}/freeradius/build-radpaths-h

%multiarch_includes %{buildroot}%{_includedir}/freeradius/radpaths.h

# the web cruft
install -d %{buildroot}%{_datadir}/%{name}-web
install -d %{buildroot}%{_sysconfdir}/%{name}-web

pushd dialup_admin
make \
    DIALUP_PREFIX=%{buildroot}%{_datadir}/freeradius-web \
    DIALUP_DOCDIR=%{buildroot}%{_docdir}/freeradius-web \
    DIALUP_CONFDIR=%{buildroot}%{_sysconfdir}/freeradius-web \
    install
popd

find %{buildroot}%{_datadir}/freeradius-web | xargs perl -pi \
    -e 's|\.\./conf/config\.php|%{_sysconfdir}/freeradius-web/config\.php|g;' \
    -e 's|%{buildroot}||g;'

find %{buildroot}%{_sysconfdir}/freeradius-web | xargs perl -pi \
    -e 's|\.\./conf/admin\.conf|%{_sysconfdir}/freeradius-web/admin\.conf|g;' \
    -e 's|%{buildroot}||g;'

find %{buildroot}%{_datadir}/freeradius-web/bin | xargs perl -pi \
    -e 's|/data/local/dialupadmin/conf/admin\.conf|%{_sysconfdir}/freeradius-web/admin\.conf|g;' \
    -e 's|/logs/radiusd/accounting|%{_localstatedir}/log/radius/accounting|g;'

mv %{buildroot}%{_datadir}/freeradius-web/bin/* %{buildroot}%{_bindir}
mv %{buildroot}%{_bindir}/snmpfinger \
    %{buildroot}%{_bindir}/freeradius-web-snmpfinger

# fix a simple redirector
cat > %{buildroot}%{_datadir}/%{name}-web/index.html << EOF
<html>
<head>
<title></title>
<meta HTTP-EQUIV="REFRESH" CONTENT="0; URL=htdocs/index.html">
</head>
<body>
</body>
</html>
EOF

# apache configuration
install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}-web.conf <<EOF
# %{name} Apache configuration
Alias /%{name}-web %{_datadir}/%{name}-web

<Directory %{_datadir}/%{name}-web>
    Require all granted
</Directory>
EOF

# cron stuff
install -d %{buildroot}%{_sysconfdir}/cron.daily
cat > %{buildroot}%{_sysconfdir}/cron.daily/%{name}-web <<EOF
#!/bin/sh
%{_bindir}/tot_stats >/dev/null 2>&1
%{_bindir}/monthly_tot_stats >/dev/null 2>&1
EOF
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/%{name}-web

install -d %{buildroot}%{_sysconfdir}/cron.monthly
cat > %{buildroot}%{_sysconfdir}/cron.monthly/%{name}-web <<EOF
#!/bin/sh
%{_bindir}/truncate_radacct >/dev/null 2>&1
%{_bindir}/clean_radacct >/dev/null 2>&1
EOF
chmod 755 %{buildroot}%{_sysconfdir}/cron.monthly/%{name}-web

# cleanup
rm -rf %{buildroot}%{_docdir}/%{name}
rm -rf %{buildroot}%{_docdir}/freeradius-web
rm -rf %{buildroot}%{_datadir}/freeradius-web/bin
rm -rf %{buildroot}%{_datadir}/freeradius-web/sql
rm -f %{buildroot}%{_bindir}/dialup_admin.cron

%pre
%_pre_useradd radius %{_localstatedir}/log/radius/radacct /bin/false

%post
%_post_service radiusd
%create_ghostfile %{_localstatedir}/log/radius/radutmp radius radius 0644
%create_ghostfile %{_localstatedir}/log/radius/radwtmp radius radius 0644
%create_ghostfile %{_localstatedir}/log/radius/radius.log radius radius 0644
%_create_ssl_certificate radiusd -g radius
if [ $1 = 1 ]; then
    openssl dhparam -out  %{_sysconfdir}/raddb/certs/dh 1024 2>&1 >/dev/null
    dd if=/dev/urandom of=%{_sysconfdir}/raddb/certs/random count=10 2>&1 >/dev/null
    chgrp radius %{_sysconfdir}/raddb/certs/random
fi

%preun
%_preun_service radiusd

%postun
%_postun_userdel radius

%files
%doc doc COPYRIGHT CREDITS INSTALL LICENSE README.rst
%doc README.sql README.smb Readme.cram Standard.draft dictionary.sandy
%{_unitdir}/radiusd.service
%{_prefix}/lib/tmpfiles.d/radiusd.conf
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%config(noreplace)  %{_sysconfdir}/sysconfig/radiusd
%dir %{_sysconfdir}/raddb
%config(noreplace) %{_sysconfdir}/raddb/attrs
%config(noreplace) %{_sysconfdir}/raddb/attrs.access_reject
%config(noreplace) %{_sysconfdir}/raddb/attrs.access_challenge
%config(noreplace) %{_sysconfdir}/raddb/attrs.accounting_response
%config(noreplace) %{_sysconfdir}/raddb/attrs.pre-proxy
%config(noreplace) %{_sysconfdir}/raddb/dictionary*
%config(noreplace) %{_sysconfdir}/raddb/experimental.conf
%config(noreplace) %{_sysconfdir}/raddb/example.pl
%config(noreplace) %{_sysconfdir}/raddb/hints
%config(noreplace) %{_sysconfdir}/raddb/huntgroups
%config(noreplace) %{_sysconfdir}/raddb/radiusd.conf
%config(noreplace) %{_sysconfdir}/raddb/panic.gdb
%config(noreplace) %{_sysconfdir}/raddb/policy.conf
%config(noreplace) %{_sysconfdir}/raddb/policy.txt
%config(noreplace) %{_sysconfdir}/raddb/proxy.conf
%config(noreplace) %{_sysconfdir}/raddb/eap.conf
%config(noreplace) %{_sysconfdir}/raddb/sql.conf
%config(noreplace) %{_sysconfdir}/raddb/sqlippool.conf
%config(noreplace) %{_sysconfdir}/raddb/templates.conf
# those contains passwords
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/acct_users
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/clients.conf
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/preproxy_users
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/users
%dir %{_sysconfdir}/raddb/certs
%dir %{_sysconfdir}/raddb/sites-available
%dir %{_sysconfdir}/raddb/sites-enabled
%config(noreplace) %{_sysconfdir}/raddb/sites-available/*
%config(noreplace) %{_sysconfdir}/raddb/sites-enabled/*
%dir %{_sysconfdir}/raddb/modules
%config(noreplace) %{_sysconfdir}/raddb/modules/*
%dir %{_sysconfdir}/raddb/sql
%dir %{_sysconfdir}/raddb/sql/ndb
%config(noreplace) %{_sysconfdir}/raddb/sql/ndb/README
%config(noreplace) %{_sysconfdir}/raddb/sql/ndb/admin.sql
%config(noreplace) %{_sysconfdir}/raddb/sql/ndb/schema.sql
%{_bindir}/radclient
%{_bindir}/radconf2xml
%{_bindir}/rad_counter
%{_bindir}/radcrypt
%{_bindir}/radeapclient
%{_bindir}/radlast
%{_bindir}/radsniff
%{_bindir}/radsqlrelay
%{_bindir}/radtest
%{_bindir}/radwho
%{_bindir}/radzap
%{_bindir}/rlm_dbm_cat
%{_bindir}/rlm_dbm_parser
%{_bindir}/rlm_ippool_tool
%{_bindir}/smbencrypt
%{_sbindir}/checkrad
%{_sbindir}/raddebug
%{_sbindir}/radiusd
%{_sbindir}/radmin
%{_sbindir}/radwatch
%attr(0755,radius,radius) %dir %{_localstatedir}/log/radius
%attr(0755,radius,radius) %dir %{_localstatedir}/log/radius/radacct
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radutmp
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radwtmp
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radius.log
%{_datadir}/snmp/mibs/*
%{_datadir}/freeradius
%{_mandir}/man*/*

%files -n %{name}-krb5
%doc rlm_krb5
%{_libdir}/%{name}/rlm_krb5.so

%files -n %{name}-ldap
%doc RADIUS*.schema rlm_ldap doc/examples/openldap.schema
%config(noreplace) %{_sysconfdir}/raddb/ldap.attrmap
%{_libdir}/%{name}/rlm_ldap.so

%files -n %{name}-postgresql
%doc src/billing
%config(noreplace) %{_sysconfdir}/raddb/sql/postgresql
%{_libdir}/%{name}/rlm_sql_postgresql.so

%files -n %{name}-mysql
%config(noreplace) %{_sysconfdir}/raddb/sql/mysql
%{_libdir}/%{name}/rlm_sql_mysql.so

%files -n %{name}-unixODBC
%{_libdir}/%{name}/rlm_sql_unixodbc.so

%files -n %{name}-sqlite
%{_libdir}/%{name}/rlm_sql_sqlite.so

%files -n %{name}-yubikey
%dir %{_sysconfdir}/raddb/yubico
%{_libdir}/%{name}/rlm_yubikey.so

%files -n %{libname}
%{_libdir}/%{name}/libfreeradius-radius.so.%{major}*
%{_libdir}/%{name}/libfreeradius-eap.so.%{major}*
%{_libdir}/%{name}/rlm_acctlog.so
%{_libdir}/%{name}/rlm_acct_unique.so
%{_libdir}/%{name}/rlm_always.so
%{_libdir}/%{name}/rlm_attr_filter.so
%{_libdir}/%{name}/rlm_attr_rewrite.so
%{_libdir}/%{name}/rlm_cache.so
%{_libdir}/%{name}/rlm_caching.so
%{_libdir}/%{name}/rlm_chap.so
%{_libdir}/%{name}/rlm_checkval.so
%{_libdir}/%{name}/rlm_copy_packet.so
%{_libdir}/%{name}/rlm_counter.so
%{_libdir}/%{name}/rlm_cram.so
%{_libdir}/%{name}/rlm_dbm.so
%{_libdir}/%{name}/rlm_detail.so
%{_libdir}/%{name}/rlm_digest.so
%{_libdir}/%{name}/rlm_dynamic_clients.so
%{_libdir}/%{name}/rlm_eap_gtc.so
%{_libdir}/%{name}/rlm_eap_leap.so
%{_libdir}/%{name}/rlm_eap_md5.so
%{_libdir}/%{name}/rlm_eap_mschapv2.so
%{_libdir}/%{name}/rlm_eap_peap.so
%{_libdir}/%{name}/rlm_eap_sim.so
%{_libdir}/%{name}/rlm_eap.so
%{_libdir}/%{name}/rlm_eap_tls.so
%{_libdir}/%{name}/rlm_eap_ttls.so
%{_libdir}/%{name}/rlm_example.so
%{_libdir}/%{name}/rlm_exec.so
%{_libdir}/%{name}/rlm_expiration.so
%{_libdir}/%{name}/rlm_expr.so
%{_libdir}/%{name}/rlm_fastusers.so
%{_libdir}/%{name}/rlm_files.so
%{_libdir}/%{name}/rlm_ippool.so
%{_libdir}/%{name}/rlm_jradius.so
%{_libdir}/%{name}/rlm_linelog.so
%{_libdir}/%{name}/rlm_logintime.so
%{_libdir}/%{name}/rlm_mschap.so
%{_libdir}/%{name}/rlm_otp.so
%{_libdir}/%{name}/rlm_pam.so
%{_libdir}/%{name}/rlm_pap.so
%{_libdir}/%{name}/rlm_passwd.so
%{_libdir}/%{name}/rlm_perl.so
%{_libdir}/%{name}/rlm_policy.so
%{_libdir}/%{name}/rlm_preprocess.so
%{_libdir}/%{name}/rlm_protocol_filter.so
%{_libdir}/%{name}/rlm_python.so
%{_libdir}/%{name}/rlm_radutmp.so
%{_libdir}/%{name}/rlm_realm.so
%{_libdir}/%{name}/rlm_replicate.so
#%{_libdir}/%{name}/rlm_ruby.so
%{_libdir}/%{name}/rlm_sim_files.so
%{_libdir}/%{name}/rlm_smsotp.so
%{_libdir}/%{name}/rlm_soh.so
%{_libdir}/%{name}/rlm_sqlcounter.so
%{_libdir}/%{name}/rlm_sqlhpwippool.so
%{_libdir}/%{name}/rlm_sqlippool.so
%{_libdir}/%{name}/rlm_sql_log.so
%{_libdir}/%{name}/rlm_sql.so
%{_libdir}/%{name}/rlm_unix.so
%{_libdir}/%{name}/rlm_wimax.so

%files -n %{develname}
%doc todo
%{multiarch_includedir}/freeradius/build-radpaths-h
%{multiarch_includedir}/freeradius/radpaths.h
%{_includedir}/%{name}
%{_libdir}/%{name}/libfreeradius-radius.so
%{_libdir}/%{name}/libfreeradius-eap.so

%files -n %{name}-web
%doc dialup_admin/sql/mysql dialup_admin/sql/postgresql dialup_admin/sql/oracle
%doc dialup_admin/doc/AUTHORS dialup_admin/doc/FAQ dialup_admin/doc/HELP_WANTED
%doc dialup_admin/doc/HOWTO dialup_admin/doc/TODO dialup_admin/Changelog
%doc dialup_admin/README dialup_admin/bin/Changelog.*
%config(noreplace) %{_sysconfdir}/cron.daily/%{name}-web
%config(noreplace) %{_sysconfdir}/cron.monthly/%{name}-web
%config(noreplace) %{_webappconfdir}/%{name}-web.conf
%dir %{_sysconfdir}/%{name}-web
%config(noreplace) %{_sysconfdir}/%{name}-web/accounting.attrs
%config(noreplace) %{_sysconfdir}/%{name}-web/auth.request
%config(noreplace) %{_sysconfdir}/%{name}-web/default.vals
%config(noreplace) %{_sysconfdir}/%{name}-web/extra.ldap-attrmap
%config(noreplace) %{_sysconfdir}/%{name}-web/sql.attrmap
%config(noreplace) %{_sysconfdir}/%{name}-web/sql.attrs
%config(noreplace) %{_sysconfdir}/%{name}-web/user_edit.attrs
%config(noreplace) %{_sysconfdir}/%{name}-web/username.mappings
# those contains passwords
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{name}-web/admin.conf
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{name}-web/captions.conf
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{name}-web/naslist.conf
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{name}-web/config.php
%{_bindir}/backup_radacct
%{_bindir}/clean_radacct
%{_bindir}/clearsession
%{_bindir}/freeradius-web-snmpfinger
%{_bindir}/log_badlogins
%{_bindir}/monthly_tot_stats
%{_bindir}/showmodem
%{_bindir}/sqlrelay_query
%{_bindir}/tot_stats
%{_bindir}/truncate_radacct
%{_datadir}/%{name}-web
