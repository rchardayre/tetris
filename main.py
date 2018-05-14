## TETRIS ###
import pyglet
import config
import grid
import json
import sys
import time
import argparse

tetris_grid = []
record = {'moves' : [], 'forms' : []}
replay_idx = 0

def draw():
    global window
    window.clear()
    pyglet.gl.glClearColor(0, 0, 0, 0)
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    tetris_grid.draw()


def update(delta_t):
    if config.is_replay:
        global replay_idx
        for move in record['moves'][replay_idx]:
            #time.sleep(config.update_frequency / 10)
            if move == grid.MOVE_LEFT:
                tetris_grid.move_left()
            elif move == grid.MOVE_RIGHT:
                tetris_grid.move_right()
            elif move == grid.ROTATE_CLOCKWISE:
                tetris_grid.rotate_clockwise()
            elif move == grid.MOVE_DOWN:
                tetris_grid.move_down()
            elif move == grid.ROTATE_COUNTERCLOCKWISE:
                tetris_grid.rotate_counteclockwise()
            elif move == grid.HARD_DROP:
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulation', dest='simulation', action='store_true') 
    parser.add_argument('--playback', dest='playback_file', type=str, default ='')
    parser.add_argument('--record', dest='record', action='store_true')
    parser.add_argument('--freq', dest='frequency', type=float, default=0.2)
    
    options = parser.parse_args()
    
    if len(sys.argv) > 1:
        filename = options.playback_file
        if filename != '':
            if options.record:
                print("Cannot record a playback")
                options.record = False
            try:
                with open(filename) as f:
                    record = json.load(f)
                    config.is_replay = True
            except Exception:
                print("Invalid playback file")
                sys.exit(1)

    config.is_record = options.record
    config.is_simulation = options.simulation
    config.update_frequency = options.frequency

    tetris_grid = grid.Grid(config.nb_block_horizontal, config.nb_block_vertical, record)
    if config.is_simulation:
        while(True):
            update(0)
    else:
        global window
        window = pyglet.window.Window(height=config.window_height, width=config.window_width)
        @window.event
        def on_draw():
            draw()
    
        def on_key_press(symbol, modifiers):
            if not config.is_replay:
                tetris_grid.key_pressed(symbol, modifiers)

        window.push_handlers(on_key_press)
        pyglet.clock.schedule_interval(update, config.update_frequency)

    pyglet.app.run()

    
    

    
