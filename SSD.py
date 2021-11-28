def SSD(first_image_part, second_image_part):
    x = 0
    y = 0
    sum_of_dif_r = 0
    sum_of_dif_g = 0
    sum_of_dif_b = 0
    while x < len(first_image_part):
        while y < len(first_image_part[0]):
            first_image_pixel = first_image_part[x][y]
            second_image_pixel = second_image_part[x][y]

            sum_of_dif_r = sum_of_dif_r + pow(first_image_pixel[0] - second_image_pixel[0], 2)
            sum_of_dif_g = sum_of_dif_g + pow(first_image_pixel[1] - second_image_pixel[1], 2)
            sum_of_dif_b = sum_of_dif_b + pow(first_image_pixel[2] - second_image_pixel[2], 2)

            y += 1
        x += 1
    return [sum_of_dif_r, sum_of_dif_g, sum_of_dif_b]
