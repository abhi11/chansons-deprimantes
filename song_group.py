import re
import json

def printf(s):
    print json.dumps(s, indent=4)

class ReadmeParser:
    def __init__(self, readme_path = "README.md"):
        self.readme_path = readme_path
        self.song_dict = {}
        self.__parse_file()
    
    def __read_file(self, filename):
        with open(filename) as fp:
            file_contents = fp.read()
            return file_contents

    def __parse_file(self):
        file_contents = self.__read_file(self.readme_path)
        placeholder = "_PLACEHOLDER_ -->"
        start_index = file_contents.index(placeholder)+len(placeholder)
        self.__offset = start_index
        parse_str = file_contents[start_index:].strip()

        #segregate by Language(defined by ## <Language>)
        lang_split = re.split(r'##\s*(.+)',parse_str)[1:]
        lang_dict = {lang_split[i]:lang_split[i+1] for i in range(0, len(lang_split),2)}
        #printf(lang_dict)
        keys = [
                    "song_name",
                    "song_link",
                    "band_name",
                    "band_link"
                ]
        for lang, song_str in lang_dict.items():
            str_re = r'^\s*\*\s+\[(?P<song_name>.*?)\]\((?P<song_link>.*?)\)\s+by\s+\[(?P<band_name>.*?)\]\((?P<band_link>.*?)\)\s*$'
            self.song_dict[lang] = []
            for e in re.finditer(str_re, song_str, re.MULTILINE):
                self.song_dict[lang].append({k:e.group(k) for k in keys})
        #printf(self.song_dict)

    def __get_print_list(self):
        return sorted(self.song_dict.items(), key=lambda t:len(t[1]), reverse=True)

    def add_song(self,language, song_name, song_link, band_name, band_link):
        self.__add_new_song({
                "song_name" : song_name,
                "song_link" : song_link,
                "band_name" : band_name,
                "band_link" : band_link,
                "language"  : language
            })

    def __add_new_song(self, song_details_dict):
        lang = song_details_dict["language"]
        song_details_dict.pop("language")
        if lang not in self.song_dict:
            self.song_dict[lang] = []
        self.song_dict[lang].append(song_details_dict)

    def __write_file(self, contents):
        with open(self.readme_path , 'r+') as fp:
            fp.seek(self.__offset)
            fp.truncate()
            fp.write(contents)
    
    def publish_new_file(self):
        song_str = ""
        for lang, song_list in self.__get_print_list():
            song_str += ("\n\n## %s\n\n" % lang)
            for s_dict in song_list:
                song_str += "* [%s](%s) by [%s](%s)\n" % (s_dict["song_name"],s_dict["song_link"],s_dict["band_name"],s_dict["band_link"])
        print song_str
        self.__write_file(song_str)
    
if __name__ == "__main__":
    readme = ReadmeParser("README.md")

    songs = [
            [
                "English",
                "Unchained Melody",
                "https://www.youtube.com/watch?v=zrK5u5W8afc",
                "Righteous Brothers",
                "http://en.wikipedia.org/wiki/The_Righteous_Brothers"
            ]            
        ]


    for s in songs:
        readme.add_song(*s)
    
    #Example of where this can help - 
    #Re-organising by Bandname
    d = readme.song_dict
    for lang,s_li in d.items():
        s_li = sorted(s_li, key=lambda t:t["band_name"])
        d[lang] = s_li

    ##IMP##
    #Be careful while using the below function.
    #It will truncate the content portion of the file.
    #Make sure you have a back up :P
    readme.publish_new_file()
    
