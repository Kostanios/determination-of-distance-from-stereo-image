def SSD(first_image_part, second_image_part):
    x_size = len(first_image_part)
    y_size = len(first_image_part[0])
    sum_of_dif_r = 0
    sum_of_dif_g = 0
    sum_of_dif_b = 0
    sum_of_dif_i = 0
    x = 0
    while x < x_size:
        y = 0
        while y < y_size:
            first_image_pixel = first_image_part[x][y]
            second_image_pixel = second_image_part[x][y]

            sum_of_dif_r = sum_of_dif_r + pow(int(first_image_pixel[0]) - int(second_image_pixel[0]), 2)
            sum_of_dif_g = sum_of_dif_g + pow(int(first_image_pixel[1]) - int(second_image_pixel[1]), 2)
            sum_of_dif_b = sum_of_dif_b + pow(int(first_image_pixel[2]) - int(second_image_pixel[2]), 2)
            sum_of_dif_i = sum_of_dif_i + pow(((int(first_image_pixel[0]) + int(first_image_pixel[1]) + int(first_image_pixel[2])) / 3) - ((int(second_image_pixel[0]) + int(second_image_pixel[1]) + int(second_image_pixel[2])) / 3), 2)

            y += 1
        x += 1
    return [sum_of_dif_r, sum_of_dif_g, sum_of_dif_b, sum_of_dif_i]
