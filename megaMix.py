import time
import math
import random
import heapq
from pprint import pprint

def main():
    directions = ['c', 'r']
    solved = "0000000000#1111111111#2222222222#3333333333#4444444444#5555555555#6666666666#7777777777#8888888888#9999999999#aaaaaaaaaa#bbbbbbbbbb"
    if len(solved) == 131:
        print("Good To Go Captain")
    else:
        print("STOOOOOOOOOOOOOOP HOLD IT RIGHT THERE")
    print(solved)
    # messy = twist(solved, 6, 'r')
    # messy = twist(messy, 2, 'c')
    # messy = twist(messy, 7, 'r')
    # messy = twist(messy, 1, 'c')
    # messy = twist(messy, 9, 'c')
    # messy = twist(messy, 3, 'r')
    # messy = twist(messy, 11, 'c')
    # messy = twist(messy, 8, 'r')
    # messy = twist(messy, 6, 'r')
    # messy = twist(messy, 5, 'c')
    # messy = twist(messy, 4, 'r')
    # messy = twist(messy, 9, 'c')
    # messy = twist(messy, 2, 'r')
    # essy = twist(messy, 8, 'c')
    # essy = twist(messy, 10, 'r')
    messy = mess_it_up(solved, 15)
    # starting_h = heuristic(messy, solved)
    print(messy)
    messy = messy + ":" #separator between state and moves
    solved = solved + ":"
    # gui(messy)
    # visited = {}
    # queue1 = []
    # queue2 = []
    # queue3 = []
    # heapq.heappush(queue1, (starting_h, messy))
    # heapq.heappush(queue2, (starting_h, messy))
    # heapq.heappush(queue3, (starting_h, messy))
    # banana_split_v1(queue1, solved, directions, visited)
    # banana_split_v2(queue2, solved, directions, visited)
    # banana_split_v3(queue3, solved, directions, visited)
    queue_messy = []
    queue_solved = []
    visited_messy = {}
    visited_solved = {}
    initial_heuristic = heuristic(messy, solved)
    heapq.heappush(queue_messy, (initial_heuristic, messy))
    heapq.heappush(queue_solved, (initial_heuristic, solved))
    banana_split_v4(queue_messy, queue_solved, messy, solved, directions, visited_messy, visited_solved)

def split_one(queue, current, solved, optional_directions):
    depth = 1
    for i in range(0,12):
        for j in range(0,2):
            if i < 10:
                side = str(i)
            elif i == 10:
                side = "a"
            else:
                side = "b"
            new_state = twist(current, i, optional_directions[j]) + ":" + side + str(optional_directions[j])
            total_cost = int(heuristic(new_state, solved) + depth)
            heapq.heappush(queue, (total_cost, new_state))
    return queue

def banana_split_v4(queue_messy, queue_solved, messy, solved, optional_directions, visited_messy, visited_solved):
    print("Solving...")
    current_messy = heapq.heappop(queue_messy)[1]
    current_solved = heapq.heappop(queue_solved)[1]
    can_probably_piece_it_together = False #flag letting me knoe if there has been a path found that needs to be retraced
    while(current_messy[0:131] != solved[0:131] and current_solved[0:131] != messy[0:131] and can_probably_piece_it_together == False):
        # print("current_messy\t", current_messy)
        # print("current_solved\t", current_solved)
        for i in range(0,12):
            for j in range(0,2):
                if i < 10:
                    side = str(i)
                elif i == 10:
                    side = "a"
                else:
                    side = "b"
                new_state_messy = twist(current_messy, i, optional_directions[j]) + side + str(optional_directions[j]) #could optimize this by not passing the path in and just concatenating it back on the end
                new_state_solved = twist(current_solved, i, optional_directions[j]) + side + str(optional_directions[j])
                if new_state_messy[0:131] in visited_solved: #expanding messy side
                    can_probably_piece_it_together = True
                    print("Solution messy side:")
                    # print("new_state_messy", new_state_messy)
                    # print("visited_solved[new_state_messy[0:131]]", visited_solved[new_state_messy[0:131]])
                    generate_solution(new_state_messy[132:], visited_solved[new_state_messy[0:131]], optional_directions)
                elif new_state_messy[0:131] in visited_messy:
                    pass #prevents expanding the same nodes
                else:
                    depth = ( len(new_state_messy) - 132 ) / 2
                    total_cost_messy = heuristic(new_state_messy, solved) + depth #takes heuristic and adds the "cost" of the current node
                    heapq.heappush(queue_messy, (total_cost_messy, new_state_messy))
                    visited_messy[new_state_messy[0:131]] = new_state_messy[132:]
                    # print(new_state_messy[0:131], end = "\r")
                # print("queue length:", len(queue), end = "\r")
                if can_probably_piece_it_together == False:
                    if new_state_solved[0:131] in visited_messy: #expanding solved side
                        can_probably_piece_it_together = True
                        print("Solution solved side:")
                        # print("new_state_solved", new_state_solved)
                        # print("visited_messy[new_state_solved[0:131]]", visited_messy[new_state_soved[0:131]])
                        generate_solution(visited_messy[new_state_solved[0:131]], new_state_solved[132:], optional_directions)
                    elif new_state_solved[0:131] in visited_solved:
                        pass #prevents expanding the same nodes
                    else:
                        depth = ( len(new_state_solved) - 132 ) / 2
                        total_cost_solved = heuristic(new_state_solved, messy) + depth #takes heuristic and adds the "cost" of the current node
                        heapq.heappush(queue_solved, (total_cost_solved, new_state_solved))
                        visited_solved[new_state_solved[0:131]] = new_state_solved[132:]
                # print("queue length:", len(queue), end = "\r")
        current_messy = heapq.heappop(queue_messy)[1]
        current_solved = heapq.heappop(queue_solved)[1]
        # print("messy queue length:", len(queue_messy), "solved queue length:", len(queue_solved), end = "\r")
    print("we fucking did it, bitch")
    print("messy queue length:", len(queue_messy), "solved queue length:", len(queue_solved))

