#!/bin/sh
# Install build dependencies required on the daily-build host before ./configure.
# Mock chroots get deps from the spec BuildRequires; this covers the make dist step.

set -e

if pkg-config --exists yaml-0.1 2>/dev/null; then
	exit 0
fi

echo "install-host-build-deps: installing libyaml-devel for host configure"
dnf install -y libyaml-devel

if ! pkg-config --exists yaml-0.1 2>/dev/null; then
	echo "install-host-build-deps: yaml-0.1 still missing after libyaml-devel install" >&2
	exit 1
fi
