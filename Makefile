.PHONY:	rpm clean

VERSION = 3.4.6
TARBALL = zookeeper-$(VERSION).tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)

rpm: $(TOPDIR)/SOURCES/$(TARBALL) $(TOPDIR)/SOURCES/zookeeper.init
	@rpmbuild -v -ba \
			--define "_sourcedir $(PWD)" \
			--define "_srcrpmdir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			zookeeper.spec

clean:
	@rm -rf $(TOPDIR)

$(TOPDIR)/SOURCES/$(TARBALL): $(TOPDIR)
	@spectool \
			--define "version $(VERSION)" \
			-g zookeeper.spec

$(TOPDIR)/SOURCES/zookeeper.init: $(TOPDIR)/SOURCES zookeeper.init
	cp zookeeper.init $(TOPDIR)/SOURCES/

$(TOPDIR):
	@mkdir -p $(TOPDIR)

$(TOPDIR)/SOURCES:
	@mkdir -p $(TOPDIR)/SOURCES
