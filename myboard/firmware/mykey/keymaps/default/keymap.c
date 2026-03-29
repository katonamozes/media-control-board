#include QMK_KEYBOARD_H

enum layer_names {
    _BASE,
};

// 1. KEYMAP DEFINITION
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE] = LAYOUT(
        MS_WHLL, KC_MEDIA_PREV_TRACK, KC_MEDIA_PLAY_PAUSE, KC_MEDIA_NEXT_TRACK, MS_WHLR, KC_AUDIO_MUTE
    )
};

// 2. ENCODER LOGIC
#ifdef ENCODER_ENABLE
bool encoder_update_user(uint8_t index, bool clockwise) {
    if (index == 0) {
        if (clockwise) {
            tap_code(KC_VOLD);
        } else {
            tap_code(KC_VOLU);
        }
    }
    return false;
}
#endif

// This goes at the very end of your keymap.c
void keyboard_post_init_user(void) {
    rgblight_enable(); // Use the standard enable
    rgblight_sethsv(0, 0, 127); // Set to a dim white immediately
    rgblight_mode(1); // Static mode
}
#ifdef OLED_ENABLE
oled_rotation_t oled_init_user(oled_rotation_t rotation) {
    return OLED_ROTATION_0; // Change to OLED_ROTATION_180 if it's upside down on your PCB
}

bool oled_task_user(void) {
    oled_write_ln("mykey active", false);
    return true; // Change from false to true
}
#endif
