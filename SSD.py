def SSD (partOfFirstImage, partOfSecondImage):
    x = 0
    y = 0
    sum_of_dif = 0
    while x < len(partOfFirstImage):
      while y < len(partOfFirstImage[0]):
        sum_of_dif = sum_of_dif + pow(partOfFirstImage[x][y] - partOfSecondImage[x][y], 2)
    return sum_of_dif
