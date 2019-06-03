'''
Names: Anan and Jack
Date: 02/24/19 (Got an extension)
Description: CRH Library Fighter - A Street Fighter style game that uses our classmates and friends as characters in the setting of the CRH library

Sources:
We referred to the following websites:
https://www.pygame.org/docs/ref/display.html
https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
https://stackoverflow.com/questions/14087609/smooth-keyboard-movement-in-pygame
https://online.photoscissors.com/
https://www.youtube.com/watch?v=i6xMBig-pP4
https://t2.rbxcdn.com/746fd80fc564330e468323d9a63df215
https://www.youtube.com/watch?v=1aGuhUFwvXA
https://onlinepngtools.com/convert-jpg-to-png
https://purepng.com/public/uploads/large/51507139889hp64fmfyew7ypzxnemuliryqbawgpltdn4s6dl9v6v7ops1sf7zderu2lpncogaq3svnipdmxulfj28s7kfzj3tnqxfnldpxtz4l.png
https://stackoverflow.com/questions/10077644/python-display-text-with-font-color

Honor Pledge: On our honor, we have neither given nor received unauthorized aid. Anan Aramthanapon, Jackson Fiala
'''

import pygame, sys, time
from pygame.locals import *
import tkinter



global exit
global winner

#Fighter class - makes it easier to refer to player attributes
class Fighter:
	def __init__(self,name, jump, speed, health):
		self.name = str(name)
		self.n = Move(name+"LN.png") # Neutral
		self.r = Move(name+"LR.png") # Running
		self.d = Move(name+"LD.png") # Duck
		self.b = Move(name+"LB.png") # Block
		self.j = Move(name+"LJ.png") # Jump
		self.p = Move(name+"LP.png") # Punch
		self.k = Move(name+"LK.png") # Kick
		self.s = Move(name+"LS.png") # Special
		self.jump_height = int(jump)
		self.speed = int(speed)
		self.totalhealth = health
		self.health = health
		self.stamina = 300


#moves class - makes it easier to refer to certain pictures, etc.
class Move:
	def __init__(self, sprite):
		self.sprite = pygame.image.load(sprite) # png file
		self.hitbox = 0 # These values get set later
		self.shift = 0
		self.dmg = 0
		self.stam = 0

	def printer(self, player): # Prints character onto the screen
		offset = 0 # Offset increases with each hit/hurtbox on one sprite
		if left_facing_list[player]: # If player is facing left
			tempshift = player_position[player][0]-self.shift # Shift a certain amount depending on how wide that sprite is
			'''
			for i in range(len(self.hitbox)): # Draw hitboxes
				x = i + 1
				if self.hitbox[-x][0] == 0:
					color = (0,255,0)
				else:
					color = (255,0,0)
				pygame.draw.rect(screen, color, [offset+tempshift,self.hitbox[-x][1]+player_position[player][1],self.hitbox[-x][2],self.hitbox[-x][3]])
				offset += self.hitbox[-x][2]
			'''
			screen.blit(self.sprite, (tempshift,player_position[player][1])) # Display image
		else: # If player is facing right
			'''
			for i in range(len(self.hitbox)): # Draw hitboxes
				if self.hitbox[i][0] == 0:
					color = (0,255,0)
				else:
					color = (255,0,0)
				pygame.draw.rect(screen, color, [offset+player_position[player][0],self.hitbox[i][1]+player_position[player][1],self.hitbox[i][2],self.hitbox[i][3]])
				offset += self.hitbox[i][2]
			'''
			flip = pygame.transform.flip(self.sprite, True, False) # Flip image
			screen.blit(flip, (player_position[player][0],player_position[player][1])) # Display image

def genbox1(p1move, p2move):
	offset = 0
	if left_facing_list[0]: # If player 1 is facing left
		tempshift = player_position[0][0]-p1move.shift
		for i in range(len(p1move.hitbox)): # Generate hitboxes starting with the "rightmost" flipped hitbox
			x = i + 1
			genbox2([offset+tempshift,p1move.hitbox[-x][1]+player_position[0][1],p1move.hitbox[-x][2],p1move.hitbox[-x][3]], p1move.hitbox[-x][0] , p2move)
			offset += p1move.hitbox[-x][2]
	else: # If player one is facing right
		for i in range(len(p1move.hitbox)): # Generate hitboxes starting with the leftmost hitbox
			genbox2([offset+player_position[0][0],p1move.hitbox[i][1]+player_position[0][1],p1move.hitbox[i][2],p1move.hitbox[i][3]], p1move.hitbox[i][0], p2move)
			offset += p1move.hitbox[i][2]
	dmgcheck() # See if damage was dealt