def generate_solution(moves_from_messy, moves_from_solved, optional_directions):
    print(moves_from_messy)
    print(moves_from_solved)
    name = {}
    name['c'] = "clockwise"
    name['r'] = "counter-clockwise"
    moves = int(len(moves_from_messy)/2)
    for i in range(moves):
        # print("turn side", moves_from_messy[i*2], name[moves_from_messy[i*2+1]])
        print("solved = twist(solved, ", moves_from_messy[i*2], ", '", moves_from_messy[i*2+1], "')", "\t# turn side ", moves_from_messy[i*2], " ", name[moves_from_messy[i*2+1]], sep = "")
    moves = int(len(moves_from_solved)/2)
    for i in range(moves):
        fake_direction = moves_from_solved[moves*2-i*2-1] #starts at last char and goes back in twos
        if fake_direction == 'c': #needs to turn the opposite direction
            real_direction = 'r'
        else:
            real_direction = 'c'
        # print("turn side", moves_from_solved[moves-i*2], name[real_direction])
        print("solved = twist(solved, ", moves_from_solved[moves*2-i*2-2], ", '", real_direction, "')", "\t# turn side ", moves_from_solved[moves-i*2], " ", name[real_direction], sep = "")

def banana_split_v3(queue, goal, optional_directions, visited):
    current = heapq.heappop(queue)[1]
    while(current[0:131] != goal[0:131]):
        for i in range(0,12):
            for j in range(0,2):
                if i < 10:
                    side = str(i)
                elif i == 10:
                    side = "a"
                else:
                    side = "b"
                new_state = twist(current, i, optional_directions[j]) + side + str(optional_directions[j]) #could optimize this by not passing the path in and just concatenating it back on the end
                if len(current) > 132 and side == current[len(current)-2] and current[len(current)-1] != optional_directions[j]:
                    pass #prevents undoing the turn you just did
                elif new_state[0:131] in visited:
                    pass #prevents expanding the same nodes
                else:
                    depth = ( len(new_state) - 132 ) / 2
                    total_cost = int(heuristic(new_state, goal)) + depth #takes heuristic and adds the "cost" of the current node
                    heapq.heappush(queue, (total_cost, new_state))
                    visited[new_state[0:131]] = True
                # print("queue length:", len(queue), end = "\r")
        current = heapq.heappop(queue)[1]
    print(current)
    print("we fucking did it, bitch")
    print("queue length:", len(queue))

def banana_split_v2(queue, goal, optional_directions, visited):
    current = heapq.heappop(queue)[1]
    while(current[0:131] != goal[0:131]):
        for i in range(0,12):
            for j in range(0,2):
                if i < 10:
                    side = str(i)
                elif i == 10:
                    side = "a"
                else:
                    side = "b"
                new_state = twist(current, i, optional_directions[j]) + side + str(optional_directions[j]) #could optimize this by not passing the path in and just concatenating it back on the end
                if len(current) > 132 and side == current[len(current)-2] and current[len(current)-1] != optional_directions[j]:
                    pass #prevents undoing the turn you just did
                else:
                    depth = ( len(new_state) - 132 ) / 2
                    total_cost = int(heuristic(new_state, goal)) + depth #takes heuristic and adds the "cost" of the current node
                    heapq.heappush(queue, (total_cost, new_state))
                print("queue length:", len(queue), end = "\r")
        current = heapq.heappop(queue)[1]
    print(current)
    print("we fucking did it, bitch")
    print("queue length:", len(queue))

