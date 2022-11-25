from gooey import Gooey, GooeyParser
import sys
import pathlib
import ctypes
import platform
import rpgmaker


class SaveEditorException(Exception):
    pass


def get_type(save, action: str = "decode"):
    action = action
    extension = pathlib.PurePath(save).suffix
    if extension == '.json':
        return get_type(pathlib.PurePath(save).stem, "encode")
    elif extension == '.rpgsave':
        return rpgmaker, action
    else:
        raise SaveEditorException("Unknown save file format")


if len(sys.argv) >= 2:
    """If any arguments are passed, run in CLI mode, otherwise run in GUI mode"""
    if '--ignore-gooey' not in sys.argv:
        sys.argv.append('--ignore-gooey')


@Gooey
def main():
    parser = GooeyParser()
    parser.add_argument('-f', '--file', help='A save file to encode / decode',
                        required=True, widget='FileChooser')
    args = parser.parse_args()

    try:
        file = open(args.file, "r")
    except FileNotFoundError:
        parser.print_usage()
        raise

    save_type, action = get_type(args.file)
    if action == "encode":
        print("Encoding...")
        output = save_type.encode(file.read())
        output_file = pathlib.PurePath(args.file).stem
    else:
        print("Decoding...")
        output = save_type.decode(file.read())
        output_file = pathlib.PurePath(args.file + '.json')

    with open(output_file, "w") as f:
        print(output_file)
        f.write(output)


if __name__ == '__main__':
    # sys.tracebacklimit = 0
    if platform.system() == "Windows":
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
    main()
