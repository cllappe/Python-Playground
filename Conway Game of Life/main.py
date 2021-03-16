import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Values: 255 = On, 0 = Off

def addGlider(i, j, grid):
    """ Adds a standardized grid """
    glider = np.array([[0,0,255],
                       [255,0,255],
                       [0,255,255]])
    grid[i:i+3, j:j+3] = glider
    return grid

def createGliderGrid(N):
    grid = np.zeros(N*N).reshape(N, N)
    for i in range(0,N,3):
        for j in range (0,N,3):
            grid = addGlider(i,j,grid)
    return grid

def randomGrid(N):
    return np.random.choice([0,255], N*N, p=[0.5, 0.5]).reshape(N,N)

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            if grid[i,j] == 255:
                if (total < 2) or (total > 3):
                    newGrid[i,j] = 0
                else:
                    if total == 3:
                        newGrid[i,j] = 255
    
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life Sim")
    parser.add_argument('--grid-size', dest='N', required=False, default='3')
    parser.add_argument('--interval', dest='interval', required=False, default='180')
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    if args.N and args.glider:
        if int(args.N) % 3 != 0:
            print("ERROR: To use the glider the size of the grid must be a multipul of 3.")
            return 1
    if args.glider:
        grid = createGliderGrid(int(args.N))
    else:
        grid = randomGrid(int(args.N))

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, int(args.N)), frames=10, interval=int(args.interval), save_count=50)
    plt.show()
    return 0

if __name__ == '__main__':
    main()