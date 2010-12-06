Name:		gfan
Group:		Sciences/Mathematics
License:	GPL
Summary:	Computation of Gröbner fans and tropical varieties
Version:	0.4plus
Release:	%mkrel 2
Source:		http://www.math.tu-berlin.de/~jensen/software/gfan/gfan0.4plus.tar.gz
URL:		http://www.math.tu-berlin.de/~jensen/software/gfan/gfan.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gcc-c++
BuildRequires:	libgmp-devel
BuildRequires:	cddlib-devel

Patch0:		sagemath.patch
Patch1:		gfan0.4plus-gcc45.patch
Patch2:		gfan0.4plus-fix-str-fmt.patch

%description
Gfan is a software package for computing Gröbner fans and tropical varieties.
These are polyhedral fans associated to polynomial ideals. The maximal cones
of a Gröbner fan are in bijection with the marked reduced Gröbner bases of
its defining ideal. The software computes all marked reduced Gröbner bases
of an ideal. Their union is a universal Gröbner basis. The tropical variety
of a polynomial ideal is a certain subcomplex of the Gröbner fan. Gfan
contains algorithms for computing this complex for general ideals and
specialized algorithms for tropical curves, tropical hypersurfaces and
tropical varieties of prime ideals. In addition to the above core functions
the package contains many tools which are useful in the study of Gröbner
bases, initial ideals and tropical geometry. Among these are an interactive
traversal program for Gröbner fans and programs for graphical renderings.
The full list of commands can be found in Appendix B of the manual. For
ordinary Gröbner basis computations Gfan is not competitive in speed
compared to programs such as CoCoA, Singular and Macaulay2.

%prep
%setup -q -n %{name}%{version}

%patch0 -p1
%patch1 -p0
%patch2 -p0 -b .str

%build
make						\
	OPTFLAGS="%{optflags} -DGMPRATIONAL"	\
	PREFIX=%{_prefix}			\
	CDD_LINKOPTIONS=-lcddgmp		\
	CDD_INCLUDEOPTIONS=-I%{_includedir}/cdd	\
	all

%install
rm -fr %buildroot
mkdir -p %{buildroot}%{_bindir}
cp -fa %{name} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -fa examples %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
cp -far doc/* %{buildroot}%{_docdir}/%{name}
cp -far homepage %{buildroot}%{_docdir}/%{name}
# this tries to do an "upload", using scp with the package's author account...
rm -f %{buildroot}%{_docdir}/%{name}/homepage/Makefile

pushd %{buildroot}%{_bindir}
    ./%{name} installlinks
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
