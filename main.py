import matplotlib.pyplot as plt
import math
import numpy as np

# sc : single crochet
# hdc : half-double crochet
# dc : double crochet
# tc : treble crochet
# ss : slip stitch
# sk : skip

base_number = {
    'sc':6,
    'hdc':8,
    'dc':12, # often 16
    'tc':18
}

stitch_name = {
    'sc' : 'single crochet',
    'hdc' : 'half-double crochet',
    'dc' : 'double crochet',
    'tc' : 'treble crochet',
    'ss' : 'slip stitch',
    'sk' : 'skip',
}

stitch_height = {
    'sc' : 1,
    'hdc' : 1.5,
    'dc' : 2,
    'tc' : 'treble crochet',
}

increase_spread_angle = 20

def crochet_circle(stitch, rounds):
    pattern = {'rnd 1': {
        'text':f'{base_number[stitch]} {stitch}',
        'count':base_number[stitch],
        'stitches':[stitch]*base_number[stitch]}
        }
    for rnd in range(2, rounds+1):
        if rnd ==2:
            pattern['rnd 2'] = {
                'text':f'{base_number[stitch]} inc ({base_number[stitch]*2} stitches)',
                'count':base_number[stitch]*2,
                'stitches':[f"{stitch}_inc"]*base_number[stitch]}
        else:
            stitch_order = [stitch]*(rnd-2) + [f"{stitch}_inc"]
            pattern[f'rnd {rnd}'] ={
                'text': f'*{rnd-2} {stitch}, inc* {base_number[stitch]} times ({base_number[stitch] * rnd} stitches)',
                'count':base_number[stitch] * rnd,
                'stitches':stitch_order * base_number[stitch]}
    return f"{stitch_name[stitch]} circle with {rounds} rounds:", pattern


def three_ss_inc():
    # 3 ss between every dc can replace increases 
    # this will create an arch
    # this will only work on the lower rounds i think
    pattern = {}
    return pattern

def one_ss_inc():
    # 1 ss between every dc can replace increases 
    # this will only work on the lower rounds i think
    pattern = {}
    return pattern




def plot_circle(radius=1, center=[0,0]):
    return plt.Circle((center[0], center[1]), radius, color='blue', fill=False)


def add_cross(x2, y2, cross_length, orig_angle):
    # cap side 1
    angle_radians = math.radians(orig_angle+90)
    cap1_x = x2 + cross_length * math.cos(angle_radians)
    cap1_y = y2 + cross_length * math.sin(angle_radians)

    # cap side 2
    angle_radians = math.radians(orig_angle-90)
    cap2_x = x2+ cross_length * math.cos(angle_radians)
    cap2_y = y2 + cross_length * math.sin(angle_radians)

    plt.plot([cap1_x, cap2_x], [cap1_y, cap2_y], linewidth=2, color="blue")


def draw_stitch(linespecs):

    if not 'x1' in linespecs:
        linespecs['x1']=0
    if not 'y1' in linespecs:
        linespecs['y1']=0
    if not 'length' in linespecs:
        linespecs['length']=1
    if not 'bottom_clearance' in linespecs:
        linespecs['bottom_clearance']=0
    if not 'cap' in linespecs:
        linespecs['cap']=True
    if not 'cross' in linespecs:
        linespecs['cross']=True

    x1 = linespecs['x1']
    y1 = linespecs['y1']
    length = linespecs['length']
    angle = linespecs['angle']
    round_height = linespecs['round_height']
    stitch = linespecs['stitch']

    x1_, y1_ =  get_point2(x1, y1, angle, round_height)
    if stitch=='dc':
        x2, y2 = draw_dc(x1_, y1_, angle, length, cap_prop = 0.1, cross_prop = 0.1)
    elif stitch=='dc_inc':
        x2, y2 =  draw_dc_inc(x1_, y1_, angle, length, cap_prop = 0.1, cross_prop = 0.1)
    else:
        print('unknown stitch type', stitch)
    return x2, y2


def get_point2(x1, y1, angle, length):
    angle_radians = math.radians(angle)
    x2 = x1 + length * math.cos(angle_radians)
    y2 = y1 + length * math.sin(angle_radians)
    return x2, y2

def draw_dc(x1, y1, angle, length, cap_prop = 0.1, cross_prop = 0.1):
    x2, y2 =  get_point2(x1, y1, angle, length)
    plt.plot([x1, x2], [y1, y2], linewidth=2, color="blue")
    add_cross(x2, y2, cross_length=(length*cap_prop), orig_angle=angle)
    x3 = (x1 + x2)/2
    y3 = (y1 + y2)/2
    add_cross(x3, y3, cross_length=(length*cross_prop), orig_angle=angle)
    return x2, y2

def draw_dc_inc(x1, y1, angle, length, cap_prop = 0.1, cross_prop = 0.1):
    x2a, y2a = draw_dc(x1, y1, angle-increase_spread_angle, length, cap_prop = cap_prop, cross_prop = cross_prop)
    x2b, y2b = draw_dc(x1, y1, angle+increase_spread_angle, length, cap_prop = cap_prop, cross_prop = cross_prop)
    return max(x2a, x2b), max(y2a, y2b)


def draw_round(stitches, rnd_height=0.1, stitch_height=1, starting_angle=0):
    line_list = []
    previous_inc = 0
    angle = starting_angle
    angle_increments = (360/len(stitches))

    for i in range(len(stitches)):

        angle = starting_angle + angle_increments*i

        # after an increase
        if not stitches[i] in ['dc_inc']:
            if i<(len(stitches)-1):
                if stitches[i+1] in ['dc_inc']:
                    angle -= angle_increments*0.1
            else:
                angle += angle_increments*0.1

        # # before an increase
        # if i<(len(stitches)-1):
        #     if stitches[i+1] in ['dc_inc']:
        #         angle -= angle_increments*0.1

        line_list.append({'x1':0, 
                        'y1':0,
                        'round_height': rnd_height,
                        'angle':angle, 
                        'length':stitch_height,
                        'stitch':stitches[i]})



    return line_list


def draw_multiround(pattern, rnd_height=1, stitch_height=0.8):
    bottom_clearance = rnd_height-stitch_height
    line_list = []
    round_counter = 0
    starting_angle = 0
    for rnd, instructions in pattern.items():
        stitches = instructions['stitches']
        line_list += draw_round(stitches, 
                                rnd_height=(round_counter*rnd_height)+bottom_clearance, 
                                stitch_height=stitch_height,
                                starting_angle = starting_angle)
        round_counter+=1
        if stitches[0] in ['dc_inc']:
            starting_angle = increase_spread_angle
        else:
            starting_angle = 0


    return line_list


def figure_helper(line_list, circle=True):
    fig, ax = plt.subplots(figsize=[20,20])
    distances = []
    if len(line_list)>0:
        for linespecs in line_list:
            x2, y2 = draw_stitch(linespecs)
            distances.append(np.linalg.norm(np.array([0,0])-np.array([abs(x2),abs(y2)])))
    # 
    limits = np.nanmax(np.array(distances))
    if circle:
        circle = plot_circle(radius = limits)
        ax.add_artist(circle)
    limits = limits*1.1
    ax.set_xlim(-limits, limits)
    ax.set_ylim(-limits, limits)
    ax.set_aspect('equal', adjustable='box')
    plt.title('Circle')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    name, pattern = crochet_circle('dc', 6)
    print(name)
    for round, instructions in pattern.items():
        print(f"{round}: {instructions['text']}")

    figure_helper(draw_multiround(pattern), circle=False)