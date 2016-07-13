class MyClass:
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def calc(self):
        return self._a + self._b


def func_a(instance):
    print(instance.calc())


def main():
    app = MyClass('a', 2)
    func_a(app)

if __name__ == '__main__':
    main()
