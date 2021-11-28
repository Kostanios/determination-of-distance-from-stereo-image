from SSD import SSD


def get_delta(point1, point2, main_image, second_image):
    delta = 0
    x_offset = 0
    min_ssd = SSD(main_image[point1.y():point2.y(), point1.x():point2.x()],
                  second_image[point1.y():point2.y(), point1.x():point2.x()])
    max_offset = len(main_image[0]) - point2.x()
    while x_offset < max_offset:
        new_ssd = SSD(main_image[point1.y():point2.y(), point1.x():point2.x()],
                      second_image[point1.y():point2.y(), point1.x() + x_offset:point2.x() + x_offset])
        print(x_offset)
        if (min_ssd[0] + min_ssd[1] + min_ssd[2]) / 3 > (new_ssd[0] + new_ssd[1] + new_ssd[2]) / 3:
            delta = x_offset
            min_ssd = new_ssd
        x_offset += 1

    print('------------------------------------------delta')
    print(delta)
    print('------------------------------------------min-ssd')
    print(min_ssd)
    return delta
