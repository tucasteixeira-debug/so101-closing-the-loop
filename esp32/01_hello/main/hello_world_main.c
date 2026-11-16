/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

void app_main(void)
{
    printf("Here goes Exercise Numebr 1 \n");
    uint8_t counter = 250;  // This emans taht counetr goes from 0 to 255

    while (1) {
        printf("The counter is at %d\n", counter);
        vTaskDelay(pdMS_TO_TICKS(1000));
        counter = counter +1;
    }

   

}

// 255 is written as 1111 1111, when youa dd 1 to a numebr in term of bits is literlaly changing one numebr so for exmaple 0000 0011 which si the numebr 3 for exmampel if youa dd one and make it into 4 it will be 000 0100 so I geuss when you recah 255 it will go down back to 0 right?