def genbox2(box1,movekind,receiver): # For every individual box player1 has active, compare them to player 2's boxes
	offset = 0
	if left_facing_list[1]: # If player 2 is facing left
		tempshift = player_position[1][0]-receiver.shift
		for i in range(len(receiver.hitbox)):
			x = i + 1
			collidetest(box1,movekind,[offset+tempshift,receiver.hitbox[-x][1]+player_position[1][1],receiver.hitbox[-x][2],receiver.hitbox[-x][3]],receiver.hitbox[-x][0])
			offset += receiver.hitbox[-x][2]
	else: # If player 2 is facing right
		for i in range(len(receiver.hitbox)):
			collidetest(box1, movekind, [offset+player_position[1][0],receiver.hitbox[i][1]+player_position[1][1],receiver.hitbox[i][2],receiver.hitbox[i][3]], receiver.hitbox[i][0])
			offset += receiver.hitbox[i][2]

def collidetest(box1, movekind1, box2, movekind2): # Checks to see if a blow has been successfully landed
	global p1hit, p2hit

	if ((box1[0]+box1[2]) > box2[0]) and (box1[0] < (box2[0]+box2[2])):
		if ((box1[1]+box1[3]) > box2[1]) and (box1[1] < (box2[1]+box2[3])): # Collision logic
			if (movekind1 == 0 or movekind1 == 1) and movekind2 == 1:
				hitcheck[1] = True # Player 2 lands a hit
			if movekind1 == 1 and (movekind2 == 0 or movekind2 == 1):
				hitcheck[0] = True # Player 1 lands a hit

def stamdrain(player):
	if player_current_state[player] != player_prev_state[player]: # If a fresh move has been thrown out
		if player_current_state[player].stam > list_of_players[player].stamina: # If not enough stamina to use move
			player_current_state[player] = list_of_players[player].n # revert to neutral state
		else:
			list_of_players[player].stamina -= player_current_state[player].stam # Use that much stamina

	list_of_players[player].stamina += 1 # Regain 1 stamina per frame
	if list_of_players[player].stamina > 300:
		list_of_players[player].stamina = 300

def dmgcheck():
	global exit
	global winner
	if hitcheck[0] == True and (player_current_state[0] != player_prev_state[0]): # If player 1 has landed a freash hit
		p2.health -= player_current_state[0].dmg # Player 2 takes damage
		if p2.health <= 0: # If player 2 dies
			p2.health = 0
			exit = True
			winner = p1.name

	if hitcheck[1] == True and (player_current_state[1] != player_prev_state[1]): # Same thing but for player 2
		p1.health -= player_current_state[1].dmg
		if p1.health <= 0: # If player 1 dies
			exit = True
			p1.health = 0	
			winner = p2.name	

def checkproj(): # Checks Kyn's ninja stars
	global hitalready
	if special_variables[1][5] and p2 == Kyn: # If player 2 is kyn and his special is active
		ptouching = False # If this ninja star has already touched the opponent
		offset = 0
		if left_facing_list[0]: # Collision check
			tempshift = player_position[0][0]-player_current_state[0].shift
			for i in range(len(player_current_state[0].hitbox)):
				x = i + 1
				ptouching = projcollide([offset+tempshift,player_current_state[0].hitbox[-x][1]+player_position[0][1],player_current_state[0].hitbox[-x][2],player_current_state[0].hitbox[-x][3]])
				offset += player_current_state[0].hitbox[-x][2]
		else:
			for i in range(len(player_current_state[0].hitbox)):
				ptouching = projcollide([offset+player_position[0][0],player_current_state[0].hitbox[i][1]+player_position[0][1],player_current_state[0].hitbox[i][2],player_current_state[0].hitbox[i][3]])
				offset += player_current_state[0].hitbox[i][2]
		if ptouching == True and hitalready == False: # If a fresh ninja star hits Kyn's opponent
			p1.health -= 50 # Deal 50 damage
			if p1.health <= 0:
				p1.health = 0
			hitalready = True
	if special_variables[0][5] and p1 == Kyn: # Same thing but if Kyn was player 1
		ptouching = False
		offset = 0
		if left_facing_list[1]:
			tempshift = player_position[1][0]-player_current_state[1].shift
			for i in range(len(player_current_state[1].hitbox)):
				x = i + 1
				ptouching = projcollide([offset+tempshift,player_current_state[1].hitbox[-x][1]+player_position[1][1],player_current_state[1].hitbox[-x][2],player_current_state[1].hitbox[-x][3]])
				offset += player_current_state[1].hitbox[-x][2]
		else:
			for i in range(len(player_current_state[1].hitbox)):
				ptouching = projcollide([offset+player_position[1][0],player_current_state[1].hitbox[i][1]+player_position[1][1],player_current_state[1].hitbox[i][2],player_current_state[1].hitbox[i][3]])
				offset += player_current_state[1].hitbox[i][2]
		if ptouching == True and hitalready == False:
			p2.health -= 50
			if p2.health <= 0:
				p2.health = 0
			hitalready = True