def banana_split_v1(queue, goal, optional_directions, visited):
    current = heapq.heappop(queue)[1]
    while(current[0:131] != goal[0:131]):
        for i in range(0,12):
            for j in range(0,2):
                if i < 10:
                    side = str(i)
                elif i == 10:
                    side = "a"
                else:
                    side = "b"
                new_state = twist(current, i, optional_directions[j]) + side + str(optional_directions[j]) #could optimize this by not passing the path in and just concatenating it back on the end
                depth = ( len(new_state) - 132 ) / 2
                total_cost = int(heuristic(new_state, goal)) + depth #takes heuristic and adds the "cost" of the current node
                heapq.heappush(queue, (total_cost, new_state))
                print("queue length:", len(queue), end = "\r")
        current = heapq.heappop(queue)[1]
    print(current)
    print("we fucking did it, bitch")
    print("queue length:", len(queue))

def banana_split(queue, goal, optional_directions):
    current = heapq.heappop(queue)[1]
    if current[0:131] == goal[0:131]:
        print(current)
        print("we fucking did it, bitch")
    else:
        for i in range(0,12):
            for j in range(0,2):
                if i < 10:
                    side = str(i)
                elif i == 10:
                    side = "a"
                else:
                    side = "b"
                if len(current) > 132 and side == current[len(current)-2] and current[len(current)-1] != optional_directions[j]:
                    pass #prevents undoing the turn you just did
                else:
                    new_state = twist(current, i, optional_directions[j]) + side + str(optional_directions[j])
                    depth = ( len(new_state) - 132 ) / 2
                    total_cost = int(heuristic(new_state, goal)) + depth #takes heuristic and adds the "cost" of the current node
                    heapq.heappush(queue, (total_cost, new_state))
        banana_split(queue, goal, optional_directions)

def gui(current):
    side_list = current.split("#")
    counter_side = 0
    print("##############")
    for side in side_list:
        print("     ", side[0], "     #")
        print("   ", side[9], "|", side[1], "   #")
        if counter_side < 10:
            print(" ", side[8], "-", counter_side, "-", side[2], " #")
        else:
            if counter_side == 10:
                print(" ", side[8], "- a -", side[2], " #")
            else:
                print(" ", side[8], "- b -", side[2], " #")
        print("  ", side[7], " | ", side[3], "  #")
        print("   ", side[6], side[5], side[4], "   #")
        print("             #")
        counter_side = counter_side + 1
    print("##############")

def mess_it_up(curr, num_rotations):
    options = ['c', 'r'] #0 corresponds to c which means a clockwise rotation
    full_names = ["clockwise", "counter-clockwise"]
    for i in range(num_rotations):
        side = random.randint(0,11)
        direction = random.randint(0,1)
        if side < 10:
            side_name = str(side)
        elif side == 10:
            side_name = "a"
        else:
            side_name = "b"
        # print("Turning side", side_name, full_names[direction])
        print("solved = twist(solved, ", side_name, ", '", options[direction], "')", "\t# turn side ", side_name, " ", full_names[direction], sep = "")
        curr = twist(curr, side, options[direction])
    return curr

