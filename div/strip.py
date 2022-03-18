messsage = "I think human: sleeping sounds great!"

print(messsage.replace('.+:', ''))

beskjed = 'Hello all please help me:'

txt = 'Hello all please help me:'
# better to not use 'string' as variable name

text2 = ' '.join(word for word in txt.split(' ') if not word.endswith(':'))


print(text2)
