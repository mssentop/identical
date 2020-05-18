from hashlib import sha256
import argparse
import os

# checks if the input given as a directory really is a directory
def is_dir_path(string):
    if not os.path.isabs(string):
        string = os.path.abspath(string)
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
# reading and parsing input
parser = argparse.ArgumentParser()
parser.add_argument("-d", action="store_true", default=False)
parser.add_argument("-f", action="store_true", default=False)
parser.add_argument("-c", action="store_true", default=False)
parser.add_argument("-n", action="store_true", default=False)
parser.add_argument("-s", action="store_true", default=False)
parser.add_argument('paths', action='store', nargs='*', default=[os.getcwd()], type=is_dir_path)
args = parser.parse_args()

# dictionaries to store path-hash pairs. Used dictionary to detect duplicates and store them in a list.
dic_dir_hashes = dict()
dic_file_hashes = dict()
dic_dirs = dict()
dic_files = dict()

# main loop where the given directories (if not any, then the current directory) are traversed.
for dir_path in args.paths:
    for root, dirs, files in os.walk(dir_path, topdown=False):
        hashes_list = list()  # store the hashes of contents in currently processed directory
        file_list = list()  # store the names of files if "-n" argument is given
        for dir in dirs:
            if os.access(os.path.join(root, dir), os.R_OK):
                hashes_list.append(dic_dirs[os.path.join(root, dir)])
        for fil in files:
            file_hash = ""  # store the hash of the file
            if args.n:
                file_hash = sha256(fil.encode('utf-8')).hexdigest()
                if args.c:
                    if os.access(os.path.join(root, fil), os.R_OK):
                        file_list.append(os.path.join(root, fil))
                        with open(os.path.join(root, fil),"rb") as f:  # get the content of the file in bytes
                            bytes = f.read()
                            hash_find = sha256()
                            hash_find.update(bytes)
                            hash_content = hash_find.hexdigest()
                            concat_hash = file_hash + hash_content  # concatenate name and content hashes for re-hashing
                            file_hash = sha256(concat_hash.encode('utf-8')).hexdigest()
                else:
                    hashes_list.append(file_hash)
            else:
                if os.access(os.path.join(root, fil), os.R_OK):
                    with open(os.path.join(root, fil),"rb") as f:
                        bytes = f.read()
                        hash_find = sha256()
                        hash_find.update(bytes)
                        file_hash = hash_find.hexdigest()
                    hashes_list.append(file_hash)
            if os.access(os.path.join(root, fil), os.R_OK):
                dic_files[os.path.join(root, fil)] = file_hash  # assign hash to the file
                val = dic_file_hashes.setdefault(file_hash, [os.path.join(root, fil)])
                if os.path.join(root, fil) not in val:  # update the paths list corresponding to the given hash
                    val += [os.path.join(root, fil)]
        if len(dirs) == 0 and len(files) == 0:
            dir_hash = sha256("".encode('utf-8')).hexdigest()  # store the hash of the directory
            if args.n:
                hash_name = sha256(os.path.split(root)[1].encode('utf-8')).hexdigest()
                concat_hash = hash_name + dir_hash  # concatenate name and content hashes for re-hashing
                dir_hash = sha256(concat_hash.encode('utf-8')).hexdigest()
            dic_dirs[root] = dir_hash  # assign hash to the empty directory
            val = dic_dir_hashes.setdefault(dir_hash, [root])
            if root not in val:  # update the paths list corresponding to the given hash
                val += [root]
        hashes_list.sort()
        file_list.sort()
        concat_hash = ""
        for elm in hashes_list:
            concat_hash += elm  # concatenate hashes from lexicographically sorted hashes list
        for elm in file_list:
            concat_hash += dic_files[elm]  # concatenate hasheh corresponding to lexicographically sorted file names list
        dir_hash = sha256(concat_hash.encode('utf-8')).hexdigest()
        if args.n:
            hash_name = sha256(os.path.split(root)[1].encode('utf-8')).hexdigest()
            concat_hash = hash_name + concat_hash  # concatenate name and content hashes for re-hashing
            dir_hash = sha256(concat_hash.encode('utf-8')).hexdigest()
        dic_dirs[root] = dir_hash  # assign hash to currently processed directory
        val = dic_dir_hashes.setdefault(dir_hash, [root])
        if root not in val:  # update the paths list corresponding to the given hash
            val += [root]

# create a list of path lists in lexicographically sorted order
def duplicates_list(dic):
    sorted_list = list()
    for key in dic:
        if len(dic[key]) > 1:
            tmp = dic[key]
            tmp.sort()
            sorted_list.append(tmp)
    sorted_list.sort()
    return sorted_list

# print the output based on the given arguments
if args.d:
    if args.f:
        dic_dir_hashes.update(dic_file_hashes)
    sorted_dirs = duplicates_list(dic_dir_hashes)
    if args.s and not (args.n and not args.c):
        for dup in sorted(sorted_dirs, key=lambda dup: os.stat(dup[0]).st_size, reverse=True):
            for elm in dup:
                print(elm, "\t", os.stat(dup[0]).st_size)
            print()
    else:
        for dup in sorted_dirs:
            for elm in dup:
                print(elm)
            print()
else:
    sorted_files = duplicates_list(dic_file_hashes)
    if args.s and not (args.n and not args.c):
        for dup in sorted(sorted_files, key=lambda dup: os.stat(dup[0]).st_size, reverse=True):
            for elm in dup:
                print(elm, "\t", os.stat(dup[0]).st_size)
            print()
    else:
        for dup in sorted_files:
            for elm in dup:
                print(elm)
            print()