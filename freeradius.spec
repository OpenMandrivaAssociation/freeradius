%define _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname freeradius %{major}
%define develname %mklibname -d freeradius

%define __noautoreq 'perl\\(DBI\\)'

Summary:	High-performance and highly configurable RADIUS server
Name:		freeradius
Version:	2.1.12
Release:	6
License:	GPL
Group:		System/Servers
URL:		http://www.freeradius.org/
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.bz2
Source1:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.bz2.sig
Source3:	freeradius.pam
Source4:	freeradius.init
Source5:	freeradius.logrotate
Source6:	freeradius.sysconfig
Patch0:		freeradius-2.1.11-ssl-config.patch
Patch1:		freeradius-server-2.1.6-fix-format-errors.patch
Patch4:		freeradius-0.8.1-use-system-com_err.patch
Patch6:		freeradius-server-2.1.10-avoid-version.diff
Patch7:		freeradius-server-2.1.10-version-info.diff
Patch8:		freeradius-2.0.0-samba3.patch
Patch9:		freeradius-server-2.1.8-ltdl_no_la.patch
Patch10:	freeradius-server-linkage_fix.diff
Patch11:	freeradius-server-2.1.7-fix-perl-scripts.patch
Patch12:	freeradius-server-2.1.12-fix_broken_perl_ldflags.diff
BuildRequires:	gdbm-devel
BuildRequires:	krb5-devel
BuildRequires:	sasl-devel
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcap-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpm-helper >= 0.21
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
# minimal version for ssl cert generation
Requires(post): openssl
Requires(post): rpm-helper >= 0.21
Requires(preun): rpm-helper >= 0.19
Requires(pre): rpm-helper >= 0.19
Requires(postun): rpm-helper >= 0.19
Conflicts:	radiusd-cistron
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
The FreeRADIUS Server Project is a high-performance and highly configurable
GPL'd RADIUS server. It is somewhat similar to the Livingston 2.0 RADIUS
server, but has many more features, and is much more configurable.

%package -n	%{name}-krb5
Summary:	The Kerberos module for %{name}
Group:		System/Servers
Requires:	krb5-libs
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-krb5

%description -n	%{name}-krb5
The FreeRADIUS server can use Kerberos to authenticate users, and this module
is necessary for that.

%package -n	%{name}-ldap
Summary:	The LDAP module for %{name}
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-ldap

%description -n	%{name}-ldap
The FreeRADIUS server can use LDAP to authenticate users, and this module is
necessary for that.

%package -n	%{name}-postgresql
Summary:	The PostgreSQL module for %{name}
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-postgresql

%description -n	%{name}-postgresql
The FreeRADIUS server can use PostgreSQL to authenticate users and do
accounting, and this module is necessary for that.

%package -n	%{name}-mysql
Summary:	The MySQL module for %{name}
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-mysql

%description -n	%{name}-mysql
The FreeRADIUS server can use MySQL to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-unixODBC
Summary:	The unixODBC module for %{name}
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-unixODBC

%description -n	%{name}-unixODBC
The FreeRADIUS server can use unixODBC to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-sqlite
Summary:	The sqlite module for %{name}
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}
Obsoletes:	%{libname}-sqlite

%description -n	%{name}-sqlite
The FreeRADIUS server can use sqlite to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
Libraries for %{name}

