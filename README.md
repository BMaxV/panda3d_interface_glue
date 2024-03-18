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

# smooth drag and drop

I built this smooth drag and drop system for e.g. card games or intuitive sorting for the user

![smoothgif](smooth.gif)


# custom button

I put in code to generate a custom button, with a text node and a DirectFrame, because that seems to be the only way of customizing the font. It doesn't have the "default" modes that DirectButton has, but you can include those in the function if you want. Not finished with this, I just built the 0.5 so to speak, I will probably update this once I use it a bit.

![custombutton](button.JPG)

font in the button example is Dela Gothic One from google fonts, original zip attached, open font license.
