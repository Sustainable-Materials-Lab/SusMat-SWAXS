## [2.1.1](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.1.0...v2.1.1) (2026-01-30)


### Bug Fixes

* prevent error when sample transmission missing from file header ([0181505](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/01815050146c13aeead8a176f643a5850b7c2807))

# [2.1.0](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.0.4...v2.1.0) (2026-01-27)


### Features

* script to convert xrdml data to xy for use in TOPAS ([ba22db8](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/ba22db81b3e993408d008c824271fa2a5ea438ca))

## [2.0.4](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.0.3...v2.0.4) (2025-12-18)


### Bug Fixes

* use line plot instead of errorbar plot for WAXS as errors are usually too small for relevancy ([0fc16d6](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/0fc16d66e15822cc0c35351814313efbfea7dd4a))

## [2.0.3](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.0.2...v2.0.3) (2025-12-18)


### Bug Fixes

* implement xmin and xmax correctly ([4d096dc](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/4d096dcafb57786db8f91e126eccae798da59a47))

## [2.0.2](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.0.1...v2.0.2) (2025-12-18)


### Bug Fixes

* switch to png output due to bitmapped 2D data on left-hand plot ([17c7f3c](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/17c7f3cd912ced917c1095f1f2ac8f0652d78961))

## [2.0.1](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v2.0.0...v2.0.1) (2025-11-14)


### Bug Fixes

* update dependencies to use pyside6 instead of pyqt5 ([0c59eed](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/0c59eed2838284bfd7fde763b1a7aaf6679a8004))

# [2.0.0](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/compare/v1.1.0...v2.0.0) (2025-11-03)


### Features

* **core:** switch to UV build system ([3bace1d](https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion/commit/3bace1d1bd7025fd1771353e26e645739991eb2f))


### BREAKING CHANGES

* **core:** change build system

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