%package -n	%{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	%{mklibname -d %{name} 1}
Provides:	freeradius-devel = %{version}-%{release}
Obsoletes:	freeradius-devel

%description -n	%{develname}
Development headers and libraries for %{name}

%package web
Summary:	Web based administration interface for freeradius
Group:		System/Servers
Requires:	apache-mod_php
Requires:	freeradius
Requires:	php-mysql
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
Provides:	dialup_admin = %{version}-%{release}
Obsoletes:	dialup_admin

%description web
dialup_admin is a web based administration interface for the freeradius radius
server. It is written in PHP4. It is modular and right now it assumes that user
information is stored in an ldap server or an sql database and accounting in an
sql server.

%prep
%setup -q -n %{name}-server-%{version}

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch0 -p0 -b .config
%patch4 -p0 -b .peroyvind
%patch6 -p1 -b .avoid-version
%patch7 -p1 -b .version-info
%patch8 -p0 -b .samba3
%patch9 -p1 -b .ltdl_no_la
%patch10 -p0 -b .linkage_fix
%patch11 -p1 -b .file-temp
%patch1 -p 1
%patch12 -p1 -b .fix_broken_perl_ldflags

# For pre release only:
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/Makefile
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/rfc/Makefile

%__install -d Mandriva
# fix conditional pam config file
cp %{SOURCE3} Mandriva/freeradius.pam
cp %{SOURCE4} Mandriva/%{name}.init
cp %{SOURCE5} Mandriva/%{name}.logrotate

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

%configure2_5x \
    --with-gnu-ld \
    --with-threads \
    --with-thread-pool \
    --with-system-libtool \
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
rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
%__install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
%__install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
%__install -d -m 755 %{buildroot}%{_initrddir}
%__install -d -m 755 %{buildroot}%{_localstatedir}/run/radiusd
%__install -d -m 755 %{buildroot}%{_includedir}/%{name}

make install R=%{buildroot}

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
%__install -m 644 src/include/*  %{buildroot}%{_includedir}/%{name}/

# install Mandriva scripts and stuff...
%__install -m 644 Mandriva/%{name}.pam %{buildroot}%{_sysconfdir}/pam.d/radiusd
%__install -m 644 Mandriva/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/radiusd
%__install -m 755 Mandriva/%{name}.init %{buildroot}%{_initrddir}/radiusd
%__install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/radiusd

# put the mibs in place
%__install -d -m 755 %{buildroot}%{_datadir}/snmp/mibs
%__install -m 644 mibs/RADIUS* %{buildroot}%{_datadir}/snmp/mibs/

# fix ghostfiles
touch %{buildroot}%{_localstatedir}/log/radius/radutmp
touch %{buildroot}%{_localstatedir}/log/radius/radwtmp
touch %{buildroot}%{_localstatedir}/log/radius/radius.log

# remove unneeded stuff
%__rm -f %{buildroot}%{_sbindir}/rc.radiusd
%__rm -f %{buildroot}%{_includedir}/%{name}/Makefile
%__rm -f %{buildroot}%{_sysconfdir}/raddb/Makefile
%__rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/mssql
%__rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/oracle
%__rm -f %{buildroot}%{_sysconfdir}/raddb/certs/*

# remove faulty perl file...
%__rm -f %{buildroot}%{_libdir}/%{name}/rlm_perl.a

# include more docs
%__cp src/modules/rlm_sql/README README.sql
%__cp src/modules/rlm_cram/Readme Readme.cram
%__cp src/modules/rlm_cram/Standard.draft .
%__cp src/modules/rlm_cram/dictionary.sandy .
%__cp src/modules/rlm_smb/README README.smb

# put specific docs and files where they belong (prepare for doc inclusion)
%__cp doc/rlm_krb5 .
%__cp doc/RADIUS*.schema .
%__cp doc/rlm_ldap .

# nuke useless dupes
rm -f %{buildroot}%{_libdir}/%{name}/*%{version}*.la

#remove buildroot from the libtool files:
perl -pi -e "s,(\s)\S+%{_builddir}\S+,\$1,g" \
    %{buildroot}%{_libdir}/%{name}/*.la 

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
    Allow from all
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

%clean

%files
%defattr(-,root,root)
%doc doc COPYRIGHT CREDITS INSTALL LICENSE README
%doc README.sql README.smb Readme.cram Standard.draft dictionary.sandy
%{_initrddir}/radiusd
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
%attr(0755,radius,radius) %dir %{_localstatedir}/run/radiusd
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radutmp
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radwtmp
%attr(0644,radius,radius) %ghost %{_localstatedir}/log/radius/radius.log
%{_datadir}/snmp/mibs/*
%{_datadir}/freeradius
%{_mandir}/man*/*

%files -n %{name}-krb5
%defattr(-,root,root)
%doc rlm_krb5
%{_libdir}/%{name}/rlm_krb5.so

%files -n %{name}-ldap
%defattr(-,root,root)
%doc RADIUS*.schema rlm_ldap doc/examples/openldap.schema
%config(noreplace) %{_sysconfdir}/raddb/ldap.attrmap
%{_libdir}/%{name}/rlm_ldap.so

%files -n %{name}-postgresql
%defattr(-,root,root)
%doc src/billing
%config(noreplace) %{_sysconfdir}/raddb/sql/postgresql
%{_libdir}/%{name}/rlm_sql_postgresql.so

%files -n %{name}-mysql
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/raddb/sql/mysql
%{_libdir}/%{name}/rlm_sql_mysql.so

%files -n %{name}-unixODBC
%defattr(-,root,root)
%{_libdir}/%{name}/rlm_sql_unixodbc.so

%files -n %{name}-sqlite
%defattr(-,root,root)
%{_libdir}/%{name}/rlm_sql_sqlite.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}/libfreeradius-radius.so.%{major}*
%{_libdir}/%{name}/libfreeradius-eap.so.%{major}*
%{_libdir}/%{name}/rlm_acctlog.so
%{_libdir}/%{name}/rlm_acct_unique.so
%{_libdir}/%{name}/rlm_always.so
%{_libdir}/%{name}/rlm_attr_filter.so
%{_libdir}/%{name}/rlm_attr_rewrite.so
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
%defattr(-,root,root)
%doc todo
%{multiarch_includedir}/freeradius/build-radpaths-h
%{multiarch_includedir}/freeradius/radpaths.h
%{_includedir}/%{name}
%{_libdir}/%{name}/libfreeradius-radius.so
%{_libdir}/%{name}/libfreeradius-eap.so

