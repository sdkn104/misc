import sys

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def main():
    if len(sys.argv) != 2:
        print("使い方: python fibonacci.py n")
        return
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("nは整数で指定してください")
        return
    print(fibonacci(n))

if __name__ == "__main__":
    main()