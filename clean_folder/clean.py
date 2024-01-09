import re
import shutil
import sys
from pathlib import Path

def main():

    def translate(name):
        return_name = ""
        for i in name:
            return_name += i.translate(TRANS)
        return return_name


    def iter_dir(path):
        for i in path.iterdir():
            if i.is_dir():
                if Path(i).stem in file_type and Path(i).parents[0] == G_path:
                    pass
                else:
                    iter_dir(i)
                    try:
                        i.rmdir()
                    except OSError:
                        norm_name_file = normalize(str(i.stem))
                        i.rename(Path(i.parents[0], norm_name_file))
            else:
                norm_name = normalize(i.stem)
                norm_name = Path(norm_name + i.suffix)
                sort_file(i, norm_name)


    def sort_file(src_file, name_file):
        suff_file = str(name_file.suffix)
        new_dir = "unknown"
        for key, my_vol in file_type.items():
            if suff_file in my_vol:
                new_dir = key
                break
        if new_dir == "archives":
            unpack_file(src_file, name_file, new_dir)
        elif new_dir == "unknown":
            pass
        else:
            move_file(src_file, name_file, new_dir)
        set_of_list_file_by_type[new_dir].append(name_file)
        set_suffix[new_dir].add((name_file.suffix)[1:])


    def unpack_file(src_file, name_file, new_dir):
        shutil.unpack_archive(src_file, Path(G_path,new_dir,name_file.stem))
        src_file.unlink()


    def move_file(src_file, name_file, new_dir):
        to_file = Path(str(G_path), new_dir, str(name_file))
        iter_post = 1
        while True:
            if Path.is_file(to_file):
                to_file = Path(str(G_path), new_dir, name_file.stem + str(iter_post) + str(name_file.suffix))
                iter_post += 1
            else:
                src_file.rename(to_file)
                break


    def normalize(name):
        trans_name = translate(name)
        norm_name = re.sub("\W", "_", trans_name)
        return(norm_name)



    file_type = {'images':['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
                'documents':['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
                'video':['.avi', '.mp4', '.mov', '.mkv'],
                'audio':['.mp3', '.ogg', '.wav', '.amr'],
                'archives':['.zip', '.gz', '.tar']}


    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()


    if  len(sys.argv) != 2:
        print("Insert path")
        sys.exit(1)
    G_path = Path((sys.argv[1]).lower())
    if not G_path.is_dir():
        print("path not found")
        sys.exit(1)

    for new_dir in file_type:
        path_new_dir = Path(sys.argv[1],new_dir)
        try:
            Path.mkdir(path_new_dir)
        except FileExistsError:
            pass

    set_of_list_file_by_type = {'images':[],
                                'documents':[],
                                'video':[],
                                'audio':[],
                                'archives':[],
                                'unknown':[]}


    set_suffix = {'images':set(),
                    'documents':set(),
                    'video':set(),
                    'audio':set(),
                    'archives':set(),
                    'unknown':set()}


    iter_dir(G_path)


    for i in set_of_list_file_by_type:
        print(f"list of {i} files: {set_of_list_file_by_type.get(i)}")
    for i in set_suffix:
        print(f"set {i} suffix: {set_suffix.get(i)}")

if __name__ == '__main__':
    main()
    