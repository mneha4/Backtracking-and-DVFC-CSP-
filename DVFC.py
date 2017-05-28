#	
#	Author - Neha M (B14113)
#	Course - CS592
#	Algorithm - Dynamic variable forward checking


import json
from Tkinter import *
import sys
import collections
import Tkinter as tk
import random
import time


def dynamic_var(domain, variables_filled):
	n = len(domain)
	Max = sys.maxint
	index = -2
	for i in range (0,n):
		if i not in variables_filled:
			if len(domain[i]) < Max:
				index = i
				Max = len(domain[i])
	
	return index			

# i is Xi+1, value is for ith variable
def forward_check(assignment,i,value, variables_filled, domain):
	
	assignment_new = assignment[:]
	assignment_new[i] = value
	variables_filled_new = variables_filled[:]
	variables_filled_new.append(i)
	n = len(domain)
	domain_ = domain[:]
	for k in range (0,n):
		if k not in variables_filled_new:
			for d in domain_[k]:
				if consistent(assignment_new,k,d,variables_filled_new)==0:
					domain_[k].remove(d)
					m = data["variables"][k]["domain"][:].index(str(d))
					time.sleep(0.5)
					cv.itemconfig(items[k][m],fill='red')			
					time.sleep(1)
					cv.update()	
			if len(domain_[k]) == 0:
				m = len(data["variables"][k]["domain"][:])
				time.sleep(0.5)
				for m_ in range (0,m):
					cv.itemconfig(items[k][m_],fill='red')			
					time.sleep(1)
				cv.update()					
				return 0

	domain = domain_[:]
	return 1
	# print domain		
			


# i is Xi+1
def consistent(assignment,i,value,variables_filled):
	if len(variables_filled) != 0 :
		var_name = var_name = "X" + str(i+1)

		for k in data["constraints"]:
			if var_name in k["scope"]:
				index_v = k["scope"].index(var_name)
				count_p = 0

				for parent in variables_filled:	
					var_name_parent = "X" + str(parent+1)
					
					if var_name_parent in k["scope"]:
						count_p = count_p + 1
						count = 0

						Index_p = k["scope"].index(var_name_parent)	
						
						for rel in k["relation"]:
							z = variables_filled.index(parent)
							if assignment[parent] == rel[Index_p] and rel[index_v] == value:
								count = 1
						
						if count == 0 :
							return 0							

				if count_p > 0 and count == 0:
					return 0	
		return 1
	else:
		return 1


def select_value(assignment, i, domain, variables_filled):
	D_ = domain[i]
	# print i,D_
	while (len(D_)!=0):
		value = D_[0]
		D_.remove(value)
		m = data["variables"][i]["domain"][:].index(str(value))
		time.sleep(0.5)
		cv.itemconfig(items[i][m],fill='cyan')			
		cv.update()
		if(consistent(assignment,i,value, variables_filled)==1):
			if(forward_check(assignment,i,value, variables_filled, domain)==1):
				return value
			else:
				m = data["variables"][i]["domain"][:].index(str(value))
				time.sleep(0.5)
				cv.itemconfig(items[i][m],fill='orange')			
				time.sleep(1)
				cv.update()
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

#----------------------
items = []
root = Tk()
root.title("Backtracking Algorithm Animation")
w = 2000
h = 2000
cv = Canvas(width=w, height=h, bg='burlywood1')
cv.create_text(900,55,fill="darkblue",font="Times 26 bold", text="Solving CSP using DVFC")
cv.create_text(1600,200,fill="cyan",font="Times 16 bold", text="Cyan - Current partial solution")
cv.create_text(1600,230,fill="darkorange2",font="Times 16 bold", text="Orange - Past values tried")
cv.create_text(1600,260,fill="white",font="Times 16 bold", text="White - future values in past and future variables")
cv.create_text(1600,290,fill="black",font="Times 16 bold", text="Black - Deadend")
cv.create_text(1600,320,fill="red",font="Times 16 bold", text="Red - Future values deleted")


x = 100
y = 200
for i in range (0,n):
	cv.create_text(x,y,fill="darkblue",font="Times 26 bold", text=data["variables"][i]["name"][:])
	x1 = x
	y1 = y
	item = []	
	for d in data["variables"][i]["domain"]:		
		item.append(cv.create_oval(x1+100,y1-30,x1+170,y1+40,fill='white',tags = i))
		cv.create_text(x1+135,y1+5,fill="darkblue",font="Times 20 bold", text=d)
		x1 = x1 + 100
	y = y + 100
	items.append(item)
cv.pack()
cv.update()

def DVFC():
	variables_filled = []
	i = dynamic_var(domain,variables_filled)
	# i is Xi+1
	while -1 < i < n:
		value = select_value(assignment, i, domain, variables_filled)
		print value
		if value == None:
			time.sleep(0.5) 
			m = len(data["variables"][i]["domain"])
			for m_ in range(0,m): 
				cv.itemconfig(items[i][m_],fill='white')			
				cv.update()
				time.sleep(1)

			i = variables_filled[-1]
			if i != -1 :
				a = assignment[i]
				print a
				m = data["variables"][i]["domain"].index(a)
				for m_ in range(0,m+1):
					cv.itemconfig(items[i][m_],fill='orange')
					cv.update()
					time.sleep(1)


			if i in variables_filled:
				variables_filled.remove(i)

			## reset domains of parents	
			for k in range (i+1,n):
				domain[k] = (data["variables"][k]["domain"][:])
			if len(variables_filled) == 0:
				i = -1	
		else:
			m = data["variables"][i]["domain"][:].index(str(value))
			time.sleep(1) 
			cv.itemconfig(items[i][m],fill='cyan')			
			time.sleep(1) 
			cv.update()
			assignment[i] = value
			variables_filled.append(i)
			i = dynamic_var(domain, variables_filled)
			if i<n :
				pass
				
	if (i == -1):
		cv.create_text(1000,700,fill="darkblue",font="Times 26 bold", text="No solution")	

	else:
		print assignment
		print variables_filled



DVFC()
root.mainloop()		