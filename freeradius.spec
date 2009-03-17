%define _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname freeradius %{major}
%define develname %mklibname -d freeradius
%define _requires_exceptions perl(DBI)

Summary:	High-performance and highly configurable RADIUS server
Name:		freeradius
Version:	2.1.4
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.freeradius.org/
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.bz2
Source1:	ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.bz2.sig
Source2:	freeradius.pam-0.77
Source3:	freeradius.pam
Source4:	freeradius.init
Source5:	freeradius.logrotate
Source6:	freeradius.sysconfig
Patch0:		freeradius-2.1.4-ssl-config.patch
Patch4:		freeradius-0.8.1-use-system-com_err.patch
Patch6:		freeradius-2.0.0-avoid-version.patch
Patch8:		freeradius-2.0.0-samba3.patch
Patch9:		freeradius-1.1.2-ltdl_no_la.diff
Patch10:	freeradius-server-linkage_fix.diff
BuildRequires:	gdbm-devel
BuildRequires:	krb5-devel
BuildRequires:	libsasl-devel
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcap-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpm-helper >= 0.21
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
# minimal version for ssl cert generation
Requires(post): openssl
Requires(post): rpm-helper >= 0.21
Requires(preun): rpm-helper >= 0.19
Requires(pre): rpm-helper >= 0.19
Requires(postun): rpm-helper >= 0.19
Conflicts:	radiusd-cistron
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The FreeRADIUS Server Project is a high-performance and highly configurable
GPL'd RADIUS server. It is somewhat similar to the Livingston 2.0 RADIUS
server, but has many more features, and is much more configurable.

%package -n	%{name}-krb5
Summary:	The Kerberos module for %{name}
Group:		System/Servers
Requires:	krb5-libs
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{libname}-krb5

%description -n	%{name}-krb5
The FreeRADIUS server can use Kerberos to authenticate users, and this module
is necessary for that.

%package -n	%{name}-ldap
Summary:	The LDAP module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{libname}-ldap

%description -n	%{name}-ldap
The FreeRADIUS server can use LDAP to authenticate users, and this module is
necessary for that.

%package -n	%{name}-postgresql
Summary:	The PostgreSQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{libname}-postgresql

%description -n	%{name}-postgresql
The FreeRADIUS server can use PostgreSQL to authenticate users and do
accounting, and this module is necessary for that.

%package -n	%{name}-mysql
Summary:	The MySQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{libname}-mysql

%description -n	%{name}-mysql
The FreeRADIUS server can use MySQL to authenticate users and do accounting,
and this module is necessary for that.

%package -n	%{name}-unixODBC
Summary:	The unixODBC module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{libname}-unixODBC

%description -n	%{name}-unixODBC
The FreeRADIUS server can use unixODBC to authenticate users and do accounting,
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
Obsoletes:	freeradius-devel

%description -n	%{develname}
Development headers and libraries for %{name}

%package -n	%{name}-web
Summary:	Web based administration interface for freeradius
Group:		System/Servers
Requires:	apache-mod_php
Requires:	freeradius
Requires:	php-mysql
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
# webapp macros and scriptlets
Requires(post):	 rpm-helper >= 0.16
Requires(postun): rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
Provides:	dialup_admin = %{version}-%{release}
Obsoletes:	dialup_admin

%description -n	%{name}-web
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

%patch0 -p1 -b .config
%patch4 -p0 -b .peroyvind
%patch6 -p1 -b .avoid-version
%patch8 -p0 -b .samba3
%patch9 -p1 -b .ltdl_no_la
%patch10 -p0 -b .linkage_fix

# For pre release only:
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/Makefile
perl -pi -e 's,\$\(RADIUSD_VERSION\),%{version},' doc/rfc/Makefile

%__install -d Mandriva
# fix conditional pam config file
%if %{mdkversion} < 200610
cp %{SOURCE2} Mandriva/freeradius.pam
%else
cp %{SOURCE3} Mandriva/freeradius.pam
%endif
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
    --with-unixodbc-dir=%{_prefix}

# enable this one with a hack...
perl -pi -e "s|^TARGET.*|TARGET=rlm_dbm|g" src/modules/rlm_dbm/Makefile
perl -pi -e "s|^SRCS.*|SRCS=rlm_dbm.c|g" src/modules/rlm_dbm/Makefile
perl -pi -e "s|^RLM_UTILS.*|RLM_UTILS=rlm_dbm_parser rlm_dbm_cat|g" src/modules/rlm_dbm/Makefile
perl -pi -e "s|^RLM_CFLAGS.*|RLM_CFLAGS=-I%{_includedir}/gdbm -DHAVE_GDBM_NDBM_H|g" src/modules/rlm_dbm/Makefile
perl -pi -e "s|^RLM_LIBS.*|RLM_LIBS=-L%{_libdir} -lgdbm -lgdbm_compat|g" src/modules/rlm_dbm/Makefile
perl -pi -e "s|^RLM_INSTALL.*|RLM_INSTALL=rlm_dbm_install|g" src/modules/rlm_dbm/Makefile

