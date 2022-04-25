def calculate_sigma_delta_pow(
        x_size,
        y_size,
        first_image_part,
        second_image_part,
        first_image_part_current_i,
        second_image_part_current_i):
    #
    # calculate sum pow of delta between pixels end current i
    #
    first_i_sigma_delta_pow = 0
    second_i_sigma_delta_pow = 0

    x = 0
    while x < x_size:
        y = 0
        while y < y_size:
            first_image_pixel = first_image_part[x][y]
            second_image_pixel = second_image_part[x][y]

            first_i = int(first_image_pixel[0]) + int(first_image_pixel[1]) + int(first_image_pixel[2])
            second_i = int(second_image_pixel[0]) + int(second_image_pixel[1]) + int(second_image_pixel[2])

            first_i_sigma_delta_pow = first_i_sigma_delta_pow + pow(first_image_part_current_i - first_i, 2)
            second_i_sigma_delta_pow = second_i_sigma_delta_pow + pow(second_image_part_current_i - second_i, 2)

            y += 1
        x += 1

    return [first_i_sigma_delta_pow, second_i_sigma_delta_pow]


def normalSSD(first_image_part, second_image_part):
    x_size = len(first_image_part)
    y_size = len(first_image_part[0])

    first_image_part_current_i = 0
    second_image_part_current_i = 0
    #
    # calculate current i
    #
    x = 0
    while x < x_size:
        y = 0
        while y < y_size:
            first_image_pixel = first_image_part[x][y]
            second_image_pixel = second_image_part[x][y]

            first_i = int(first_image_pixel[0]) + int(first_image_pixel[1]) + int(first_image_pixel[2])
            second_i = int(second_image_pixel[0]) + int(second_image_pixel[1]) + int(second_image_pixel[2])

            first_image_part_current_i = first_image_part_current_i + (first_i / (x_size * y_size))
            second_image_part_current_i = second_image_part_current_i + (second_i / (x_size * y_size))

            y += 1
        x += 1
    #
    # calculate k
    #
    k_r = 0
    k_g = 0
    k_b = 0
    k_i = 0

    x = 0
    while x < x_size:
        y = 0
        while y < y_size:
            first_image_pixel = first_image_part[x][y]
            second_image_pixel = second_image_part[x][y]

            first_i = int(first_image_pixel[0]) + int(first_image_pixel[1]) + int(first_image_pixel[2])
            second_i = int(second_image_pixel[0]) + int(second_image_pixel[1]) + int(second_image_pixel[2])

            pow_deltas = calculate_sigma_delta_pow(
                x_size,
                y_size,
                first_image_part,
                second_image_part,
                first_image_part_current_i,
                second_image_part_current_i
            )

            k_i = k_i + pow((
                (first_i - first_image_part_current_i) / pow_deltas[0]
            ) - (
                (second_i - second_image_part_current_i) / pow_deltas[0]
            ), 2)

            y += 1
        x += 1
    return [k_r, k_g, k_b, k_i]
