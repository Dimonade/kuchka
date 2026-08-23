"""Quick task: diode pre-flight check.

We're prototyping a pre-flight safety check for the new diode driver before it goes into the acquisition pipeline.
Nothing fancy - just a first pass.

Time box: 10 minutes.
Don't overthink it, don't go looking things up, just write what you'd normally write.

What you're given
-----------------

1. `read_status()` which returns the `status` of the diode.
2. From the datasheet, section 4.2 (Absolute Maximum Ratings):
    MAX_CURRENT_MA = 250
    MAX_CASE_TEMP_C = 45
    MAX_POWER_MW = 500

What we need
------------

Write a function `check_diode_status(status: dict) -> None: ...` that:

1. Computes the dissipated power from `status`.
2. Checks current, case temperature, and power against the three limits above.
3. Prints one line per check: which metric, its value, and `PASS`/`FAIL`.

Run this file when you're done.
It should print three PASS/FAIL lines.
"""

status = {
    "i_meas": 187500,
    "v_meas": 2350,
    "t_case": 314.85,
}

MAX_CURRENT_MA = 250
MAX_CASE_TEMP_C = 45
MAX_POWER_MW = 500


def read_status():
    return status


def check_diode_status(status: dict) -> None: ...


if __name__ == "__main__":
    status = read_status()
    check_diode_status(status)
