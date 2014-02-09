#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests
#
%include	/usr/lib/rpm/macros.java
Summary:	Java binding to the Augeas library
Summary(pl.UTF-8):	Wiązanie Javy do biblioteki Augeas
Name:		java-augeas
Version:	0.0.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Java
Source0:	http://download.augeas.net/java/%{name}-%{version}.tar.gz
# Source0-md5:	9d5cbad6a5b2fb82b8cdaa43e9791db3
URL:		http://augeas.net/
BuildRequires:	augeas-libs
BuildRequires:	java-jna
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with tests}
BuildRequires:	ant-junit
BuildRequires:	java-junit
%endif
# dlopened
Requires:	augeas-libs
Requires:	java-jna
# for %{_javadir}
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Java binding to the Augeas library.

%description -l pl.UTF-8
Wiązanie Javy do biblioteki Augeas.

%package javadoc
Summary:	Javadoc documentation for Augeas Java binding
Summary(pl.UTF-8):	Dokumentacja javadoc do wiązania Javy do Augeasa
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc documentation for Augeas Java binding.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc do wiązania Javy do Augeasa.

%prep
%setup -q

%build
export JAVA_HOME="%{java_home}"

required_jars="jna"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant build %{?with_javadoc:docs} %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}}

# jars
cp -p target/augeas-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/augeas-%{version}.jar
ln -s augeas-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/augeas.jar

%if %{with javadoc}
cp -pr target/javadoc $RPM_BUILD_ROOT%{_javadocdir}/augeas-%{version}
ln -sf augeas-%{version} $RPM_BUILD_ROOT%{_javadocdir}/augeas
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs augeas-%{version} %{_javadocdir}/augeas

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_javadir}/augeas-%{version}.jar
%{_javadir}/augeas.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/augeas-%{version}
%ghost %{_javadocdir}/augeas
%endif
