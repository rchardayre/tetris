## TETRIS ###
import pyglet
import config
import grid
import json
import sys

MOVE_LEFT = "L"
MOVE_RIGHT = "R"
MOVE_DOWN = "D"
ROTATE_CLOCKWISE = "T"
ROTATE_COUNTERCLOCKWISE = "Y"
HARD_DROP = "H"


tetris_grid = []
record = {'moves' : [], 'forms' : []}
replay_idx = 0

if not config.is_simulation:
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
    if config.is_replay:
        global replay_idx
        for move in record['moves'][replay_idx]:
            #time.sleep(config.update_frequency / 10)
            if move == MOVE_LEFT:
                tetris_grid.move_left()
            elif move == MOVE_RIGHT:
                tetris_grid.move_right()
            elif move == ROTATE_CLOCKWISE:
                tetris_grid.rotate_clockwise()
            elif move == MOVE_DOWN:
                tetris_grid.move_down()
            elif move == ROTATE_COUNTERCLOCKWISE:
                tetris_grid.rotate_counteclockwise()
            elif move == HARD_DROP:
                tetris_grid.hard_drop()

        replay_idx = replay_idx + 1
    if tetris_grid.clock_update() == grid.GAME_OVER:
        if config.is_record:
            with open("./record.json", 'w') as f:
                json.dump(record, f)
            
        print("GAME OVER")
        print("FINAL SCORE : %d" % tetris_grid.score)
        exit(0)


if __name__ == "__main__":
    print("Launching Tetris...")

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename) as f:
            record = json.load(f)
            config.is_record = False
            config.is_replay = True

    tetris_grid = grid.Grid(config.nb_block_horizontal, config.nb_block_vertical, record)

    if config.is_simulation:
        while(True):
            update(0)
    else:
        @window.event
        def on_draw():
            draw()
    
        def on_key_press(symbol, modifiers):
            if not config.is_replay:
                tetris_grid.key_pressed(symbol, modifiers)

        window.push_handlers(on_key_press)
        pyglet.clock.schedule_interval(update, config.update_frequency)

    pyglet.app.run()

    
    

    