%if "%{_lib}" == "lib64"
perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

make

%install
rm -rf %{buildroot}

%__install -d %{buildroot}%{_sysconfdir}/logrotate.d
%__install -d %{buildroot}%{_sysconfdir}/pam.d
%__install -d %{buildroot}%{_sysconfdir}/sysconfig
%__install -d %{buildroot}%{_initrddir}
%__install -d %{buildroot}/var/run/radiusd
%__install -d %{buildroot}%{_includedir}/%{name}

make install R=%{buildroot}

# install headers
%__install -m0644 src/include/*  %{buildroot}%{_includedir}/%{name}/

# install Mandriva scripts and stuff...
%__install -m0644 Mandriva/%{name}.pam %{buildroot}%{_sysconfdir}/pam.d/radiusd
%__install -m0644 Mandriva/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/radiusd
%__install -m0755 Mandriva/%{name}.init %{buildroot}%{_initrddir}/radiusd
%__install -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/radiusd

# put the mibs in place
%__install -d %{buildroot}%{_datadir}/snmp/mibs
%__install -m0644 mibs/RADIUS* %{buildroot}%{_datadir}/snmp/mibs/

# fix ghostfiles
touch %{buildroot}/var/log/radius/radutmp
touch %{buildroot}/var/log/radius/radwtmp
touch %{buildroot}/var/log/radius/radius.log

# remove unneeded stuff
%__rm -f %{buildroot}%{_sbindir}/rc.radiusd
%__rm -f %{buildroot}%{_includedir}/%{name}/Makefile
%__rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/mssql
%__rm -rf %{buildroot}%{_sysconfdir}/raddb/sql/oracle
%__rm -f %{buildroot}%{_sysconfdir}/raddb/certs/*

# remove faulty perl file...
%__rm -f %{buildroot}%{_libdir}/%{name}/rlm_perl.a

# this annoying file gets installed on ML9.0, remove it...
%__rm -f %{buildroot}%{_sysconfdir}/raddb/Makefile

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
perl -pi -e "s,(\s)\S+$RPM_BUILD_DIR\S+,\$1,g" %{buildroot}%{_libdir}/%{name}/*.la 

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/freeradius/build-radpaths-h
%multiarch_includes %{buildroot}%{_includedir}/freeradius/radpaths.h
%endif

# the web cruft
install -d %{buildroot}/var/www/%{name}-web
install -d %{buildroot}%{_sysconfdir}/%{name}-web

pushd dialup_admin
make \
    DIALUP_PREFIX=%{buildroot}/var/www/freeradius-web \
    DIALUP_DOCDIR=%{buildroot}%{_docdir}/freeradius-web \
    DIALUP_CONFDIR=%{buildroot}%{_sysconfdir}/freeradius-web \
    install
popd

find %{buildroot}/var/www/freeradius-web | xargs perl -pi -e "s|%{buildroot}||g"
find %{buildroot}%{_sysconfdir}/freeradius-web | xargs perl -pi -e "s|%{buildroot}||g"
find %{buildroot}/var/www/freeradius-web | xargs perl -pi -e "s|\.\./conf/config\.php|%{_sysconfdir}/freeradius-web/config\.php|g"
find %{buildroot}%{_sysconfdir}/freeradius-web | xargs perl -pi -e "s|\.\./conf/admin\.conf|%{_sysconfdir}/freeradius-web/admin\.conf|g"

perl -pi -e "s|/data/local/dialupadmin/conf/admin\.conf|%{_sysconfdir}/freeradius-web/admin\.conf|g" %{buildroot}/var/www/freeradius-web/bin/*
perl -pi -e "s|/logs/radiusd/accounting|/var/log/radius/accounting|g"  %{buildroot}/var/www/freeradius-web/bin/*

mv %{buildroot}/var/www/freeradius-web/bin/* %{buildroot}%{_bindir}/
mv %{buildroot}%{_bindir}/snmpfinger %{buildroot}%{_bindir}/freeradius-web-snmpfinger

# fix a simple redirector
cat > %{buildroot}/var/www/%{name}-web/index.html << EOF
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
Alias /%{name}-web %{_var}/www/%{name}-web

<Directory %{_var}/www/%{name}-web>
    Allow from all
</Directory>
EOF

# cron stuff
install -d %{buildroot}%{_sysconfdir}/cron.d
cat > %{buildroot}%{_sysconfdir}/cron.d/%{name}-web <<EOF
1 0 * * * %{_bindir}/tot_stats >/dev/null 2>&1
5 0 * * * %{_bindir}/monthly_tot_stats >/dev/null 2>&1
10 0 1 * * %{_bindir}/truncate_radacct >/dev/null 2>&1
15 0 1 * * %{_bindir}/clean_radacct >/dev/null 2>&1
EOF

# cleanup
rm -rf %{buildroot}%{_docdir}/%{name}
rm -rf %{buildroot}%{_docdir}/freeradius-web
rm -rf %{buildroot}/var/www/freeradius-web/bin
rm -rf %{buildroot}/var/www/freeradius-web/sql
rm -f %{buildroot}%{_bindir}/dialup_admin.cron

%pre
%_pre_useradd radius /var/log/radius/radacct /bin/false

%post
%_post_service radiusd
%create_ghostfile /var/log/radius/radutmp radius radius 0644
%create_ghostfile /var/log/radius/radwtmp radius radius 0644
%create_ghostfile /var/log/radius/radius.log radius radius 0644
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

%post -n %{name}-web
%_post_webapp

%postun -n %{name}-web
%_postun_webapp

%clean
rm -rf %{buildroot}

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
%{_bindir}/radclient
%{_bindir}/radconf2xml
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
%{_sbindir}/radiusd
%{_sbindir}/radmin
%{_sbindir}/radwatch
%{_sbindir}/raddebug
%attr(0755,radius,radius) %dir /var/log/radius
%attr(0755,radius,radius) %dir /var/log/radius/radacct
%attr(0755,radius,radius) %dir /var/run/radiusd
%attr(0644,radius,radius) %ghost /var/log/radius/radutmp
%attr(0644,radius,radius) %ghost /var/log/radius/radwtmp
%attr(0644,radius,radius) %ghost /var/log/radius/radius.log
%{_datadir}/snmp/mibs/*
%{_datadir}/freeradius
%{_mandir}/man*/*

