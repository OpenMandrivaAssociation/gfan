Name:           gfan
Version:        0.5
Release:        1%{?dist}
Summary:        Software for Computing Gröbner Fans and Tropical Varieties
License:        GPL+
URL:            https://www.math.tu-berlin.de/~jensen/software/gfan/gfan.html
Source0:        http://www.math.tu-berlin.de/~jensen/software/gfan/gfan%{version}.tar.gz
# Sent upstream 2011 Apr 27.  Respect DESTDIR
Patch0:         gfan-respect-destdir.patch
# Sent upstream 2011 Apr 27.  Fix 64-bit issues in printf statements by
# using %%zu instead of %%i for printing size_t values.
Patch1:         gfan-format.patch
# Sent upstream 2011 Apr 27.  Fix warnings that could indicate runtime
# problems.
Patch2:         gfan-warning.patch
# Treate plain "gfan" call as "gfan_bases" call (as done in previous versions)
# instead of priting warning telling to call it as "gfan_bases" and exiting
Patch3:         gfan-permissive.patch

BuildRequires:  cddlib-devel
BuildRequires:  gmp-devel


%description
The software computes all marked reduced Gröbner bases of an ideal.
Their union is a universal Gröbner basis. Gfan contains algorithms for
computing this complex for general ideals and specialized algorithms
for tropical curves, tropical hypersurfaces and tropical varieties of
prime ideals. In addition to the above core functions the package
contains many tools which are useful in the study of Gröbner bases,
initial ideals and tropical geometry. Among these are an interactive
traversal program for Gröbner fans and programs for graphical renderings.

%package        doc
Summary:        Gfan examples and documentation files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
Gfan examples and documentation files.

%prep
%setup -q -n %{name}%{version}
%patch0
%patch1
%patch2
%patch3 -p1

# manual is non-free
rm -rf doc

# Point to where the TOPCOM binaries will be installed
sed -i \
  "s|^#define MINKOWSKIPROG.*|#define MINKOWSKIPROGRAM \"%{_bindir}/essai\"|" \
  minkowskisum.cpp

# Fix the tests
sed -i 's/^%s/%s _bases/' \
    testsuite/0000InstallationSection/command \
    testsuite/0001GroebnerFan/command \
    testsuite/0003GroebnerFanMod3/command \
    testsuite/0004GroebnerFanSymmetry/command \
    testsuite/0007LeadingTerms/command \
    testsuite/0008PolynomialSetUnion/command \
    testsuite/0100SymmetricGfan/command \
    testsuite/0100TwoVariables/command
sed -i 's/^gfan/%s/' \
    testsuite/0507InitialIdeal/command \
    testsuite/0508IntegerGroebnerCone/command \
    testsuite/0509IntegerGroebnerFan/command
sed -i 's|func.poly|testsuite/0056WeildDivisor/func.poly|g' \
    testsuite/0056WeildDivisor/command

# No need to install a simple upstream Makefile to rsync homepage
# directory to upstream page.
rm -f homepage/Makefile

%build
make %{?_smp_mflags} \
  OPTFLAGS="%{optflags} -DGMPRATIONAL -I/usr/include/cddlib" \
  PREFIX=%{_prefix}


%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
pushd $RPM_BUILD_ROOT%{_bindir}
    ./%{name} installlinks
popd

#%#check
#./gfan _test


%files
%doc COPYING LICENSE
%{_bindir}/*

%files          doc
%doc examples
%doc homepage
