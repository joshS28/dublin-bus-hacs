# Dublin Bus RTPI for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/joshS28/north-dublin-dog-walker.svg)](https://github.com/joshS28/north-dublin-dog-walker/releases)
[![License](https://img.shields.io/github/license/joshS28/north-dublin-dog-walker.svg)](LICENSE)

A Home Assistant custom component that integrates with Dublin Bus Real-Time Passenger Information (RTPI) using the National Transport Authority's GTFS-R API.

## Features

- 🚌 Real-time bus arrival information for Dublin Bus stops
- 📍 Monitor multiple bus stops simultaneously
- 🔢 Filter by specific bus routes
- ⏱️ Shows next arrivals with estimated times
- 🔄 Automatic updates every 30 seconds
- 🎨 Beautiful Lovelace card support

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/joshS28/north-dublin-dog-walker`
6. Select category "Integration"
7. Click "Add"
8. Search for "Dublin Bus RTPI" and install

### Manual Installation

1. Copy the `custom_components/dublin_bus` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Prerequisites

You need an API key from the National Transport Authority:

1. Register at [NTA Developer Portal](https://developer.nationaltransport.ie/)
2. Create an application to get your API key

### Setup via UI

1. Go to Configuration → Integrations
2. Click "+ Add Integration"
3. Search for "Dublin Bus RTPI"
4. Enter your NTA API key
5. Add bus stops and optional route filters

### Configuration Options

- **API Key**: Your NTA GTFS-R API key (required)
- **Stop IDs**: Comma-separated list of Dublin Bus stop IDs (e.g., "1234,5678")
- **Route Filters**: Optional comma-separated list of route numbers to filter (e.g., "16,41")

## Finding Stop IDs

You can find Dublin Bus stop IDs:

1. Visit [Transport for Ireland Journey Planner](https://www.transportforireland.ie/)
2. Search for your stop
3. The stop ID is the numeric code shown on the stop information
4. Alternatively, check the physical bus stop sign - the stop ID is usually displayed

## Usage

### Sensors

The integration creates sensors for each configured stop:

- **Entity ID**: `sensor.dublin_bus_stop_[stop_id]`
- **State**: Number of upcoming buses
- **Attributes**:
  - `next_buses`: List of upcoming buses with route, destination, and arrival time
  - `stop_name`: Name of the bus stop
  - `last_update`: Last update timestamp

### Example Lovelace Card

```yaml
type: custom:auto-entities
card:
  type: entities
  title: Dublin Bus Arrivals
filter:
  include:
    - entity_id: sensor.dublin_bus_stop_*
  exclude: []
show_empty: false
```

### Advanced Card Example

```yaml
type: markdown
content: |
  ## 🚌 Next Buses at {{ state_attr('sensor.dublin_bus_stop_1234', 'stop_name') }}
  
  {% for bus in state_attr('sensor.dublin_bus_stop_1234', 'next_buses')[:5] %}
  **{{ bus.route }}** to {{ bus.destination }} - {{ bus.due_time }}
  {% endfor %}
```

## Troubleshooting

### No data showing

- Verify your API key is correct
- Check that the stop IDs are valid
- Ensure you have an active internet connection
- Check Home Assistant logs for error messages

### API Rate Limits

The NTA API has rate limits. This integration updates every 30 seconds by default, which should be well within limits.

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- National Transport Authority for providing the GTFS-R API
- Dublin Bus for real-time data
- Home Assistant community

## Support

If you encounter any issues or have questions:

- Open an issue on [GitHub](https://github.com/joshS28/north-dublin-dog-walker/issues)
- Check the [Home Assistant Community Forum](https://community.home-assistant.io/)

## Version History

### 1.0.0 (2026-01-02)
- Initial release
- Real-time bus arrival information
- Multi-stop support
- Route filtering
- Configuration flow UI
