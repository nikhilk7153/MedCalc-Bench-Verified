def age_conversion(input):
    count = 0
    while count < len(input):
        if 'year' in input[count + 1]:
            return input[count]
        elif 'months' in input[count + 1]:
            return input[count] // 12
        elif 'weeks' in input[count + 1]:
            return input[count] // 52
        elif 'days' in input[count + 1]:
            return 0
        count += 2
