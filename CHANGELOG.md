# [1.1.0](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v1.0.0...v1.1.0) (2025-10-31)


### Features

* **sphharm:** spherical harmonics function was added as a project script. ([4408d1f](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/4408d1f4c07cbc88c5d5fa70a751d4eeb598641b))

# [1.0.0](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.2.2...v1.0.0) (2025-10-31)


### Features

* add __init__.py with package metadata and CLI function imports ([096cd8c](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/096cd8c0c6ca738c84983d6dbcc5eaf784ad7069))


### BREAKING CHANGES

* no longer namespace package

## [0.2.2](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.2.1...v0.2.2) (2025-10-28)


### Bug Fixes

* **WAXS:** fix incorrect conversion of q to 2 theta ([c2c2f2d](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/c2c2f2da7c4c12c666b052bb5add1834fe542e75))

## [0.2.1](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.2.0...v0.2.1) (2025-10-28)


### Bug Fixes

* **WAXS:** fix calculation of absorption coefficient when q instead of 2 theta ([b39173c](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/b39173c2ecfbf232f2bec3e052575dc1c9522373))

# [0.2.0](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.1.4...v0.2.0) (2025-10-28)


### Features

* **WAXS:** checked and re-created the WAXS integration script to give TOPAS compatible output ([55c56ac](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/55c56ac199361c801af2008e2d9e163f5ddca8e7))

## [0.1.4](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.1.3...v0.1.4) (2025-09-03)


### Bug Fixes

* determine h5 filename from input folder or edf filename ([a282ae3](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/a282ae39a721de62ab2dd44811f246b4dbfd299e))

## [0.1.3](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.1.2...v0.1.3) (2025-07-14)


### Bug Fixes

* change CI image to use full python image for build testing ([8a8c72c](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/8a8c72c9962d4bf0956db1dcc36c81fe3b58714e))

## [0.1.2](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v0.1.1...v0.1.2) (2025-07-14)


### Bug Fixes

* change from pyfai.azimuthalintegrator to pyFAI.integrator.azimuthal due to deprecation of the former ([75dc603](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/75dc603e957bb9aaa5c4f6dc91115b8f9da83ceb))
