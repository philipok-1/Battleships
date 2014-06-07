#Battleships


import random, sys, pickle


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

def set_boundaries(position):

         row, row_letter, column=position2grid(position)
         max_left=grid2position(row_letter, 0)
         max_right=grid2position(row_letter, (grid_size[0]-1))
         max_top=grid2position('a',column)
         max_bottom=grid2position(row_letters[(grid_size[0]-1)], column)

         return max_left, max_right, max_top, max_bottom

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
        self.hit=[]
        self.move_history=[]
        self.targeting=False
        self.targets=[]
        
        
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

        def __init__(self, position, computer):

                self.direction=0
                self.position=position
                self.right=1
                self.left=1
                self.up=1
                self.down=1
                
                
                #set row/column limits for firing

                self.max_left, self.max_right, self.max_top, self.max_bottom=set_boundaries(self.position)

                pass
           
        def __str__(self):


                rep='Current targets='+str(self.position)
                return rep
                
        def predictive_targeting(self, computer):

                
                                
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
        orientation=['v', 'h']
        self.direction=random.choice(orientation)
        
    def add_to_grid(self, grid, mode):

        limit=((grid_size[0])-(self.length))
            
        occupied=True
        while occupied==True:

            boxes=[]
            boxhit=False

            if mode=='auto':
                    
                start_position=random_shot()
                max_left, max_right, max_top, max_bottom=set_boundaries(start_position)

            else:
                    print('Input position and orientation for', ship_types[self.type])
                    row, column, self.direction=input_position(True)
                    start_position=grid2position(row, column)
                    max_left, max_right, max_top, max_bottom=set_boundaries(start_position)
                                
            
            for i in range (self.length):

                if self.direction=='h':
                    boxes.append(start_position+i)
                else: boxes.append(start_position+((grid_size[0])*i))
                 
            for box in boxes:
                if box in grid.occupied: boxhit=True

                if self.direction=='h' and box>max_right: boxhit=True
                elif self.direction=='v' and box>max_bottom: boxhit=True
                
            if boxhit==True:
                
                occupied=True
                
                    
            else:

                occupied=False
                self.cells=boxes
                boxes=[]
                
        for j in range (self.length):

            if self.direction=='h':
                    
                grid.box[start_position+j]=[self.type]
                grid.occupied.append(start_position+j)

            else:
                
                grid.box[start_position+((grid_size[0])*j)]=[self.type]
                grid.occupied.append(start_position+(grid_size[0]*j))


                
        return grid.box, grid.occupied
				                            
					  

def create_fleet(grid, mode):
        
        acc=Ship(5)
        destroyer=Ship(4)
        frigate=Ship(3)
        cruiser=Ship(2)
        sub=Ship(1)
        
        
        ships=[acc, destroyer, frigate, cruiser, sub]

        for ship in ships:
                grid.box, grid.occupied=ship.add_to_grid(grid, mode)
                grid.ships.append(ship)
                if mode=='manual': grid.print_grid()

                
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

                                                                                              
                        #is the computer locked onto a target?
                        
                        if computer.targeting:

                                
                                position=(computer.targets[-1]).predictive_targeting(computer)
                     

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
                                target=Target(position, computer)
                                                           
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
                                                	 
                                                	 target=Target(computer.hit[-1], computer)
                                                	 computer.targets.insert(0, target)
                                                	 
                                                
                                                
                                            
                                                computer.targets.pop()
                
        else:
                print ('computer missed')
                player.box[position]='M'
                
                computer.already_tried.append(position)
                
                if computer.targets!=[]:
                        computer.targets[-1].direction+=1
                

        

#game starts

def main():

        player=Grid()
        player_target=Grid()
        computer=Grid()
            
        create_fleet(player, mode='manual')
        create_fleet(computer, mode='auto')

        game_over=False
        player.ships=[]

        p=open('moves.pickle')
        player_moves=pickle.load(p)
        p.close()

        while game_over==False:
       
                player.print_grid()
                print ('\n')
                player_target.print_grid()
                player_move(player, player_target, computer)
                computer_move(player, player_target, computer)
                if player.ships==[] or computer.ships==[]:
                        game_over=True

        if player.ships==[]:
                print ('Computer has won.  Play again?')
        elif computer.ships==[]:
                print ('You won.  Play again?')
        play=input()
        if play=='y':
                main()
        else: sys.exit()



main()

                
        

        


        