def checkfire(): # For Scott's special
	if special_variables[1][5] and p2 == Scott: # If player 2 is scott and his special is active
		ftouching = False # If the fire is touching opponent or not
		offset = 0
		if left_facing_list[0]: # Collision check
			tempshift = player_position[0][0]-player_current_state[0].shift
			for i in range(len(player_current_state[0].hitbox)):
				x = i + 1
				ftouching = firecollide([offset+tempshift,player_current_state[0].hitbox[-x][1]+player_position[0][1],player_current_state[0].hitbox[-x][2],player_current_state[0].hitbox[-x][3]],1)
				offset += player_current_state[0].hitbox[-x][2]
		else:
			for i in range(len(player_current_state[0].hitbox)):
				ftouching = firecollide([offset+player_position[0][0],player_current_state[0].hitbox[i][1]+player_position[0][1],player_current_state[0].hitbox[i][2],player_current_state[0].hitbox[i][3]],1)
				offset += player_current_state[0].hitbox[i][2]
		if ftouching == True: # If opponent is on fire
			p1.health -= 20
			if p1.health <= 0:
				p1.health = 0
	if special_variables[0][5] and p1 == Scott: # Same thing but for player 1
		ftouching = False
		offset = 0
		if left_facing_list[1]:
			tempshift = player_position[1][0]-player_current_state[1].shift
			for i in range(len(player_current_state[1].hitbox)):
				x = i + 1
				ftouching = firecollide([offset+tempshift,player_current_state[1].hitbox[-x][1]+player_position[1][1],player_current_state[1].hitbox[-x][2],player_current_state[1].hitbox[-x][3]],0)
				offset += player_current_state[1].hitbox[-x][2]
		else:
			for i in range(len(player_current_state[1].hitbox)):
				ftouching = firecollide([offset+player_position[1][0],player_current_state[1].hitbox[i][1]+player_position[1][1],player_current_state[1].hitbox[i][2],player_current_state[1].hitbox[i][3]],0)
				offset += player_current_state[1].hitbox[i][2]
		if ftouching == True:
			p2.health -= 20
			if p2.health <= 0:
				p2.health = 0

def projcollide(hurtbox): # Checks collision for ninja star
	if ((hurtbox[0]+hurtbox[2]) > starbox[0]) and (hurtbox[0] < (starbox[0]+starbox[2])):
		if ((hurtbox[1]+hurtbox[3]) > starbox[1]) and (hurtbox[1] < (starbox[1]+starbox[3])):
			return True
	else:
		return False

def firecollide(hurtbox, x): # Checks collision for flame
	if ((hurtbox[0]+hurtbox[2]) > (special_variables[x][3] + special_variables[x][1])) and (hurtbox[0] < (special_variables[x][3] + special_variables[x][1] + 140)):
		if ((hurtbox[1]+hurtbox[3]) > (special_variables[x][4]+special_variables[x][2])) and (hurtbox[1] < (special_variables[x][4]+special_variables[x][2] + 100)):
			return True
	else:
		return False

#engages a special attack for players when special move is pressed
def powermove(x, player):
	#adds 20 frames worth of ninja star travel if no ninja star is currently being fired
	if player.name == "kyn":
		if special_variables[x][0] == 0:
			special_variables[x][5] = True
			special_variables[x][0] = 20

	#engages scotts special if special being pressed
	if player.name == "scott":
		if player_current_state[x] == list_of_players[x].s:
			special_variables[x][5] = True

	#engages and carries out doms special
	if player.name == "dom":
		if list_of_players[x].health + 20 <= list_of_players[x].totalhealth: #adds to his health
			list_of_players[x].health += 20
		else:
			list_of_players[x].health = list_of_players[x].totalhealth #subtracts from stamina


