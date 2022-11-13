import numpy as np
import random
import keyboard

class Field():
    
    def __init__(self,size):
        self.size = size
        self.field=[[0 for i in range(self.size)] for j in range(self.size)]
        self.former_field=self.field[:]
        self.turn = 1
        self.updated=False


    def draw(self):
        for i in range(self.size):
            print(self.field[i])
        print("------------")

    #iが行、jが列を表す。
    def createBlock(self,i,j):
        self.field[i][j]=2

    #空いているセルにランダムにブロックを作る
    def createRandomBlock(self):
        is_zero=False
        while(is_zero==False):
            i=random.randrange(self.size)
            j=random.randrange(self.size)
            is_zero=self.isZero(i,j)
        self.createBlock(i,j)

    #該当するブロックが空であるか調べる。
    def isZero(self,i,j):
        return self.field[i][j]==0

    #(上に)移動させる。
    def slide(self):
        for j in range(self.size):
            column = [row[j] for row in self.field]
            column = sort2048(column)
            for i in range(self.size):
                self.field[i][j]=column[i]

    def up(self):
        self.rotate(0)
        self.slide()
        self.rotate(0)

    def down(self):
        self.rotate(2)
        self.slide()
        self.rotate(2)

    def left(self):
        self.rotate(3)
        self.slide()
        self.rotate(1)

    def right(self):
        self.rotate(1)
        self.slide()
        self.rotate(3)

    def update(self):
        if(self.field!=self.former_field):
            self.turn+=1
            self.updated=True

    def update2(self):
        self.former_field=self.field
        self.updated=False

    #反時計回りに90*n度回転
    def rotate(self,n):
        arr = np.array(self.field)
        self.field = np.rot90(arr,n).tolist()

    #終了判定。動かせなければ終わり。
    def is_end(self):
        is_end = True
        
        self.up()
        if(self.former_field!=self.field):
            is_end = False
        else:
            self.down()
            if(self.former_field!=self.field):
                is_end = False
            else:
                self.left()
                if(self.former_field!=self.field):
                    is_end = False
                else:
                    self.right()
                    if(self.former_field!=self.field):
                        is_end = False
        if(is_end==False):
            self.field=self.former_field[:]

        return is_end

#配列をスライドさせたときの関数
def sort2048(list):

    edge=-1

    new_list = [0 for i in range(len(list))]
    is_fix = new_list[:]

    for i in range(len(list)):
        if(list[i]!=0):
            if(edge==-1):
                new_list[0]=list[i]
                edge=0
            else:
                if(list[i]!=new_list[edge] or is_fix[edge]==True):
                    new_list[edge+1]=list[i]
                    edge+=1
                else:
                    new_list[edge]*=2
                    is_fix[edge]=True

    return new_list

def main():

    field = Field(4)

    field.createRandomBlock()
    print("turn:" + str(field.turn))
    field.draw()

    field.former_field=field.field[:]


    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP and event.name == 'up':
            field.up()
        elif event.event_type == keyboard.KEY_UP and event.name == 'down':
            field.down()
        elif event.event_type == keyboard.KEY_UP and event.name == 'left':
            field.left()
        elif event.event_type == keyboard.KEY_UP and event.name == 'right':
            field.right()
        
        if(event.event_type == keyboard.KEY_UP):
            field.update()
            if(field.updated):
                field.createRandomBlock()
                field.update2()
                print("turn:" + str(field.turn))
                field.draw()

            if(field.is_end()):
                print("End! your score is:" + str(field.turn))
                exit()

    return
    

if __name__ == "__main__":
    main()