def twist(curr, face, direction):
    new = curr
    n = list(new)
    c = list(curr)
    if face == 0:
        if direction == 'c':
            n[11*1+4]=c[11*5+4]
            n[11*1+5]=c[11*5+5]
            n[11*1+6]=c[11*5+6]
            n[11*2+4]=c[11*1+4]
            n[11*2+5]=c[11*1+5]
            n[11*2+6]=c[11*1+6]
            n[11*3+4]=c[11*2+4]
            n[11*3+5]=c[11*2+5]
            n[11*3+6]=c[11*2+6]
            n[11*4+4]=c[11*3+4]
            n[11*4+5]=c[11*3+5]
            n[11*4+6]=c[11*3+6]
            n[11*5+4]=c[11*4+4]
            n[11*5+5]=c[11*4+5]
            n[11*5+6]=c[11*4+6]
        elif direction == 'r':
            n[11*1+4]=c[11*2+4]
            n[11*1+5]=c[11*2+5]
            n[11*1+6]=c[11*2+6]
            n[11*2+4]=c[11*3+4]
            n[11*2+5]=c[11*3+5]
            n[11*2+6]=c[11*3+6]
            n[11*3+4]=c[11*4+4]
            n[11*3+5]=c[11*4+5]
            n[11*3+6]=c[11*4+6]
            n[11*4+4]=c[11*5+4]
            n[11*4+5]=c[11*5+5]
            n[11*4+6]=c[11*5+6]
            n[11*5+4]=c[11*1+4]
            n[11*5+5]=c[11*1+5]
            n[11*5+6]=c[11*1+6]
    elif face == 1:
        if direction == 'c':
            n[11*0+0]=c[11*2+6]
            n[11*0+1]=c[11*2+7]
            n[11*0+2]=c[11*2+8]
            n[11*5+2]=c[11*0+0]
            n[11*5+3]=c[11*0+1]
            n[11*5+4]=c[11*0+2]
            n[11*6+8]=c[11*5+2]
            n[11*6+9]=c[11*5+3]
            n[11*6+0]=c[11*5+4]
            n[11*7+0]=c[11*6+8]
            n[11*7+1]=c[11*6+9]
            n[11*7+2]=c[11*6+0]
            n[11*2+6]=c[11*7+0]
            n[11*2+7]=c[11*7+1]
            n[11*2+8]=c[11*7+2]
        elif direction == 'r':
            n[11*0+0]=c[11*5+2]
            n[11*0+1]=c[11*5+3]
            n[11*0+2]=c[11*5+4]
            n[11*2+6]=c[11*0+0]
            n[11*2+7]=c[11*0+1]
            n[11*2+8]=c[11*0+2]
            n[11*5+2]=c[11*6+8]
            n[11*5+3]=c[11*6+9]
            n[11*5+4]=c[11*6+0]
            n[11*6+8]=c[11*7+0]
            n[11*6+9]=c[11*7+1]
            n[11*6+0]=c[11*7+2]
            n[11*7+0]=c[11*2+6]
            n[11*7+1]=c[11*2+7]
            n[11*7+2]=c[11*2+8]
    elif face == 2:
        if direction == 'c':
            n[11*0+2]=c[11*3+6]
            n[11*0+3]=c[11*3+7]
            n[11*0+4]=c[11*3+8]
            n[11*1+2]=c[11*0+2]
            n[11*1+3]=c[11*0+3]
            n[11*1+4]=c[11*0+4]
            n[11*7+8]=c[11*1+2]
            n[11*7+9]=c[11*1+3]
            n[11*7+0]=c[11*1+4]
            n[11*8+0]=c[11*7+8]
            n[11*8+1]=c[11*7+9]
            n[11*8+2]=c[11*7+0]
            n[11*3+6]=c[11*8+0]
            n[11*3+7]=c[11*8+1]
            n[11*3+8]=c[11*8+2]
        elif direction == 'r':
            n[11*0+2]=c[11*1+2]
            n[11*0+3]=c[11*1+3]
            n[11*0+4]=c[11*1+4]
            n[11*1+2]=c[11*7+8]
            n[11*1+3]=c[11*7+9]
            n[11*1+4]=c[11*7+0]
            n[11*7+8]=c[11*8+0]
            n[11*7+9]=c[11*8+1]
            n[11*7+0]=c[11*8+2]
            n[11*8+0]=c[11*3+6]
            n[11*8+1]=c[11*3+7]
            n[11*8+2]=c[11*3+8]
            n[11*3+6]=c[11*0+2]
            n[11*3+7]=c[11*0+3]
            n[11*3+8]=c[11*0+4]

    elif face == 3:
        if direction == 'c':
            n[11*0+4]=c[11*4+6]
            n[11*0+5]=c[11*4+7]
            n[11*0+6]=c[11*4+8]
            n[11*2+2]=c[11*0+4]
            n[11*2+3]=c[11*0+5]
            n[11*2+4]=c[11*0+6]
            n[11*8+8]=c[11*2+2]
            n[11*8+9]=c[11*2+3]
            n[11*8+0]=c[11*2+4]
            n[11*9+0]=c[11*8+8]
            n[11*9+1]=c[11*8+9]
            n[11*9+2]=c[11*8+0]
            n[11*4+6]=c[11*9+0]
            n[11*4+7]=c[11*9+1]
            n[11*4+8]=c[11*9+2]
        elif direction == 'r':
            n[11*0+4]=c[11*2+2]
            n[11*0+5]=c[11*2+3]
            n[11*0+6]=c[11*2+4]
            n[11*2+2]=c[11*8+8]
            n[11*2+3]=c[11*8+9]
            n[11*2+4]=c[11*8+0]
            n[11*8+8]=c[11*9+0]
            n[11*8+9]=c[11*9+1]
            n[11*8+0]=c[11*9+2]
            n[11*9+0]=c[11*4+6]
            n[11*9+1]=c[11*4+7]
            n[11*9+2]=c[11*4+8]
            n[11*4+6]=c[11*0+4]
            n[11*4+7]=c[11*0+5]
            n[11*4+8]=c[11*0+6]

    elif face == 4:
        if direction == 'c':
            n[11*0+6]=c[11*5+6]
            n[11*0+7]=c[11*5+7]
            n[11*0+8]=c[11*5+8]
            n[11*3+2]=c[11*0+6]
            n[11*3+3]=c[11*0+7]
            n[11*3+4]=c[11*0+8]
            n[11*9+8]=c[11*3+2]
            n[11*9+9]=c[11*3+3]
            n[11*9+0]=c[11*3+4]
            n[11*10+0]=c[11*9+8]
            n[11*10+1]=c[11*9+9]
            n[11*10+2]=c[11*9+0]
            n[11*5+6]=c[11*10+0]
            n[11*5+7]=c[11*10+1]
            n[11*5+8]=c[11*10+2]
        elif direction == 'r':
            n[11*0+6]=c[11*3+2]
            n[11*0+7]=c[11*3+3]
            n[11*0+8]=c[11*3+4]
            n[11*3+2]=c[11*9+8]
            n[11*3+3]=c[11*9+9]
            n[11*3+4]=c[11*9+0]
            n[11*9+8]=c[11*10+0]
            n[11*9+9]=c[11*10+1]
            n[11*9+0]=c[11*10+2]
            n[11*10+0]=c[11*5+6]
            n[11*10+1]=c[11*5+7]
            n[11*10+2]=c[11*5+8]
            n[11*5+6]=c[11*0+6]
            n[11*5+7]=c[11*0+7]
            n[11*5+8]=c[11*0+8]

    elif face == 5:
        if direction == 'c':
            n[11*0+8]=c[11*1+6]
            n[11*0+9]=c[11*1+7]
            n[11*0+0]=c[11*1+8]
            n[11*4+2]=c[11*0+8]
            n[11*4+3]=c[11*0+9]
            n[11*4+4]=c[11*0+0]
            n[11*10+8]=c[11*4+2]
            n[11*10+9]=c[11*4+3]
            n[11*10+0]=c[11*4+4]
            n[11*6+0]=c[11*10+8]
            n[11*6+1]=c[11*10+9]
            n[11*6+2]=c[11*10+0]
            n[11*1+6]=c[11*6+0]
            n[11*1+7]=c[11*6+1]
            n[11*1+8]=c[11*6+2]
        elif direction == 'r':
            n[11*0+8]=c[11*4+2]
            n[11*0+9]=c[11*4+3]
            n[11*0+0]=c[11*4+4]
            n[11*4+2]=c[11*10+8]
            n[11*4+3]=c[11*10+9]
            n[11*4+4]=c[11*10+0]
            n[11*10+8]=c[11*6+0]
            n[11*10+9]=c[11*6+1]
            n[11*10+0]=c[11*6+2]
            n[11*6+0]=c[11*1+6]
            n[11*6+1]=c[11*1+7]
            n[11*6+2]=c[11*1+8]
            n[11*1+6]=c[11*0+8]
            n[11*1+7]=c[11*0+9]
            n[11*1+8]=c[11*0+0]

    elif face == 6:
        if direction == 'c':
            n[11*5+0]=c[11*1+8]
            n[11*5+1]=c[11*1+9]
            n[11*5+2]=c[11*1+0]
            n[11*10+6]=c[11*5+0]
            n[11*10+7]=c[11*5+1]
            n[11*10+8]=c[11*5+2]
            n[11*11+4]=c[11*10+6]
            n[11*11+5]=c[11*10+7]
            n[11*11+6]=c[11*10+8]
            n[11*7+2]=c[11*11+4]
            n[11*7+3]=c[11*11+5]
            n[11*7+4]=c[11*11+6]
            n[11*1+8]=c[11*7+2]
            n[11*1+9]=c[11*7+3]
            n[11*1+0]=c[11*7+4]
        elif direction == 'r':
            n[11*5+0]=c[11*10+6]
            n[11*5+1]=c[11*10+7]
            n[11*5+2]=c[11*10+8]
            n[11*10+6]=c[11*11+4]
            n[11*10+7]=c[11*11+5]
            n[11*10+8]=c[11*11+6]
            n[11*11+4]=c[11*7+2]
            n[11*11+5]=c[11*7+3]
            n[11*11+6]=c[11*7+4]
            n[11*7+2]=c[11*1+8]
            n[11*7+3]=c[11*1+9]
            n[11*7+4]=c[11*1+0]
            n[11*1+8]=c[11*5+0]
            n[11*1+9]=c[11*5+1]
            n[11*1+0]=c[11*5+2]

    elif face == 7:
        if direction == 'c':
            n[11*1+0]=c[11*2+8]
            n[11*1+1]=c[11*2+9]
            n[11*1+2]=c[11*2+0]
            n[11*6+6]=c[11*1+0]
            n[11*6+7]=c[11*1+1]
            n[11*6+8]=c[11*1+2]
            n[11*11+2]=c[11*6+6]
            n[11*11+3]=c[11*6+7]
            n[11*11+4]=c[11*6+8]
            n[11*8+2]=c[11*11+2]
            n[11*8+3]=c[11*11+3]
            n[11*8+4]=c[11*11+4]
            n[11*2+8]=c[11*8+2]
            n[11*2+9]=c[11*8+3]
            n[11*2+0]=c[11*8+4]
        elif direction == 'r':
            n[11*1+0]=c[11*6+6]
            n[11*1+1]=c[11*6+7]
            n[11*1+2]=c[11*6+8]
            n[11*6+6]=c[11*11+2]
            n[11*6+7]=c[11*11+3]
            n[11*6+8]=c[11*11+4]
            n[11*11+2]=c[11*8+2]
            n[11*11+3]=c[11*8+3]
            n[11*11+4]=c[11*8+4]
            n[11*8+2]=c[11*2+8]
            n[11*8+3]=c[11*2+9]
            n[11*8+4]=c[11*2+0]
            n[11*2+8]=c[11*1+0]
            n[11*2+9]=c[11*1+1]
            n[11*2+0]=c[11*1+2]

    elif face == 8:
        if direction == 'c':
            n[11*2+0]=c[11*3+8]
            n[11*2+1]=c[11*3+9]
            n[11*2+2]=c[11*3+0]
            n[11*7+6]=c[11*2+0]
            n[11*7+7]=c[11*2+1]
            n[11*7+8]=c[11*2+2]
            n[11*11+0]=c[11*7+6]
            n[11*11+1]=c[11*7+7]
            n[11*11+2]=c[11*7+8]
            n[11*9+2]=c[11*11+0]
            n[11*9+3]=c[11*11+1]
            n[11*9+4]=c[11*11+2]
            n[11*3+8]=c[11*9+2]
            n[11*3+9]=c[11*9+3]
            n[11*3+0]=c[11*9+4]
        elif direction == 'r':
            n[11*2+0]=c[11*7+6]
            n[11*2+1]=c[11*7+7]
            n[11*2+2]=c[11*7+8]
            n[11*7+6]=c[11*11+0]
            n[11*7+7]=c[11*11+1]
            n[11*7+8]=c[11*11+2]
            n[11*11+0]=c[11*9+2]
            n[11*11+1]=c[11*9+3]
            n[11*11+2]=c[11*9+4]
            n[11*9+2]=c[11*3+8]
            n[11*9+3]=c[11*3+9]
            n[11*9+4]=c[11*3+0]
            n[11*3+8]=c[11*2+0]
            n[11*3+9]=c[11*2+1]
            n[11*3+0]=c[11*2+2]

    elif face == 9:
        if direction == 'c':
            n[11*3+0]=c[11*4+8]
            n[11*3+1]=c[11*4+9]
            n[11*3+2]=c[11*4+0]
            n[11*8+6]=c[11*3+0]
            n[11*8+7]=c[11*3+1]
            n[11*8+8]=c[11*3+2]
            n[11*11+8]=c[11*8+6]
            n[11*11+9]=c[11*8+7]
            n[11*11+0]=c[11*8+8]
            n[11*10+2]=c[11*11+8]
            n[11*10+3]=c[11*11+9]
            n[11*10+4]=c[11*11+0]
            n[11*4+8]=c[11*10+2]
            n[11*4+9]=c[11*10+3]
            n[11*4+0]=c[11*10+4]
        elif direction == 'r':
            n[11*3+0]=c[11*8+6]
            n[11*3+1]=c[11*8+7]
            n[11*3+2]=c[11*8+8]
            n[11*8+6]=c[11*11+8]
            n[11*8+7]=c[11*11+9]
            n[11*8+8]=c[11*11+0]
            n[11*11+8]=c[11*10+2]
            n[11*11+9]=c[11*10+3]
            n[11*11+0]=c[11*10+4]
            n[11*10+2]=c[11*4+8]
            n[11*10+3]=c[11*4+9]
            n[11*10+4]=c[11*4+0]
            n[11*4+8]=c[11*3+0]
            n[11*4+9]=c[11*3+1]
            n[11*4+0]=c[11*3+2]

    elif face == 10:
        if direction == 'c':
            n[11*4+0]=c[11*5+8]
            n[11*4+1]=c[11*5+9]
            n[11*4+2]=c[11*5+0]
            n[11*9+6]=c[11*4+0]
            n[11*9+7]=c[11*4+1]
            n[11*9+8]=c[11*4+2]
            n[11*11+6]=c[11*9+6]
            n[11*11+7]=c[11*9+7]
            n[11*11+8]=c[11*9+8]
            n[11*6+2]=c[11*11+6]
            n[11*6+3]=c[11*11+7]
            n[11*6+4]=c[11*11+8]
            n[11*5+8]=c[11*6+2]
            n[11*5+9]=c[11*6+3]
            n[11*5+0]=c[11*6+4]
        elif direction == 'r':
            n[11*4+0]=c[11*9+6]
            n[11*4+1]=c[11*9+7]
            n[11*4+2]=c[11*9+8]
            n[11*9+6]=c[11*11+6]
            n[11*9+7]=c[11*11+7]
            n[11*9+8]=c[11*11+8]
            n[11*11+6]=c[11*6+2]
            n[11*11+7]=c[11*6+3]
            n[11*11+8]=c[11*6+4]
            n[11*6+2]=c[11*5+8]
            n[11*6+3]=c[11*5+9]
            n[11*6+4]=c[11*5+0]
            n[11*5+8]=c[11*4+0]
            n[11*5+9]=c[11*4+1]
            n[11*5+0]=c[11*4+2]

    elif face == 11:
        if direction == 'c':
            n[11*8+4]=c[11*9+4]
            n[11*8+5]=c[11*9+5]
            n[11*8+6]=c[11*9+6]
            n[11*7+4]=c[11*8+4]
            n[11*7+5]=c[11*8+5]
            n[11*7+6]=c[11*8+6]
            n[11*6+4]=c[11*7+4]
            n[11*6+5]=c[11*7+5]
            n[11*6+6]=c[11*7+6]
            n[11*10+4]=c[11*6+4]
            n[11*10+5]=c[11*6+5]
            n[11*10+6]=c[11*6+6]
            n[11*9+4]=c[11*10+4]
            n[11*9+5]=c[11*10+5]
            n[11*9+6]=c[11*10+6]
        elif direction == 'r':
            n[11*8+4]=c[11*7+4]
            n[11*8+5]=c[11*7+5]
            n[11*8+6]=c[11*7+6]
            n[11*7+4]=c[11*6+4]
            n[11*7+5]=c[11*6+5]
            n[11*7+6]=c[11*6+6]
            n[11*6+4]=c[11*10+4]
            n[11*6+5]=c[11*10+5]
            n[11*6+6]=c[11*10+6]
            n[11*10+4]=c[11*9+4]
            n[11*10+5]=c[11*9+5]
            n[11*10+6]=c[11*9+6]
            n[11*9+4]=c[11*8+4]
            n[11*9+5]=c[11*8+5]
            n[11*9+6]=c[11*8+6]

    new = ''.join(n)
    new = face_rotation(new, face, direction)
    return new

