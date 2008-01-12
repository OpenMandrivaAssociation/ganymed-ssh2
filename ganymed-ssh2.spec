%define gcj_support     1

Name:           ganymed-ssh2
Version:        210
Release:        %mkrel 5
Epoch:          0
Summary:        SSH-2 protocol implementation in pure Java
Group:          Development/Java
License:        BSD
URL:            http://www.ganymed.ethz.ch/ssh2/
Source0:        http://www.ganymed.ethz.ch/ssh2/ganymed-ssh2-build%{version}.zip
BuildRequires:  java-rpmbuild >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%setup -q -n %{name}-build%{version}

# delete the jars that are in the archive
%{__rm} %{name}-build%{version}.jar

# fixing wrong-file-end-of-line-encoding warnings
%{__sed} -i 's/\r$//g' LICENSE.txt README.txt HISTORY.txt faq/FAQ.html
%{_bindir}/find examples -name \*.java | %{_bindir}/xargs -t %{__sed} -i 's/\r$//g'

%build
%{javac} -d build src/
%{jar} -cf %{name}.jar -C build ch

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
%{__cp} -a javadoc/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}

# gcj support
%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

pushd %{buildroot}%{_javadir}/
%{__ln_s} %{name}-%{version}.jar %{name}.jar
popd

%clean
%{__rm} -rf %{buildroot}

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


