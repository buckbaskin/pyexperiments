from collections import defaultdict

namedict = {
1880: 
[('Mary', 'F', '7065', 1), 
('Anna', 'F', '2604', 2), 
('John', 'M', '9655', 1)],
1881: 
[('Mary', 'F', '8065', 1), 
('Anna', 'F', '9604', 2), 
('John', 'M', '5655', 1)],
1882: 
[('Mary', 'F', '9065', 1), 
('Anna', 'F', '9604', 2), 
('John', 'M', '5655', 1)]
}

output_to_match = [
[{str(('Anna', 'F',)): {1880: [2604, 2], 1881: [9604, 2], 1882: [9604, 2],}}],
[{str(('John', 'M',)): {1880: [9655, 1], 1881: [5655, 1], 1882: [5655, 1],}}],
[{str(('Mary', 'F',)): {1880: [7065, 1], 1881: [8065, 1], 1882: [9065, 1],}}],
]

def reorder_namedict(namedict):
    new_list_representation = defaultdict(dict)
    for year in namedict:
        for user_tuple in namedict[year]:
            name, gender, num1, num2 = user_tuple
            new_list_representation[str((name, gender,))][year] = [int(num1), int(num2)]

    new_list = []

    for key in sorted(new_list_representation):
        new_list.append([{key: new_list_representation[key]}])

    return new_list

if __name__ == '__main__':
    match_this = str(output_to_match)
    iTried = str(reorder_namedict(namedict))
    # print(match_this)
    # print('---')
    # print(iTried)
    for i in range(0, len(match_this)):
        if not match_this[i] == iTried[i]:
            print('%d %s %s' % (i, match_this[i], iTried[i],))
    print(match_this == iTried)