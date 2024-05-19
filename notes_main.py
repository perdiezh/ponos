#начни тут создавать приложение с умными заметкамиfr
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt 
import json
app = QApplication([])
main_win = QWidget()

main_win.setWindowTitle('Умные Заметки')
main_win.move(900, 70)
main_win.resize(400,200)
 
text1 = QLabel('Список заметок')
text2 = QLabel('Список тегов')
textedit = QTextEdit()
lineedit = QLineEdit()
zmtbtn1 = QPushButton('Создать заметку') 
zmtbtn2 = QPushButton('Удалить заметку')
zmtbtn3 = QPushButton('Сохранить заметку')
tegbtn1 = QPushButton('Добавить к заметке')
tegbtn2 = QPushButton('Открепить от заметки')
tegbtn3 = QPushButton('Искать заметки по тегу')

notes_list1 = QListWidget()
notes_list2 = QListWidget()

v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line = QHBoxLayout()

v_line1.addWidget(textedit)
v_line2.addWidget(text1)
v_line2.addWidget(notes_list1)
v_line2.addWidget(zmtbtn1)
v_line2.addWidget(zmtbtn2)
v_line2.addWidget(zmtbtn3)
v_line2.addWidget(text2)
v_line2.addWidget(lineedit)
v_line2.addWidget(notes_list2)
v_line2.addWidget(tegbtn1)
v_line2.addWidget(tegbtn2)
v_line2.addWidget(tegbtn3)
h_line.addLayout(v_line1)
h_line.addLayout(v_line2)
main_win.setLayout(h_line)

notes = {
    'Великая отечественная война 1941':{
        'текст': 'фильм повествует историю адольфа гитлера',
        'теги': ['ужасы', 'триллер']
    },
    'Блокада Ленинграда':{
        'текст': 'фильм о ужасах',
        'теги': ['блокада']
    }
}
with open('f.json','w') as file:
    json.dump(notes, file)

with open('f.json', 'r') as file:
    data = json.load(file)
notes_list1.addItems(data)

def show_note():
    name = notes_list1.selectedItems()[0].text()
    textedit.setText(notes[name]['текст'])
    notes_list2.clear()
    notes_list2.addItems(notes[name]['теги'])
notes_list1.itemClicked.connect(show_note)

def addnote():
    note_name, ok = QInputDialog.getText(
        main_win, "Добавить заметку", "Название заметки: "
    )
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        notes_list1.addItem(note_name)
def del_notes():
    if notes_list1.selectedItems():
        note_name = notes_list1.selectedItems()[0].text()
        del notes[note_name]
        notes_list1.clear()
        notes_list1.addItems(notes)
        notes_list2.clear()
        textedit.clear()
        with open('f.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка не выбрана')
def save_note():
    if notes_list1.selectedItems():
        name = notes_list1.selectedItems()[0].text()
        notes[name]['текст'] = textedit.toPlainText()
        with open('f.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка не выбрана') 
def add_tag():
    if notes_list1.selectedItems():
        name = notes_list1.selectedItems()[0].text()
        tag = lineedit.text()
        if not tag in notes[name]['теги']:
            notes[name]['теги'].append(tag)
            notes_list2.clear()
            notes_list2.addItems(notes[name]['теги'])
            lineedit.clear()
            with open('f.json', 'w') as file:
                json.dump(notes, file)
        else:
            print("Заметка не выбрана")
def del_note():
    if notes_list1.selectedItems():
        note_name = notes_list1.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[note_name]['теги'].remove(tag)
        notes_list1.clear()
        notes_list1.addItems(notes)
        notes_list2.clear()
        lineedit.clear()
        with open('f.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка не выбрана')

def search_tag_text():
    tag = lineedit.text()
    if tag and tegbtn3.text() == 'Искать заметки по тегу':
        notes_filtered = []
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered.append(note)
        notes_list1.clear()
        notes_list2.clear()
        lineedit.clear()
        notes_list1.addItems(notes_filtered)
        tegbtn3.setText('Сбросить поиск')
    
    elif tegbtn3.text() == 'Сбросить поиск':
        lineedit.clear()
        notes_list1.clear()
        notes_list2.clear()
        notes_list1.addItems(notes)
        tegbtn3.setText('Искать заметки по тегу')
    elif tag == '' and tegbtn3.text() == 'Искать заметки по тегу':
        print('тег для поиска не был введён')
    
tegbtn3.clicked.connect(search_tag_text)
zmtbtn1.clicked.connect(addnote)
zmtbtn2.clicked.connect(del_notes)
zmtbtn3.clicked.connect(save_note)
tegbtn1.clicked.connect(add_tag)
tegbtn2.clicked.connect(del_note)





main_win.show()
app.exec_()
