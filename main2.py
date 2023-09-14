# SAME AS APP 13 BUT WE USE MYSQL DATABASE WHICH IS A BIGGER AND BETTER DATABASE
# COMPARED TO THE SQLITE



from PyQt6.QtWidgets import QApplication,QVBoxLayout,QLabel,QWidget,QGridLayout,QLineEdit,\
    QPushButton,QMainWindow,QTableWidget,QTableWidgetItem,QDialog,QDial,QComboBox,QToolBar,\
    QStatusBar,QMessageBox
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import QSize,Qt
import sys
from datetime import datetime
import mysql.connector

class DataBase():
    def __init__(self,host='localhost',user='root',password='segelulu96',database="school"):
        self.database=database 
        self.host=host
        self.user=user
        self.password=password
    def connect(self):
        connection=mysql.connector.connect(database=self.database,user=self.user,
        password=self.password,host=self.host) 
        return connection
    def close(self):
        pass


# First check out the tutorial examples before this
# You inherit from QMainWindow when you have a larger apps with multiple windows
# QMainWindow has a feat
# 
# ures such as status bar, menu bar, tool bar etc
# QWidget is limited and used for smaller apps such as the ones in the tutorialo folder

class MainWindow(QMainWindow):
    def __init__(self):
        # Instantiating parent __init__ method
        super().__init__() 
        self.setWindowTitle("Student Management System") 
        self.setFixedWidth(500)
        self.setFixedHeight(500)        
        # Adding MEnu Bar
        file_menu=self.menuBar().addMenu("&File")
        help_menu=self.menuBar().addMenu("&Help") 
        edit_menu=self.menuBar().addMenu("&Edit")

        add_student_action=QAction(QIcon("icons/add.png"),"Add Student",self) 
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action) 

        search_action=QAction(QIcon("icons/search.png"),"Search",self)
        search_action.triggered.connect(self.search)
        edit_menu.addAction(search_action)

        about_action=QAction("About",self)  
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action) 

        self.table=QTableWidget() 
        self.table.setColumnCount(4)   
        self.table.setHorizontalHeaderLabels(("ID","NAME","COURSE","MOBILE"))  
        self.table.verticalHeader().setVisible(False)   # To hide the index column
        self.setCentralWidget(self.table) 

        
        # Create Toolbars
        add_toolbar=QToolBar() 
        add_toolbar.setMovable(True)
        self.addToolBar(add_toolbar) 
        add_toolbar.addAction(add_student_action)

        search_toolbar=QToolBar() 
        search_toolbar.setMovable(True)
        self.addToolBar(search_toolbar) 
        search_toolbar.addAction(search_action)


        # Create status Bar
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar) 

        # Insert a Cell Click  
        self.table.cellClicked.connect(self.cell_clicked)  



        self.show()
        self.load_data() 


    def cell_clicked(self):
        edit_button=QPushButton("Edit") 
        edit_button.clicked.connect(self.edit) 

        delete_button=QPushButton("Delete Record") 
        delete_button.clicked.connect(self.delete) 

        children=self.findChildren(QPushButton) # To prevent the status bar from increasing the numbers of buttond 
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button) 
        self.statusbar.addWidget(delete_button)

    def load_data(self):  
        connection=DataBase().connect()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM students")
        rows=cursor.fetchall() 
        self.table.setRowCount(0)  # This makes sure the data being written inside the table is not being overwritten
        for row_number,row_data in enumerate(rows):
            self.table.insertRow(row_number) # To insert empty row in a table
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))  
        connection.close()    

    def insert(self):
        # InsertDialog is a class we created just below
        dialog=InsertDialog() 
        dialog.exec()  # This executes the class

    def search(self):
        search_student=SearchStudent()
        search_student.exec()

    def edit(self):
        dialog =EditDialog()
        dialog.exec()    

    def delete(self):
        dialog =DeleteDialog()
        dialog.exec()   

    def about(self):
        dialog=AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("About") 
        content='''App was created during the python course.
Feel free to modify and use this app
        '''
        self.setText(content)

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Insert Student Data") 
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout=QVBoxLayout()      

        # Add student name widget
        self.student_name=QLineEdit() 
        self.student_name.setPlaceholderText("Name") 
        layout.addWidget(self.student_name) 

        # Add courses widget
        self.course_name=QComboBox() 
        courses=["Biology","Mathematics","Computer Engineering", "System Engineering",
        "Business Adminisration","Music","BioChemistry","Astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # Add mobile widget
        self.mobile=QLineEdit() 
        self.mobile.setPlaceholderText("Mobile Number") 
        layout.addWidget(self.mobile) 

        # Add a submit button
        button=QPushButton("Register") 
        #button.setFixedSize(100,35) 
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def add_student(self):
        name=self.student_name.text()
        course=self.course_name.itemText(self.course_name.currentIndex())
        mobile=self.mobile.text()
        # SINCE WE WILL BE INSERTING SO WE NEED A CURSOR
        connection=DataBase().connect()
        cursor=connection.cursor() 
        cursor.execute("INSERT INTO students (NAME,COURSE,MOBILE) VALUES (%s,%s,%s)",
        (name,course,mobile)) 
        connection.commit()
        cursor.close()
        connection.close()
        self.close() 
        # To fefresh window
        main.load_data()   


class SearchStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search students") 
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout=QVBoxLayout()      

        # Add search box widget
        self.searchbox=QLineEdit() 
        self.searchbox.setPlaceholderText("Type in a student name to search") 
        layout.addWidget(self.searchbox)

        # Add a submit button
        search_button=QPushButton("Search") 
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)
        self.setLayout(layout) 

    def search_student(self):  
        searchwild = '%'+ self.searchbox.text()+ '%'
        connection=DataBase().connect()
        cursor=connection.cursor()  
        cursor.execute("SELECT * FROM students WHERE name LIKE %s",(searchwild,))
        rows=cursor.fetchall()
        rows=rows[0][1]
        print(rows) 
        items=main.table.findItems(rows,Qt.MatchFlag.MatchFixedString)
        for item in items:
            main.table.item(item.row(),1).setSelected(True) 
        cursor.close()
        connection.close() 
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Update Student Data") 
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout=QVBoxLayout()  # Arranges elements verically  
        
        # To get the index of the current selection
        self.index=main.table.currentRow()
        # Get id from selected row
        self.student_id=main.table.item(self.index,0).text()
        # Get student name from selected row
        student_name=main.table.item(self.index,1).text()
        self.student_name=QLineEdit(student_name) 
        self.student_name.setPlaceholderText(student_name) # This will show the initial name that was added
        layout.addWidget(self.student_name) 
        # Get course name from selected row
        course_name=main.table.item(self.index,2).text()
        self.course_name=QComboBox() 
        courses=["Biology","Mathematics","Computer Engineering", "System Engineering",
        "Business Adminisration","Music","BioChemistry","Astronomy"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        # Get mobile from selected row
        mobile=main.table.item(self.index,3).text()
        self.mobile=QLineEdit(mobile) 
        self.mobile.setPlaceholderText("Mobile Number") 
        self.mobile.setPlaceholderText(mobile)
        layout.addWidget(self.mobile) 



        # Add a submit button
        button=QPushButton("Update") 
        #button.setFixedSize(100,35) 
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def update_student(self):
        connection=DataBase().connect()
        cursor=connection.cursor() 
        cursor.execute("UPDATE students SET NAME =%s,COURSE=%s, MOBILE=%s WHERE ID = %s",
        (self.student_name.text(),
        self.course_name.itemText(self.course_name.currentIndex())
        ,self.mobile.text(),self.student_id)) 
        connection.commit()
        cursor.close()
        connection.close() 
        self.close()
        # To refresh the table
        main.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Delete Record") 
        #self.setFixedWidth(250)
        #self.setFixedHeight(100)
        layout=QGridLayout()  # Arranges elements horizontally and vertically
        confirmation=QLabel("Are you sure you want to delete this\nstudent data?")
        yes=QPushButton("YES")
        no=QPushButton("NO")
        yes.clicked.connect(self.yes_click)
        no.clicked.connect(self.no_click)
        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1) 
        self.setLayout(layout) 

    def no_click(self):
        self.close()
    def yes_click(self):
        # Getting the index of the data clicked on the table
        index=main.table.currentRow()
        student_id=main.table.item(index,0).text()
        print(student_id)
        connection=DataBase().connect()
        cursor=connection.cursor() 
        cursor.execute("DELETE FROM students WHERE id=%s",(student_id,)) 
        connection.commit()
        cursor.close()
        connection.close() 
        self.close()
        confirmation_msg=QMessageBox()
        confirmation_msg.setWindowTitle("success")
        confirmation_msg.setText("The record was deleted successfully")
        confirmation_msg.exec()
        # To refresh the table

        main.load_data()        
        

app=QApplication(sys.argv)
main=MainWindow()  
sys.exit(app.exec()) 

