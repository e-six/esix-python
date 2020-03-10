#!/usr/bin/env python3

import argparse
import esix
import hashlib
import json
import os
import shutil


__NAME__ = 'e621 Downloader'
__VERSION__ = '0.91'
__UPDATED__ = '2014-07-21'

FILE_MD5_DATA = '.md5data'
FILE_DOWNLOAD_LOG = 'download-log.txt'


class ArgumentParserError(Exception): pass
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def get_args():
    parser = ArgumentParser(fromfile_prefix_chars='@',
                            epilog="Multiple queries can be run in a single "+\
                            "session. Format must follow the pattern of -q "+\
                            "QUERY1 -d DEST1 -q QUERY2 -d DEST2[...] "+\
                            "--other-options.")
    parser.add_argument('-q', '--query',action='append',required=True,type=str,
                        help="Indicates the following parameter is a search "+\
                        "query. Must be surrounded by quotes if spaces exist.")
    parser.add_argument('-d', '--dest',action='append',required=True,type=str,
                        help="Indicates the following parameter is a "+\
                        "destination directory. Must be paired with a query.")
    parser.add_argument('--noverify',dest='verify',action='store_false',
                        help='Do not verify settings before downloading.')
    parser.add_argument('--nolog',action='store_true',
                        help='Do not save a log file for this session.')
    parser.add_argument('--enumerate',action='store_true',
                        help='Prepend a number to downloaded files.')
    parser.add_argument('--storemeta',dest='store_meta',action='store_true',
                        help='Save downloaded posts\' metadata in a subfolder.')
    parser.add_argument('--nocheck',dest='check_extra',action='store_false',
                        help='Do not check if extra folder images exist on '+\
                        'the site.')
    parser.add_argument('--onlynew',dest='new_only',action='store_true',
                        help='Stop downloading once an image that already '+\
                        'exists is found.')
    parser.add_argument('--copyextras',dest='copy_extras',action='store_true',
                        help='Copy existing files not found in search to '+\
                        'subdirectories. Will not run if --onlynew is set.')
    args = vars(parser.parse_args())
    if len(args['query']) != len(args['dest']):
        parser.error('You must specify the same number of queries and '+\
                     'destination directories.')
    args['data'] = []
    for i in range(len(args['dest'])):
        if args['dest'][i] != "" and not args['dest'][i].endswith("/"):
            args['dest'][i] += "/"
        elif args['dest'][i] == "": args['dest'][i] = "./"
        args['data'].append((args['query'][i],args['dest'][i]))
    del args['query'],args['dest']
    return args

def log_msg(folder,msg,echo=False):
    if folder != "" and not folder.endswith("/"): folder += "/"
    if echo:
        print(msg)
    log = open(folder+FILE_DOWNLOAD_LOG, "a")
    log.write(msg+'\n')
    log.close()

def main_menu():
    dl_loc = None
    enum = False
    store_meta = False
    ver = True
    dl_data = []
    ans = -1
    while ans != 0:
        print('1. Add query to queue.')
        print('2. Clear download queue.')
        print('3. '+('Set' if not dl_loc else 'Clear')+\
              ' global download location.')
        print('4. Turn '+('on' if not enum else 'off')+' enumeration.')
        print('5. '+('Store' if not store_meta else 'Do not store')+\
              ' image metadata.')
        print('6. Turn '+('on' if not ver else 'off')+ ' query verification.')
        print('7. Begin download of '+str(len(dl_data))+' queries.')
        print('0. Cancel and exit')
        try: ans = int(input('> '))
        except: ans = -1
        print()
        if ans == 1:
            query = input('Enter search query:\n')
            if dl_loc: loc = dl_loc
            else: loc = input('Enter download location (leave blank for '+\
                              'current directory):\n')
            if loc == '': loc = './'
            dl_data.append((query,loc))
        elif ans == 2:
            print('This will clear all '+str(len(dl_data))+ ' queries '+\
                  'from the queue.')
            chk_clear = input('Is this okay? [y/n]: ').lower()
            while chk_clear not in ['y','n']:
                print('\nInvalid input.')
                print('This will clear all '+str(len(dl_data))+ ' queries '+\
                      'from the queue.')
                chk_clear = input('Is this okay? [y/n]: ').lower()
            if chk_clear == 'y':
                dl_data = []
                print('Queue cleared.')
        elif ans == 3:
            if dl_loc:
                dl_loc = None
                continue
            dl_loc = input('Enter global download location:\n')
        elif ans == 4: enum = not enum
        elif ans == 5: store_meta = not store_meta
        elif ans == 6: ver = not ver
        elif ans == 7:
            return {'data': dl_data,
                    'verify': ver,
                    'enumerate': enum,
                    'store_meta': store_meta,
                    'check_extra': True,
                    'new_only': False,
                    'copy_extras': False}
        elif ans == 0:
            break
        print()
    return {'data':[], 'verify':True, 'enumerate':False,
            'check_extra':True, 'new_only':False,
            'store_meta':False, 'copy_extras':False}

