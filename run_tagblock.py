"""
Mass block account followers based on a string in their description
"""

import argparse
import sys

from time import sleep
from atproto import Client, models


def main():
    """Main Function"""

    parser = argparse.ArgumentParser(
        prog="run_tagblock",
        description="Mass block account followers based on a string in their description",
        epilog="https://www.ryanmunz.com/contact/",
    )
    parser.add_argument(
        "--handle", help="Your handle on the bluesky network ex: username.bsky.social"
    )
    parser.add_argument("--password", help="Your password")
    parser.add_argument(
        "--search", help="A string to search followers descriptions for"
    )
    parser.add_argument("--block", action="store_true", default=False)
    args = parser.parse_args()
    client = Client()
    client.login(args.handle, args.password)

    print(f"We are going to read the followers for {args.handle}")
    print("")
    if args.block:
        print("***We are going to block users. This action is not reversible!***")
    else:
        print(
            "We are just going to output matching users and descriptions. Pass this command --block to block them."
        )
    ready = input("Enter yes to proceed. All other responses exit: ")
    if ready != "yes":
        sys.exit(1)

    # I'm tracking cursor history as get_followers pagination will loop
    # If we see the same cursor twice we know we are done
    cursor_history = []
    data = client.get_followers(actor=args.handle)

    while data.cursor not in cursor_history:
        cursor_history.append(data.cursor)

        print(
            f"INFO Checking {len(data.followers)} followers and then sleeping 10 seconds for politeness."
        )
        for follower in data.followers:
            match = False
            # Rather than expose regex to the user, I'm just blocking 4 separate situations
            # I'm ignoring weirder situations like tabs or nonprintable characters
            try:
                if follower.description.find(f" {args.search} ") != -1:
                    # String in description surrounded spaces (i.e. in the middle of a sentence)
                    print(
                        f"MATCH FIND handle: {follower.handle}, description: {follower.description}"
                    )
                    match = True
                if follower.description.startswith(args.search):
                    # String starts the description
                    print(
                        f"MATCH STARTSWITH handle: {follower.handle}, description: {follower.description}"
                    )
                    match = True
                if follower.description.endswith(args.search):
                    # String ends the description
                    print(
                        f"MATCH ENDSWITH handle: {follower.handle}, description: {follower.description}"
                    )
                    match = True
                if follower.description == args.search:
                    # String is the entire description
                    print(
                        f"MATCH EQUALS handle: {follower.handle}, description: {follower.description}"
                    )
                    match = True
            except AttributeError:
                # If we can't parse the description, dump out (ex. if they have no description)
                match = False
            if args.block and match:
                print(f"BLOCK {follower.handle}")
                # There's no direct client function for blocks, but we can reach out into the bsky.graph https://docs.bsky.app/docs/tutorials/blocking
                record = models.AppBskyGraphBlock.Record(
                    subject=follower.did, created_at=client.get_current_time_iso()
                )
                client.app.bsky.graph.block.create(repo=client.me.did, record=record)
        sleep(10)
        data = client.get_followers(actor=args.handle, cursor=data.cursor)


if __name__ == "__main__":
    main()