#for more complicated specials (scott and kyn) needed a second function
def special_attack(x, player):
	global starbox, hitalready

	#fires kyns star
	if player.name == "kyn":
		
		starimage = pygame.image.load("ninjastar.png")
			
		#if first time in special, uses that current position to fire from
		if special_variables[x][0] == 20:
			hitalready = False
			#shifts so lines up with hands
			if left_facing_list[x]:
				special_variables[x][1] = -40
				special_variables[x][2] = -15
			else:
				special_variables[x][1] = 100
				special_variables[x][2] = 15

			special_variables[x][3] = player_position[x][0]
			special_variables[x][4] = player_position[x][1]
		#alternates b/w tilted and straight - rotating effect
		if special_variables[x][0]%2 == 0:
			ninjastarimage = starimage
		else:
			ninjastarimage = pygame.transform.rotate(starimage, 45)

		screen.blit(ninjastarimage, (special_variables[x][3] + special_variables[x][1] + special_variables[x][2]*(20- special_variables[x][0]), special_variables[x][4]+15))
		starbox = [special_variables[x][3] + special_variables[x][1] + special_variables[x][2]*(20- special_variables[x][0]), special_variables[x][4]+15, 50, 50]
		special_variables[x][0] -= 1

		if special_variables[x][0] == 0:
			special_variables[x][5] = False

	if player.name == "scott":
		#makes sure only working when his sprite is that of a special - had problems where he was able to shoot fire while running, etc.
		if player_states[x][13] == True:
			special_variables[x][5] = False

		if player_current_state[x] != list_of_players[x].s:
			special_variables[x][5] = False

		if special_variables[x][5]:

			if list_of_players[x].stamina - 10 > 0: #removes stamina
				list_of_players[x].stamina -= 10
			else:
				list_of_players[x].stamina = 0
				special_variables[x][5] = False


			fireimage = pygame.image.load("breathing_fire.png")

			if left_facing_list[x]:
				special_variables[x][1] = -220
				special_variables[x][2] = -20
				fireimage2 = pygame.transform.rotate(fireimage, 40) #tilts down
			else:
				special_variables[x][1] = 65
				special_variables[x][2] = 7
				fireimage2 = pygame.transform.rotate(fireimage, 160)

			special_variables[x][3] = player_position[x][0]
			special_variables[x][4] = player_position[x][1]


			screen.blit(fireimage2, (special_variables[x][3] + special_variables[x][1], special_variables[x][4]+special_variables[x][2]))



def drawHealth(): # Draw health bars
		healthbar = 300 * p1.health // p1.totalhealth # Get the health bar as a fraction of total health

		pygame.draw.rect(screen, (255,0,0), [30,30,300,20]) # Draw redness behind health bar
		pygame.draw.rect(screen, (0,255,0), [30,30,healthbar,20]) # Draw green health
		pygame.draw.rect(screen, (0,0,0), [30,30,300,20], 2) # Draw border

		pygame.draw.rect(screen, (255,0,0), [30,70,300,20]) # Same thing but for stamina bar
		pygame.draw.rect(screen, (0,0,255), [30,70,list_of_players[0].stamina,20])
		pygame.draw.rect(screen, (0,0,0), [30,70,300,20], 2)

		healthbar = 300 * p2.health // p2.totalhealth # Same thing but for player 2

		pygame.draw.rect(screen, (255,0,0), [669,30,300,20])
		pygame.draw.rect(screen, (0,255,0), [969-healthbar,30,healthbar,20])
		pygame.draw.rect(screen, (0,0,0), [669,30,300,20], 2)

		pygame.draw.rect(screen, (255,0,0), [669,70,300,20])
		pygame.draw.rect(screen, (0,0,255), [969-list_of_players[1].stamina,70,list_of_players[1].stamina,20])
		pygame.draw.rect(screen, (0,0,0), [669,70,300,20], 2)

# Kyn Setup

Kyn = Fighter("kyn", 20, 30, 400)
#coordinates for hitboxes of different positions
Kyn.n.hitbox = [[0,0,39,220],[0,70,20,30]]
Kyn.r.hitbox = [[0,0,60,200],[0,50,20,20]]
Kyn.d.hitbox = [[0,0,91,140]]
Kyn.b.hitbox = []
Kyn.j.hitbox = [[0,0,50,220]]
Kyn.p.hitbox = [[0,0,50,220],[1,30,60,30]]
Kyn.k.hitbox = [[0,0,40,220],[0,50,20,120],[1,70,75,60]]
Kyn.s.hitbox = [[0,0,100,200],[0,30,40,40]]
#damage and stam for each move
Kyn.n.shift, Kyn.n.dmg, Kyn.n.stam = 0, 0, 0
Kyn.p.shift, Kyn.p.dmg, Kyn.p.stam = 52, 20, 20
Kyn.r.shift, Kyn.r.dmg, Kyn.r.stam = 21, 0, 0
Kyn.s.shift, Kyn.s.dmg, Kyn.s.stam = 79, 40, 40
Kyn.d.shift, Kyn.d.dmg, Kyn.d.stam = 33, 0, 0
Kyn.k.shift, Kyn.k.dmg, Kyn.k.stam = 75, 20, 20
Kyn.j.shift, Kyn.j.dmg, Kyn.j.stam = -5, 0, 0
Kyn.b.shift, Kyn.b.dmg, Kyn.b.stam = -2, 0, 0
kynspecial = 0

