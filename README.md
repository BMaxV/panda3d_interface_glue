# panda3d_interface_glue


I usually install with

```
python3 setup.py install --user
```

which drops it into the home dir on linux and makes it easy to find should it conflict. Not that that's likely.

# examples

A correctly scaled scrollable table. Elements inside don't have to be
Labels, they can be buttons too, so this could use some fine tuning.

```
from direct.showbase.ShowBase import ShowBase
from panda_interface_glue import panda_interface_glue


class Wrapper:
    def __init__(self):

        # this is required for this demo
        self.b = ShowBase()

        # this is sort of optional allows for easily building and deleting
        # elements
        self.UI_elements = []
        self.build()

    def build(self):
        my_table = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore".split(" "),
        ]

        elements = panda_interface_glue.package_my_table(my_table, 3)
        self.UI_elements = elements

    def clean(self):
        """delete all elements"""
        for x in self.UI_elements:
            x.removeNode()
        self.UI_elements = []


def main():
    W = Wrapper()
    W.build()

    while True:
        W.b.taskMgr.step()


if __name__ == "__main__":
    main()
```
