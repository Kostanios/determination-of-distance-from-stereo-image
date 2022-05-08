def calculate_size(camera_delta, delta1, delta2, x1, x2, y1, y2, F, matrix_size, pixel_size):
    Za = camera_delta / delta1
    Zb = camera_delta / delta2

    Xa = x1 * pixel_size * Za / F
    Xb = x2 * pixel_size * Zb / F

    Ya = y1 * pixel_size * Za / F
    Yb = y2 * pixel_size * Zb /F
    print(
      [camera_delta],
      ' ',
      [delta1],
      ' ',
      [Xa],
      ' ',
      [Ya],
      ' ',
      [delta2],
      ' ',
      [Xb],
      ' ',
      [Yb],
      ' ',
      [F],
      ' ',
      matrix_size)
    return pow(pow(Za - Zb, 2) + pow(Xa - Xb, 2) + pow(Ya - Yb, 2), 1/2)
