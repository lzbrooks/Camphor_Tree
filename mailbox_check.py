from apis.rock_block_api import RockBlockAPI

if __name__ == "__main__":  # pragma: no cover
    rock_block_ping = RockBlockAPI()
    rock_block_ping.check_mailbox()
