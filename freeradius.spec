%define major 1
%define libname %mklibname freeradius %{major}
%define _requires_exceptions perl(DBI)

Name:		freeradius
Version:	1.1.7
Release:	%mkrel 2
Summary:	High-performance and highly configurable RADIUS server
License:	GPL
Group:		System/Servers
URL:		http://www.freeradius.org/
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.gz.sig
Source2:	freeradius.pam-0.77
Source3:	freeradius.pam
Source4:	freeradius.init
Source5:	freeradius.logrotate
Patch0:		freeradius-0.9.2-config.patch
Patch4:		freeradius-0.8.1-use-system-com_err.patch
Patch5:		freeradius-1.1.2-libdir.diff
Patch6:		freeradius-1.1.2-avoid-version.diff
Patch8:		freeradius-1.0.0-samba3.patch
Patch9:		freeradius-1.1.2-ltdl_no_la.diff
BuildRequires:	krb5-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool-devel
BuildRequires:	MySQL-devel
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	openldap-devel
BuildRequires:	libtool
BuildRequires:	unixODBC-devel
BuildRequires:	net-snmp
BuildRequires:	net-snmp-utils
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	zlib-devel
BuildRequires:	python-devel
Requires:	net-snmp-utils
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
Conflicts:	radiusd-cistron

%description
The FreeRADIUS Server Project is a high-performance and highly
configurable GPL'd RADIUS server. It is somewhat similar to the
Livingston 2.0 RADIUS server, but has many more features, and is
much more configurable.

%package -n	%{libname}-krb5
Summary:	The Kerberos module for %{name}
Group:		System/Servers
Requires:	krb5-libs
Requires:	%{name} = %{version}
Obsoletes:	freeradius-krb5
Provides:	freeradius-krb5

%description -n	%{libname}-krb5
The FreeRADIUS server can use Kerberos to authenticate users, and
this module is necessary for that.

%package -n	%{libname}-ldap
Summary:	The LDAP module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	freeradius-ldap
Provides:	freeradius-ldap

%description -n	%{libname}-ldap
The FreeRADIUS server can use LDAP to authenticate users, and this
module is necessary for that.

%package -n	%{libname}-postgresql
Summary:	The PostgreSQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	freeradius-postgresql
Provides:	freeradius-postgresql

%description -n	%{libname}-postgresql
The FreeRADIUS server can use PostgreSQL to authenticate users and
do accounting, and this module is necessary for that.

%package -n	%{libname}-mysql
Summary:	The MySQL module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	freeradius-mysql
Provides:	freeradius-mysql

%description -n	%{libname}-mysql
The FreeRADIUS server can use MySQL to authenticate users and do
accounting, and this module is necessary for that.

%package -n	%{libname}-unixODBC
Summary:	The unixODBC module for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	freeradius-unixODBC
Provides:	freeradius-unixODBC

%description -n	%{libname}-unixODBC
The FreeRADIUS server can use unixODBC to authenticate users and
do accounting, and this module is necessary for that.

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}

%description -n	%{libname}
Libraries for %{name}

%package -n	%{libname}-devel
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{name} = %{version}
Obsoletes:	freeradius-devel
Provides:	freeradius-devel

%description -n	%{libname}-devel
Development headers and libraries for %{name}

%prep
%setup -q -n %{name}-%{version}

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch0 -p0
%patch4 -p1 -b .peroyvind
%patch5 -p1
%patch6 -p1
%patch8 -p1 -b .samba3
%patch9 -p1 -b .ltdl_no_la

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

# lib64 fixes
find -type f -name "configure*" | xargs perl -pi -e "s|/lib\b|/%{_lib}|g"

%build
%serverbuild
# use bundled libtool...
%define __libtoolize /bin/true

export CFLAGS="$CFLAGS -fPIC -DLDAP_DEPRECATED"
export CXXFLAGS="$CXXFLAGS -fPIC -DLDAP_DEPRECATED"

%configure2_5x \
    --with-gnu-ld \
    --with-threads \
    --with-thread-pool \
    --libdir=%{_libdir}/%{name}  \
    --libexecdir=%{_libdir}/%{name} \
    --localstatedir=%{_var} \
    --with-logdir=%{_var}/log/radius \
    --disable-ltdl-install \
    --with-ltdl-lib=%{_libdir} \
    --with-ltdl-include=%{_includedir} \
    --with-radacctdir=%{_var}/log/radius/radacct \
    --with-raddbdir=%{_sysconfdir}/raddb \
    --with-snmp \
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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%__install -d %{buildroot}%{_sysconfdir}/logrotate.d
%__install -d %{buildroot}%{_sysconfdir}/pam.d
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

# put the mibs in place
%__install -d %{buildroot}%{_datadir}/snmp/mibs
%__install -m0644 mibs/GNOME* mibs/RADIUS* %{buildroot}%{_datadir}/snmp/mibs/

# fix ghostfiles
touch %{buildroot}/var/log/radius/radutmp
touch %{buildroot}/var/log/radius/radwtmp
touch %{buildroot}/var/log/radius/radius.log

