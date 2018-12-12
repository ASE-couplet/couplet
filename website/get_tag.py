from img2tag import img2tag
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_url", help="file_url")
    parser.add_argument("-p", "--save_path", help="save_path")

    args = parser.parse_args()
    url = args.file_url
    save_path = args.save_path

    keywords = "，".join(img2tag(url))
    f = open(save_path, "w")
    f.write(keywords)
    f.close()
    
    exit()
