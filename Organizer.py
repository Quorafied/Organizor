

''' BEFORE RUNNING THE PROGRAM PLEASE MAKE SURE MYSQL SERVER IS UP '''
''' ALSO MAKE SURE THERE IS A USER REGISTERED IN THE DATABASE FOR YOU TO CONNECT '''

# importing modules that the software will use.

import tkinter as tk # module needed to create the user interface and input boxes.
from tkinter import *
import mysql.connector # module that allows me to connect to the database. 
import sqlite3 # module needed to create/modify/delete databases.


# Connecting to the database (MySQL Server must be active on any unused port).
mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'admin',
        autocommit=True # automatically commit instead of using .commit() every time making the program more efficient.
    )
# mycursor variable is created to execute sql commands (currently connected to the database).
mycursor = mydb.cursor()


# Creating database 'organizer' if it does not already exist.
# We want this because the software first needs to see how many boards the user has
mycursor.execute(
    """CREATE
    DATABASE
    IF NOT EXISTS
    Necro_Organizer"""
    )

# Use database to allow alterations
mycursor.execute(
    """USE Necro_Organizer"""
    )



# Table that describes each user (In our case it may only be one)
mycursor.execute(
    """CREATE
    TABLE
    IF NOT EXISTS
    user
    (
        user_id int NOT NULL AUTO_INCREMENT,
        username varchar(255),
        identity varchar(255),
        PRIMARY KEY(user_id)
    );    
    """
    )


# Table that describes tasks
mycursor.execute(
    """CREATE
    TABLE
    IF NOT EXISTS
    task
    (
    task_id int NOT NULL AUTO_INCREMENT,
    description varchar(255),
    status varchar(255),
    PRIMARY KEY (task_id)
    );
    """
    )

# Table that describes assessments
mycursor.execute(
    """CREATE
    TABLE
    IF NOT EXISTS
    assessment
    (
    student_id int NOT NULL AUTO_INCREMENT,
    name varchar(255),
    topic varchar(255),
    grade varchar(255),
    percentage varchar(255),
    completed varchar(255),
    deadline varchar(255),
    PRIMARY KEY (student_id)
    )
    ;
    """
    )










