# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command


# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class token_my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

########### =========================== MY Custom Commands ===================================
class vscode(Command):
    def execute(self):
        if self.fm.thisdir.marked_items:
            selection = [f.path for f in self.fm.thistab.get_selection()]
            for file in selection:
                self.fm.execute_command(f"code '{file}'")
        else:
            target_filename = self.fm.thisfile.path
            self.fm.execute_command(f"code '{target_filename}'")
    def tab(self, tabnum):
        return self._tab_directory_content()


class gk(Command):
    def execute(self):
        self.fm.execute_command('guake -n $(pwd) --show')
    def tab(self, tabnum):
        return self._tab_directory_content()


class dol(Command):
    def execute(self):
        self.fm.execute_command('dolphin --new-window . &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()

class k4(Command):
    def execute(self):
        self.fm.execute_command('k4dirstat . &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()

class kon(Command):
    def execute(self):
        self.fm.execute_command('konsole . &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()

class sublimeDir(Command):
    def execute(self):
        self.fm.execute_command(f'/home/t/stuff/sublime_text/sublime_text . -n &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()

class sublimeSingle(Command):
    def execute(self):
        if self.fm.thisdir.marked_items:
            sel_list = []
            selection = [f.path for f in self.fm.thistab.get_selection()]
            for file in selection:
                sel_list.append(file)
            self.fm.execute_command(f'''/home/t/stuff/sublime_text/sublime_text {' '.join(f"'{w}'" for w in sel_list)} -n''')
        else:
            target_filename = self.fm.thisfile.path
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return
        self.fm.execute_command(f"/home/t/stuff/sublime_text/sublime_text '{target_filename}' -n")
    def tab(self, tabnum):
        return self._tab_directory_content()

class vscodedir(Command):
    def execute(self):
        self.fm.execute_command('code . -n &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()


class bash(Command):
    def execute(self):
        self.fm.execute_command('bash')
    def tab(self, tabnum):
        return self._tab_directory_content()


class git(Command):
    def execute(self):
        if self.arg(1):
            url = self.rest(1)
            repo_name = url.replace('.git', '/').split('/')[-2]
            self.fm.execute_command(f"git clone {url}") 
            self.fm.cd(repo_name)
            self.fm.execute_command(f"rm -rf .git")
            self.fm.execute_command(f"echo {url} > ORIG_REPO_URL.txt")
    def tab(self, tabnum):
        return self._tab_directory_content()

class ln(Command):
    def execute(self):
        self.fm.notify(f"'{self.fm.thisfile}'")
        self.fm.execute_command(f"ln -s {self.fm.thisfile} /home/t/Desktop/paths")
    def tab(self, tabnum):
        return self._tab_directory_content()

class copy_file_content(Command):
    def execute(self):
        if self.fm.thisfile.is_directory:
            self.fm.notify('not allowed on directories', bad=True)
            return
        else:
            self.fm.execute_command(f"xclip -sel c < '{self.fm.thisfile}'")
            self.fm.notify(f"'{self.fm.thisfile}' copied")
    def tab(self, tabnum):
        return self._tab_directory_content()

class paste_file_content(Command):
    def execute(self):
        if self.fm.thisfile.is_directory:
            self.fm.notify('not allowed on directories', bad=True)
            return
        else:
            self.fm.execute_command(f"xsel -b > '{self.fm.thisfile}'")
            self.fm.notify(f"'{self.fm.thisfile}' pasted")
    def tab(self, tabnum):
        return self._tab_directory_content()

class append_file_content(Command):
    def execute(self):
        if self.fm.thisfile.is_directory:
            self.fm.notify('not allowed on directories', bad=True)
            return
        else:
            self.fm.execute_command(f"xsel -b >> '{self.fm.thisfile}'")
            self.fm.notify(f"'{self.fm.thisfile}' pasted")
    def tab(self, tabnum):
        return self._tab_directory_content()

class open_nvim(Command):
    def execute(self):
        self.fm.execute_command('nvim')
    def tab(self, tabnum):
        return self._tab_directory_content()

class vim_rename(Command):
    def execute(self):
        import random
        import string
        chars = string.ascii_letters + string.digits 
        r_string = ''.join([random.choice(chars) for x in range(15)])
        if len(self.fm.thisdir.marked_items) > 1:
            self.fm.notify(f'only 1 file per')
        else:
             old_name = self.fm.thisfile.basename
             new_name = f"temp_rename_{r_string}"
             self.fm.execute_command(f"echo '{old_name}' > {new_name}")
             self.fm.execute_command(f"nvim {new_name}")
             with open(new_name, 'r') as f:
                content = f.read().split('\n')[0]
                self.fm.rename(self.fm.thisfile, content)
             self.fm.execute_command(f"rm {self.fm.thisdir}/{new_name}")
    def tab(self, tabnum):
        return self._tab_directory_content()

class runbuild(Command):
    def execute(self):
        if self.fm.thisdir.marked_items:
            selection = [f.path for f in self.fm.thistab.get_selection()]
            for file in selection:
                ext = file.split('.')[-1]
                self.runfile(ext, file)
        else:
            file = self.fm.thisfile.path
            ext = file.split('.')[-1]
            self.runfile(ext, file)

    def runfile(self, ext, file):
        if ext=='py':
            self.fm.execute_command(f"path/to/builds/runpy.sh {file} &> /dev/null & disown")
        if ext=='js': 
            self.fm.execute_command(f"path/to/builds/runjs.sh {file} &> /dev/null & disown")
        if ext=='go': 
            self.fm.execute_command(f"path/to/builds/rungo.sh {file} &> /dev/null & disown")

    def tab(self, tabnum):
        return self._tab_directory_content()


class yank_realpath(Command):
    def execute(self):
        real_p = f"realpath {self.fm.thisfile}"
        self.fm.execute_command(f"{real_p} | xclip -sel clip")
        self.fm.notify(f"{real_p} copied")
    def tab(self, tabnum):
        return self._tab_directory_content()

class ranger_here(Command):
    def execute(self):
        self.fm.execute_command(f"xfce4-terminal --hold -x ranger . & /dev/null & disown")

    def tab(self, tabnum):
        return self._tab_directory_content()


class shutter_edit(Command):
    def execute(self):
        file = self.fm.thisfile
        self.fm.execute_command(f"""xfce4-terminal -e '''bash -c "shutter {file}"'''""")
    def tab(self, tabnum):
        return self._tab_directory_content()


class animated_gif_mp4(Command):
    def execute(self):
        file = self.fm.thisfile
        # self.fm.execute_command(f'shutter {file} &> /dev/null & disown')
        self.fm.execute_command(f'')
        # self.fm.execute_command(f"""xfce4-terminal -e '''bash -c "shutter {file}"'''""")
        # self.fm.notify(file)
    def tab(self, tabnum):
        return self._tab_directory_content()

class trashcli(Command):
    def execute(self):
        if self.fm.thisdir.marked_items:
            selection = [f.path for f in self.fm.thistab.get_selection()]
            for file in selection:
                self.fm.execute_command(f"trash-put '{file}'")
        else:
            target_filename = self.fm.thisfile.path
            self.fm.execute_command(f"trash-put '{target_filename}'")
    def tab(self, tabnum):
        return self._tab_directory_content()


class gwenview_here(Command):
    def execute(self):
        self.fm.execute_command('gwenview . &> /dev/null & disown')
    def tab(self, tabnum):
        return self._tab_directory_content()


# -------------- unused examples
# -------------- unused examples
# -------------- unused examples


class kk(Command):
    def execute(self):
        self.fm.execute_command(f"./path/to/test.sh {self.fm.thisfile}")
    def tab(self, tabnum):
        return self._tab_directory_content()

class simple_execute(Command):
    def execute(self):
        self.fm.execute_command('guake -n $(pwd) --show')
    def tab(self, tabnum):
        return self._tab_directory_content()

############## ---------NOTES--------------------------


# self.fm.thisfile.basename
# --- returns just the basename of file (something.txt)

#self.fm.thisfile
#--- return the path + file name. full path to file


#self.fm.thisfile.path
# --- returns same as thisfile, full path to file

#self.fm.<command>(args)
# --- executes an existing command in this file/Commands


#self.fm.open_console
# --- open string in console but doesnt execute


# self.fm.execute_console(string): 
# --- Execute the string as a ranger command.




