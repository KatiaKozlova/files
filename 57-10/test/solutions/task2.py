def solve() -> int:
    """
    A function that finds a greedy sum of arrays.

    Returns:
        int: greedy sum of an array.
    """
    _ = input()
    arr = map(int, input().split())
    sum, mn = 0, 0
    for elem in arr:
        sum += elem
        mn = min(mn, sum)
    return sum - 2 * mn


def main() -> None:
    t = int(input())
    for _ in range(t):
        print(solve())


if __name__ == "__main__":
    main()
