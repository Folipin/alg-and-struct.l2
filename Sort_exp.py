import random
import time

product_list = []
words_pool = ['Яблоко', 'Машина', 'Телефон', 'Книга', 'Стол', 'Лампа', 'Часы', 'Рюкзак', 'Кот', 'Дом']

for i in range(10 ** 6 + 1):
    name = f"{random.choice(words_pool)}_{random.randint(100, 9999999)}"
    product = {'id': i, 'nazvanie': name}
    product_list.append(product)

random.shuffle(product_list)
product_listb = product_list.copy()
product_listv = product_list.copy()
product_listp = product_list.copy()

print('##################')

def vibor(list):
    index = 0
    for i in range(index,len(list)):
        max_id = i
        for j in range(i+1,len(list)):
            if list[j]['id'] < list[max_id]['id']:
                max_id = j
        list[i], list[max_id] = list[max_id], list[i]
    return list


def bubble_sort(list):
    n = len(list)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if list[j]['id'] > list[j + 1]['id']:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list


def quick_sort(arr):

    def _quick_sort(items, low, high):
        if low < high:

            pi = partition(items, low, high)

            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)


    def partition(items, low, high):
        pivot = items[high]['id']
        i = low - 1
        for j in range(low, high):
            if items[j]['id'] <= pivot:
                i = i + 1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1


    _quick_sort(arr, 0, len(arr) - 1)
    return arr

startp = time.perf_counter()
rezq = quick_sort(product_listp)
endp = time.perf_counter()
timerp = endp - startp
print('Быстрая сортировка' ,'\n', f" отработала за {timerp:.8f} сек")
#print(rezq)

startv = time.perf_counter()
rezv = vibor(product_listv)
endv = time.perf_counter()
timerv = endv - startv
print('Сортировка выбором' ,'\n', f" отработала за {timerv:.8f} сек")
#print(rezv)


startb = time.perf_counter()
rezb = bubble_sort(product_listb)
endb = time.perf_counter()
timerb = endb - startb
print('Сортировка пузыриком' ,'\n', f" отработала за {timerb:.8f} сек")
#print(rezb)



