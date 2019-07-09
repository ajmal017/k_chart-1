def gen_numbers(limit):
    for item in range(limit):
        yield item*item
        print(f"Inside the yield: {item}")

numbers = gen_numbers(3)

print(numbers)

for item in numbers:
    print(item)