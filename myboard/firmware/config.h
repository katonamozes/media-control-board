#pragma once

/* Encoder Push Switch */
#define ENCODERS_PAD_A { GP6 }
#define ENCODERS_PAD_B { GP5 }
#define ENCODER_RESOLUTION 4

/* I2C pins for OLED */
#define I2C_DRIVER I2CD1
#define I2C1_SDA_PIN GP2
#define I2C1_SCL_PIN GP3

/* RGB LED Type */
#define WS2812_DI_PIN GP1
#define RGB_DI_PIN GP1