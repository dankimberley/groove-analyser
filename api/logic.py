import grid

# returns the timing differences for an input array and grid array. e.g. compare_timing([102, 399], [100, 400]) returns [2, -1]
def compare_timing(input, grid):
    difs = []
    for i in range(len(input)):
        difs.append(input[i] - grid[i])
    return difs

def convert_abs_to_rel(difs, tempo):
    rels = []
    beat = grid.bpm_to_ms(tempo)
    for dif in difs:
        rel = dif / beat
        percentage = f"{rel * 100:.1f}%"
        rels.append(percentage)
    return rels    

def get_average(array):
    average = sum(array) / len(array)
    return average

# test = compare_timing([102, 399], [100, 400])
# print(test)