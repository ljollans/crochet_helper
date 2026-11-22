import matplotlib.pyplot as plt

# sc : single crochet
# hdc : half-double crochet
# dc : double crochet
# tc : treble crochet
# ss : slip stitch
# sk : skip

base_number = {
    'sc':6,
    'hdc':10,
    'dc':15,
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

def crochet_circle(stitch, rounds):
    pattern = {'rnd 1': f'{base_number[stitch]} {stitch}'}
    for rnd in range(2, rounds):
        if rnd ==2:
            pattern['rnd 2'] = f'{base_number[stitch]} inc ({base_number[stitch]*2} stitches)'
        else:
            pattern[f'rnd {rnd}'] = f'*{rnd-2} {stitch}, inc* {base_number[stitch]} times ({base_number[stitch] * rnd} stitches)'
    return f"{stitch_name[stitch]} circle with {rounds} rounds:", pattern
    

def plot_circle():
    # Create a circle using matplotlib
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), 1, color='blue', fill=False)
    ax.add_artist(circle)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal', adjustable='box')
    plt.title('Circle')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    name, pattern = crochet_circle('hdc', 15)
    print(name)
    for round, instructions in pattern.items():
        print(f"{round}: {instructions}")