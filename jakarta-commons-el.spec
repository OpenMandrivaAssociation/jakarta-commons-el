# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0
%define base_name       el
%define short_name      commons-el

%define section         free

Summary:	The Jakarta Commons Extension Language
Name:		jakarta-commons-el
Version:	1.0
Release:	9.4.3
License:	Apache License
Group:		Development/Java
Url:		https://jakarta.apache.org/commons/el/
Source0:	http://archive.apache.org/dist/jakarta/commons/el/source/commons-el-%{version}-src.tar.gz
Patch0:		%{short_name}-%{version}-license.patch
Patch1:		%{short_name}-eclipse-manifest.patch
Patch2:		jakarta-commons-el-enum.patch
%if ! %{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant
#BuildRequires:	jsp
BuildRequires:	junit
BuildRequires:	servlet6
BuildRequires:	tomcat6-jsp-2.1-api

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
BuildRequires:	java-javadoc
Requires(post):	/bin/rm /bin/ln
Requires(postun):	/bin/rm

%description    javadoc
Javadoc for %{name}.

%prep
%setup -qn %{short_name}-%{version}-src
%patch0 -p1 -b .license
pushd src/conf
%patch1 -p1
popd
%patch2 -p1

# remove all precompiled stuff
find . -type f -name "*.jar" -exec rm -f {} \;

cat > build.properties <<EOBP
build.compiler=modern
junit.jar=$(build-classpath junit)
servlet-api.jar=$(build-classpath tomcat6-servlet-2.5-api)
jsp-api.jar=$(build-classpath tomcat6-jsp-2.1-api)
servletapi.build.notrequired=true
jspapi.build.notrequired=true
EOBP

%build
%ant \
	-Dfinal.name=%{short_name} \
	-Dj2se.javadoc=%{_javadocdir}/java \
	jar javadoc


%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%gcj_compile

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt STATUS.html
%{_javadir}/*
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

