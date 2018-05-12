## TETRIS ###
import pyglet
import config
import grid

tetris_grid = []
window = pyglet.window.Window(height=config.window_height, width=config.window_width)

def draw():
    """
    Clears screen and then renders our list of ball objects
    :return:
    """
    window.clear()
    pyglet.gl.glClearColor(0, 0, 0, 0)
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    tetris_grid.draw()


def update(time):
    if tetris_grid.clock_update() == grid.GAME_OVER:
        print("GAME OVER")
        print("FINAL SCORE : %d" % tetris_grid.score)
        exit(0)


if __name__ == "__main__":
    print("Launching Tetris...")

    tetris_grid = grid.Grid(config.nb_block_horizontal, config.nb_block_vertical)

    @window.event
    def on_draw():
        draw()
    
    def on_key_press(symbol, modifiers):
         tetris_grid.key_pressed(symbol, modifiers)

    window.push_handlers(on_key_press)
    pyglet.clock.schedule_interval(update, 1/8)
    pyglet.app.run()

    
    

    