# Creating a container for windows to stack on top of to switch between windows.
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('780x600')
        self.frames = {}
        # pages' order
        for F in (Main_Page, todo_Page, inprogress_Page, done_Page, teacher_Page, assessment_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main_Page")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Main_Page(tk.Frame):   # The first window the user is prompted when starting the program

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Creating a label at the top that fills up some space
        label = tk.Label(self, text="")
        label.pack(side="top", fill="x", pady=0)

        # Creating a welcome label at the top just after the fill label
        label = tk.Label(self, text="Welcome to your planner")
        label.pack()

        label = tk.Label(self, text="")
        label.pack(side="top", fill="x", pady=5)

        # Creating the widgets
        button1 = tk.Button(self, height=2, width=20, text="To do",
                            command = lambda: controller.show_frame('todo_Page')) 
        button2 = tk.Button(self, height=2, width=20, text="In progress",
                            command = lambda: controller.show_frame('inprogress_Page'))
        button3 = tk.Button(self, height=2, width=20, text="Done",
                            command = lambda: controller.show_frame('done_Page'))
        button4 = tk.Button(self, height=2, width=20, text="Teacher",
                            command = lambda: controller.show_frame('teacher_Page'))

        # Placing the widgets down.
        button1.pack(pady=5)
        button2.pack(pady=5)
        button3.pack(pady=5)
        button4.pack(pady=5)
        
        # TIPS
        label = tk.Label(self, text="")
        label.pack(side="top", fill="x", pady=16)
        
        tips_title = tk.Label(self, text="Legend")
        tips_title.pack()
        
        tip1 = tk.Label(self, text="In any of the 3 pages, you can use the scrollwheel to navigate through the list of tasks")
        tip1.pack()
        




class todo_Page(tk.Frame):    # The window which contains tasks with a status 'todo'.

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller.
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creating a label to state which page is currently shown.
        label = tk.Label(self, text="This is the to do page")
        label.pack(side="top", fill="x", pady=10)

        # Create a button that would change the window to the Main_Page window.
        main_button = tk.Button(self, width=50, text="Go to the main page",
                           command=lambda: controller.show_frame("Main_Page"))
        main_button.pack()

        listbox = Listbox(self)
        listbox.yview() # Make the listbox scrollable via mousewheel.
        listbox.pack(pady=10)



        '''Inserting (loading) data phase.'''
        def insert_data_to_listbox(self, the_listbox):
            list_entries = []
            select_todo_id_description()

            # Create a variable to hold the ids and descriptions for each task which have a 'done' status.
            list_entries = select_todo_id_description()

            # Goes through every sub-list and insert the second value of each sub-list (the description).
            for i in range(len(list_entries)):
                the_listbox.insert(i, list_entries[i][1])

        insert_data_to_listbox(self, listbox)


        '''Functions to be used in buttons (Remove, Get and Add buttons)'''

        # Function to get selected item (to allow deletion of the item in the database not just the listbox) and printing item in console for debugging.
        def select_and_print(self, the_listbox): # the_listbox is used as a parameter to enter the name of the widget (listbox) outside.
            selection = the_listbox.get(tk.ACTIVE)
            print(selection)       
            return selection

        # Function to get selected item in the listbox and put it into a variable 'to_delete' which is used to delete the value in the listbox and database
        def delete_selected_item(self, the_listbox):
            to_delete = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)
            print(to_delete)

            mycursor.execute('DELETE FROM task WHERE description=%s', (to_delete, ))



        # Function to retrieve data in an entry widget and destroy both the entry and submit button widgets. USED IN add_an_item(self, the_listbox)
        def retrieve_and_insert(self, entry1, submit_button, the_listbox):
            retrieved_data = entry1.get()
            print(retrieved_data)

            entry1.destroy()
            submit_button.destroy()

            the_listbox.insert(END, retrieved_data)

            mycursor.execute("INSERT INTO task (description, status) VALUES (%s, 'todo')", (retrieved_data, ))

            return retrieved_data


        # Function to create an entry box to enter a description, a button to get data input and insert into database.
        def add_an_item(self, the_listbox):
            entry1 = Entry(self)
            entry1.pack(pady=10)

            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: retrieve_and_insert(self, entry1, submit_button, listbox))
            submit_button.pack()





        # Function to retrieve relative data to remove description from listbox, insert new description and update the database.
        def modify_selected_item(self, the_listbox):
            # Return description of the selected task.
            old_description = select_and_print(self, the_listbox)   #SELECTED DESCRIPTION
            print(old_description)

            # Return the index of the selected task.
            index = the_listbox.curselection()   #INDEX OF SELECTED TASK
            print(index)


            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_description = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_description)

                the_listbox.insert(index, new_description)

                modify_entry.destroy()
                submit_button.destroy()

                return new_description

            def remove_old_data(self, the_listbox):
                the_listbox.delete(tk.ANCHOR)    #DELETE SELECTED DESCRIPTION

            def update_task(self, new_description, old_description):
                mycursor.execute("UPDATE task SET description=%s WHERE description=%s", (new_description, old_description, ))
                
            
                
            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(
                self,
                text='Submit',
                command=lambda: [
                    remove_old_data(self, listbox),
                    update_task(self,
                                retrieve_data_entry(self, modify_entry, submit_button, the_listbox), old_description
                                )
                                 ]
                                      )
            submit_button.pack(pady=5)


        # Function to move a task form one status to another by getting selected task, removing from current listbox and updating the status
        def move_selected_item(self, the_listbox): # Take selected description, remove from listbox, update
            selected = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)



            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_status = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_status)

                modify_entry.destroy()
                submit_button.destroy()

                return new_status

            def update_status(self, new_status, selected):
                mycursor.execute("Update task SET status=%s WHERE description=%s", (new_status, selected, ))



            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: update_status(self, retrieve_data_entry(self, modify_entry, submit_button, listbox), selected))
            submit_button.pack(pady=5)


        # Function to delete all the tasks in the listbox and then re-inserting the data
        def refresh_tasks(self, the_listbox):
            the_listbox.delete(0,'end')

            insert_data_to_listbox(self, listbox)
            
                
                



    
            
            
        '''Remove, Get, Add and Move buttons'''
         
        button1 = tk.Button(self, text="Remove item",
                            command=lambda: delete_selected_item(self, listbox))
        button1.pack(pady=3)

        button2 = tk.Button(self, text="Add item",
                            command=lambda: add_an_item(self, listbox))
        button2.pack(pady=3)

        button3 = tk.Button(self, text="Modify task",
                            command=lambda: modify_selected_item(self, listbox))
        button3.pack(pady=3)

        button4 = tk.Button(self, text='Move task',
                            command=lambda: move_selected_item(self, listbox))
        button4.pack(pady=3)

        button5 = tk.Button(self, text='Refresh tasks',
                           command=lambda: refresh_tasks(self, listbox))
        button5.pack(pady=3)
        


        
        
        


