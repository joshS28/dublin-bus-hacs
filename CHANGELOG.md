# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-02

### Added
- Initial release of Dublin Bus RTPI integration
- Real-time bus arrival information using NTA GTFS-R API
- Support for multiple bus stops
- Route filtering capability
- Configuration flow UI for easy setup
- Sensor entities for each configured stop
- Detailed attributes including next buses, arrival times, and destinations
- Automatic updates every 30 seconds
- Comprehensive documentation and examples
- HACS support
- Example Lovelace cards
- Installation guide
- MIT License

### Features
- 🚌 Real-time bus arrival data
- 📍 Multi-stop monitoring
- 🔢 Route-specific filtering
- ⏱️ Human-readable arrival times (e.g., "5 mins", "Due")
- 🔄 Automatic polling with configurable interval
- 🎨 Rich sensor attributes for custom cards
- 📱 Mobile-friendly data format
- 🌐 Uses official NTA GTFS-R API
- 🔐 Secure API key authentication
- ⚡ Efficient data processing

### Technical Details
- Uses GTFS-Realtime protobuf format
- Implements Home Assistant DataUpdateCoordinator
- Follows Home Assistant integration best practices
- Includes proper error handling and logging
- Supports Home Assistant 2023.1.0+

[1.0.0]: https://github.com/joshS28/north-dublin-dog-walker/releases/tag/v1.0.0
