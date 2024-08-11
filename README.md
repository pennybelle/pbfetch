## pbfetch

![Screenshot_20240803_191108](https://github.com/user-attachments/assets/8fb08b86-90ce-48d7-a428-dbc8c6dbf848)

An unbelievably customizable hardware/software fetch. No more being limited to a logo on the left.

## Installation:
Paru:
> This package is now hosted on the [Arch User Repository](https://aur.archlinux.org/packages/pbfetch-git). If you have paru you can install with `paru -S pbfetch-git`

Rye:
> This program is bootstrapped by Rye. If you have Rye installed, in `/pbfetch/` use `rye sync` and `rye run pbfetch` to run fetch.

Binary:
> To install directly from the PKGBUILD, navigate to `pbfetch/bin/` and use `makepkg -si`.

## Config Examples
These are some of the things you can do with pbfetch. The config is a simple text file and you can design the output to be whatever you want within the limits of text (for now...), and can display stat info wherever you'd like in whatever fashion you desire by inputting certain keyword tags into the config. For example, the tag `$host` would be replaced by hostname when you run the program. So a config with only the word `$host` in it would print as yoru hostname in the format of `user@device`. See photos below of the things you can do with this amount of creative freedom;

![Screenshot_20240808_214059](https://github.com/user-attachments/assets/948fd649-cde5-4b4a-a92d-6114bcffcaf9)

![Screenshot_20240808_214525](https://github.com/user-attachments/assets/a7f0b9f6-710f-43d6-ba2c-4035c6c0c46d)

![Screenshot_20240808_215154](https://github.com/user-attachments/assets/d22b57b3-a641-468b-809d-520b15c6e173)

![Screenshot_20240810_105613](https://github.com/user-attachments/assets/b114f119-87a3-446a-8f17-a6441bf74e85)

Creating your own custom configuration is a bit more work than other fetches but the benefit is obviously not being limited to the creator's vision of the output format, rather the user themselves having almost complete freedom to change what they want how they want. 

## License
The code is FOSS and licensed uner Apache 2.0, so you may alter and use the code how you'd like as long as you give proper credit.

## Disclaimer
This project is very much a WIP, and only Arch Linux is supported. If you'd like to help me get this working on your system, please let me know! I'd like for this project to be as comprehensive as possible. I hope you like it!
