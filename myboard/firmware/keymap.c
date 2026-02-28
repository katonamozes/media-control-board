#include QMK_KEYBOARD_H

// Define the keymap for the 5 buttons
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_direct(
        KC_WH_L, KC_MPRV, KC_MPLY, KC_MNXT, KC_WH_R
    )
};

// Encoder Logic: Volume and Mute
bool encoder_update_user(uint8_t index, bool clockwise) {
    if (index == 0) { 
        if (clockwise) {
            tap_code(KC_VOLU);
        } else {
            tap_code(KC_VOLD);
        }
    }
    return true;
}

// Basic OLED Display setup
#ifdef OLED_ENABLE
bool oled_task_user(void) {
    oled_write_P(PSTR("Media Control\n"), false);
    oled_write_P(PSTR("Ready\n"), false);
    return false;
}
#endif