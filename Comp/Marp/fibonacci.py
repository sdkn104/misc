def fibonacci(n):
    """n番目までのフィボナッチ数列をリストで返す"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq

if __name__ == "__main__":
    try:
        n = int(input("出力したいフィボナッチ数列の項数を入力してください: "))
        result = fibonacci(n)
        print(result)
    except Exception as e:
        print("エラー: ", e)