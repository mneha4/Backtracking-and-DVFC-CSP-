#	
#	Author - Neha M (B14113)
#	Course - CS592
#	Algorithm - Backtracking


import json
import time
import sys
import collections
from Tkinter import *
import random


# i is Xi+1
def consistent(assignment,i,value,variables_filled):
	if len(variables_filled) != 0 :
		var_name = var_name = "X" + str(i+1)

		count_scope = 0
		for k in data["constraints"]:
			
			if var_name in k["scope"]:
				# count_scope = count_scope + 1
				index_v = k["scope"].index(var_name)
				count_p = 0

				for parent in variables_filled:	
					var_name_parent = "X" + str(parent+1)
					
					if var_name_parent in k["scope"]:
						count_p = count_p + 1
						count = 0

						Index_p = k["scope"].index(var_name_parent)	
						
						for rel in k["relation"]:
							z = order_.index(str(parent+1))
							if assignment[z] == rel[Index_p] and rel[index_v] == value:
								count = 1						
						if count == 0 :
							return 0							
				if count_p > 0 and count == 0:
					return 0
		# if count_scope == 0:
		# 	return 0				
		return 1
	else:
		return 1


def select_value(assignment, i, domain, variables_filled):
	D_ = domain[i]
	while (len(D_)!=0):
		value = D_[0]
		D_.remove(value)
		m = data["variables"][i]["domain"][:].index(str(value))
		time.sleep(0.5)
		cv.itemconfig(items[i][m],fill='cyan')			
		cv.update()
		if(consistent(assignment,i,value, variables_filled)==1):
				return value
		else:
			m = data["variables"][i]["domain"][:].index(str(value))
			time.sleep(0.5)
			cv.itemconfig(items[i][m],fill='orange')			
			time.sleep(1)
			cv.update()

	return None	

#-----------------------

with open('input.json') as data_file:    
    data = json.load(data_file)

assignment = []

n = len(data["variables"])
domain = []
for j in range(0,n):
	domain.append(data["variables"][j]["domain"][:])
	assignment.append(1)

order = data["ordering"]
order_ = []
for i in order:
	order_.append(i[1])

string = ""
for i in range (0,len(order_)):
	string = string +"X"+str(i+1)+", "

string = string[0:-1]
string = string[0:-1]

# def create_graphics(assignment):
items = []
root = Tk()
root.title("Backtracking Algorithm Animation")
w = 2000
h = 2000
cv = Canvas(width=w, height=h, bg='burlywood1')
cv.create_text(900,55,fill="darkblue",font="Times 26 bold", text="Solving CSP using backtracking")
cv.create_text(900,105,fill="darkblue",font="Times 26 bold", text="Order - " + str(string))
cv.create_text(1600,200,fill="cyan",font="Times 16 bold", text="Cyan - Current partial solution")
cv.create_text(1600,230,fill="darkorange2",font="Times 16 bold", text="Orange - Past values tried")
cv.create_text(1600,260,fill="white",font="Times 16 bold", text="White - future values in past and future variables")
# cv.create_text(1600,290,fill="black",font="Times 16 bold", text="Black - Deadend")
x = 100
y = 200
for i in range (0,n):
	cv.create_text(x,y,fill="darkblue",font="Times 26 bold", text=data["variables"][i]["name"][:])
	x1 = x
	y1 = y
	item = []	
	for d in data["variables"][i]["domain"]:
		if assignment != [] and assignment[order_.index(str(i+1))] == str(d):
			item.append(cv.create_oval(x1+100,y1-30,x1+170,y1+40,fill='cyan',tags = i))
			cv.create_text(x1+135,y1+5,fill="darkblue",font="Times 20 bold", text=d)
		else:		
			item.append(cv.create_oval(x1+100,y1-30,x1+170,y1+40,fill='white',tags = i))
			cv.create_text(x1+135,y1+5,fill="darkblue",font="Times 20 bold", text=d)
		x1 = x1 + 100
	y = y + 100
	items.append(item)
cv.pack()
cv.update()


def backtrack():
	i = 0
	variables_filled = []
	while -1 < i < n:
		# print i
		j = int(order_[i]) - 1
		value = select_value(assignment, j, domain, variables_filled)
		print value
		if value == None:
			time.sleep(0.5) 
			m = len(data["variables"][j]["domain"])
			for m_ in range(0,m): 
				cv.itemconfig(items[j][m_],fill='white')			
				cv.update()
				time.sleep(1) 

			i = i - 1
			j = int(order_[i]) - 1
			if i != -1 :
				a = assignment[i]
				print a
				m = data["variables"][j]["domain"].index(a)
				for m_ in range(0,m+1):
					cv.itemconfig(items[j][m_],fill='orange')
					cv.update()
					# time.sleep(1)

			if j in variables_filled:
				variables_filled.remove(j)


		else:
			print j
			m = data["variables"][j]["domain"][:].index(str(value))
			time.sleep(1) 
			cv.itemconfig(items[j][m],fill='cyan')			
			time.sleep(1) 
			cv.update()
			assignment[i] = value
			variables_filled.append(j)
			i = i + 1

			if i<n:
				j = int(order_[i]) - 1
				domain[j] = data["variables"][j]["domain"][:]
				
	if (i == -1):
		cv.create_text(1000,700,fill="darkblue",font="Times 26 bold", text="No solution")

	else:
		pass

backtrack()
root.mainloop()