def verify(query, dest):
    print('\nDownloading ALL images containing search term(s): '+query)
    print('\nDownloading to folder: '+dest)
    correct = input("\n\tIs this correct? [y/n]: ").lower()
    while correct not in ['y', 'n']:
        correct = input("\tInvalid Input. Are the Above Correct? [y/n]: ")
    if correct == 'n':
        print("\nScript Stopped by User\n")
        return False
    return True

def gen_md5_list(folder):
    valid_exts = ('.png','.gif','.jpg','.swf','.webm')
    files = {}
    print('Generating folder images md5 list')
    if not os.path.exists(folder):
        print('Directory Not Found. Creating Folder...')
        os.makedirs(folder)
    data_file = open(folder+FILE_MD5_DATA,'wb')
    for f in os.listdir(folder):
        if os.path.isfile(folder+f) and f.endswith(valid_exts):
            try:
                with open(folder+f,'rb') as file:
                    md5 = hashlib.md5(file.read()).hexdigest()
                files[md5] = f
            except: continue
    data_file.write(bytes(json.dumps(files,indent=4,sort_keys=True),'UTF-8'))
    data_file.close()
    return files

def get_md5_list(folder):
    if not os.path.isfile(folder+FILE_MD5_DATA):
        return gen_md5_list(folder)
    with open(folder+FILE_MD5_DATA) as data_file:
        try: data = json.load(data_file)
        except: data = gen_md5_list(folder)
    return data

def copy_file(src,dest):
    if not os.path.isdir(dest): os.makedirs(dest)
    if not os.path.isfile(src): return
    shutil.copy2(src,dest)


