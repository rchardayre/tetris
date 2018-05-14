## TETRIS ###
import pyglet
import config
import grid
import json
import sys
import time
import argparse


def draw():
    global window
    window.clear()
    pyglet.gl.glClearColor(0, 0, 0, 0)
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    tetris_grid.draw()


def update(delta_t):
    if config.is_replay:
        global playback_idx
        for move in recordData['moves'][playback_idx]:
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

        playback_idx = playback_idx + 1
    if tetris_grid.clock_update() == grid.GAME_OVER:
        if config.is_record:
            with open("./record.json", 'w') as f:
                json.dump(recordData, f)
            
        print("GAME OVER")
        print("FINAL SCORE : %d" % tetris_grid.score)
        exit(0)

 
def run_tetris(is_record, is_simulation, playback_file, frequency):
    global recordData
    
    recordData = {'moves' : [], 'forms' : []}
     
    if playback_file != '':
        if is_record:
            print("Cannot record a playback")
            is_record = False
        try:
            with open(playback_file) as f:
                recordData = json.load(f)
                config.is_replay = True
                global playback_idx
                playback_idx = 0
        except Exception:
            print("Invalid playback file")
            sys.exit(1)

    config.is_record = is_record
    config.is_simulation = is_simulation
    config.update_frequency = frequency

    global tetris_grid
    tetris_grid = grid.Grid(config.nb_block_horizontal, config.nb_block_vertical, recordData)
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

    
if __name__ == "__main__":
    print("Launching Tetris...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulation', dest='simulation', action='store_true')
    parser.add_argument('--playback', dest='playback_file', type=str, default ='')
    parser.add_argument('--record', dest='record', action='store_true')
    parser.add_argument('--freq', dest='frequency', type=float, default=0.2)

    options = parser.parse_args()

    run_tetris(options.record, options.simulation, options.playback_file, options.frequency)    

    
