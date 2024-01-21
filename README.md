# bwt_perla_smartmeter
Read throughput and volume of BWT Perla water softening system (new VNC based firmware!)
Original code by [d3m0nxxl](https://github.com/d3m0nxxl/bwt_perla_smartmeter), but somehow my BWT Perla has a fully different resolution so I changed most of the mouse and capture coordinates.


## improvements
* Reusable method for capturing
* Also including NaCl (Regeneriermittel)
* mqtt with username/password
* config on own perla.cfg file

## requirements

python3, pip3

```bash
git clone bwt_perla_smartmeter
cd bwt_perla_smartmeter
python3 -m venv .
source bin/activate
pip3 install pytesseract paho-mqtt vncdotool
python3 bwt_perla_smartmeter.py
```
create your own `perla.cfg` from the `perla.cfg-EXAMPLE` in the same folder.