%files -n %{name}-web
%defattr(-,root,root)
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


%changelog
* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.12-4mdv2012.0
+ Revision: 739190
- rebuilt for new unixODBC (second try)
- rebuilt for new unixODBC

* Mon Nov 28 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.12-2
+ Revision: 734982
- relink against new pcap

* Sat Nov 12 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.12-1
+ Revision: 730297
- whoops!
- better fix
- fix build
- 2.1.12

* Sat Jun 25 2011 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.11-1
+ Revision: 687125
- new version

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 2.1.10-6
+ Revision: 661954
- fix building

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.10-5
+ Revision: 645745
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.10-4mdv2011.0
+ Revision: 627018
- rebuilt against mysql-5.5.8 libs, again

* Wed Dec 29 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.10-3mdv2011.0
+ Revision: 625969
- fix build, %%make works fine locally with 8 cores but not in the bs
- fix deps
- major overhaul
- rebuilt against mysql-5.5.8 libs

  + Funda Wang <fwang@mandriva.org>
    - rebuild for py2.7

* Fri Oct 01 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.10-1mdv2011.0
+ Revision: 582364
- 2.1.10

* Mon Jul 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.9-1mdv2011.0
+ Revision: 554949
- new version

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 2.1.8-6mdv2010.1
+ Revision: 533319
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.8-5mdv2010.1
+ Revision: 513129
- fix installation dependencies

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.8-4mdv2010.1
+ Revision: 511567
- rebuilt against openssl-0.9.8m

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.8-3mdv2010.1
+ Revision: 507458
- rebuild

* Tue Feb 16 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.8-2mdv2010.1
+ Revision: 506695
- change default permissions for configuration files, only restrict those containing passwords

