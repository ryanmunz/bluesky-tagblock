# bsky-tagblock
## Description
Mass block account followers based on a string in their description

Inspired by this post https://bsky.app/profile/amyhoy.bsky.social/post/3leiq67hfla2x

Uses the python atproto client by MarshalX https://github.com/MarshalX/atproto

## Installation
- Tested with python 3.11 on windows, however it should work on other platforms and later versions without issue
- Clone the repository locally and cd into it
- pip install -r requirements.txt

## Usage

```
usage: run_tagblock [-h] [--handle HANDLE] [--password PASSWORD] [--search SEARCH] [--block]

Reads your bluesky account, finds followers with specific tags, and the blocks them

options:
  -h, --help           show this help message and exit
  --handle HANDLE      Your handle on the bluesky network ex: username.bsky.social
  --password PASSWORD  Your password
  --search SEARCH      A string to search followers descriptions for
  --block

https://www.ryanmunz.com/contact/
```

By default all we do is output the users we would have blocked and their descriptions:
```
python .\run_tagblock.py --handle ryanmunz.com --password nothisisntmypassword --search '#WakeUp' 
```

If you pass a --block flag it will actually block them:
```
python .\run_tagblock.py --handle ryanmunz.com --password nothisisntmypassword --search '#WakeUp' --block 
```

## Notes
Pagination from get_followers is a little weird to work with which is why INFO counts may be in odd increments

The count on your profile page also appears to be completely made up or have some foible I'm not aware of
ex: My test account showed a count a little under double my actual follower count from counting them manually

The match patterns I'm using are as follows:
- find(' search ')
- startswith(search)
- endswith(search)
- == search

I didn't go crazy with logging/verbosity as this was an insomnia project

I'm over here! https://www.ryanmunz.com/contact/
