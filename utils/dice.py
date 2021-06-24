import random

dice_types = {
    'y': 'proficiency',
    'proficiency': 'proficiency',
    'g': 'ability',
    'green': 'ability',
    'ability': 'ability',
    'b': 'boost',
    'blue': 'boost',
    'bl': 'boost',
    's': 'setback',
    'k': 'setback',
    'bk': 'setback',
    'black': 'setback',
    'setback': 'setback',
    'p': 'difficulty',
    'purple': 'difficulty',
    'difficulty': 'difficulty',
    'r': 'challenge',
    'red': 'challenge',
    'challenge': 'challenge',
    'w': 'force',
    'white': 'force',
    'force': 'force',
}

dice_imgs = {
    'proficiency': {
        'rolling': '<a:yellowanim:857698662083723314>',
        '': '<:yellow:857709119002640435>',
        's': '<:yellows:857708682406264893>',
        'ss': '<:yellowss:857708683060052038>',
        'a': '<:yellowa:857708682271916083>', 
        'sa': '<:yellowsa:857708682569187328>', 
        'aa': '<:yellowaa:857708682628694076>',
        't': '<:yellowr:857708682736566332>',
    },
    'ability': {
        'rolling': '<a:green:857707918266204180>',
        '': '<:green:857709119506350132>',
        's': '<:greens:857708925531717642>', 
        'ss': '<:greenss:857708925277044817>',
        'a': '<:greena:857708925507731456>', 
        'sa': '<:greensa:857708925851664394>',
        'aa': '<:greenaa:857708925629759538>',
    },
    'boost': {
        'rolling': '<a:blueanim:857687152581148702>',
        '': '<:blue:857709119611732028>',
        'aa': '<:blueaa:857708925013327883>',
        'a': '<:bluea:857708924744892429>', 
        'sa': '<:bluesa:857708925427777616>',
        's': '<:blues:857708925125132288>',
    },
    'setback': {
        'rolling': '<a:blackanim:857687152417308703>',
        '': '<:black:857709119385632789>',
        'f': '<:blackf:857708925033775104>',
        'd': '<:blackt:857708925004939314>',
    },
    'difficulty': {
        'rolling': '<a:purple:857707917598785567>',
        '': '<:purple:857709119681986590>',
        'f': '<:purplef:857708925096427521>',
        'ff': '<:purpleff:857708925411524649>',
        'd': '<:purplet:857708924949495858>',
        'dd': '<:purplett:857708925074669608>',
        'fd': '<:purpleft:857708925322002452>',
    },
    'challenge': {
        'rolling': '<a:redanim:857707768496390185>',
        '': '<:red:857709119329665056>',
        'f': '<:redf:857708817416716319>',
        'ff': '<:redff:857708817579638814>',
        'd': '<:redt:857708817730240592>',
        'fd': '<:redft:857708817592614932>',
        'dd': '<:redtt:857708817528914021>',
        'e': '<:redd:857708817478844478>',

    },
    
    'force': {
        'rolling': '<a:whiteanim:857687150366556190>',
        'x': '<:whiten:857708765239705630>',
        'xx': '<:whitenn:857708765334601778>',
        'w': '<:whitel:857708765426876489>',
        'ww': '<:whitell:857708765611687946>',
    },
}

other_imgs = {
    't': '<:tri:644601354865737738>',
    's': '<:success:857687152602906634>',
    'a': '<:advantage:857734853352226846>',
    'd': '<:threat:857687151835742218>',
    'f': '<:fail:644655569059184660>',
    'e': '<:des:644602557213310976>',
    'w': '<:lightpip:857687152476160000>',
    'x': '<:darkpip:857687151600074754>',
}

dice_chance = {
    'proficiency': ['', 's', 's', 'ss', 'ss', 'a', 'sa', 'sa', 'sa', 'aa', 'aa', 't'], 
    'ability': ['', 's', 's', 'ss', 'a', 'a', 'sa', 'aa'],
    'boost': ['', '', 'aa', 'a', 'sa', 's'],
    'setback': ['', '', 'f', 'f', 'd', 'd'],
    'difficulty': ['', 'f', 'ff', 'd', 'd', 'd', 'dd', 'fd'],
    'challenge': ['', 'f', 'f', 'ff', 'ff', 'd', 'd', 'fd', 'fd', 'dd', 'dd', 'e'],
    'force': ['x', 'x', 'x', 'x', 'x', 'x', 'xx', 'w', 'w', 'ww', 'ww', 'ww'],
}

def interpret_dice(s):
    dice_list = []
    if len(s) == 1: # Single string
        repeat = 1
        for c in s[0]:
            if c.isnumeric():
                repeat = int(c)
            else:
                for _ in range(repeat):
                    dice_list.append(dice_types.get(c.lower(), None))
                repeat = 1
    else:   # List-string
        repeat = 1
        for i in s:
            if i.isnumeric():
                repeat = int(i)
            else:
                for _ in range(repeat):
                    dice_list.append(dice_types.get(i.lower(), None))
                repeat = 1

    return dice_list

def dice_to_anim(l):
    a = []
    for d in l:
        try:
            a.append(dice_imgs[d]['rolling'])
        except:
            a.append('❓')
    return a

def roll_dice(l):
    dice_res = []
    dice_im = []
    for d in l:
        if d is None:
            continue
        try:
            x = random.choice(dice_chance[d])
        except Exception as e:
            print(e)
        try:
            dice_res.append(x)
        except Exception as e:
            print(e)
        try:
            dice_im.append(dice_imgs[d][x])
        except Exception as e:
            print(e)

    res_str = ''.join(dice_res)
    t_score = res_str.count('t') - res_str.count('e')
    s_score = res_str.count('s') - res_str.count('f') + res_str.count('t') - res_str.count('e')
    a_score = res_str.count('a') - res_str.count('d')
    w_score = res_str.count('w') - res_str.count('x')

    res_l = []
    for _ in range(t_score):
        res_l.append(other_imgs['t'])
    for _ in range(-t_score):
        res_l.append(other_imgs['e'])
    for _ in range(s_score):
        res_l.append(other_imgs['s'])
    for _ in range(-s_score):
        res_l.append(other_imgs['f'])
    for _ in range(a_score):
        res_l.append(other_imgs['a'])
    for _ in range(-a_score):
        res_l.append(other_imgs['d'])
    for _ in range(w_score):
        res_l.append(other_imgs['w'])
    for _ in range(-w_score):
        res_l.append(other_imgs['x'])

    return ''.join(dice_im), ''.join(res_l)