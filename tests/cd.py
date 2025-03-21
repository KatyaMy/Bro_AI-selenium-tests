#1

def function(nums):
    num = []
    for a in list(range(min(nums), max(nums) + 1)):
        num.append(a)
    return num

lst = [1,2,3,5,7,12]
print(function(lst))


#2
def sum_mul(n, m):
    if n <= 0 or m <= 0:
        return "INVALID"
    else:
        total = 0 #[18+]
        for i in range(n, m, n):
            print(f'n = {n}')# проходим по всем кратным n, начиная с n до m (не включая m)

            print(f'n = {n}')
            print(f'i = {i}')
            total += i
            # print(f'i = {i}')
            # print(f' total = {total}')
        return total

print(sum_mul(6, 38))