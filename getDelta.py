from SSD import SSD
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('classic')

def get_delta(point1, point2, main_image, second_image):
    print(len(main_image))
    print(len(main_image[0]))
    fig1, plts1 = plt.subplots()
    plts1.set_title('gra ssd')
    delta = 0
    x_offset = 0
    r_ssd = []
    g_ssd = []
    b_ssd = []
    i_ssd = []
    min_ssd = SSD(main_image[point1.y():point2.y(), point1.x():point2.x()],
                  second_image[point1.y():point2.y(), point1.x():point2.x()])
    max_offset = 50
    # max_offset = len(main_image[0]) - point2.x()
    print(max_offset, '-max offset')
    while x_offset < max_offset:
        new_ssd = SSD(main_image[point1.y():point2.y(), point1.x():point2.x()],
                      second_image[point1.y():point2.y(), (point1.x() + x_offset):(point2.x() + x_offset)])

        r_ssd.append(new_ssd[0])
        g_ssd.append(new_ssd[1])
        b_ssd.append(new_ssd[2])
        i_ssd.append(new_ssd[3])

        if min_ssd[3] > new_ssd[3]:
            delta = x_offset
            min_ssd = new_ssd
        x_offset += 1
    delta_range = range(0, max_offset)
    plts1.plot(np.array(delta_range), np.array(r_ssd), label='red spectral', color='r')
    plts1.plot(np.array(delta_range), np.array(g_ssd), label='green spectral', color='g')
    plts1.plot(np.array(delta_range), np.array(b_ssd), label='blue spectral', color='b')
    plts1.plot(np.array(delta_range), np.array(i_ssd), label='all spectral', color='grey')

    plts1.legend()
    plt.xlabel('delta px')
    plt.xlabel(SSD)
    # plt.imshow(second_image[point1.y():point2.y(), (point1.x() + delta):(point2.x() + delta)], interpolation='nearest')
    plt.show()
    print('------------------------------------------delta')
    print(delta)
    print('------------------------------------------min-ssd')
    print(min_ssd)
    return delta
