# Example Lovelace Cards for Dublin Bus RTPI

This document contains ready-to-use Lovelace card configurations for displaying Dublin Bus information in your Home Assistant dashboard.

## 1. Simple Next Buses Card

A clean, simple card showing the next buses at your stop:

```yaml
type: markdown
title: 🚌 Next Buses
content: |
  {% set stop = 'sensor.dublin_bus_stop_1234' %}
  {% if states(stop) != 'unavailable' and states(stop) != 'unknown' %}
    {% for bus in state_attr(stop, 'next_buses')[:5] %}
    **{{ bus.route }}** → {{ bus.destination }}  
    *{{ bus.due_time }}*
    {% if not loop.last %}---{% endif %}
    {% endfor %}
  {% else %}
    *No buses scheduled*
  {% endif %}
```

## 2. Multi-Stop Dashboard

Display multiple stops in a single card:

```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🏠 Home Stop (1234)
    content: |
      {% set stop = 'sensor.dublin_bus_stop_1234' %}
      {% for bus in state_attr(stop, 'next_buses')[:3] %}
      **{{ bus.route }}** → {{ bus.destination }} - {{ bus.due_time }}
      {% endfor %}
  
  - type: markdown
    title: 💼 Work Stop (5678)
    content: |
      {% set stop = 'sensor.dublin_bus_stop_5678' %}
      {% for bus in state_attr(stop, 'next_buses')[:3] %}
      **{{ bus.route }}** → {{ bus.destination }} - {{ bus.due_time }}
      {% endfor %}
```

## 3. Detailed Bus Information Card

A comprehensive card with more details:

```yaml
type: markdown
title: 🚌 Dublin Bus - Detailed View
content: |
  {% set stop = 'sensor.dublin_bus_stop_1234' %}
  {% if states(stop) != 'unavailable' %}
  
  **Stop {{ state_attr(stop, 'stop_id') }}**  
  *{{ states(stop) }} buses coming*
  
  ---
  
  {% for bus in state_attr(stop, 'next_buses')[:8] %}
  ### Route {{ bus.route }}
  📍 **Destination:** {{ bus.destination }}  
  ⏱️ **Arriving:** {{ bus.due_time }}
  {% if bus.minutes_until <= 2 %}
  🔴 **Arriving Now!**
  {% elif bus.minutes_until <= 5 %}
  🟡 **Coming Soon**
  {% endif %}
  
  {% if not loop.last %}---{% endif %}
  {% endfor %}
  
  *Last updated: {{ state_attr(stop, 'last_update') | as_timestamp | timestamp_custom('%H:%M:%S') }}*
  {% else %}
  *No data available*
  {% endif %}
```

## 4. Specific Route Filter Card

Only show specific routes you care about:

```yaml
type: markdown
title: 🚌 Route 16 & 41 Only
content: |
  {% set stop = 'sensor.dublin_bus_stop_1234' %}
  {% set routes = ['16', '41', '41A', '41B'] %}
  {% if states(stop) != 'unavailable' %}
    {% set filtered = state_attr(stop, 'next_buses') | selectattr('route', 'in', routes) | list %}
    {% if filtered | length > 0 %}
      {% for bus in filtered[:5] %}
      **{{ bus.route }}** → {{ bus.destination }}  
      *{{ bus.due_time }}*
      {% if not loop.last %}---{% endif %}
      {% endfor %}
    {% else %}
      *No Route 16 or 41 buses scheduled*
    {% endif %}
  {% else %}
    *No data available*
  {% endif %}
```

## 5. Urgent Buses Alert Card

Only show buses arriving in the next 10 minutes:

```yaml
type: conditional
conditions:
  - entity: sensor.dublin_bus_stop_1234
    state_not: '0'
card:
  type: markdown
  title: ⚠️ Buses Leaving Soon!
  content: |
    {% set stop = 'sensor.dublin_bus_stop_1234' %}
    {% set urgent = state_attr(stop, 'next_buses') | selectattr('minutes_until', '<=', 10) | list %}
    {% if urgent | length > 0 %}
      {% for bus in urgent %}
      ## Route {{ bus.route }}
      **{{ bus.destination }}**  
      {% if bus.minutes_until <= 2 %}
      🔴 **LEAVING NOW!**
      {% else %}
      🟡 **{{ bus.due_time }}**
      {% endif %}
      {% if not loop.last %}---{% endif %}
      {% endfor %}
    {% endif %}
```

