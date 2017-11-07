RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
SERVER_VERSION=$(shell awk '/Version:/ { print $$2; }' onemetre-telescope-server.spec)

all:
	mkdir -p build
	cp teld teld.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SERVER_VERSION) ($(GIT_VERSION))\""); print $0}' teld.bak > teld
	${RPMBUILD} -ba onemetre-telescope-server.spec
	${RPMBUILD} -ba onemetre-telescope-client.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv teld.bak teld

