import I2C_LCD_driver

textLcd = I2C_LCD_driver.lcd()

textLcd.lcd_display_string("I WANNA",1)
textLcd.lcd_display_string_pos("GO HOME", 2,3)