## 6. Glance Card for Quick View

Perfect for a small dashboard widget:

```yaml
type: glance
title: Bus Stops
columns: 3
entities:
  - entity: sensor.dublin_bus_stop_1234
    name: Home
    icon: mdi:home
  - entity: sensor.dublin_bus_stop_5678
    name: Work
    icon: mdi:briefcase
  - entity: sensor.dublin_bus_stop_9012
    name: City
    icon: mdi:city
```

## 7. Picture Elements Card (Advanced)

Create a visual map of your bus stops:

```yaml
type: picture-elements
image: /local/dublin_map.png
elements:
  - type: state-label
    entity: sensor.dublin_bus_stop_1234
    prefix: 'Home: '
    suffix: ' buses'
    style:
      top: 30%
      left: 20%
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      padding: 5px
      border-radius: 5px
  
  - type: state-label
    entity: sensor.dublin_bus_stop_5678
    prefix: 'Work: '
    suffix: ' buses'
    style:
      top: 60%
      left: 70%
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      padding: 5px
      border-radius: 5px
```

## 8. Button Card with Custom Styling

Requires the `button-card` custom component:

```yaml
type: custom:button-card
entity: sensor.dublin_bus_stop_1234
name: Home Bus Stop
show_state: true
state_display: |
  [[[ return `${entity.state} buses` ]]]
styles:
  card:
    - background-color: '#1a1a1a'
    - border-radius: 10px
  name:
    - color: '#ffd700'
  state:
    - color: '#00ff00'
tap_action:
  action: more-info
custom_fields:
  next_bus: |
    [[[
      const buses = entity.attributes.next_buses;
      if (buses && buses.length > 0) {
        return `Next: ${buses[0].route} - ${buses[0].due_time}`;
      }
      return 'No buses';
    ]]]
```

## 9. Auto-Entities Card (Dynamic)

Automatically shows all Dublin Bus sensors:

```yaml
type: custom:auto-entities
card:
  type: entities
  title: All Bus Stops
filter:
  include:
    - entity_id: sensor.dublin_bus_stop_*
      options:
        type: custom:template-entity-row
        name: |
          {{ state_attr(config.entity, 'stop_id') }}
        secondary: |
          {% set buses = state_attr(config.entity, 'next_buses') %}
          {% if buses and buses | length > 0 %}
            {{ buses[0].route }} - {{ buses[0].due_time }}
          {% else %}
            No buses
          {% endif %}
sort:
  method: state
  numeric: true
  reverse: true
```

## 10. Horizontal Stack for Compact View

```yaml
type: horizontal-stack
cards:
  - type: markdown
    content: |
      **Stop 1234**
      {% for bus in state_attr('sensor.dublin_bus_stop_1234', 'next_buses')[:2] %}
      {{ bus.route }}: {{ bus.due_time }}
      {% endfor %}
  
  - type: markdown
    content: |
      **Stop 5678**
      {% for bus in state_attr('sensor.dublin_bus_stop_5678', 'next_buses')[:2] %}
      {{ bus.route }}: {{ bus.due_time }}
      {% endfor %}
  
  - type: markdown
    content: |
      **Stop 9012**
      {% for bus in state_attr('sensor.dublin_bus_stop_9012', 'next_buses')[:2] %}
      {{ bus.route }}: {{ bus.due_time }}
      {% endfor %}
```

## Tips for Customization

1. **Replace Stop IDs**: Change `1234`, `5678`, etc. to your actual stop IDs
2. **Adjust Number of Buses**: Modify `[:5]` to show more or fewer buses
3. **Color Coding**: Add conditional formatting based on arrival times
4. **Icons**: Use different MDI icons for different stops
5. **Combine Cards**: Use `vertical-stack` or `horizontal-stack` to organize

## Required Custom Components

Some advanced examples require:
- `custom:auto-entities` - [GitHub](https://github.com/thomasloven/lovelace-auto-entities)
- `custom:button-card` - [GitHub](https://github.com/custom-cards/button-card)
- `custom:template-entity-row` - [GitHub](https://github.com/thomasloven/lovelace-template-entity-row)

Install these via HACS for the best experience!
