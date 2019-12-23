# GridFrequency
Python wrapper for obtaining the current frequency of the Swedish national power grid

### Sources
https://www.svk.se/drift-av-stamnatet/kontrollrummet/ (Swedish National Grid - Inspiration to this project)
http://driftsdata.statnett.no/restapi/ (Norwegian National Grid - data provider)



## Installation
This program only has one dependency; the ```requests``` module. The dependency can be be installed with ```pip``` using
```bash
pip install -r requirements.txt
```
## Usage
Below are a few snippets of example usage. For more thorough usage, please see the source code. 

### Continous measurement
```python
pollGridFrequency()
```
Polls every 0.5s [default], only printing result [default]. Calls callback only if value changed [default]

```python
 pollGridFrequency(my_callback, 0.1)
```
Polls with custom callback function `my_callback` taking ONE argument (frequency). I.e. my_callback(freq) is called. Custom refresh rate.
```python
 pollGridFrequency(None, 2, False)
```
No callback (prints values only), polling every 2s and returning values regardless of whether they have changed.

### Obtain a single frequency measurement
```python
 print("This is freq: " + str(getCurrentFrequency()[1]))
```
Single-capture frequency.

### Callback
The data obtained in the continous polling is passed to a provided callback. The format of the callback is as follows
```python
def my_callback(frequency):
  desired_freq = 50
  print("We differ by {} Hertz".format((desired_freq - frequency))
```