# Scott Setup

Scott = Fighter("scott", 8, 20, 500)
Scott.n.hitbox = [[0,0,37,199]]
Scott.r.hitbox = [[0,0,37,199]]
Scott.d.hitbox = [[0,0,80,140]]
Scott.b.hitbox = []
Scott.j.hitbox = [[0,0,50,220]]
Scott.p.hitbox = [[0,0,70,220],[1,30,40,30]]
Scott.k.hitbox = [[0,0,37,199],[1,100,81,60]]
Scott.s.hitbox = [[0,0,60,200],[0,0,23,60]]
Scott.n.shift, Scott.n.dmg, Scott.n.stam = 0, 0, 0
Scott.p.shift, Scott.p.dmg, Scott.p.stam = 81, 40, 20
Scott.r.shift, Scott.r.dmg, Scott.r.stam = 0, 0, 0
Scott.s.shift, Scott.s.dmg, Scott.s.stam = 79, 40, 20
Scott.d.shift, Scott.d.dmg, Scott.d.stam = 33, 0, 0
Scott.k.shift, Scott.k.dmg, Scott.k.stam = 75, 40, 20
Scott.j.shift, Scott.j.dmg, Scott.j.stam = -5, 0, 0
Scott.b.shift, Scott.b.dmg, Scott.b.stam = -2, 0, 0

# Cam

Cam = Fighter("cam", 8, 10, 800)
Cam.n.hitbox = [[0,0,52,199]]
Cam.r.hitbox = [[0,0,86,199]]
Cam.d.hitbox = [[0,0,136,120]]
Cam.b.hitbox = []
Cam.j.hitbox = [[0,0,121,200]]
Cam.p.hitbox = [[0,0,120,190],[1,10,55,30]]
Cam.k.hitbox = [[0,0,80,199],[1,30,121,60]]
Cam.s.hitbox = [[0,0,175,200],[0,30,80,30],[1,30,90,30]]
Cam.n.shift, Cam.n.dmg, Cam.n.stam = 0, 0, 0
Cam.p.shift, Cam.p.dmg, Cam.p.stam = 123, 40, 20
Cam.r.shift, Cam.r.dmg, Cam.r.stam = 34, 0, 0
Cam.s.shift, Cam.s.dmg, Cam.s.stam = 200, 40, 20
Cam.d.shift, Cam.d.dmg, Cam.d.stam = 84, 0, 0
Cam.k.shift, Cam.k.dmg, Cam.k.stam = 148, 40, 20
Cam.j.shift, Cam.j.dmg, Cam.j.stam = 69, 0, 0
Cam.b.shift, Cam.b.dmg, Cam.b.stam = 61, 0, 0

# Dom

Dom = Fighter("dom", 8, 20, 800)
Dom.n.hitbox = [[0,0,42,200]]
Dom.r.hitbox = [[0,0,50,200],[0,170,30,30]]
Dom.d.hitbox = [[0,0,80,140],[0,40,40,100]]
Dom.b.hitbox = []
Dom.j.hitbox = [[0,0,68,200]]
Dom.p.hitbox = [[0,0,60,190],[1,30,60,30]]
Dom.k.hitbox = [[0,0,70,199],[1,60,110,60]]
Dom.s.hitbox = [[0,0,90,200]]
Dom.n.shift, Dom.n.dmg, Dom.n.stam = 0, 0, 0
Dom.p.shift, Dom.p.dmg, Dom.p.stam = 78, 40, 20
Dom.r.shift, Dom.r.dmg, Dom.r.stam = 34, 0, 0
Dom.s.shift, Dom.s.dmg, Dom.s.stam = 48, 40, 20
Dom.d.shift, Dom.d.dmg, Dom.d.stam = 84, 0, 0
Dom.k.shift, Dom.k.dmg, Dom.k.stam = 138, 40, 20
Dom.j.shift, Dom.j.dmg, Dom.j.stam = 26, 0, 0
Dom.b.shift, Dom.b.dmg, Dom.b.stam = 52, 0, 0

