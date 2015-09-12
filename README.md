# Autotablet
### Automatic mode switching for convertable notebooks

This project is currently at best in an alpha stage. The code runs, but has some hard-coded paths. The configuration is expected to be located in `/etc/autotablet/inputDevices.json` at the Moment.

My primary goal for this project is to provide Linux support for automatic rotation of screens and input devices of convertable notbooks. Being the owner of a Lenovo ThinkPad Yoga, I found no satisfactory solution to address this task. 

Based on my experience from trying to make this work using what others have provided so far I identify three aspects which I would like to keep as independent as possible:

* Configuration Detection (make\_input\_config.py): As every device will be different, and I have only one device at hand, I tried to keep the detection script as general as possible, but also tried to enable manual configuration by writing the detected configuration to JSON. As JSON-libraries are widely available, this will hopefully enable others to write detection code more easily in case my code cannot be extended or adapted to work in a generic way.

* Mode Selection (tablet\_control.py): The different modes in which convertales can be operated will differ for every model. I currenlty define four modes: normal (notebook), tablet, tent(which is currently pretty much identical to tablet), and scratchpad, which for my notebook turns off all inputs but the stylus pen. Tablet mode comes with an orientation parameter, so this is very likely the most important mode for most people, because it covers rotation of the screen and inputs as well as disabling keyboard and trackpad inputs.

* Mode Detection (monitor\_accel.py): Being able to switch modes is important, but usually you would not want to do it manually, and doing so via the command line is a pain in some cases (e.g. in tablet mode using the onscreen keyboard). While some may prefer assigning hotkeys or implementing this via a graphical element such as a panel item, I personally prefer automatic detection of the modes. I currenlty use the accelerometer to detect which mode is active, and the modes are currently hard-coded, although I will move them into a config file some time soon.

I hope that by defining these three tasks, as many people as possible can use this code to do at least part of the work.

## Usage:

There are currently a few different options on how to use this.
* `tablet_control.py` enables mode-switching via the command line. You can also import it into your code to switch into the predefined modes. 

* `monitor_accel.py` can be run from the command line with no arguments to automatically monitor the accelerometer and switch into the modes automatically.

* `autotablet.service` will run `monitor_accel.py` via systemd

## Existing issues:

* Mode detection currently does not handle the accelerometer's file becoming unreadable after a sleep phase well and will exit in case that happens.

* Mode detection uses a hard-coded configuration of modes

* For my hardware some devices may be unavailable for some time after rotating the screen, which can lead to failure of the proper rotation, which necessitates checking whether the mode change was successful. For my setup this produces error-messages on some mode-switches, but does not impact functionality.
