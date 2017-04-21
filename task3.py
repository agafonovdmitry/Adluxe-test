from subprocess import Popen, PIPE


command = "python main.py --url " \
          "'http://lib.ru/FOUNDATION/r_pervyj_zakon.txt'"
p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

text, title = p.communicate()
text = text.decode()

text_length = len(text)
lowered_text = text.lower()

print(title.decode())
print('Symbol', 'Number', 'Percentage')

sorted_letters = sorted(
    set(lowered_text), key=lambda x: -lowered_text.count(x))

for let in sorted_letters:
    let_amount = lowered_text.count(let)
    print('{0: <6}'.format(repr(let)),
          '{0: <6}'.format(let_amount),
          '{0: <6}%'.format(round(let_amount/text_length*100, 3)))
