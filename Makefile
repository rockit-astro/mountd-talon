RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
ONEMETRE_VERSION=$(shell awk '/Version:/ { print $$2; }' onemetre-talon-server.spec)
SUPERWASP_VERSION=$(shell awk '/Version:/ { print $$2; }' superwasp-talon-server.spec)

all:
	mkdir -p build
	cp teld teld.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(ONEMETRE_VERSION) ($(GIT_VERSION))\""); print $0}' teld.bak > teld
	${RPMBUILD} -ba onemetre-talon-server.spec
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SUPERWASP_VERSION) ($(GIT_VERSION))\""); print $0}' teld.bak > teld
	${RPMBUILD} -ba superwasp-talon-server.spec
	${RPMBUILD} -ba observatory-talon-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-talon.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv teld.bak teld
