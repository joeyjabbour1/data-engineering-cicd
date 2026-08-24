import argparse


def extract():
    print("Extracting orders...")


def validate():
    print("Validating orders...")


def transform():
    print("Transforming orders...")


def load():
    print("Loading orders...")


def main():
    parser = argparse.ArgumentParser(description="Order Pipeline CLI")
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["run", "extract", "validate", "transform", "load"],
    )
    args = parser.parse_args()

    if args.command == "run":
        print("Order pipeline container is running successfully.")
    elif args.command == "extract":
        extract()
    elif args.command == "validate":
        validate()
    elif args.command == "transform":
        transform()
    elif args.command == "load":
        load()


if __name__ == "__main__":
    main()
