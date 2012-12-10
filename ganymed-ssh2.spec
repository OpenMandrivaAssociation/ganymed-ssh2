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


%changelog
* Tue Feb 28 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 251-0.beta1.1
+ Revision: 781277
- latest version 251beta1
- build.xml from Fedora

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:210-3mdv2008.0
+ Revision: 87376
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:210-2mdv2008.0
+ Revision: 82973
- rebuild


* Mon Jan 15 2007 David Walluck <walluck@mandriva.org> 210-1mdv2007.0
+ Revision: 109359
- 210
- Import ganymed-ssh2

* Wed Jul 19 2006 David Walluck <walluck@mandriva.org> 0:209-4mdv2007.0
- release

* Mon Jun 26 2006 Robert Marcano <robert@marcanoonline.com> 209-4
- created javadoc package
- renamed to ganymed-ssh2

* Mon Jun 12 2006 Robert Marcano <robert@marcanoonline.com> 209-3
- rpmlint fixes and debuginfo generation workaround
- doc files added

* Mon May 29 2006 Robert Marcano <robert@marcanoonline.com> 209-2
- review updates

* Mon May 08 2006 Robert Marcano <robert@marcanoonline.com> 209-1
- initial version

