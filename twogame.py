import random
import tkinter as tk
from tkinter import messagebox

# Diccionario de colores para los números del juego
COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}


class Game2048(tk.Frame):

  def __init__(self):
    tk.Frame.__init__(self)
    self.grid()
    self.master.title("2048 - Python Tkinter")
    self.master.bind("<Key>", self.key_down)

    # Mapeo de teclas de flecha de Tkinter
    self.commands = {
        "Up": self.up,
        "Down": self.down,
        "Left": self.left,
        "Right": self.right,
    }

    self.board = [[0] * 4 for _ in range(4)]
    self.score = 0
    self.setup_gui()
    self.start_game()
    self.mainloop()

  def setup_gui(self):
    self.background = tk.Frame(self, bg="#bbada0", width=400, height=400)
    self.background.grid()
    self.cell_labels = []

    for i in range(4):
      row_labels = []
      for j in range(4):
        label = tk.Label(
            self.background,
            text="",
            bg="#cdc1b4",
            font=("Helvetica", 22, "bold"),
            width=4,
            height=2,
        )
        label.grid(row=i, column=j, padx=5, pady=5)
        row_labels.append(label)
      self.cell_labels.append(row_labels)

    score_frame = tk.Frame(self)
    score_frame.grid(pady=10)
    tk.Label(score_frame, text="Puntaje: ", font=("Helvetica", 14)).pack(
        side=tk.LEFT
    )
    self.score_label = tk.Label(score_frame, text="0", font=("Helvetica", 14, "bold"))
    self.score_label.pack(side=tk.LEFT)

  def start_game(self):
    self.board = [[0] * 4 for _ in range(4)]
    self.score = 0
    self.add_new_tile()
    self.add_new_tile()
    self.update_gui()

  def add_new_tile(self):
    empty_cells = [
        (i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0
    ]
    if empty_cells:
      i, j = random.choice(empty_cells)
      self.board[i][j] = 2 if random.random() < 0.9 else 4

  def update_gui(self):
    for i in range(4):
      for j in range(4):
        val = self.board[i][j]
        bg_color, fg_color = COLORS.get(val, ("#3c3a32", "#f9f6f2"))
        text = str(val) if val > 0 else ""
        self.cell_labels[i][j].configure(
            text=text, bg=bg_color, fg=fg_color
        )
    self.score_label.configure(text=str(self.score))

  # Lógica de movimiento auxiliar
  def stack(self):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
      position = 0
      for j in range(4):
        if self.board[i][j] != 0:
          new_board[i][position] = self.board[i][j]
          position += 1
    self.board = new_board

  def combine(self):
    for i in range(4):
      for j in range(3):
        if self.board[i][j] != 0 and self.board[i][j] == self.board[i][j + 1]:
          self.board[i][j] *= 2
          self.board[i][j + 1] = 0
          self.score += self.board[i][j]

  def reverse(self):
    self.board = [row[::-1] for row in self.board]

  def transpose(self):
    self.board = [list(row) for row in zip(*self.board)]

  # Movimientos de dirección
  def left(self):
    self.stack()
    self.combine()
    self.stack()

  def right(self):
    self.reverse()
    self.stack()
    self.combine()
    self.stack()
    self.reverse()

  def up(self):
    self.transpose()
    self.stack()
    self.combine()
    self.stack()
    self.transpose()

  def down(self):
    self.transpose()
    self.reverse()
    self.stack()
    self.combine()
    self.stack()
    self.reverse()
    self.transpose()

  # Comprobación de movimientos restantes
  def can_move(self):
    for i in range(4):
      for j in range(4):
        if self.board[i][j] == 0:
          return True
        if j < 3 and self.board[i][j] == self.board[i][j + 1]:
          return True
        if i < 3 and self.board[i][j] == self.board[i + 1][j]:
          return True
    return False

  # Manejo de eventos de teclado
  def key_down(self, event):
    key = event.keysym
    if key in self.commands:
      # Guardar estado previo para saber si hubo cambios
      old_board = [row[:] for row in self.board]

      # Ejecutar el movimiento
      self.commands[key]()

      # Si el tablero cambió, añadir nueva ficha y actualizar
      if self.board != old_board:
        self.add_new_tile()
        self.update_gui()

        # Verificar si no quedan más movimientos
        if not self.can_move():
          messagebox.showinfo("2048", "¡Juego terminado! No quedan movimientos.")


if __name__ == "__main__":
  Game2048()