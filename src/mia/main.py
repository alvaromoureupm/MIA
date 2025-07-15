import argparse




def main():
    args = parse_args()
    print("Welcome to MIA")
    


def parse_args():
    parser = argparse.ArgumentParser(description="MIA: A simple CLI for managing your media files")
    parser.add_argument("--chunk_size", type=int, help="Size of the chunks to split the file into")
    parser.add_argument("--chunk_overlap", type=int, help="Size of the overlap between chunks")
    parser.add_argument("--model_name", type=str, help="Name of the model to use")
    parser.add_argument("--collection_name", type=str, help="Name of the collection to use", default="mia-test")
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()