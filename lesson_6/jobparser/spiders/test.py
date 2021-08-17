def test_yield():
    for i in range (10):
        yield i*i
        yield i

print(test_yield())
