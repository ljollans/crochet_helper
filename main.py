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
    pattern = {'rnd 1': f'{base_number[stitch]} {stitch}'}
    for rnd in range(2, rounds):
        if rnd ==2:
            pattern['rnd 2'] = f'{base_number[stitch]} inc ({base_number[stitch]*2} stitches)'
        else:
            pattern[f'rnd {rnd}'] = f'*{rnd-2} {stitch}, inc* {base_number[stitch]} times ({base_number[stitch] * rnd} stitches)'
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


def draw_line(angle=45, x1=0, y1=0, length=1):
    angle_radians = math.radians(angle)
    x2 = x1 + length * math.cos(angle_radians)
    y2 = y1 + length * math.sin(angle_radians)
    plt.plot([x1, x2], [y1, y2], linewidth=2, color="blue")
    return x2, y2


def figure_helper(line_list, circle=True):
    fig, ax = plt.subplots()
    distances = []
    if len(line_list)>0:
        for linespecs in line_list:
            angle = linespecs[2]
            x1 = linespecs[0]
            y1 = linespecs[1]
            length = linespecs[3]
            x2, y2 = draw_line(angle=angle, x1=x1, y1=y1, length=length)
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
    name, pattern = crochet_circle('hdc', 15)
    print(name)
    for round, instructions in pattern.items():
        print(f"{round}: {instructions}")