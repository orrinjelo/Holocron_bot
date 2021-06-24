import json
import os

current_path = os.path.split(os.path.realpath(__file__))[0]

def load_config():
    with open('{}/../config/config.json'.format(current_path), 'r') as f:
        return json.load(f)

def update_bot(message):
    g = git.cmd.Git(working_dir=os.getcwd())
    g.execute(["git", "fetch", "origin", "master"])
    update = g.execute(["git", "remote", "show", "origin"])
    if ('up to date' in update or 'fast-forward' in update) and message:
        print('{}'.format(update))
        return False
    else:
        if message is False:
            version = 4
        else:
            version = g.execute(["git", "rev-list", "--right-only", "--count", "master...origin/master"])
        version = description = str(int(version) + 1)
        if int(version) > 4:
            version = "4"
        commits = g.execute(["git", "rev-list", "--max-count=%s" % version, "origin/master"])
        commits = commits.split('\n')
        em = discord.Embed(color=0x24292E, title='Latest changes for Charlie:', description='%s release(s) behind.' % description)
        for i in range(int(version)-1):
            title = g.execute(["git", "log", "--format=%ar", "-n", "1", "%s" % commits[i]])
            field = g.execute(["git", "log", "--pretty=oneline", "--abbrev-commit", "--shortstat", "%s" % commits[i], "^%s" % commits[i+1]])
            field = field[8:].strip()
            link = 'https://github.com/appu1232/Discord-Selfbot/commit/%s' % commits[i]
            em.add_field(name=title, value='%s\n[Code changes](%s)' % (field, link), inline=False)
        # em.set_thumbnail(url='https://image.flaticon.com/icons/png/512/25/25231.png')
        # em.set_footer(text='Full project: https://github.com/appu1232/Discord-Selfbot')
        return em


def cmd_prefix_len():
    config = load_config()
    return len(config['cmd_prefix'])


def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True

    return check