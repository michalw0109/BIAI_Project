# ------------------ IMPORTS ------------------


from render.engine import Engine


# ------------------ GLOBAL VARIABLES ------------------


MAX_SIMULATIONS = 100000


# ------------------ MAIN FUNCTION ------------------


def main() -> None:
    window = Engine(MAX_SIMULATIONS)
    window.run()


# ------------------ MAIN CALL ------------------


if __name__ == "__main__":
    main()