class inprogress_Page(tk.Frame):

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller.
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creating a label to state which page is currently shown.
        label = tk.Label(self, text="This is the in progress page")
        label.pack(side="top", fill="x", pady=10)

        # Create a button that would change the window to the Main_Page window.
        main_button = tk.Button(self, width=50, text="Go to the main page",
                           command=lambda: controller.show_frame("Main_Page"))
        main_button.pack()

        listbox = Listbox(self)
        listbox.yview() # Make the listbox scrollable via mousewheel.
        listbox.pack(pady=10)



        '''Inserting (loading) data phase.'''
        def insert_data_to_listbox(self, the_listbox):
            list_entries = []
            select_inprogress_id_description()

            # Create a variable to hold the ids and descriptions for each task which have a 'done' status.
            list_entries = select_inprogress_id_description()

            # Goes through every sub-list and insert the second value of each sub-list (the description).
            for i in range(len(list_entries)):
                the_listbox.insert(i, list_entries[i][1])

        insert_data_to_listbox(self, listbox)


        '''Functions to be used in buttons (Remove, Get and Add buttons)'''

        # Function to get selected item (to allow deletion of the item in the database not just the listbox) and printing item in console for debugging.
        def select_and_print(self, the_listbox): # the_listbox is used as a parameter to enter the name of the widget (listbox) outside.
            selection = the_listbox.get(tk.ACTIVE)
            print(selection)       
            return selection

        # Function to get selected item in the listbox and put it into a variable 'to_delete' which is used to delete the value in the listbox and database
        def delete_selected_item(self, the_listbox):
            to_delete = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)
            print(to_delete)

            mycursor.execute('DELETE FROM task WHERE description=%s', (to_delete, ))



        # Function to retrieve data in an entry widget and destroy both the entry and submit button widgets. USED IN add_an_item(self, the_listbox)
        def retrieve_and_insert(self, entry1, submit_button, the_listbox):
            retrieved_data = entry1.get()
            print(retrieved_data)

            entry1.destroy()
            submit_button.destroy()

            the_listbox.insert(END, retrieved_data)

            mycursor.execute("INSERT INTO task (description, status) VALUES (%s, 'inprogress')", (retrieved_data, ))

            return retrieved_data


        # Function to create an entry box to enter a description, a button to get data input and insert into database.
        def add_an_item(self, the_listbox):
            entry1 = Entry(self)
            entry1.pack(pady=10)

            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: retrieve_and_insert(self, entry1, submit_button, listbox))
            submit_button.pack()





        # Function to retrieve relative data to remove description from listbox, insert new description and update the database.
        def modify_selected_item(self, the_listbox):
            # Return description of the selected task.
            old_description = select_and_print(self, the_listbox)   #SELECTED DESCRIPTION
            print(old_description)

            # Return the index of the selected task.
            index = the_listbox.curselection()   #INDEX OF SELECTED TASK
            print(index)


            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_description = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_description)

                the_listbox.insert(index, new_description)

                modify_entry.destroy()
                submit_button.destroy()

                return new_description

            def remove_old_data(self, the_listbox):
                the_listbox.delete(tk.ANCHOR)    #DELETE SELECTED DESCRIPTION

            def update_task(self, new_description, old_description):
                mycursor.execute("UPDATE task SET description=%s WHERE description=%s", (new_description, old_description, ))
                
            
                
            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(
                self,
                text='Submit',
                command=lambda: [
                    remove_old_data(self, listbox),
                    update_task(self,
                                retrieve_data_entry(self, modify_entry, submit_button, the_listbox), old_description)
                                 ]
                                      )
            submit_button.pack(pady=5)

        # Function to move a task form one status to another by getting selected task, removing from current listbox and updating the status
        def move_selected_item(self, the_listbox): # Take selected description, remove from listbox, update
            selected = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)



            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_status = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_status)

                modify_entry.destroy()
                submit_button.destroy()

                return new_status

            def update_status(self, new_status, selected):
                mycursor.execute("Update task SET status=%s WHERE description=%s", (new_status, selected, ))



            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: update_status(self, retrieve_data_entry(self, modify_entry, submit_button, listbox), selected))
            submit_button.pack(pady=5)


        # Function to delete all the tasks in the listbox and then re-inserting the data
        def refresh_tasks(self, the_listbox):
            the_listbox.delete(0,'end')

            insert_data_to_listbox(self, listbox)
            
                
                



    
            
            
        '''Remove, Get, Add and Move buttons'''
         
        button1 = tk.Button(self, text="Remove item",
                            command=lambda: delete_selected_item(self, listbox))
        button1.pack(pady=3)

        button2 = tk.Button(self, text="Add item",
                            command=lambda: add_an_item(self, listbox))
        button2.pack(pady=3)

        button3 = tk.Button(self, text="Modify task",
                            command=lambda: modify_selected_item(self, listbox))
        button3.pack(pady=3)

        button4 = tk.Button(self, text='Move task',
                            command=lambda: move_selected_item(self, listbox))
        button4.pack(pady=3)

        button5 = tk.Button(self, text='Refresh tasks',
                           command=lambda: refresh_tasks(self, listbox))
        button5.pack(pady=3)




        

