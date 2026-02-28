# Media Control Board

A custom 5-key macropad with a rotary encoder, an OLED display, and RGB indicators, powered by a Seeed XIAO RP2040.

## Hardware Features
* **Microcontroller:** Seeed Studio XIAO RP2040
* **Switches:** 5x mechanical switches + 1x rotary encoder with push-button
* **Display:** 0.91" I2C OLED
* **Lighting:** 4x SK6812MINI-E RGB LEDs

The button connected to pin 10 plays the previous track.
The button connected to pin 8 plays the next track.
The button connected to pin 9 pauses the media.
The button connected to pin 7 scrolls right.
The button connected to pin 11 scrolls left.

The rotary encoder's button is connected to pin 6 and mutes.
The Rotary encoder's rotation is connected to pin 4 and controls the volume.

The sk6812MINI-E leds are connected to pin 1.

The 0.91 inch OLED display is connected to pins 2(SCL) and 3(SDA).