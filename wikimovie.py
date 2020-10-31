import argparse


def main():
    parser = argparse.ArgumentParser(prog='Wikipedia Movie Maker',
                                     description='Make movies from Wikipedia articles, combined with Giffs!',
                                     usage='Example: wikimovie.py Justin Bieber --language en',
                                     )
    parser.add_argument('subject', help='The subject of your movie.', required=True)
    parser.add_argument('--language', default='en', required=False,
                        help='You can provide any language, this will be the language of the Google speech API and the language of the Wikipedia article')
    parser.add_argument('--paragraphs', required=False, default=3, help='The amount paragraphs taken from the Wikipredia article.')
    parser.add_argument('--gif-interval', default=2, help='The time a gif is show in the image', required=False)

    args = parser.parse_args()
    print(args)

    print('Done...')


if __name__ == '__main__':
    main()
