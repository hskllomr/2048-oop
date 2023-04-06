import tkinter as tk
import colors as c
import random

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()#çerçeve oluştur
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=2, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))  # yüksekliği ayarla
        self.make_gui() #satır ve sütunları oluştur
        self.start_game()#değerleri gir
        self.master.bind("<Left>",self.left)#tuş kombinasyonlarına göre istenilen fonksiyonları çağır
        self.master.bind("<Right>",self.right)
        self.master.bind("<Up>",self.up)
        self.master.bind("<Down>",self.down)
        self.mainloop()

    def make_gui(self):
        self.cells=[]
        for i in range(4):#her bir hücre için liste oluştur
            row=[]
            for j in range(4):#
                cell_frame=tk.Frame(self.main_grid,bg=c.EMPTY_CELL_COLOR,width=150,height=150)#her bir hücrenin genişliği yüksekliği ayarla
                cell_frame.grid(row=i,column=j,padx=5,pady=5)#hücreyi oluştur(aralarındaki uzunluk dahil)
                cell_number=tk.Label(self.main_grid,bg=c.EMPTY_CELL_COLOR)#hücrenin sayısı
                cell_number.grid(row=i,column=j)#hücreye yerleştir
                cell_data={"frame":cell_frame,"number":cell_number}#verileri sözlüğün içine yerleştir(daha sonra değerlerin atanması için kullanılacak)
                row.append(cell_data)#listeye ekle
            self.cells.append(row)#tek bir liste haline getir

        score_frame=tk.Frame(self)#skor penceresi
        score_frame.place(relx=0.5,y=45,anchor="center")#konumunu ayarla
        tk.Label(score_frame,text="Score",font=c.SCORE_LABEL_FONT).grid(row=0)#"skor" yazısını yazdır
        self.score_label=tk.Label(score_frame,text="0",font=c.SCORE_FONT)#skor
        self.score_label.grid(row=1)#skoru yerleştir

    def start_game(self):
        self.matrix=[[0]*4 for i in range(4)]#dörde dört matris
        row=random.randint(0,3)
        col=random.randint(0,3)
        self.matrix[row][col] = 2#rastgele konuma 2 değerinin koy
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])#hücrenin rengini 2'ye karşılık gelen değeri koy
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2],fg=c.CELL_NUMBER_COLORS[2],font=c.CELL_NUMBER_FONTS[2],text="2")#numarayı ve rengini ayarla

        while (self.matrix[row][col] != 0):  # 0'dan farklı olduğu sürece değer üret
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2],
                                                 font=c.CELL_NUMBER_FONTS[2], text="2")
        self.score = 0

    def stack(self):#sağa doğru bir birim kaydır
        new_matrix=[[0]*4 for k in range(4)]
        for i in range(4):
            fill_position=0
            for j in range(4):
                if self.matrix[i][j]!=0:
                    new_matrix[i][fill_position]=self.matrix[i][j]
                    fill_position=fill_position+1
        self.matrix=new_matrix

    def combine(self):#ardışık değerleri topla ve skoru arttır
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j]!=0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j]*=2
                    self.matrix[i][j+1]=0
                    self.score+=self.matrix[i][j]

    def reverse(self):#matrisi ters çevir(geçici liste oluştur her bir listeyi ters çevir ve yeni matrisi oluştur)
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix=new_matrix

    def transpose(self):#transpozesini al(geçiçi matris oluştur güncel matrisin yer değişikliğini geçici matrise ata,matrisi yenile)
        new_matrix=[[0]*4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j]=self.matrix[j][i]
        self.matrix=new_matrix

    def add_new_tile(self):#2 ya da 4'ü boş kutuya yerleştir
        row=random.randint(0,3)
        col=random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col]=random.choice([2,4])

    def update_gui(self):#matrix listesindeki değişiklikleri ekrana yazdırma fonksiyonu(tuş komutları sonrası değişikliği ekrana yazdır)
        for i in range(4):
            for j in range(4):
                cell_value=self.matrix[i][j]
                if cell_value==0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)#renk
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR,text="")#yazı
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])#renk
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value],fg=c.CELL_NUMBER_COLORS[cell_value],font=c.CELL_NUMBER_FONTS[cell_value],text=str(cell_value))#yazı

        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def right(self,event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def up(self,event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def down(self,event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def horizontal_move_exist(self):#ardışık yatay bloklar eşitse true döndür
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j]==self.matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exists(self):#ardışık dikey bloklar eşitse true döndür
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j]==self.matrix[i+1][j]:
                    return True
        return False

    def game_over(self):#eğer tuş komutlarından sonra matrisde 2048 değeri varsa kazandın etiketini yazdır
        if any(2048 in row for row in self.matrix):
            game_over_frame=tk.Frame(self.main_grid,borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(game_over_frame,text="You win",bg=c.WINNER_BG,fg=c.GAME_OVER_FONT_COLOR,font=c.GAME_OVER_FONT).pack()

        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exist() and not self.vertical_move_exists():#eğer matrisdeki bir değer 0'a eşitse ve hareket edecek yeri kalmamışsa oyun bitti yazdır.
            game_over_frame=tk.Frame(self.main_grid,borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(game_over_frame,text="Game Over",bg=c.LOSER_BG,fg=c.GAME_OVER_FONT_COLOR,font=c.GAME_OVER_FONT).pack()


def main():
    Game()

if __name__ == "__main__":
    main()