#winning and continue screen
def winning_screen(player):
	
	global hub
	#function for replaying
	def replayy():
		master2.destroy()

	#function for quitting, hub variable set to false means main loop at bottom of the code stops, terminating code 
	def quiter():
		global hub
		hub = False
		master2.destroy()

	#goes back to character menus before restarting
	def selecter():
		master2.destroy()
		menus()

	master2 = tkinter.Tk()
	
	starting_width = 600
	starting_height = 400

	master2.maxsize(width =starting_width, height = starting_height)
	master2.minsize(width =starting_width, height = starting_height)

	master2.title('Library Fighter')

	#winning statement
	status_label = tkinter.Label(master2, text =str(player) + ' Wins', pady = 38, padx = 240, font=("Courier", 20), fg = 'blue', bg = 'black')
	status_label.pack()

	#replay button
	replay_button = tkinter.Button(master2, text = "Play Again", pady = 38, padx = 240, font=("Courier", 20), fg = 'green', command = replayy)
	replay_button.pack()

	#select characters button
	character_select = tkinter.Button(master2, text = "Change Characters", pady = 38, padx = 240, font=("Courier", 20), fg = 'purple', command = selecter)
	character_select.pack()

	#quit button
	quit_button = tkinter.Button(master2, text = "Quit", pady = 43, padx = 275, font=("Courier", 20), fg = 'red', command = quiter)
	quit_button.pack()

	tkinter.mainloop()

#character menu selection
def menus():
	global p1
	global p2
	master = tkinter.Tk()


	starting_width = 600
	starting_height = 400

	master.maxsize(width =starting_width, height = starting_height)
	master.minsize(width =starting_width, height = starting_height)

	master.title('Library Fighter')

	#characters profile images
	scottimg = tkinter.PhotoImage(file="scottProfile2.png") 
	kynimg = tkinter.PhotoImage(file="kynProfile.png") 
	domimg = tkinter.PhotoImage(file="domProfile2.png") 
	camimg = tkinter.PhotoImage(file="CamProfile.png") 

	#destroys window, allows for pygame to now appear
	def quit():
		master.destroy()

	#after beginning screen clicked, shows characters options
	def begin():
		starting_button.pack_forget()
		player_1_prompt.pack(side = tkinter.TOP)
		dom_button.pack(side = tkinter.LEFT)
		kyn_button.pack(side = tkinter.LEFT)
		scott_button.pack(side = tkinter.LEFT)
		cam_button.pack(side=tkinter.LEFT)
		
	#clears player1 selection, places character2
	def clear():
		dom_button.pack_forget()
		kyn_button.pack_forget()
		scott_button.pack_forget()
		cam_button.pack_forget()
		player_1_prompt.pack_forget()
		player_2_prompt.pack()
		dom_button_2.pack(side = tkinter.LEFT)
		kyn_button_2.pack(side = tkinter.LEFT)
		scott_button_2.pack(side = tkinter.LEFT)
		cam_button_2.pack(side=tkinter.LEFT)

	#tells player 2 they can't pick same character as player 1
	def reset():
		dom_button_2.pack_forget()
		kyn_button_2.pack_forget()
		scott_button_2.pack_forget()
		cam_button_2.pack_forget()
		player_2_prompt.pack_forget()
		error_label.pack()
		dom_button_2.pack(side = tkinter.LEFT)
		kyn_button_2.pack(side = tkinter.LEFT)
		scott_button_2.pack(side = tkinter.LEFT)
		cam_button_2.pack(side=tkinter.LEFT)
	
	#sets player 1 as dom, proceeds to player 2
	def dom_1():
		global p1
		global p2
		p1 = Dom
		clear()
	def kyn_1():
		global p1
		global p2
		p1 = Kyn
		clear()
	def scott_1():
		global p1
		global p2
		p1 = Scott
		clear()
	def cam_1():
		global p1
		global p2
		p1 = Cam
		clear()
	#if new character selected, allows it, proceed to pygame. If same as player 1, tells them to retry
	def dom_2():
		global p1
		global p2
		p2 = Dom
		if p2 != p1:
			quit()
		else:
			reset()

	def kyn_2():
		global p1
		global p2
		p2 = Kyn
		if p2 != p1:
			quit()
		else:
			reset()
	def scott_2():
		global p1
		global p2
		p2 = Scott
		if p2 != p1:
			quit()
		else:
			reset()
	def cam_2():
		global p1
		global p2
		p2 = Cam
		if p2 != p1:
			quit()
		else:
			reset()


	#text prompts
	player_1_prompt = tkinter.Label(master, fg = 'blue',  text = 'Player 1, select a character')
	player_2_prompt = tkinter.Label(master, fg = 'green', text = 'Player 2, select a character')

	#opening greeting
	starting_button = tkinter.Button(master, text = 'Welcome to Library Fighter! Click to Continue', font=("Courier", 20), pady = 200, padx = 300, fg = 'blue', bg = 'black', command = begin)
	starting_button.pack()

	#pick another player
	error_label = tkinter.Label(master, fg = 'green', text = 'Player 2, select a character different from Player 1')

	#buttons for player 1
	dom_button = tkinter.Button(master, image= domimg, text= 'Dom', command = dom_1)
	kyn_button = tkinter.Button(master, image = kynimg, text = 'Kyn', command = kyn_1)
	scott_button = tkinter.Button(master, image = scottimg, text = 'Scott', command = scott_1)
	cam_button = tkinter.Button(master, image = camimg, text = 'Cam', command = cam_1)

	#buttons for player 2
	dom_button_2 = tkinter.Button(master, image= domimg, text= 'Dom', command = dom_2)
	kyn_button_2 = tkinter.Button(master, image = kynimg, text = 'Kyn', command = kyn_2)
	scott_button_2 = tkinter.Button(master, image = scottimg, text = 'Scott', command = scott_2)
	cam_button_2 = tkinter.Button(master, image = camimg, text = 'Cam', command = cam_2)




	tkinter.mainloop()

