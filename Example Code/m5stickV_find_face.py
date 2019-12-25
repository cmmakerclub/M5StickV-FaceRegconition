# M5Stick-V Face Regconition
# Chiang Mai Maker Club 
# 25-Dec-19

import sensor, image, time, lcd
import KPU as kpu

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.skip_frames(time = 2000)
sensor.run(1)

clock = time.clock()

lcd.init()
lcd.rotation(2)
lcd.clear()

# Load model from SD Card
task = kpu.load("/sd/model.kmodel")

# Create Class name
classes = ['man', 'tong']

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)

    if code:
        for i in code:
            print(i)
            a = img.draw_rectangle(i.rect())
            for i in code:
                a = lcd.draw_string(10, 10, str(clock.fps()), lcd.RED, lcd.WHITE)
                a = lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                a = lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
                time.sleep(0.2)
            a = lcd.display(img)
    else:
        a = lcd.draw_string(10, 10, str(clock.fps()), lcd.RED, lcd.WHITE)
        a = lcd.display(img)
a = kpu.deinit(task)
