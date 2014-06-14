#! /usr/bin/env python3
"""
Demo script showing examples of the library's functionality.
"""
import esix

# Enter your credentials here
USERNAME = 'your_username'
PASSWORD = 'your_password'

# Login and save our user object
try:
    me = esix.user.login(USERNAME,PASSWORD)
except esix.errors.APILoginError as e:
    # If login fails, continue with the program
    print(e, '\n')
    me = None
else:
    print('Successfully logged in as ' + me.name)

# Show us a list of the 10 most recent post IDs and their uploaders
print('10 most recent posts:')
for p in esix.post.recent_posts(limit=10):
    print('#' + str(p.id) + ' by ' + p.author)
print()

# Now let's run a search and get a list of resulting post IDs
print('10 most recent posts matching "blotch rating:safe":')
for p in esix.post.search('blotch rating:safe',limit=10):
    print('#' + str(p.id) + ' by ' + p.author)
print()

# How about a list of the highest-rated posts for today?
print('Most popular posts today:')
for p in esix.post.popular_by_day():
    print('#' + str(p.id) + ' by ' + p.author)
print()

# Note that these above functions (and many others in the API) return
# object generators rather than a list of results. This means the server
# is queried as you iterate through the results, resulting in less load
# on the server and resources saved on your computer.

# Now let's get a specific post and print some of its properties
print('Fetching post with ID 476264')
post = esix.post.Post(476264)
print('Uploader: ' + post.author)
print('Source: ' + post.source)
print('First five tags: ' + ', '.join(post.tags[:5]))
print('Score: ' + str(post.score))
print('File URL: ' + post.file_url)
print()

# Let's say we want to find out more about the user who uploaded this post.
# Here we'll create a user object based on their ID
print('Fetching user ' + str(post.creator_id))
uploader = esix.user.User(post.creator_id)
print('Username: ' + uploader.name)
print('User level: ' + str(uploader.level))
print('Join date: ' + uploader.created_at)
print()

# What if we're not sure of a user's name and want to run a search?
print('Searching for users with "phantom7" in username')
for u in esix.user.search('phantom7'):
    print(u.name)
print()

# Let's look back at that post earlier. Maybe we want to read the comments
# users have made on it?
print('Comments made on post ' + str(post.id) + ':')
for c in post.comments:
    print('\t' + c.creator + ' - ' + c.body)
print()

# We can also get a list of the most recent comments made site-wide
print('25 most recent comments on the site:')
for c in esix.comment.recent_comments():
    print('#' + str(c.id) + ' by ' + c.creator)
print()

# We can even pick out a comment by ID and find out more about it
# Note that you must successfully log in before fetching a comment by ID.
print('Comment ID 1491038:')
try:
    comment = esix.comment.Comment(1491038)
except esix.errors.APIUnauthorizedError as e:
    print(e, '\n')
    comment = None
else:
    print('Author: ' + comment.creator)
    print('Post ID: ' + str(comment.post_id))
    print('Posted: ' + comment.created_at)
    print('Body: ' + comment.body)
    print('Score: ' + str(comment.score))
    print()

# We can also get some basic information about the site's tags...
print('Fetching info for tag "blotch"')
tag = esix.tag.Tag('blotch')
print('Tag ID: ' + str(tag.id))
print('Type: ' + tag.type_str)
print('Posts with this tag: ' + str(tag.count))
print()

# ...As well as a list of related tags
print('Tags related to "blotch":')
for t in tag.related:
    print(t.name + ' (' + t.type_str + ')')
print()

# Finally, we can fetch information about image pools on the site
# Let's get a list of the most recently updated pools
print('20 most recently updated pools:')
for pl in esix.pool.recent():
    print('#' + str(pl.id) + ': ' + pl.name_normal)
print()

# We can also search for a pool if we know part of the name
print('Searching for pools containing "False Start"')
for pl in esix.pool.search('False Start'):
    print('#' + str(pl.id) + ': ' + pl.name_normal)
print()

# Let's grab a specific pool and show some information about it
print('Fetching pool 3484')
pool = esix.pool.Pool(3484)
print('Name: ' + pool.name_normal)
print('Created by: ' + esix.user.User(pool.user_id).name)
print('Number of images: ' + str(pool.post_count))


# That's more or less all the basics! Each class has a few other properties and
# functions that you can take a look at, and you can easily pass information
# between objects (as seen in the last example). This API is still under
# development, so more functionality will come down the line.
