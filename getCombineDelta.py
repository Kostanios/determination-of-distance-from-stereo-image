from normalSSD import normalSSD
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('classic')

def get_combune_delta(
        point1, point2,
        main_image, second_image):

    print(len(main_image))
    print(len(main_image[0]))
    fig1, plts1 = plt.subplots()
    fig2, plts2 = plt.subplots()

    delta1 = 0
    delta2 = 0
    x_offset = 0

    max_offset = 50

    i_ssd1 = []
    i_ssd2 = []

    min_ssd1 = normalSSD(
            main_image[point1.y() - 5:point1.y() + 5, point1.x() - 5:point1.x() + 5],
            second_image[point1.y() - 5:point1.y() + 5, (point1.x() - 5):(point1.x() + 5)]
    )

    min_ssd2 = normalSSD(
            main_image[point2.y() - 5:point2.y() + 5, point2.x() - 5:point2.x() + 5],
            second_image[point2.y() - 5:point2.y() + 5, (point2.x() - 5):(point2.x() + 5)]
    )

    while x_offset < max_offset:
        new_ssd1 = normalSSD(
            main_image[point1.y() - 5:point1.y() + 5, point1.x() - 5:point1.x() + 5],
            second_image[point1.y() - 5:point1.y() + 5, (point1.x() - 5 + x_offset):(point1.x() + 5 + x_offset)]
        )

        new_ssd2 = normalSSD(
            main_image[point2.y() - 5:point2.y() + 5, point2.x() - 5:point2.x() + 5],
            second_image[point2.y() - 5:point2.y() + 5, (point2.x() - 5 + x_offset):(point2.x() + 5 + x_offset)]
        )

        i_ssd1.append(new_ssd1[3])
        i_ssd2.append(new_ssd2[3])

        if min_ssd1[3] > new_ssd1[3]:
            delta1 = x_offset
            min_ssd1 = new_ssd1

        if min_ssd2[3] > new_ssd2[3]:
            delta2 = x_offset
            min_ssd2 = new_ssd2
        x_offset += 1

    delta_range = range(0, max_offset)
    plts1.plot(np.array(delta_range), np.array(i_ssd1), label='first part', color='r')
    plts2.plot(np.array(delta_range), np.array(i_ssd2), label='second part', color='b')

    plt.show()
    return delta1, delta2
