# Changelog

## [0.2.4] - 2025-06-16

### Changed
- Updated dependencies to latest versions:
  - aiodns: 3.4.0 → 3.5.0
  - aiohttp: 3.12.0 → 3.12.13
  - pytest: 8.3.5 → 8.4.0
  - pytest-cov: 6.1.1 → 6.2.1
  - ruff: 0.11.11 → 0.11.13
- All tests pass with updated dependencies

## [0.2.1] - 2025-05-03

### Fixed
- Updated field validators to be compatible with Pydantic v2
- Fixed validator decorators to use @classmethod as required by Pydantic v2

## [0.2.0] - 2024-07-15

### Changed
- Dropped support for Pydantic v1, now requires Pydantic v2+
- Updated codebase to use Pydantic v2 features

## [0.1.5] - 2024-03-XX

### Changed
- Relaxed Pydantic version constraints to support both v1 and v2 versions
- Fixed dependency conflicts with other packages

## [0.1.4] - 2024-03-XX

### Added
- Support for Pydantic v2 while maintaining compatibility with v1.10.21
- Fixed MaintenanceStatus model to handle both string and integer status values

## [0.1.3] - 2024-03-14

### Added
- Initial release
- Support for WhiteBit Public API v1, v2, and v4
- Support for Private API v4
- WebSocket client implementation
- Webhook support