class done_Page(tk.Frame):

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller.
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creating a label to state which page is currently shown.
        label = tk.Label(self, text="This is the done page")
        label.pack(side="top", fill="x", pady=10)

        # Create a button that would change the window to the Main_Page window.
        main_button = tk.Button(self, width=50, text="Go to the main page",
                           command=lambda: controller.show_frame("Main_Page"))
        main_button.pack()

        listbox = Listbox(self)
        listbox.yview() # Make the listbox scrollable via mousewheel.
        listbox.pack(pady=10)



        '''Inserting (loading) data phase.'''
        def insert_data_to_listbox(self, the_listbox):
            list_entries = []
            select_done_id_description()

            # Create a variable to hold the ids and descriptions for each task which have a 'done' status.
            list_entries = select_done_id_description()

            # Goes through every sub-list and insert the second value of each sub-list (the description).
            for i in range(len(list_entries)):
                the_listbox.insert(i, list_entries[i][1])

        insert_data_to_listbox(self, listbox)


        '''Functions to be used in buttons (Remove, Get and Add buttons)'''

        # Function to get selected item (to allow deletion of the item in the database not just the listbox) and printing item in console for debugging.
        def select_and_print(self, the_listbox): # the_listbox is used as a parameter to enter the name of the widget (listbox) outside.
            selection = the_listbox.get(tk.ACTIVE)
            print(selection)       
            return selection

        # Function to get selected item in the listbox and put it into a variable 'to_delete' which is used to delete the value in the listbox and database
        def delete_selected_item(self, the_listbox):
            to_delete = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)
            print(to_delete)

            mycursor.execute('DELETE FROM task WHERE description=%s', (to_delete, ))



        # Function to retrieve data in an entry widget and destroy both the entry and submit button widgets. USED IN add_an_item(self, the_listbox)
        def retrieve_and_insert(self, entry1, submit_button, the_listbox):
            retrieved_data = entry1.get()
            print(retrieved_data)

            entry1.destroy()
            submit_button.destroy()

            the_listbox.insert(END, retrieved_data)

            mycursor.execute("INSERT INTO task (description, status) VALUES (%s, 'done')", (retrieved_data, ))

            return retrieved_data


        # Function to create an entry box to enter a description, a button to get data input and insert into database.
        def add_an_item(self, the_listbox):
            entry1 = Entry(self)
            entry1.pack(pady=10)

            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: retrieve_and_insert(self, entry1, submit_button, listbox))
            submit_button.pack()





        # Function to retrieve relative data to remove description from listbox, insert new description and update the database.
        def modify_selected_item(self, the_listbox):
            # Return description of the selected task.
            old_description = select_and_print(self, the_listbox)   #SELECTED DESCRIPTION
            print(old_description)

            # Return the index of the selected task.
            index = the_listbox.curselection()   #INDEX OF SELECTED TASK
            print(index)


            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_description = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_description)

                the_listbox.insert(index, new_description)

                modify_entry.destroy()
                submit_button.destroy()

                return new_description

            def remove_old_data(self, the_listbox):
                the_listbox.delete(tk.ANCHOR)    #DELETE SELECTED DESCRIPTION

            def update_task(self, new_description, old_description):
                mycursor.execute("UPDATE task SET description=%s WHERE description=%s", (new_description, old_description, ))
                
            
                
            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(
                self, text='Submit',
                command=lambda: [
                    remove_old_data(self, listbox),
                    update_task(self, retrieve_data_entry(self, modify_entry, submit_button, the_listbox), old_description)
                                 ]
                                      )
            submit_button.pack(pady=5)

        # Function to move a task form one status to another by getting selected task, removing from current listbox and updating the status
        def move_selected_item(self, the_listbox): # Take selected description, remove from listbox, update
            selected = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)



            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_status = modify_entry.get()    #NEW DESCRIPTION FROM INPUT BOX
                print(new_status)

                modify_entry.destroy()
                submit_button.destroy()

                return new_status

            def update_status(self, new_status, selected):
                mycursor.execute("Update task SET status=%s WHERE description=%s", (new_status, selected, ))



            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: update_status(self, retrieve_data_entry(self, modify_entry, submit_button, listbox), selected))
            submit_button.pack(pady=5)


        # Function to delete all the tasks in the listbox and then re-inserting the data
        def refresh_tasks(self, the_listbox):
            the_listbox.delete(0,'end')

            insert_data_to_listbox(self, listbox)

    
            
                
        '''Remove, Get and Add item buttons'''
         
        button1 = tk.Button(self, text="Remove item",
                            command=lambda: delete_selected_item(self, listbox))
        button1.pack(pady=3)

        button2 = tk.Button(self, text="Add item",
                            command=lambda: add_an_item(self, listbox))
        button2.pack(pady=3)

        button3 = tk.Button(self, text="Modify task",
                            command=lambda: modify_selected_item(self, listbox))
        button3.pack(pady=3)

        button4 = tk.Button(self, text='Move task',
                            command=lambda: move_selected_item(self, listbox))
        button4.pack(pady=3)

        button5 = tk.Button(self, text='Refresh tasks',
                           command=lambda: refresh_tasks(self, listbox))
        button5.pack(pady=3)       


