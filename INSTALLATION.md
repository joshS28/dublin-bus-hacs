# Dublin Bus RTPI Integration

## Installation Guide

### Step 1: Get Your NTA API Key

1. Visit the [NTA Developer Portal](https://developer.nationaltransport.ie/)
2. Create an account or sign in
3. Register a new application
4. Copy your API key

### Step 2: Find Your Bus Stop IDs

There are several ways to find Dublin Bus stop IDs:

#### Method 1: Physical Stop Sign
- Look at the bus stop sign
- The stop ID is usually displayed as a 4-digit number

#### Method 2: Transport for Ireland Website
1. Go to [Transport for Ireland](https://www.transportforireland.ie/)
2. Search for your bus stop
3. The stop ID will be shown in the stop details

#### Method 3: Real-Time Information Displays
- Check the RTPI display at the bus stop
- The stop number is shown at the top

### Step 3: Install the Integration

#### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots (⋮) in the top right
4. Select "Custom repositories"
5. Add: `https://github.com/joshS28/north-dublin-dog-walker`
6. Category: "Integration"
7. Click "Add"
8. Search for "Dublin Bus RTPI"
9. Click "Download"
10. Restart Home Assistant

#### Manual Installation
1. Download the latest release
2. Extract the `dublin_bus` folder
3. Copy to `config/custom_components/dublin_bus`
4. Restart Home Assistant

### Step 4: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Dublin Bus RTPI"
4. Enter your configuration:
   - **NTA API Key**: Your API key from Step 1
   - **Stop IDs**: Comma-separated list (e.g., `1234,5678,9012`)
   - **Route Filters** (optional): Only show specific routes (e.g., `16,41,46A`)
5. Click **Submit**

## Usage Examples

### Basic Entities Card

```yaml
type: entities
title: Next Buses
entities:
  - sensor.dublin_bus_stop_1234
  - sensor.dublin_bus_stop_5678
```

### Markdown Card with Next Arrivals

```yaml
type: markdown
title: 🚌 Next Buses at My Stop
content: |
  {% set stop = 'sensor.dublin_bus_stop_1234' %}
  {% if states(stop) != 'unavailable' %}
    **{{ state_attr(stop, 'stop_id') }}** - {{ states(stop) }} buses coming
    
    {% for bus in state_attr(stop, 'next_buses')[:5] %}
    **Route {{ bus.route }}** → {{ bus.destination }}
    *{{ bus.due_time }}*
    {% endfor %}
  {% else %}
    No data available
  {% endif %}
```

### Conditional Card (Only Show When Buses Coming)

```yaml
type: conditional
conditions:
  - entity: sensor.dublin_bus_stop_1234
    state_not: '0'
card:
  type: markdown
  content: |
    ## 🚌 Buses Coming Soon!
    {% for bus in state_attr('sensor.dublin_bus_stop_1234', 'next_buses')[:3] %}
    **{{ bus.route }}** to {{ bus.destination }} - {{ bus.due_time }}
    {% endfor %}
```

### Multiple Stops with Auto-Entities

```yaml
type: custom:auto-entities
card:
  type: entities
  title: All My Bus Stops
filter:
  include:
    - entity_id: sensor.dublin_bus_stop_*
  exclude: []
show_empty: false
sort:
  method: state
  numeric: true
```

### Glance Card for Quick Overview

```yaml
type: glance
title: Bus Stops
entities:
  - entity: sensor.dublin_bus_stop_1234
    name: Home Stop
  - entity: sensor.dublin_bus_stop_5678
    name: Work Stop
```

## Automations

### Notification When Bus is Due

```yaml
automation:
  - alias: "Notify when bus is coming"
    trigger:
      - platform: template
        value_template: >
          {% set buses = state_attr('sensor.dublin_bus_stop_1234', 'next_buses') %}
          {{ buses and buses[0].minutes_until <= 5 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Bus Alert"
          message: >
            Route {{ state_attr('sensor.dublin_bus_stop_1234', 'next_buses')[0].route }} 
            arriving in {{ state_attr('sensor.dublin_bus_stop_1234', 'next_buses')[0].due_time }}
```

### Turn on Lights When Bus is 10 Minutes Away

```yaml
automation:
  - alias: "Lights on when bus approaching"
    trigger:
      - platform: template
        value_template: >
          {% set buses = state_attr('sensor.dublin_bus_stop_1234', 'next_buses') %}
          {{ buses and buses | selectattr('route', 'eq', '16') | 
             selectattr('minutes_until', '<=', 10) | list | length > 0 }}
    action:
      - service: light.turn_on
        target:
          entity_id: light.hallway
```

## Troubleshooting

### No Data Showing

1. **Check API Key**: Ensure your NTA API key is valid
2. **Verify Stop IDs**: Confirm the stop IDs are correct
3. **Check Logs**: Look in Home Assistant logs for errors
4. **Internet Connection**: Ensure Home Assistant can reach the internet

### Sensor Shows "Unavailable"

- The API might be temporarily down
- Check your internet connection
- Verify the stop ID exists and has active service

### Wrong Buses Showing

- Check your route filters
- Verify you're using the correct stop ID
- Some stops serve multiple routes

### API Rate Limiting

The integration updates every 30 seconds, which should be well within NTA's rate limits. If you experience issues:
- Reduce the number of stops being monitored
- Check the NTA developer portal for your API usage

## Advanced Configuration

### Custom Update Interval

To change the update interval, you'll need to modify the integration code. Edit `custom_components/dublin_bus/__init__.py`:

```python
SCAN_INTERVAL = timedelta(seconds=60)  # Change from 30 to 60 seconds
```

### Multiple Instances

You can add multiple instances of the integration with different configurations:
- Different API keys
- Different sets of stops
- Different route filters

## Support

- **Issues**: [GitHub Issues](https://github.com/joshS28/north-dublin-dog-walker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/joshS28/north-dublin-dog-walker/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)