%files -n %{name}-krb5
%defattr(-,root,root)
%doc rlm_krb5
%{_libdir}/%{name}/rlm_krb5*.so*

%files -n %{name}-ldap
%defattr(-,root,root)
%doc RADIUS*.schema rlm_ldap doc/examples/openldap.schema
%config(noreplace) %{_sysconfdir}/raddb/ldap.attrmap
%{_libdir}/%{name}/rlm_ldap*.so*

%files -n %{name}-postgresql
%defattr(-,root,root)
%doc src/billing
%config(noreplace) %{_sysconfdir}/raddb/sql/postgresql
%{_libdir}/%{name}/rlm_sql_postgresql*.so*

%files -n %{name}-mysql
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/raddb/sql/mysql
%{_libdir}/%{name}/rlm_sql_mysql*.so*

%files -n %{name}-unixODBC
%defattr(-,root,root)
%{_libdir}/%{name}/rlm_sql_unixodbc*.so*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}/libfreeradius-radius*.la
%{_libdir}/%{name}/libfreeradius-radius*.so
%{_libdir}/%{name}/libfreeradius-eap*.la
%{_libdir}/%{name}/libfreeradius-eap*.so
%{_libdir}/%{name}/rlm_*.la
%{_libdir}/%{name}/rlm_*.so

# these belong to their respective sub package
%exclude %{_libdir}/%{name}/rlm_sql_mysql*
%exclude %{_libdir}/%{name}/rlm_sql_postgresql*
%exclude %{_libdir}/%{name}/rlm_sql_unixodbc*
%exclude %{_libdir}/%{name}/rlm_krb5*
%exclude %{_libdir}/%{name}/rlm_ldap*

%files -n %{develname}
%defattr(-,root,root)
%doc todo
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/freeradius/build-radpaths-h
%multiarch %{multiarch_includedir}/freeradius/radpaths.h
%endif
%{_includedir}/%{name}
%{_libdir}/%{name}/*.a

%files -n %{name}-web
%defattr(-,root,root)
%doc dialup_admin/sql/mysql dialup_admin/sql/postgresql dialup_admin/sql/oracle
%doc dialup_admin/doc/AUTHORS dialup_admin/doc/FAQ dialup_admin/doc/HELP_WANTED
%doc dialup_admin/doc/HOWTO dialup_admin/doc/TODO dialup_admin/Changelog
%doc dialup_admin/README dialup_admin/bin/Changelog.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/%{name}-web
%attr(0644,root,root) %config(noreplace) %{_webappconfdir}/%{name}-web.conf
%dir %{_sysconfdir}/%{name}-web
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}-web/admin.conf
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}-web/captions.conf
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}-web/naslist.conf
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}-web/config.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/accounting.attrs
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/auth.request
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/default.vals
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/extra.ldap-attrmap
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/sql.attrmap
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/sql.attrs
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/user_edit.attrs
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}-web/username.mappings
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
/var/www/%{name}-web