class teacher_Page(tk.Frame):    # Windows for educational purposes.

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller.
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creating a label to state which page is currently shown.
        label = tk.Label(self, text="Teacher page")
        label.pack(side="top", fill="x", pady=10)

        # Create a button that would change the window to the Main_Page window.
        main_button = tk.Button(self, width=50, text="Go to the main page",
                           command=lambda: controller.show_frame("Main_Page"))
        main_button.pack()

        button1 = tk.Button(self, width=15, height=3, text="Assessments",
                            command= lambda: controller.show_frame("assessment_Page"))
        button1.pack(pady=20)

class assessment_Page(tk.Frame):

    def __init__(self, parent, controller):
        # Defining the Main_Page 's parent and controller.
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creating a label to state which page is currently shown.
        label = tk.Label(self, text="Assessment page")
        label.pack(side="top", fill="x", pady=10)

        back_button = tk.Button(self, width=50, text="Go to the teacher page",
                           command=lambda: controller.show_frame("teacher_Page"))
        back_button.pack()

        listbox = Listbox(self, width=50)
        listbox.yview() # Make the listbox scrollable via mousewheel.
        listbox.pack(pady=10)

        for i in range(len(select_assessment())):
            listbox.insert(i, select_assessment()[i])





            '''FUNCTIONS'''
            
        # Function to get selected item (to allow deletion of the item in the database not just the listbox) and printing item in console for debugging.
        def select_and_print(self, the_listbox): # the_listbox is used as a parameter to enter the name of the widget (listbox) outside.
            selection = the_listbox.get(tk.ACTIVE)
            print(selection)       
            return selection




        def delete_selected_item(self, the_listbox):
            to_delete = select_and_print(self, listbox)
            the_listbox.delete(tk.ANCHOR)
            print(to_delete)

            mycursor.execute('DELETE FROM assessment WHERE student_id=%s', (to_delete[0], ))




        # Function to retrieve data in an entry widget and destroy both the entry and submit button widgets. USED IN add_assessment
        def retrieve_and_insert(self, entry1, submit_button, the_listbox):
            retrieved_data = entry1.get()
            split_retrieved_data = retrieved_data.split()
            
            
            entry1.destroy()
            submit_button.destroy()

            the_listbox.insert(END, retrieved_data)  # Insert the data into the listbox

            mycursor.execute("""INSERT INTO assessment(name, topic, grade, percentage, completed) VALUES(%s, %s, %s, %s, %s)""", (split_retrieved_data[0], split_retrieved_data[1], split_retrieved_data[2], split_retrieved_data[3], split_retrieved_data[4], ))

            return retrieved_data






        # Function to create an entry box to enter a description, a button to get data input and insert into database.
        def add_assessment(self, the_listbox):
            entry1 = Entry(self)
            entry1.pack(pady=10)

            submit_button = tk.Button(
                self,
                text='Submit',
                command=lambda: retrieve_and_insert(
                                    self,
                                    entry1,
                                    submit_button,
                                    listbox
                                    )
                                )
            
            submit_button.pack()







        # Function to retrieve relative data to remove description from listbox, insert new description and update the database.
        def modify_selected_assessment(self, the_listbox):
            # Return description of the selected task.
            old_assessment = select_and_print(self, the_listbox)   #SELECTED DESCRIPTION
            print(old_assessment)

            # Return the index of the selected task.
            index = the_listbox.curselection()   #INDEX OF SELECTED TASK
            print(index)


            def retrieve_data_entry(self, modify_entry, submit_button, the_listbox):
                new_assessment = modify_entry.get()    # NEW ASSESSMENT FROM INPUT BOX

                the_listbox.insert(index, new_assessment)

                modify_entry.destroy()
                submit_button.destroy()

                return new_assessment

            def remove_old_data(self, the_listbox):
                the_listbox.delete(tk.ANCHOR)    # DELETE SELECTED ASSESSMENT

            def update_assessment(self, new_assessment, old_assessment):
                new_assessment = new_assessment.split()
                print(new_assessment)

                old_assessment = old_assessment
                print(old_assessment)

                
                    # Create variables for database insertion
                student_id = old_assessment[0]
                name = new_assessment[0]
                print(name)
                topic = new_assessment[1]
                grade = new_assessment[2]
                percentage = new_assessment[3]
                completed = new_assessment[4]
                deadline = new_assessment[5]
                
                mycursor.execute(
                                """
                                Update assessment SET name=%s, topic=%s, grade=%s, percentage=%s, completed=%s, deadline=%s WHERE student_id=%s
                                """,
                                 (name, topic, grade, percentage, completed, deadline, student_id, )
                                 )

                    
            
            modify_entry = Entry(self)    #INPUT BOX
            modify_entry.pack(pady=10)

               #SUBMIT BUTTON
            submit_button = tk.Button(self, text='Submit',
                                      command=lambda: [
                                          remove_old_data(self, listbox),
                                          update_assessment(self, retrieve_data_entry(self, modify_entry, submit_button, listbox), old_assessment),
                                          show_horizontal_buttons(self)                                          
                                          ]
                                      )
            submit_button.pack(pady=5)



        """ SORTING FUNCTIONS """

        def sortby_name(self, the_listbox):
            the_listbox.delete(0,'end')

            for i in range(len(select_assessment_sortby_name())-1):
                listbox.insert(i, select_assessment_sortby_name()[i])

        def sortby_topic(self, the_listbox):
            the_listbox.delete(0,'end')

            for i in range(len(select_assessment_sortby_topic())-1):
                listbox.insert(i, select_assessment_sortby_topic()[i])

        def sortby_grade(self, the_listbox):
            the_listbox.delete(0,'end')

            for i in range(len(select_assessment_sortby_grade())-1):
                listbox.insert(i, select_assessment_sortby_grade()[i])

        def sortby_percentage(self, the_listbox):
            the_listbox.delete(0,'end')

            for i in range(len(select_assessment_sortby_percentage())-1):
                listbox.insert(i, select_assessment_sortby_percentage()[i])

        def sortby_completed(self, the_listbox):
            the_listbox.delete(0,'end')

            for i in range(len(select_assessment_sortby_completed())-1):
                listbox.insert(i, select_assessment_sortby_completed()[i])



        """ VISIBILITY TOGGLE OF HORIZONTAL BUTTONS FUNCTIONS """

        def show_horizontal_buttons(self):
            button1.pack(padx=10, side='left')            
            button2.pack(side='left')            
            button3.pack(side='left')
            button4.pack(side='left')
            button5.pack(side='left')

        def hide_horizontal_buttons(self):
            button1.pack_forget()
            button2.pack_forget()
            button3.pack_forget()
            button4.pack_forget()
            button5.pack_forget()
            



            """ Remove, add and modify buttons for assessments """

        remove_button = tk.Button(self, width=25, height=2, text="Remove selected assessment",
                                  command= lambda: delete_selected_item(self, listbox)
                                  )
        remove_button.pack(pady=5)

        add_button = tk.Button(self, width=25, height=2, text="Add an assessment",
                               command= lambda: [hide_horizontal_buttons(self), add_assessment(self, listbox), show_horizontal_buttons(self)])
        add_button.pack(pady=2)

        modify_button = tk.Button(self, width=25, height=2, text="Modify selected assessment",
                                  command= lambda: [
                                      hide_horizontal_buttons(self),
                                      modify_selected_assessment(self, listbox),
                                      show_horizontal_buttons(self)
                                      ]
                                  )
        modify_button.pack(pady=2)



        """ Define assessment functions locally in the assessment page class """
        button1 = tk.Button(self, width=20, height=2, text="Sort by name",
                                command= lambda: sortby_name(self, listbox))
        button2 = tk.Button(self, width=20, height=2, text="Sort by topic",
                                command= lambda: sortby_topic(self, listbox))
        button3 = tk.Button(self, width=20, height=2, text="Sort by grade",
                                command= lambda: sortby_grade(self, listbox))
        button4 = tk.Button(self, width=20, height=2, text="Sort by percentage",
                                command= lambda: sortby_percentage(self, listbox))
        button5 = tk.Button(self, width=20, height=2, text="Sort by completed",
                                command= lambda: sortby_completed(self, listbox))


        """ The page starts with horizontal buttons visible """
        show_horizontal_buttons(self)

            



                    
            