global p1
global p2 
p1 = 0
p2 = 0



class Background(pygame.sprite.Sprite): # Background class for different stages
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file) # Load image from file
        self.rect = self.image.get_rect() #get sizing
        self.rect.left, self.rect.top = location

dining_hall_pic = Background('choate_adm.png', [0,0]) #creating a backround    

#original sprite state - image and position



#to start, the sprite is facing left

#originally not moving and not in a jump



#jump function: if y = 540 (not currently in a jump), it will create a new jump. If already in a jump, will not create a new jump


def gameplay():
	global exit
	while not exit: # Allows the game to run until quit
		screen.fill([255,255,255]) # Make the screen white
		screen.blit(dining_hall_pic.image, dining_hall_pic.rect) #puts image on top of whiteness

		#Conversion key - stores each of these values in player_states[which player][state]
		# up_p = False #0
		# down_p = False #1
		# left_p = False #2
		# right_p = False #3

		# left_r = False #4
		# right_r = False #5
		# down_r = False #6

		# punch_p = False #7
		# kick_p = False #8
		# special_p = False #9
		# block_p = False #10

		# punch_r = False #11
		# kick_r= False #12
		# special_r = False #13
		# block_r = False #14


		for x in range(2):
			for q in range (len(player_states[x])):
				player_states[x][q] = False


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True


			#checks to see if any keys pressed
			if event.type == KEYDOWN:
				for x in range(2):
					if (event.key == player_keys[x][0]):
						player_states[x][2] = True
					elif (event.key == player_keys[x][1]):
						player_states[x][3] = True
					elif (event.key == player_keys[x][2]):
						player_states[x][0] = True
					elif (event.key == player_keys[x][3]):
						player_states[x][1] = True
					elif (event.key == player_keys[x][4]):
						player_states[x][7] = True
					elif (event.key == player_keys[x][5]):
						player_states[x][8] = True
					elif (event.key == player_keys[x][6]):
						player_states[x][9] = True
					elif (event.key == player_keys[x][7]):
						player_states[x][10] = True

			#checks to see if any keys released
			if event.type == KEYUP:
				for x in range(2):
					if (event.key == player_keys[x][0]):
						player_states[x][4] = True
					elif (event.key == player_keys[x][1]):
						player_states[x][5] = True
					elif (event.key == player_keys[x][3]):
						player_states[x][6] = True
					elif (event.key == player_keys[x][4]):
						player_states[x][11] = True
					elif (event.key == player_keys[x][5]):
						player_states[x][12] = True
					elif (event.key == player_keys[x][6]):
						player_states[x][13] = True
					elif (event.key == player_keys[x][7]):
						player_states[x][14] = True





		for x in range(2):
			hitcheck[x] = False
			player_position[x][1] = 390
			player_prev_state[x] = player_current_state[x]

			#if any button released, will face in whatever direction it finished on
			if player_states[x][5] or player_states[x][4] or player_states[x][6] or player_states[x][11] or player_states[x][12] or player_states[x][13] or player_states[x][14]:
				player_vel[x][0] = 0
				player_current_state[x] = list_of_players[x].n

			#if  left/right pressed, will add velocity that way
			if player_states[x][2]:
				player_vel[x][0] = -list_of_players[x].speed
				player_current_state[x] = list_of_players[x].r
				left_facing_list[x] = True
			elif player_states[x][3]:
				player_vel[x][0] = list_of_players[x].speed
				player_current_state[x] = list_of_players[x].r
				left_facing_list[x] = False

			#if ducking
			elif player_states[x][1]:
				player_current_state[x] = list_of_players[x].d

			#if jumping
			elif player_states[x][0]:
				if player_position[x][1] == 390:
					jump_variables[x][0] = list_of_players[x].jump_height
			
			#if sprite close to left, wont go over limit
			if player_position[x][0] -list_of_players[x].speed <= 0:
				if player_vel[x][0] > 0:
					player_position[x][0] = player_vel[x][0] + player_position[x][0]
				elif player_vel[x][0] < 0:
					player_position[x][0] = 0

			#if sprite close to right, wont go over limit
			elif player_position[x][0]+list_of_players[x].speed >= width-30:
				if player_vel[x][0] < 0:
					player_position[x][0] = player_vel[x][0] + player_position[x][0]
				elif player_vel[x][0] > 0:
					player_position[x][0] = width - 30

			#moves sprite according to velocity if in middleish area
			else:
				player_position[x][0] = player_vel[x][0] + player_position[x][0]

			#only applies if in a jump
			if jump_variables[x][0] != 0:
				#if less than halfway through jump, continues to rise
				if jump_variables[x][0] >(list_of_players[x].jump_height/2):
					player_position[x][1] = 390 - (80*(list_of_players[x].jump_height+1-jump_variables[x][0]))
				#if over halfway through jump, falls
				elif (list_of_players[x].jump_height/2)>= jump_variables[x][0]>0:
					player_position[x][1] = (390-(80*list_of_players[x].jump_height/2)) + (80*((list_of_players[x].jump_height/2)+1-jump_variables[x][0]))
				jump_variables[x][0] -= 1

				#jumping image
				player_current_state[x] = list_of_players[x].j

				#normal image on last stage
				if jump_variables[x][0] == 0:
					player_current_state[x] = list_of_players[x].n

			#if punching
			if player_states[x][7]:
				player_current_state[x] = list_of_players[x].p

			#if special move
			if player_states[x][9]:
				player_current_state[x] = list_of_players[x].s
				powermove(x, list_of_players[x])

				
			#if kicking
			if player_states[x][8]:
				player_current_state[x] = list_of_players[x].k

			#if blocking
			if player_states[x][10] and list_of_players[x].stamina > 5:
				player_current_state[x] = list_of_players[x].b
	



			#if running, shifts sprite for appearnce
			if player_current_state[x] == list_of_players[x].r:
				player_position[x][1] += 7

			#if ducking, shifts sprite
			if player_current_state[x] == list_of_players[x].d:
				player_position[x][1] += 65

			#if special attack engaged
			if special_variables[x][5]:
				special_attack(x, list_of_players[x])

			


			#if blocking
			if player_current_state[x] == list_of_players[x].b:
				if list_of_players[x].stamina -5 > 0: # drain stamina
					list_of_players[x].stamina -= 5
				else:
					list_of_players[x].stamina = 0
			if list_of_players[x].stamina < 5 and player_current_state[x] == list_of_players[x].b: # If stamina runs out
				player_current_state[x] = list_of_players[x].n # 

			stamdrain(x) # Drain the player's stamina
			player_current_state[x].printer(x) # Print player's sprite

		genbox1(player_current_state[0],player_current_state[1]) # Check collisions
		checkproj() # Check Kyn's star
		checkfire() # Check Scott's fire
		drawHealth() # Draw the health bars

		


		pygame.display.update() # Refresh display
		Clock.tick(fps) # Set framerate

