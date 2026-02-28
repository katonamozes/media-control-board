# Media Control Board

A custom 5-key macropad with a rotary encoder, an OLED display, and RGB indicators, powered by a Seeed XIAO RP2040.
<img width="743" height="788" alt="image" src="https://github.com/user-attachments/assets/4767f666-a09f-413f-a0db-b6e6261581c4" />
<img width="865" height="858" alt="image" src="https://github.com/user-attachments/assets/a4acb264-5d12-400d-b660-9b5c570a7247" />
<img width="602" height="844" alt="image" src="https://github.com/user-attachments/assets/e8ba6a89-b146-4bfa-bbde-7637fcc56b45" />
<img width="1146" height="716" alt="image" src="https://github.com/user-attachments/assets/2c318efb-93c4-4f73-a0a7-e605e9538943" />




BOM:
Everything that you need in order to make this hackpad
1x Seeed Studio XIAO RP2040
5x mechanical switches
1x rotary encoder with push-button
1x 0.91" I2C OLED
4x SK6812MINI-E RGB LEDs
1x Case (2 3d printed parts)
4x M3 bolts

The button connected to pin 10 plays the previous track.
The button connected to pin 8 plays the next track.
The button connected to pin 9 pauses the media.
The button connected to pin 7 scrolls right.
The button connected to pin 11 scrolls left.

The rotary encoder's button is connected to pin 6 and mutes.
The Rotary encoder's rotation is connected to pin 4 and controls the volume.

The sk6812MINI-E leds are connected to pin 1.

The 0.91 inch OLED display is connected to pins 2(SCL) and 3(SDA).