def run(query,dest,do_verify=True,do_enum=False,write_metadata=False,
        check_extra=True,new_only=False,copy_extras=False):
    if dest != "" and not dest.endswith("/"): dest += "/"
    downloaded,failed,extras,notfound = ([] for x in range(4))
    downloaded = 0
    if do_verify:
        if not verify(query,dest): return
    folder_md5_list = get_md5_list(dest)
    new_md5_list = folder_md5_list.copy()
    search_md5_list = []
    log = open(dest+FILE_DOWNLOAD_LOG, "w")
    log.close()
    if not do_verify:
        log_msg(dest,
                'Downloading images containing search term(s): '+query,True)
        log_msg(dest,'Downloading to folder: '+dest+'\n',True)

    log_msg(dest,'Running search...',True)
    # Hack for getting pools - TODO make this better
    check = query.split(':')
    if len(check) == 2 and check[0].lower() == 'pool':
        search_result = esix.pool.Pool(check[1]).posts
        is_pool = True
    else:
        search_result = esix.post.search(query,0)
        is_pool = False
    if do_enum:
        search_result = list(search_result)
        if is_pool: search_result = list(reversed(search_result))
        total_imgs = len(search_result)
        log_msg(dest,
                '\n\n'+str(total_imgs)+' images found. Downloading images...',
                True)
    else:
        log_msg(dest,'\n\nDownloading images...',True)
        total_imgs = 0
    for post in search_result:
        log_msg(dest,'Post '+str(post.id))
        file_name = post.md5 + '.' + post.ext
        if do_enum:
            save_name = str(
                total_imgs-search_result.index(post)
                ).zfill(len(str(total_imgs)))+' - '+file_name
        else:
            total_imgs += 1
            save_name = file_name
        search_md5_list.append(post.md5)
        if post.md5 in folder_md5_list:
            existing_file = folder_md5_list[post.md5]
            if not existing_file == save_name:
                log_msg(dest,'\tRenaming file '+existing_file+' to '+save_name,
                        True)
                try: os.rename(dest+existing_file,dest+save_name)
                except:
                    log_msg(dest,'\tError renaming file',True)
            else:
                log_msg(dest,'\tFile '+save_name+' already exists.')
                if new_only:
                    log_msg(dest,'Ending download...')
                    break
        else:
            dl_success = False
            while not dl_success:
                log_msg(dest,'\tDownloading: '+save_name,True)
                try:
                    post.download(dest,save_name)
                except esix.errors.SiteLoadError as err:
                    log_msg(dest,'\tError downloading post: '+str(err),True)
                    print("\tPlease wait a bit and press [Enter] to try again.")
                    input()
                except Exception as err:
                    log_msg(dest,'\tError, unable to download post '+\
                            str(post.id)+': '+str(err),True)
                    failed.append(post.id)
                    break
                else:
                    downloaded += 1
                    dl_success = True
                    new_md5_list[post.md5] = save_name
        if write_metadata:
            dl_success = False
            while not dl_success:
                try:
                    post.download_metadata(dest + '.metadata/',
                                           comments=False, pretty=True)
                except esix.errors.SiteLoadError as err:
                    log_msg(dest,'\tError writing metadata: '+str(err),True)
                    print("\tPlease wait a bit and press [Enter] to try again.")
                    input()
                except Exception as err:
                    log_msg(dest,'\tError writing metadata: '+str(err),True)
                    break
                else:
                    log_msg(dest,'\tWrote/Updated metadata: '+post.md5)
                    dl_success = True
    if downloaded > 0:
        with open(dest+FILE_MD5_DATA,'wb') as data_file:
            data_file.write(bytes(json.dumps(new_md5_list,indent=4,
                                             sort_keys=True),'UTF-8'))

    log_msg(dest,'Done.',True)
    if check_extra and not new_only:
        log_msg(dest,'\nSearching for extra images...',True)
        for md5 in folder_md5_list:
            if md5 not in search_md5_list:
                img = folder_md5_list[md5]
                srch = list(esix.post.search('md5:'+md5))
                if len(srch):
                    extras.append(img)
                    log_msg(dest,"File "+img+" found in folder and on site, "+\
                            "but not in requested search.")
                    try:
                        srch[0].download_metadata(dest+'.metadata/',
                                                  comments=True, pretty=True)
                    except: pass
                    if copy_extras: copy_file(dest+img,dest+'!extra/onsite/')
                else:
                    notfound.append(img)
                    log_msg(dest,
                            "File "+img+" found in folder, but not on site.")
                    if copy_extras: copy_file(dest+img,dest+'!extra/notfound/')
    if not new_only or is_pool:
        log_msg(dest,"\nSuccessfully downloaded "+str(downloaded)+" of "+\
                str(total_imgs)+" images\n",True)
    else:
        log_msg(dest,"\nSuccessfully downloaded "+str(downloaded)+" images\n",
                True)
    if extras or notfound:
        log_msg(dest,str(len(extras+notfound))+" files found in folder "+\
                "but not in requested search.",True)
        if copy_extras: log_msg(dest,"Copied to /!extra.",True)
    if failed: log_msg(dest,str(len(failed))+" posts failed to download.",True)
    for post_id in failed:
        log_msg(dest,str(post_id))
    print("See "+FILE_DOWNLOAD_LOG+" for details.")
    print("\n\n")
    return downloaded


if __name__ == '__main__':
    print(__NAME__+' v'+__VERSION__+' - Updated '+__UPDATED__+'\n')
    try: args = get_args()
    except ArgumentParserError: args = main_menu()
    total_downloaded = 0
    for query,dest in args['data']:
        total_downloaded += run(query,dest,args['verify'],
                                args['enumerate'],args['store_meta'],
                                args['check_extra'],args['new_only'],
                                args['copy_extras'])
    print("Total images downloaded: "+str(total_downloaded)+"\n")
    if args['verify']:
        input('Press ENTER to Exit')
    print("________DONE________\n\n")
