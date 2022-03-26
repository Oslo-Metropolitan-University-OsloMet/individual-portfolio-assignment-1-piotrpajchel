to_exclude = {0}
vector = ['a', 'b', 'c', 'd']
vector2 = [element for i, element in enumerate(vector) if i not in to_exclude]
print(vector2)