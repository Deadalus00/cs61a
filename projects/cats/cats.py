"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    output_list = [item for item in paragraphs if select(item)]
    return output_list[k] if k <= len(output_list) - 1 else ''
    # END PROBLEM 1

def leave_lower_cha(inputstr):
        output = ''
        for char in inputstr:       
            if char.isalpha():
                output += char
        output = output.lower()
        return output


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2

    def select(target_words):
        target_list = [words.lower() for words in target_words.split()]
        true_saver = False
        index = max(len(target_list),len(topic))
        
        for item in topic:
            for target in target_list:               
                if item == leave_lower_cha(target):
                    true_saver = True    
        return true_saver
        
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct_num = 0
    total_num = len(typed_words)

    for i in range(min(len(reference_words),len(typed_words))):
        if reference_words[i] == typed_words[i]:
            correct_num += 1
    return 0.0 if min(len(reference_words),len(typed_words)) == 0 else correct_num / total_num * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed) / 5) / (elapsed / 60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    diff_word_set = [(diff_function(user_word,valid_single,limit),valid_single) for valid_single in valid_words]
    min_diff = limit
    valid_dict = {}
    for item in diff_word_set:
        if item[0] <= limit and item[0] <= min_diff:
            min_diff = item[0]
            valid_dict.setdefault(min_diff, [])
            valid_dict[min_diff] .append(item[1])
            min_key = min([key for key in valid_dict.keys()])
    return user_word if user_word in valid_words or valid_dict == {} else valid_dict[min_key][0]
    # END PROBLEM 5


def log_diff(t=0):
    t += 1
    return t

def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6

    abs_diff = abs(len(goal) - len(start))
    if limit >= 0:  
        if start == '' or goal == '':
            return abs_diff
        elif start[0] != goal[0]:
            return 1 + shifty_shifts(start[1:],goal[1:],limit-1)
        else:
            return shifty_shifts(start[1:],goal[1:],limit)
    else:
        return 0
            
    # END PROBLEM 6


def pawssible_patches(s, g, l):
    """A diff function that computes the edit distance from START to GOAL."""

    # Note that you don't have to make the function to do exactly how the procedure works 
    # but rather take note of how many TIMES the opertion runs. So no need for helper function
    # nor return a modified string(it'll do nothing but increase the difficulty).

    if l >= 0 and s != g:
        if s == '' and g == '':
            return 0
        elif s == '' or g == '':
            return abs(len(s) - len(g))
        elif s[0] == g[0]:
            return pawssible_patches(s[1:],g[1:],l)
        else:
            add = pawssible_patches(s,g[1:], l - 1)
            remove = pawssible_patches(s[1:], g, l - 1)
            sub = pawssible_patches(s[1:],g[1:], l - 1)
            return 1 + min(add,remove,sub)
    else:
        return 0




    '''def add_diff(s,g,l):
        i = 0
        if l >= 0 and s != g:
            while i < min(len(s),len(g)):
                print(i)
                if i > 0 and s[i] != g[i] and g[i+1] == s[i] :
                    print(i, s[:i] + g[i-1] + s[i- 1:])
                    return s[:i] + g[i] + s[i:]
                elif i == 0 and s[i] != g[i] and g[i+1] == s[i] :
                
                    return g[i] + s[i:]
                i += 1
            return s            
        else:                    
            return s
    
    def remove_diff(s,g,l):
        if l >= 0 and s != g:
            if len(s) <= len(g):
                for i in range(min(len(s),len(g))):
                    
                    if i == 0 and s[i] != g[i] and   s[i+1] == g[i] :
                        print( s[i+1:])
                        return s[i+1:]
                    elif i > 0 and s[i-1] != g[i-1] and s[i] == g[i-1]:
                        print(s[:i] + s[i+1:])
                        return s[:i-1] + s[i:]
            elif len(s) > len(g):
                for i in range(min(len(s),len(g))):
                   
                    if s[i] != g[i] and s[i+1] == g[i]:
                        
                        return s[:i] + s[i+1:]
                    elif s[:i+1] == g[:i+1]:
                        
                        return s[:i+1]
            return s
        else:                    
            return s
    
    def substitute_diff(s,g,l):
        for i in range(min(len(s),len(g))):
            if s[i] != g[i] and i < (len(s) - 1):
              
                return s[:i] + g[i] + s[i+1:]
            elif s[i] != g[i] and i == len(s) - 1:
                
                return s[:i] + g[i]
        return s

    if l >= 0:   
        if s == g:
            return 0
        elif len(s) <= len(g) and add_diff(s, g, l) != s:
            return  1 + pawssible_patches(add_diff(s, g, l - 1), g, l - 1)
        elif len(s) >= len(g) and remove_diff(s, g, l) != s:
            
            return  1 + pawssible_patches(remove_diff(s, g, l - 1), g, l - 1) 
        elif substitute_diff(s, g, l) != s:
            return  1 + pawssible_patches(substitute_diff(s, g, l - 1), g, l - 1)
        else:
            return 0
    else:
        return 0
    
    '''
    
    '''abs_diff = abs(len(goal) - len(start))
        if limit >= 0:
        if start == '' or goal == '':
            return abs_diff
        elif start[-1] != goal[-1]:
            if len(goal) >=2 and len(goal) >= len(start) and add_diff(start, goal):
                return 1 + pawssible_patches((start + goal[-1])[:-1], goal[:-1], limit - 1)
            elif len(start) >= 2 and len(goal) <= len(start) and remove_diff(start, goal):
                return 1 + pawssible_patches(start[:-2], goal[:-1], limit - 1)
            else:
                return substitute_diff(start, goal) + pawssible_patches(start[:-1], goal[:-1], limit - 1)    
        else:
            return pawssible_patches(start[:-1], goal[:-1], limit)
    else:
        return 0
    '''
        
    
        # BEGIN
        
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    typed_count = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            typed_count += 1
        else:
            break
    progress = typed_count / len(prompt)
    d = {'id':user_id,'progress':progress}
    send(d)
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9

    times = [[player[i]-player[i-1] for i in range(len(player)) if i > 0] for player in times_per_player ]
    return game(words,times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    player_time = all_times(game)
    word = all_words(game)
    d = {}
    out = [[] for i in player_time]
    for i in word_indices:    
        for j in player_indices:
            if player_time[j][i] == min([player_time[j][i] for j in player_indices]):
                d[word[i]] = j
                break
    for key, value in d.items():
        out[value] .append( key)
            
    return out
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)