def face_rotation(curr, face, direction):
    new = curr
    n = list(new)
    c = list(curr)
    if direction == 'c':
        n[11*face+0]=c[11*face+8]
        n[11*face+1]=c[11*face+9]
        n[11*face+2]=c[11*face+0]
        n[11*face+3]=c[11*face+1]
        n[11*face+4]=c[11*face+2]
        n[11*face+5]=c[11*face+3]
        n[11*face+6]=c[11*face+4]
        n[11*face+7]=c[11*face+5]
        n[11*face+8]=c[11*face+6]
        n[11*face+9]=c[11*face+7]
    elif direction == 'r':
        n[11*face+0]=c[11*face+2]
        n[11*face+1]=c[11*face+3]
        n[11*face+2]=c[11*face+4]
        n[11*face+3]=c[11*face+5]
        n[11*face+4]=c[11*face+6]
        n[11*face+5]=c[11*face+7]
        n[11*face+6]=c[11*face+8]
        n[11*face+7]=c[11*face+9]
        n[11*face+8]=c[11*face+0]
        n[11*face+9]=c[11*face+1]
    new = ''.join(n)
    return new
    # if direction == 'c':
    #     curr = curr[0:face*11] + curr[face*11+8:face*11+10] + curr[face*11:face*11+8] + "#" + curr[face*11 + 11:]
    #
    # elif direction == 'r':
    #     curr = curr[0:face*11] + curr[face*11+2:face*11+10] + curr[face*11:face*11+2] + "#" + curr[face*11 + 11:]
    # if face == 11:
    #     curr = curr[:-1]
    # return curr

