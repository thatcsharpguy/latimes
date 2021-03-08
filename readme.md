#  latimes (as in Latin Times) 
# 🇲🇽🇨🇷🇵🇪🇵🇦🇨🇱🇻🇪🇧🇴🇸🇻🇬🇶🇬🇹🇨🇴🇪🇨🇦🇷🇨🇺🇧🇷

 > A tool that helps you schedule international events by converting time across timezones.

Download it from:
 [![PyPI version shields.io](https://img.shields.io/pypi/v/latimes.svg)](https://pypi.python.org/pypi/latimes/)

Use *latimes* to convert your natural language dates/times (in your timezone of choice) from one timezone to another.

## Out of the box usage

```shell
latime jueves 10:33 pm
```

Output:

```text
22:33 🇲🇽🇨🇷, 23:33 🇨🇴🇪🇨🇵🇪, 01:33+1 🇨🇱🇦🇷, 05:33+1 🇬🇶
```

## Configuration file  

Of course, not everyone wants to schedule their events based on Mexico City time, you can extract the configuration in a file using the command:

```shell script
latime --create-config
```  

After which you'll end up with a file like the following:  

```yaml
# The timezones must be expressed in TZ timezone
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
convert_to:
- "\U0001F1F2\U0001F1FD:America/Mexico_City"
- "\U0001F1E8\U0001F1F4:America/Bogota"
- "\U0001F1E8\U0001F1F1:America/Santiago"
- "\U0001F1EA\U0001F1E8:America/Guayaquil"
- "\U0001F1F5\U0001F1EA:America/Lima"
- "\U0001F1E6\U0001F1F7:America/Argentina/Buenos_Aires"
- "\U0001F1EC\U0001F1F6:Africa/Malabo"
- "\U0001F1E8\U0001F1F7:America/Costa_Rica"
output_formatting:
  aggregate: true
  aggregate_joiner: ''
  different_time_joiner: ', '
  time_format_string: '%H:%M'
starting_timezone: America/Mexico_City
```

**Don't get turned away by the `\U0001F1F2\U0001F1FD`**, that is just the code for this 🇲🇽 emoji, you can safely change whatever goes before the `:` in each of the entries under `convert_to` to any key you want, for example if you have this file:  

```yaml
starting_timezone: Europe/London
convert_to:
- "Japón 🍣:Asia/Tokyo"
- "Hawaii 🌺:Pacific/Honolulu"
output_formatting:
  aggregate: true
  aggregate_joiner: ''
  different_time_joiner: ', '
  time_format_string: '%I:%M%p'
```

And you run:

```shell script
latimes martes 10:30 pm
```

The output will be:


```
07:33AM+1 Japón 🍣, 12:33PM Hawaii 🌺
```

As you can see, it is highly customisable.