global hub
hub = True
menus()
#loops until user decides to quit
while hub:

	#resets all variables and states when game begins
	list_of_players = [p1, p2]
	player_keys = [[K_a, K_d, K_w, K_s, K_f, K_g, K_h, K_j],[K_LEFT,K_RIGHT, K_UP,K_DOWN,K_u,K_i, K_o, K_p]]
	player_states =[[False, False, False, False, False, False, False, False ,False, False, False, False, False, False, False],[False, False, False, False, False, False, False, False ,False, False, False, False, False, False, False]]
	player_position = [[200,390],[500,390]]
	player_vel = [[0], [0]]
	special_variables = [[0,0,0,0,0, False],[0,0,0,0,0, False]]
	jump_variables = [[0],[0]]
	left_facing_list = [False,True]
	player_current_state = [p1.n, p2.n]
	player_prev_state = [p1.n, p2.n]
	hitcheck = [False,False]
	hitalready = False
	p1.health = p1.totalhealth
	p2.health =p2.totalhealth
	p1.stamina = 300
	p2.stamina = 300





	pygame.init() #allow game to run

	width, length = 999, 600 #width of screen = width of pic

	screen = pygame.display.set_mode((width,length)) #setting size

	pygame.display.set_caption("Library Fighter")

	fps = 120 #120 frames per sec

	Clock = pygame.time.Clock() #clock, for delaying each frame refresh

	exit = False


	gameplay()
	pygame.quit()
	winning_screen(winner)





