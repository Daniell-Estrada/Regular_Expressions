"""
This is the main file of the project. It is the entry point of the project.
"""

from views.app import App


def main() -> None:
    try:
        App().mainloop()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
