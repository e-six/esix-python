# Python Esix #

An easy to use Python 3 frontend for e621.net's JSON API. Currently includes all basic site functionality, from searching posts to getting user information to managing tags.

----
## Setup ##
### Dependencies ###
* [Python 3](https://www.python.org/downloads/)

### Installing ###
Simply run `python setup.py install` from your download directory. The package should automatically install to your Python directory. From there you can `import esix` in any Python script.

----
## Using the Library ##
Functionality is divided up by major features of the site. Each feature has its own module with a related class and functions. For example, everything related to fetching post information is located in `esix.post`. To search for posts with a tag query, simply run `esix.post.search("your_query_here")`.

Each module also has a class of the same name, in which you can fetch an object of data for the module. So to fetch a post with a specific ID, run `esix.post.Post(post_id)`. The script will query the server and return all of the specified post's related data as object properties.

Full documentation is available on the [wiki](wiki/Home).