# remove unneeded stuff
%__rm -f %{buildroot}%{_sbindir}/rc.radiusd
%__rm -f %{buildroot}%{_sysconfdir}/raddb/mssql.conf
%__rm -f %{buildroot}%{_sysconfdir}/raddb/oraclesql.conf
%__rm -f %{buildroot}%{_includedir}/%{name}/Makefile

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

# fix the naming of the sql.conf file
%__mv %{buildroot}%{_sysconfdir}/raddb/sql.conf %{buildroot}%{_sysconfdir}/raddb/mysql.conf

# nuke useless dupes
rm -f %{buildroot}%{_libdir}/%{name}/*%{version}*.la

#remove buildroot from the libtool files:
perl -pi -e "s,(\s)\S+$RPM_BUILD_DIR\S+,\$1,g" %{buildroot}%{_libdir}/%{name}/*.la 

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/freeradius/build-radpaths-h
%multiarch_includes %{buildroot}%{_includedir}/freeradius/radpaths.h
%endif

# cleanup
rm -rf  %{buildroot}%{_docdir}/%{name}

%pre
%_pre_useradd radius /var/log/radius/radacct /bin/false

%post
%_post_service radiusd
%create_ghostfile /var/log/radius/radutmp radius radius 0644
%create_ghostfile /var/log/radius/radwtmp radius radius 0644
%create_ghostfile /var/log/radius/radius.log radius radius 0644

%preun
%_preun_service radiusd

%postun
%_postun_userdel radius

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc COPYRIGHT CREDITS INSTALL LICENSE README
%doc README.sql README.smb Readme.cram Standard.draft dictionary.sandy

%attr(0755,radius,radius) %dir %{_sysconfdir}/raddb
%attr(0755,radius,radius) %dir %{_sysconfdir}/raddb/certs

%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/radiusd
%attr(0755,root,root) %{_initrddir}/radiusd

%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/acct_users
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/attrs
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/dictionary*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/experimental.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/example.pl
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/hints
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/huntgroups
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/naslist
#%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/persistent.pl
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/radiusd.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/realms
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/clients
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/clients.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/naspasswd
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/preproxy_users
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/proxy.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/snmp.conf
%config(noreplace) %attr(0640,root,radius) %{_sysconfdir}/raddb/users
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/eap.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/otp.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/sqlippool.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/postgresqlippool.conf
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/raddb/certs/*

%{_bindir}/rad*
%{_bindir}/rlm_*
%{_bindir}/smbencrypt
%{_sbindir}/check*
%{_sbindir}/rad*

%attr(0755,radius,radius) %dir /var/log/radius
%attr(0755,radius,radius) %dir /var/log/radius/radacct
%attr(0755,radius,radius) %dir /var/run/radiusd
%attr(0644,radius,radius) %ghost /var/log/radius/radutmp
%attr(0644,radius,radius) %ghost /var/log/radius/radwtmp
%attr(0644,radius,radius) %ghost /var/log/radius/radius.log
%attr(0644,root,root) %{_datadir}/snmp/mibs/*
%{_datadir}/freeradius
%attr(0644,root,root) %{_mandir}/man*/*

%files -n %{libname}-krb5
%defattr(-,root,root)
%doc rlm_krb5
%{_libdir}/%{name}/rlm_krb5*.so*

%files -n %{libname}-ldap
%defattr(-,root,root)
%doc RADIUS*.schema rlm_ldap doc/examples/openldap.schema

%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/raddb/ldap.attrmap
%{_libdir}/%{name}/rlm_ldap*.so*

%files -n %{libname}-postgresql
%defattr(-,root,root)
%doc doc/examples/postgresql.sql
%doc src/billing
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/postgresql.conf
%{_libdir}/%{name}/rlm_sql_postgresql*.so*

%files -n %{libname}-mysql
%defattr(-,root,root)
%doc doc/examples/mysql.sql
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/raddb/mysql.conf
%{_libdir}/%{name}/rlm_sql_mysql*.so*

%files -n %{libname}-unixODBC
%defattr(-,root,root)
%{_libdir}/%{name}/rlm_sql_unixodbc*.so*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}/libradius*.la
%{_libdir}/%{name}/libradius*.so
%{_libdir}/%{name}/libeap.la
%{_libdir}/%{name}/libeap*.so
%{_libdir}/%{name}/rlm_*.la
%{_libdir}/%{name}/rlm_*.so

# these belong to their respective sub package
%exclude %{_libdir}/%{name}/rlm_sql_mysql*
%exclude %{_libdir}/%{name}/rlm_sql_postgresql*
%exclude %{_libdir}/%{name}/rlm_sql_unixodbc*
%exclude %{_libdir}/%{name}/rlm_krb5*
%exclude %{_libdir}/%{name}/rlm_ldap*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc todo
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/freeradius/build-radpaths-h
%multiarch %{multiarch_includedir}/freeradius/radpaths.h
%endif
%{_includedir}/%{name}
%{_libdir}/%{name}/*.a
