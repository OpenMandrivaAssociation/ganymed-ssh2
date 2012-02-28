%define gcj_support     1
%define prerel		beta1
%define rel		1

Name:           ganymed-ssh2
Version:        251
Release:        %{?prerel:0.%prerel.}%{rel}
Summary:        SSH-2 protocol implementation in pure Java
Group:          Development/Java
License:        BSD
URL:            https://code.google.com/p/ganymed-ssh-2/
Source0:        https://ganymed-ssh-2.googlecode.com/files/%{name}-build%{version}%{?prerel:%prerel}.zip
Source1:	build.xml
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif

%description
Ganymed SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for ganymed-ssh2
Group:          Development/Java

%description javadoc
Javadoc for ganymed-ssh2.

%prep
%setup -q -n %{name}-build%{version}%{?prerel:%prerel}
cp %{SOURCE1} .

# delete the jars that are in the archive
%{__rm} %{name}-build%{version}%{?prerel:%prerel}.jar

# fixing wrong-file-end-of-line-encoding warnings
%{__sed} -i 's/\r$//g' LICENSE.txt README.txt HISTORY.txt faq/FAQ.html
%{_bindir}/find examples -name \*.java | %{_bindir}/xargs -t %{__sed} -i 's/\r$//g'

%build
%ant

# Link source files to fix -debuginfo generation.
%{__rm} -f ch
%{__ln_s} src/ch


%install
%{__rm} -rf %{buildroot}

# jar
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a javadoc/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}

# gcj support
%if %{gcj_support}
export RPM_PACKAGE_NAME=%{name}
%{_bindir}/aot-compile-rpm
%endif

pushd %{buildroot}%{_javadir}/
%{__ln_s} %{name}-%{version}.jar %{name}.jar
popd

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt HISTORY.txt README.txt faq examples
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name} 
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
