%{?scl:%scl_package docker-client}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 3

Name:           %{?scl_prefix}docker-client
Version:        3.1.9
Release:        1.%{baserelease}%{?dist}
Summary:        Docker Client

License:        ASL 2.0
URL:            https://github.com/spotify/docker-client
Source0:        https://github.com/spotify/docker-client/archive/v%{version}.tar.gz

Patch0:         add-manifest.patch
# Apache httpcomponents-core >= 4.4 calls setSoLinger
Patch2:         %{pkg_name}-so-linger.patch
Patch3:         notimeoutresource.patch

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix_java_common}apache-commons-compress
BuildRequires: %{?scl_prefix}bouncycastle-pkix >= 1.50
BuildRequires: %{?scl_prefix}glassfish-hk2-utils >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}jffi >= 1.2.7
BuildRequires: %{?scl_prefix}jnr-constants >= 0.8.4
BuildRequires: %{?scl_prefix}jnr-enxio >= 0.3
BuildRequires: %{?scl_prefix}jnr-ffi >= 2.0.1
BuildRequires: %{?scl_prefix}jnr-posix >= 3.0.9
BuildRequires: %{?scl_prefix}jnr-unixsocket >= 0.2
BuildRequires: %{?scl_prefix}jnr-x86asm >= 1.0.2
BuildRequires: %{?scl_prefix}glassfish-annotation-api >= 1.2
BuildRequires: %{?scl_prefix}glassfish-hk2-api >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}glassfish-hk2-locator >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}glassfish-jaxb-api >= 2.2.12
BuildRequires: %{?scl_prefix}glassfish-jax-rs-api >= 2.0.1
BuildRequires: %{?scl_prefix}jackson-annotations >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-core >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-databind >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-datatype-guava >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-jaxrs-json-provider >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-jaxrs-providers >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-module-jaxb-annotations >= 2.5.0
BuildRequires: %{?scl_prefix}jersey >= 2.17

# This is provided by JRE but need it until either
# - jackson-module-jaxb-annotations adds Requires to it
# - jackson-module-jaxb-annotations removes it from Import-Package entirely
Requires: %{?scl_prefix}glassfish-jaxb-api >= 2.2.12

BuildArch: noarch

%description
The Docker Client is a Java API library for accessing a Docker daemon.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n docker-client-%{version}
%patch0
%patch2
%patch3
%pom_remove_plugin org.sonatype.plugins:nexus-staging-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-shade-plugin
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
export MAVEN_OPTS="-XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"
%mvn_build -j -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%dir %{_javadir}/docker-client
%dir %{_mavenpomdir}/docker-client
%doc LICENSE
%doc NOTICE README.md

%changelog
* Wed Feb 10 2016 Mat Booth <mat.booth@redhat.com> - 3.1.9-1.3
- Add patch to remove timeout for certain API calls

* Tue Feb 09 2016 Mat Booth <mat.booth@redhat.com> - 3.1.9-1.2
- Fix dependency on commons-compress

* Fri Feb 05 2016 Mat Booth <mat.booth@redhat.com> - 3.1.9-1.1
- Import latest from Fedora

* Fri Oct 23 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.9-1
- Update to upstream 3.1.9 release.

* Tue Oct 6 2015 akurtakov <akurtakov@localhost.localdomain> 3.1.5-1
- Update to upstream 3.1.5.
- Stripdown useless BRs.

* Thu Sep 24 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.4-1
- Update to upstream 3.1.4 release.

* Mon Aug 17 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- Update to upstream 3.1.3 release.

* Wed Aug 5 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.2-1
- Update to upstream 3.1.2 release.

* Thu Jul 30 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.1-2
- Update manifest's Bundle-Version to match %%{version}.

* Thu Jul 30 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.1-1.1
- Import latest from Fedora.

* Thu Jul 30 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.1-1
- Update to upstream 3.1.1 release.

* Wed Jul 22 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-2
- Support the 1.19 Docker Remote API.
- Support SO_LINGER option needed when httpcomponents-core >= 4.4.

* Thu Jul 16 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-1.2
- Reduce commons-compress requirement to match available version.

* Mon Jul 13 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-1.1
- SCL-ize.

* Wed Jul 08 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-1
- Update to 3.0.0.

* Wed Jun 24 2015 Roland Grunberg <rgrunber@redhat.com> - 2.7.26-3
- Depend upon hk2-locator as it's needed by jersey-client at runtime.
- Require jaxb-api to temporarily satisfy an invalid requirement.

* Tue Jun 23 2015 Roland Grunberg <rgrunber@redhat.com> - 2.7.26-2
- Depend on versionless bouncycastle within manifest.

* Mon Jun 8 2015 Jeff Johnston <jjohnstn@redhat.com> 2.7.26-1
- Initial packaging.
