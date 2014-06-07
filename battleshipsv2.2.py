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


        total=(grid_size[0])**2
        position=random.randint(0,(total-1))

        return position

def input_position(placement=False):

        row='z'
        column=1000
        orientation=''

        while row not in allowed_rows:
                             
                row=input('enter row')

        while column not in column_list:

                try:
                        column=int(input('enter column'))

                except ValueError:
                        pass

        if placement==True:
                
                
                while orientation not in ['v', 'h']:

                        orientation=input('enter orientation(v or h)')
                

                return row, column, orientation

        return row, column
	

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
        self.targets=[]
        
        
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

class Target:

        def __init__(self, position):

                self.direction=0
                self.position=position
                self.right=1
                self.left=1
                self.up=1
                self.down=1
                
                
                
                #set row/column limits for firing

                self.row, self.row_letter, self.column=position2grid(position)
                self.max_left=grid2position(self.row_letter, 0)
                self.max_right=grid2position(self.row_letter, (grid_size[0]-1))
                self.max_top=grid2position('a',self.column)
                self.max_bottom=grid2position(row_letters[(grid_size[0]-1)], self.column)

                pass
           
        def __str__(self):


                rep='Current targets='+str(self.position)
                return rep
                
        def predictive_targeting(self):

                
                if self.direction==0:

                        proposed=self.position+self.right

                        if proposed <=self.max_right and proposed not in computer.already_tried:

                                fire=proposed
                                self.right+=1
                        else:
                                self.direction+=1

                if self.direction==1:

                        proposed=self.position-self.left

                        if proposed>=self.max_left and proposed not in computer.already_tried:

                                fire=proposed
                                self.left+=1
                                

                        else:
                                self.direction+=1


                if self.direction==2:

                        proposed=self.position-(self.up*grid_size[0])

                        if proposed>=self.max_top and proposed not in computer.already_tried:

                                fire=proposed
                                self.up+=1
                                

                        else:
                                self.direction+=1

                if self.direction==3:

                        proposed=self.position+(self.down*grid_size[0])

                        if proposed<=self.max_bottom and proposed not in computer.already_tried:

                                fire=proposed
                                self.down+=1
                                
                
                return fire


class Ship:

       

    def __init__(self, length):

        self.type=length
        self.length=length
        self.hp=length
        self.cells=[]
        orientation=['vertical', 'horizontal']
        self.direction=random.choice(orientation)
        
    def add_to_grid(self, grid, mode='Auto'):

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
    


      
def player_move(player, player_target, computer):

        allowed=False
        
        while allowed==False:

                row, column=input_position(False)
                                
                                            
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

                                                                                              
                        #is tge computer locked onto a target?
                        
                        if computer.targeting:

                                
                                position=(computer.targets[-1]).predictive_targeting()
                     

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
                                target=Target(position)
                                                           
                                computer.targets.append(target)
                                
                                
                        computer.targeting=True
                                              
                                               
                        for ship in player.ships:
                                if position in ship.cells:
                                        ship.hp-=1
                                        if ship.hp==0:
                                                print ('computer destroyed ', ship_types[ship.type])
                                                for cell in ship.cells:
                                                        player.box[cell]='X'
                                                        computer.hit.remove(cell)

                                                player.ships.remove(ship)
                                                if computer.hit==[]: 
                                                	computer.targeting=False
                                                else:
                                                	 computer.targeting=True
                                                	 
                                                	 target=Target(computer.hit[-1])
                                                	 computer.targets.insert(0, target)
                                                	 
                                                
                                                
                                            
                                                computer.targets.pop()
                
        else:
                print ('computer missed')
                player.box[position]='M'
                
                computer.already_tried.append(position)
                computer.missed.append(position)
                if computer.targets!=[]:
                        computer.targets[-1].direction+=1
                

        

#game starts

player=Grid()
player_target=Grid()
computer=Grid()
    
create_fleet(player)
create_fleet(computer)

while True:

        
       
        player.print_grid()
        print ('\n')
        player_target.print_grid()
        player_move(player, player_target, computer)
        computer_move(player, player_target, computer)
      
      


        
