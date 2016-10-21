%define __jar_repack 0
%define debug_package %{nil}
%define name         zookeeper
%define _prefix      /opt
%define _conf_dir    %{_sysconfdir}/zookeeper
%define _log_dir     %{_var}/log/zookeeper

Summary: ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
Name: zookeeper
Version: %{version}
Release: %{build_number}%{?dist}
License: Apache License, Version 2.0
Group: Applications/Databases
URL: http://zookeper.apache.org/
Source0: http://apache.mirrors.spacedump.net/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1: zookeeper.init
Source2: zookeeper.logrotate
Source3: zoo.cfg
Source4: log4j.properties
Source5: java.env
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Prefix: %{_conf_dir}
Prefix: %{_log_dir}
Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: zookeeper

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them ,which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%setup

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/zookeeper
mkdir $RPM_BUILD_ROOT%{_prefix}/zookeeper/bin
mkdir $RPM_BUILD_ROOT%{_prefix}/zookeeper/data
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
cp -a bin/*.sh $RPM_BUILD_ROOT%{_prefix}/zookeeper/bin/
cp -a lib $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 644 zookeeper-%{version}.jar $RPM_BUILD_ROOT%{_prefix}/zookeeper/zookeeper-%{version}.jar
install -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_initddir}/zookeeper
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_conf_dir}/zoo.cfg
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_conf_dir}/log4j.properties
install -p -D -m 644 %{S:5} $RPM_BUILD_ROOT%{_conf_dir}/java.env
install -p -D -m 644 conf/configuration.xsl $RPM_BUILD_ROOT%{_conf_dir}/configuration.xsl

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null ; then
    /usr/sbin/useradd -r -g zookeeper -m -d %{_prefix}/zookeeper -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add zookeeper
fi

%preun
# When the last version of a package is erased, $1 is 0
if [ $1 = 0 ]; then
    /sbin/service zookeeper stop >/dev/null
    /sbin/chkconfig --del zookeeper
fi

%postun
# When the last version of a package is erased, $1 is 0
# Otherwise it's an upgrade and we need to restart the service
if [ $1 -ge 1 ]; then
    /sbin/service zookeeper stop >/dev/null 2>&1
    sleep 1
    /sbin/service zookeeper start >/dev/null 2>&1
fi

%files
%defattr(-,root,root)
%attr(0775,root,zookeeper) %{_initddir}/zookeeper
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_conf_dir}/*
%{_prefix}
%attr(0700,zookeeper,zookeeper) %dir %{_log_dir}
%attr(0700,zookeeper,zookeeper) %dir %{_prefix}/zookeeper/data

