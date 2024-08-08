# Maintainer: Your Name <penny belle 98 at gmail dot com>
pkgname=pbfetch-git
pkgver=r124.dc4b440
pkgrel=1
pkgdesc="An unbelievably customizable hardware/software fetch"
arch=('x86_64' 'aarch64')
url="https://github.com/pennybelle/pbfetch"
license=('Apache-2.0')
depends=("python-psutil")
makedepends=(python-build python-installer python-wheel python-hatchling git)
provides=("${pkgname}")
conflicts=("${pkgname}")
source=("git+https://github.com/pennybelle/pbfetch.git")
sha256sums=('SKIP')
# dist=("${pkgname}")
# groups=()omg

pkgver() {
    cd "$srcdir/${pkgname%-git}"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
    cd "$srcdir/${pkgname%-git}"
    python -m build --wheel --no-isolation
    # rye publish
    # build --wheel --no-isolation
}

package() {
    cd "$srcdir/${pkgname%-git}"
    echo "Copying config to /usr/share/pbfetch/config/"
    sudo cp "$srcdir/${pkgname%-git}/src/${pkgname%-git}/config/config.txt" "/usr/share/pbfetch/config/config.txt"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm0755 pbfetch "$pkgdir/usr/bin/pbfetch"
}