""" SELECTION FUNCTIONS AND SORTING FUNCTIONS """        


def select_assessment():
    mycursor.execute("""SELECT * FROM assessment""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched


def select_assessment_sortby_name():
    mycursor.execute("""SELECT * FROM assessment ORDER BY name""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched

def select_assessment_sortby_topic():
    mycursor.execute("""SELECT * FROM assessment ORDER BY topic""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched

def select_assessment_sortby_grade():
    mycursor.execute("""SELECT * FROM assessment ORDER BY grade""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched

def select_assessment_sortby_percentage():
    mycursor.execute("""SELECT * FROM assessment ORDER BY percentage""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)
    
    return data_fetched

def select_assessment_sortby_completed():
    mycursor.execute("""SELECT * FROM assessment ORDER BY completed""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched







""" FUNCTIONS TO SELECT FROM DATABASE (todo, inprogress, done) """

def select_todo_id_description():
    mycursor.execute("""SELECT task_id, description FROM task WHERE status='todo';""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)
    
    return data_fetched

def select_inprogress_id_description():
    mycursor.execute("""SELECT task_id, description FROM task WHERE status='inprogress';""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched

def select_done_id_description():
    mycursor.execute("""SELECT task_id, description FROM task WHERE status='done';""")
    data_fetched = mycursor.fetchall()
    print(data_fetched)

    return data_fetched









#premadeboard()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
        















# SELECT COUNT(BoardID) FROM student_board where UserID = 1;


root = Tk()

root.mainloop()


mycursor.close()



