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

def crochet_circle(stitch, rounds):
    pattern = {'rnd 1': {
        'text':f'{base_number[stitch]} {stitch}',
        'count':base_number[stitch]}
        }
    for rnd in range(2, rounds):
        if rnd ==2:
            pattern['rnd 2'] = {
                'text':f'{base_number[stitch]} inc ({base_number[stitch]*2} stitches)',
                'count':base_number[stitch]*2}
        else:
            pattern[f'rnd {rnd}'] ={
                'text': f'*{rnd-2} {stitch}, inc* {base_number[stitch]} times ({base_number[stitch] * rnd} stitches)',
                'count':base_number[stitch] * rnd}
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


def draw_line(linespecs):

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

    angle_radians = math.radians(linespecs['angle'])
    x2 = linespecs['x1'] + linespecs['length'] * math.cos(angle_radians)
    y2 = linespecs['y1'] + linespecs['length'] * math.sin(angle_radians)
    x1_ = linespecs['x1'] + linespecs['bottom_clearance'] * math.cos(angle_radians)
    y1_ = linespecs['y1'] + linespecs['bottom_clearance'] * math.sin(angle_radians)
    plt.plot([x1_, x2], [y1_, y2], linewidth=2, color="blue")

    actual_length = np.linalg.norm(np.array([abs(x1_),abs(y1_)])-np.array([abs(x2),abs(y2)]))

    if linespecs['cap']:
        cap_prop = 0.1
        add_cross(x2, y2, cross_length=(actual_length*cap_prop), orig_angle=linespecs['angle'])

    if linespecs['cross']:
        cross_prop = 0.1
        
        x3 = (x1_ + x2)/2
        y3 = (y1_ + y2)/2
        add_cross(x3, y3, cross_length=(actual_length*cross_prop), orig_angle=linespecs['angle'])

    return x2, y2


def draw_round(rnd, rnd_height, num_stitches):
    line_list = []
    for st in range(num_stitches):
        line_list.append({'x1':0, 
                        'y1':0,
                        'angle':(360/num_stitches)*st, 
                        'length':rnd_height*(rnd+1),
                        'bottom_clearance': (rnd_height*(rnd+0.5))})
    return line_list


def draw_multiround(num_stitches_list, rnd_height=1):
    line_list = []
    for rnd, num_stitches in enumerate(num_stitches_list):
        line_list += draw_round(rnd, rnd_height, num_stitches)
    return line_list


def figure_helper(line_list, circle=True):
    fig, ax = plt.subplots(figsize=[20,20])
    distances = []
    if len(line_list)>0:
        for linespecs in line_list:
            x2, y2 = draw_line(linespecs)
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
    name, pattern = crochet_circle('dc', 5)
    #print(name)
    #for round, instructions in pattern.items():
    #    print(f"{round}: {instructions}")

    figure_helper(draw_multiround([spec['count'] for spec in pattern.values()], rnd_height=20), circle=False)