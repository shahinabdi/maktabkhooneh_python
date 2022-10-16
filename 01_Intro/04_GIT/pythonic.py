number_list = []
for i in range(10):
    number_list.append(i)


print(number_list)

# List Comperhension
number_list2 = [i for i in range(10)]
print(number_list2)

number_list3 = [*range(10)]
print(number_list3)


# ----------------------

list_city = ['Tehran', 'Berlin', 'Paris', 'NY']
list_zipcode = [25, 34, 75, 16]

dict_cities = dict()
for i in range(len(list_zipcode)):
    dict_cities[list_zipcode[i]] = list_city[i]
print(dict_cities)

dict_cities2 = {k: v for k, v in zip(list_zipcode, list_city)}
print(dict_cities2)

dict_cities3 = dict(zip(list_zipcode, list_city))
print(dict_cities3)
