import random
import sqlite3
import re
import time

def get_six_random_hex():
    hex_numbers = []
    while len(hex_numbers) < 6:
        random_number = random.randint(0, 255)
        hex_number = format(random_number, '02X')
        if hex_number not in hex_numbers:
            hex_numbers.append(hex_number)
    return hex_numbers


def get_randomness(round):
    conn = sqlite3.connect('drand.db')
    c = conn.cursor()
    c.execute("SELECT randomness FROM drand WHERE round IN (?, ?) LIMIT 2", (round, round+1))
    results = c.fetchall()
    conn.close()
    return results


def hex_to_upper_case_array(hex_string):
    if not hex_string:
        return []
    hex_array = list(hex_string.upper())
    result_array = []
    hex_value = ''
    for char in hex_array:
        if re.match('[0-9A-F]', char):
            hex_value += char
            if len(hex_value) == 2:
                result_array.append(hex_value)
                hex_value = ''
    return result_array


def check_matching_numbers(randomness_array, single_bet):
    score = 0
    for position, extraction in enumerate(randomness_array):
        if single_bet == extraction:
            score += position + 1
    return score

def getscore(randomness_array, bet):
    total_score = 0
    for single_bet in bet:
        total_score += check_matching_numbers(randomness_array, single_bet)
    return total_score

def cpubet(randomness_array):
    unique_array = []
    for hexnum in randomness_array:
        if hexnum not in unique_array:
            unique_array.append(hexnum)
        if len(unique_array) == 6:
            break
    return unique_array


def challenge(attempts, jackpotlimit, slice, iterations):
    cpu_win = 0
    user_win = 0
    tie = 0
    jackpot = 0
    count = 0
    total_attempts = (attempts * iterations)

    start_time = time.time()

    for _ in range(iterations):
        for i in range(1, attempts-1):
            count += 1
            randomness = get_randomness(i)
            user_bet = get_six_random_hex()
            user_randomness_array = hex_to_upper_case_array(randomness[0][0])
            cpu_randomness_array = hex_to_upper_case_array(randomness[1][0])
            cpu_bet = cpubet(user_randomness_array)

            user_score = getscore(user_randomness_array, user_bet)
            cpu_score = getscore(cpu_randomness_array, cpu_bet)

            if user_score > cpu_score:
                user_win += 1
                if user_score >= jackpotlimit:
                    jackpot += 1
            elif user_score < cpu_score:
                cpu_win += 1
            else:
                tie += 1

            if count % slice == 0:
                elapsed_time = time.time() - start_time
                eta = (total_attempts - count) * (elapsed_time / count)
                jackpotpercentage = jackpot / count * 100
                winpercentage = user_win / count * 100
                losepercentage = cpu_win / count * 100
                tiepercentage = tie / count * 100
                print(f"{count}/{total_attempts} - User wins: {user_win} ({winpercentage:.2f}%) - CPU wins: {cpu_win} ({losepercentage:.2f}%) - Ties: {tie} ({tiepercentage:.2f}%) - Jackpots: {jackpot} ({jackpotpercentage:.2f}%) - Elapsed time: {elapsed_time/60:.2f} minutes - ETA: {eta/60:.2f} minutes")