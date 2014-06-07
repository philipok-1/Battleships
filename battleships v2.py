#Battleships


import random

#set up grid parameters and allowed rows/columns

grid_size=[10,10]

row_letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n']

allowed_rows=row_letters[:grid_size[0]]
allowed_columns=grid_size[0]

column_list=[]
for i in range (0,allowed_columns):
        column_list.append(i)

       

ship_types={5:'an aircraft carrier', 4:'a destroyer', 3:'a frigate', 2:'a cruiser', 1:'a sub'}


def grid2position(row, column):
	
	row_position=row_letters.index(str(row))
	column_position=int(column)
	cell=(row_position*(grid_size[0]))+column_position
	
	return cell

def position2grid(position):

        row=(position//grid_size[0])
        row_letter=row_letters[row]
        column=position%grid_size[0]

        return row, row_letter, column

def random_shot():

        row=random.choice(allowed_rows)
        column=random.randint(0,allowed_columns)
        position=grid2position(row, column)

        return position
	

class Grid:

    def __init__(self):

        #set up grid

        self.box=[]
        self.occupied=[]
        self.ships=[]
        self.already_tried=[]
        self.missed=[]
        self.hit=[]
        self.move_history=[]
        self.targeting=False
        self.strike=0
        self.strike_hits=0
        
        
        count=0

        for row in range (grid_size[0]):

            for column in range (grid_size[0]):

                self.box.append('0')
                             
    def print_grid(self):

            columncount=grid_size[0]
        
            for i in range(0,grid_size[0]):

                    print (row_letters[i], self.box[(i*grid_size[0]):columncount])
                    columncount+=grid_size[0]
            return


#add a ship


class Ship:

    #images=[image1, image2, image3 etc]
    

    def __init__(self, length):

        self.type=length
        self.length=length
        self.hp=length
        self.cells=[]
        orientation=['vertical', 'horizontal']
        self.direction=random.choice(orientation)
        


    def add_to_grid(self, grid):

        limit=((grid_size[0])-(self.length))
            
        occupied=True
        while occupied==True:

            boxes=[]
            boxhit=False

            if self.direction=='horizontal':

                start_column=random.randint(0,(limit))
                start_row=random.randint(0,grid_size[0]-1)
                start_position=(start_row*grid_size[0])+start_column
                

            elif self.direction=='vertical':

                start_row=random.randint(0,limit)
                start_column=random.randint(0,grid_size[0]-1)
                start_position=(start_row*(grid_size[0]-1)+(start_row+start_column))
                
            
            for i in range (self.length):

                if self.direction=='horizontal':
                    boxes.append(start_position+i)
                else: boxes.append(start_position+((grid_size[0])*i))
                 
            for box in boxes:
                if box in grid.occupied: boxhit=True
                
            if boxhit==True:
                print (boxes, grid.occupied, boxhit)
                occupied=True
                
                    
            else:

                occupied=False
                self.cells=boxes
                boxes=[]
                
        for j in range (self.length):

            if self.direction=='horizontal':
                    
                grid.box[start_position+j]=[self.type]
                grid.occupied.append(start_position+j)

            else:
                
                grid.box[start_position+((grid_size[0])*j)]=[self.type]
                grid.occupied.append(start_position+(grid_size[0]*j))
                
        return grid.box, grid.occupied
				                            
					  

def create_fleet(grid):
	
	acc=Ship(5)
	destroyer=Ship(4)
	frigate=Ship(3)
	cruiser=Ship(2)
	sub=Ship(1)
	
	ships=[acc, destroyer, frigate, cruiser, sub]
	
	for ship in ships:
		grid.box, grid.occupied=ship.add_to_grid(grid)
		grid.ships.append(ship)
    


def predictive_target(computer, player):


        targetr=computer.strike+(computer.strike_hits)
        print (targetr)
        targetl=computer.strike-(computer.strike_hits)
        print(targetl)
        targetu=computer.strike-(computer.strike_hits*grid_size[0])
        print(targetu)
        targetd=computer.strike+(computer.strike_hits*grid_size[0])
        print(targetd)
        
       
        # try firing to the right

        if      ((targetr not in computer.already_tried)
                and ((targetr%grid_size[0])<=grid_size[0])):
                

                fire=targetr
                
        #try left

        elif ((targetl not in computer.already_tried)
              and ((targetl%grid_size[0])<=0)):

                fire=targetl

        #try up

        elif ((targetu not in computer.already_tried)
                and (targetu>=0)):
                fire=targetu

        #try down

        elif ((targetd not in computer.already_tried)
             and (targetd<=(grid_size[0]*grid_size[0]))):

                fire=targetd

        else: fire=random_shot()

        return fire

        


def player_move(player, player_target, computer):

        allowed=False
        
        while allowed==False:

                row='z'
                column=1000
        
                while row not in allowed_rows:
                             
                        row=input('enter row')

                while column not in column_list:

                        try:
                                column=int(input('enter column'))

                        except ValueError:
                                pass
                                
                                            
                position=grid2position(row, column)
                
                if position not in player.already_tried:
                        print('position=', position)
                        allowed=True
                else:
                        print ('Already fired on that square!')
                        allowed=False

        if position in computer.occupied:
                        print ('hit')
                        computer.box[position]='!'
                        player_target.box[position]='!'
                        player.already_tried.append(position)
                        computer.occupied.remove(position)
                        for ship in computer.ships:
                                if position in ship.cells:
                                        ship.hp-=1
                                        if ship.hp==0:
                                                print ('destroyed', ship_types[ship.type])
                                                computer.ships.remove(ship)
                                                for cell in ship.cells:
                                                        player_target.box[cell]='X'
                
        else:
                print ('miss')
                player_target.box[position]='M'
                player.already_tried.append(position)
                
def computer_move(player, player_target, computer):

        allowed=False
        
        while allowed==False:

                if computer.move_history!=[]:

                                                                                              
                        #has the computer hit a ship?
                        
                        if computer.targeting:
                                
                                position=predictive_target(computer, player)        
                     

                        else:
                                print ('last shot was a miss')
                                position=random_shot()

                else:
                        position=random_shot()
                        
                computer.move_history.append(position)
                row, row_letter, column=position2grid(position)
                
                if position not in computer.already_tried:
                        print('Firing on', position,' Row', row_letter, ' Column', column)
                        allowed=True
                else:
                        allowed=False

        if position in player.occupied:
                        print ('hit')
                        player.box[position]='!'
                        computer.already_tried.append(position)
                        computer.hit.append(position)
                        player.occupied.remove(position)
                        if computer.targeting==False:
                                computer.strike=position
                                
                        computer.targeting=True
                                              
                        computer.strike_hits+=1
                        
                        for ship in player.ships:
                                if position in ship.cells:
                                        ship.hp-=1
                                        if ship.hp==0:
                                                print ('computer destroyed ', ship_types[ship.type])
                                                player.ships.remove(ship)
                                                computer.targeting=False
                                                computer.strike=0
                                                computer.strike_hits=0
                
        else:
                print ('computer missed')
                player.box[position]='M'
                computer.already_tried.append(position)
                computer.missed.append(position)
                computer.strike_hits=0

#game starts

player=Grid()
player_target=Grid()
computer=Grid()
    
create_fleet(player)
create_fleet(computer)

while True:

        
        
        player.print_grid(), print ('\n'), player_target.print_grid()
        player_move(player, player_target, computer)
        computer_move(player, player_target, computer)
        print(computer.targeting, computer.strike, computer.strike_hits)
      
       


           
        

        