* Tue Jan 12 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.8-1mdv2010.1
+ Revision: 490250
- new version

* Sat Jan 09 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.7-4mdv2010.1
+ Revision: 488013
- no need to explicit calls to %%_post_webapp/%%_postun_webapp, we have filetriggers now
- don't forget to apply patch...

* Sat Jan 09 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.7-3mdv2010.1
+ Revision: 487978
- fix scripts shipped in freeradius-web package (bud #56866)

* Fri Oct 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.7-2mdv2010.0
+ Revision: 456255
- move crontab in scripts, and install them in /etc/cron/{daily,monthly} (#46739)

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.7-1mdv2010.0
+ Revision: 445976
- new version
- spec cleanup
- install web files under %%{_datadir}/freeradius-web
- fix initscript LSB dependency

* Thu Jun 11 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.6-1mdv2010.0
+ Revision: 385293
- new version

* Tue Mar 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.4-1mdv2009.1
+ Revision: 356678
- rediff fuzzy patch
- force system libtool usage
- new version
- fix perms on some config files

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 2.1.3-3mdv2009.1
+ Revision: 319937
- rebuild for new python

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.3-2mdv2009.1
+ Revision: 315153
- bump release
- rediffed fuzzy patches

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.3-1mdv2009.1
+ Revision: 311824
- 2.1.3 (fixes CVE-2008-4474)
- rediffed P10

* Mon Dec 08 2008 Funda Wang <fwang@mandriva.org> 2.1.1-3mdv2009.1
+ Revision: 311797
- rebuild for new mysql

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-2mdv2009.1
+ Revision: 298254
- rebuilt against libpcap-1.0.0

* Wed Oct 15 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-1mdv2009.1
+ Revision: 293908
- fix build
- 2.1.1

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2009.0
+ Revision: 282138
- bump release
- fix deps
- provide dialup_admin as the freeradius-web subpackage

* Fri Sep 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1mdv2009.0
+ Revision: 281123
- 2.1.0
- rediffed P0

* Tue Aug 19 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.5-1mdv2009.0
+ Revision: 273882
- 2.0.5
- use _disable_ld_no_undefined due to ugly autopoo
- rediffed P0
- fix some linking (P10)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Wed Apr 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.3-1mdv2009.0
+ Revision: 199400
- new version
  clean file section

* Tue Apr 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-8mdv2009.0
+ Revision: 196536
- fix cert file names in configuration

* Thu Apr 10 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-7mdv2009.0
+ Revision: 192550
- don't hardcode options in the init script, it breaks

* Mon Mar 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-6mdv2008.1
+ Revision: 189765
- fix dependencies from krb5 plugin

* Fri Feb 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-5mdv2008.1
+ Revision: 168812
- rebuild with fixed version of rpm-helper

* Wed Feb 13 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-4mdv2008.1
+ Revision: 166947
- add versioned build dependency on rpm-helper
- fix %%post

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-3mdv2008.1
+ Revision: 158717
- use new create ssl certificate helper macro interface

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 2.0.0-2mdv2008.1
+ Revision: 157250
- rebuild with fixed %%serverbuild macro

* Thu Jan 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-1mdv2008.1
+ Revision: 154222
- spec cleanup
- plugins package renaming, as they are not concerned by lib policy naming
- devel policy compliance
- library package doesn't need main package, but devel package requires library package
- new version
  rediff patches 0, 6 and 8
  drop useless patch 5
  post-installation ssl configuration, according to ssl policy

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.1.7-3mdv2008.1
+ Revision: 150082
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.7-2mdv2008.0
+ Revision: 89646
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

* Fri Aug 17 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.7-1mdv2008.0
+ Revision: 64984
- rewrite init script
- revert wrong previous commiy
- fix automatic perl dependency
- new version

* Thu Jun 28 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.6-2mdv2008.0
+ Revision: 45543
- rebuild with new serverbuild macro (-fstack-protector-all)

* Mon May 28 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.6-1mdv2008.0
+ Revision: 32081
- updated to version 1.1.6
- removed enormous libtool patch
- removed security patch that was already applied

* Thu Apr 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.2-6mdv2008.0
+ Revision: 14940
- P10: security fix for CVE-2007-2028


* Mon Jan 15 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.2-5mdv2007.0
+ Revision: 109065
- fixed rpm group for library and devel package (#28162)

* Fri Jan 05 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.2-4mdv2007.1
+ Revision: 104506
- rebuild with python 2.5

  + Oden Eriksson <oeriksson@mandriva.com>
    - bzip2 cleanup
    - bunzip sources
    - Import freeradius

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Thu Jun 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2-1mdv2007.0
- 1.2.2
- rediffed P5,P6
- dropped upstream patches; P9,P10,P11
- added libtool fixes (P3, by debian)
- re-added the dl patch (P9, by fedora)
- make it backportable for older pam (S2,S3)

* Wed Mar 29 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-3mdk
- added P11 to fix CVE-2006-1354

* Fri Jan 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-2mdk
- fix one packaging bug introduced in 1.0.0-pre3.4mdk
- fix deps

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdk
- 1.1.0
- droped upstream/obsolete patches; P7, P10
- fix deps
- added P10 from http://bugs.freeradius.org/show_bug.cgi?id=312

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-2mdk
- rebuilt due to package loss

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1mdk
- 1.0.5
- sync with fedora; P8,P9,P10 (1.0.4-5)
- drop redundant patches; P3
- rediffed patches; P5,P6
- use bundled libtool, otherwise it won't build

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-2mdk
- rebuilt against new openldap-2.3.6 libs
- pass "-DLDAP_DEPRECATED" to the CFLAGS

* Mon Jun 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1mdk
- 1.0.4
- fix deps

* Fri Jun 10 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.0.2-4mdk
- Rebuild for libkrb53-devel 1.4.1
- clean build dir paths from libtool files

* Sat May 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.0.2-3mdk
- rebuild for new perl

* Mon Apr 18 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdk
- fix build on x86_64
- rediff P3,P6

* Sat Apr 09 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2-1mdk
- 1.0.2
- use the %%mkrel macro
- misc rpmlint fixes

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.0-6mdk
- fix deps and conditional %%multiarch

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.0-5mdk
- rebuilt against MySQL-4.1.x system libs

* Tue Dec 07 2004 Michael Scherer <misc@mandrake.org> 1.0.0-4mdk
- Rebuild for new python

* Thu Sep 02 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-3mdk
- add obsolete/provide to new libpackages

* Thu Sep 02 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.0-2mdk
- fix build

* Fri Aug 20 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-1mdk
- 1.0.0

* Mon Aug 02 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-pre3.4mdk
- new release
- package libification

* Mon May 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.3-8mdk
- fix the %%vendor and %%distribution string

* Mon Apr 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.3-7mdk
- fix changelog and some rpmlint errors

* Mon Apr 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.3-6mdk
- added P6 because that's what it's really asking for... (fix #6797 ?)

* Sat Apr 03 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.9.3-5mdk
- remove dirty tricks with rlm_ldap, fixed on openldap package
- incerease rpm build - problem with previous error in changelog

* Sun Feb 22 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.9.3-2mdk
- updated to 0.9.3
- freeradius requires openldap2-devel/libs and sasl2-devel/libs
- some macroszification in configure stage
- remove duplicate --with-system-libtool from configure macro
- remove --enable-developer from configure macro, we are users :)
- added dirty trick to allow build rlm_ldap; somewhere is problem caused that
  libtool only here can't find liblber.la and libsasl2.la
- /var/log/radius as --with-logdir
- some cleanup

* Fri Jan 30 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.9.3-1mdk
- fixed freeradius-mysql and freeradius-unixODBC packages to really include so
  library not only symlink

