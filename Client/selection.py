"""
Select Class builds the slection page for user - talk to Server
1. Check Games: Show some filters:
  * check current opening games - User could select which game(room number) to join.
2. Create a new game
"""

class Selection():
    def __init__(self, msg) -> None:
        self.msg = msg
        self.showPage()

    # just create a board inside the Select
    def showPage(self):
        message = self.msg
        print(message)
        # TODO
        # board

    def showFilter(self, select):
      pass


if __name__ == "__main__":
    Selection("Show Test Messages!")