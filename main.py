from views.app import App


def main() -> None:
    """
    Entry point of the program.
    """
    try:
        App().mainloop()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