def heuristic(current, solved):
    total = 0
    for i in range(0,131):
        if current[i] != solved[i]:
            dist = how_far(current[i], solved[i])
            total += dist
    # final = int(math.floor(total/15))
    final = total/10
    return final

def how_far(iz, needs_to_be):
    scroll_of_truth = {} #look up table for distances
    scroll_of_truth["0"] = {
        "1" : 1,
        "2" : 1,
        "3" : 1,
        "4" : 1,
        "5" : 1,
        "6" : 2,
        "7" : 2,
        "8" : 2,
        "9" : 2,
        "a" : 2,
        "b" : 3
    }
    scroll_of_truth["1"] = {
        "0" : 1,
        "2" : 1,
        "3" : 2,
        "4" : 2,
        "5" : 2,
        "6" : 1,
        "7" : 1,
        "8" : 2,
        "9" : 3,
        "a" : 2,
        "b" : 2
    }
    scroll_of_truth["2"] = {
        "0" : 1,
        "1" : 1,
        "3" : 1,
        "4" : 2,
        "5" : 2,
        "6" : 2,
        "7" : 1,
        "8" : 1,
        "9" : 2,
        "a" : 3,
        "b" : 2
    }
    scroll_of_truth["3"] = {
        "0" : 1,
        "1" : 2,
        "2" : 1,
        "4" : 1,
        "5" : 2,
        "6" : 3,
        "7" : 2,
        "8" : 1,
        "9" : 1,
        "a" : 2,
        "b" : 2
    }
    scroll_of_truth["4"] = {
        "0" : 1,
        "1" : 2,
        "2" : 2,
        "3" : 1,
        "5" : 1,
        "6" : 2,
        "7" : 3,
        "8" : 2,
        "9" : 1,
        "a" : 1,
        "b" : 2
    }
    scroll_of_truth["5"] = {
        "0" : 1,
        "1" : 1,
        "2" : 2,
        "3" : 2,
        "4" : 1,
        "6" : 1,
        "7" : 2,
        "8" : 3,
        "9" : 2,
        "a" : 1,
        "b" : 2
    }
    scroll_of_truth["6"] = {
        "0" : 2,
        "1" : 1,
        "2" : 2,
        "3" : 3,
        "4" : 2,
        "5" : 1,
        "7" : 1,
        "8" : 2,
        "9" : 2,
        "a" : 1,
        "b" : 1
    }
    scroll_of_truth["7"] = {
        "0" : 2,
        "1" : 1,
        "2" : 1,
        "3" : 2,
        "4" : 3,
        "5" : 2,
        "6" : 1,
        "8" : 1,
        "9" : 2,
        "a" : 2,
        "b" : 1
    }
    scroll_of_truth["8"] = {
        "0" : 2,
        "1" : 2,
        "2" : 1,
        "3" : 1,
        "4" : 2,
        "5" : 3,
        "6" : 2,
        "7" : 1,
        "9" : 1,
        "a" : 2,
        "b" : 1
    }
    scroll_of_truth["9"] = {
        "0" : 2,
        "1" : 3,
        "2" : 2,
        "3" : 1,
        "4" : 1,
        "5" : 2,
        "6" : 2,
        "7" : 2,
        "8" : 1,
        "a" : 1,
        "b" : 1
    }
    scroll_of_truth["a"] = {
        "0" : 2,
        "1" : 2,
        "2" : 3,
        "3" : 2,
        "4" : 1,
        "5" : 1,
        "6" : 1,
        "7" : 2,
        "8" : 2,
        "9" : 1,
        "b" : 1
    }
    scroll_of_truth["b"] = {
        "0" : 3,
        "1" : 2,
        "2" : 2,
        "3" : 2,
        "4" : 2,
        "5" : 2,
        "6" : 1,
        "7" : 1,
        "8" : 1,
        "9" : 1,
        "a" : 1
    }
    return(scroll_of_truth[iz][needs_to_be])

if __name__ == "__main__":
    main()