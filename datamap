#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from urllib.parse import quote
from copy import deepcopy


def parse_command_line():
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--list", action="store_true", help="List mappings")
    parser.add_argument("-b", "--update-bookmarks", action="store_true", help="Update gtk (3.0) bookmarks file")
    parser.add_argument("--create-datamap-files", action="store_true", help="Create datamap files for maps it doesnt exist")
    parser.add_argument("--create-datamap-folder", action="store_true", help="Make a datamap folder with links to every mapped folder")
    parser.add_argument("-c", "--check", action="store_true", help="Check health of mappings")
    # parser.add_argument("-f", "--find-maps", help="Find for .description files from current folder")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbosity")


    return parser.parse_args()


def xdg_config_home():
    return os.environ.get("XDG_CONFIG_HOME", os.environ.get("HOME") + "/.config")


def datamap_home():
    return xdg_config_home() + "/datamap"


def load_mappings():
    mappings_file = open(datamap_home() + "/mappings")

    mappings = []

    for line in mappings_file:
        stripped_line = line.strip()

        if not stripped_line.startswith("#") and stripped_line != "":
            mappings.append(os.path.expandvars(stripped_line))

    return mappings


def load_properties(file, copy_default=True):
    properties = deepcopy(default_properties) if copy_default else {}

    with open(file, 'r') as f:
        for line in f:
            line = line.rstrip()

            if "=" not in line:
                continue
            if line.startswith("#"):
                continue

            k, v = line.split("=", 1)
            properties[k] = v

    return properties


global default_properties
default_properties = load_properties(datamap_home() + "/default_properties.datamap", copy_default=False)


def get_datamap_filename(folder):
    return "{}/.datamap".format(folder)


def visit_mappings(visitor):
    mappings = load_mappings()

    for folder in mappings:
        if not os.path.isdir(folder):
            visitor.not_found(folder)
        else:
            properties_file = get_datamap_filename(folder)

            if not os.path.isfile(properties_file):
                visitor.no_datamap_file(folder)
            else:
                props = load_properties(properties_file)

                props["folder"] = folder
                props.setdefault("gtk_bookmark", os.path.basename(folder))
                props.setdefault("disable_bookmark", "no")

                visitor.visit(folder, props)


class ShowMaps(object):

    def not_found(self, folder):
        print("- '{}' folder #not_found".format(folder))
        print()

    def no_datamap_file(self, folder):
        print("- {} #no_datamap_file".format(folder))
        print()

    def visit(self, folder, props):
        map_line = "- " + props["description"]

        for k in props:
            if k not in ["description"]:
                if k != "disable_bookmark" or props[k] != "no":
                    map_line += " #{}:{}".format(k, props[k])

        print(map_line)
        print()

    def run(self):
        print(":: Datamap")
        print()

        visit_mappings(self)


class BookmarkUpdater(object):

    def _get_bookmarks_file_name(self):
        return "{}/gtk-3.0/bookmarks".format(xdg_config_home())

    def not_found(self, folder):
        print("'{}' not found".format(folder))

    def no_datamap_file(self, folder):
        self.visit(folder, {})

    def visit(self, folder, props):
        if props.get("disable_bookmark") == "yes":
            if args.verbose:
                print("Skipping bookmark at '{folder}' (disable_bookmark set to 'yes')".format(**props))

            return

        props["folder"] = quote(folder)
        props.setdefault("gtk_bookmark", os.path.basename(folder))
        self.bookmarks.write("file://{folder} {gtk_bookmark}\n".format(**props))

    def run(self):
        # TODO Save old bookmarks file
        self.bookmarks = open(self._get_bookmarks_file_name(), 'w')

        visit_mappings(self)

        self.bookmarks.close()


class DatamapFileCreator(object):

    def not_found(self, folder):
        print("{} not found".format(folder))

    def no_datamap_file(self, folder):
        datamap_file = open(get_datamap_filename(folder), "w")

        description = os.path.basename(folder)

        datamap_file.write("description={}\n".format(description))

        datamap_file.close()

    def visit(self, folder, props):
        pass

    def run(self):
        visit_mappings(self)


class DatamapChecker(object):

    def _check_required_properties_on_default_properties(self):
        if not "description" in default_properties:
            print("[WARNING] 'description' property not set in 'default_properties'")


        if not "category" in default_properties:
            print("[WARNING] 'category' property not set in 'default_properties'")

    def _status(self, folder, status):
        print("'{}': {}".format(folder, status))

    def not_found(self, folder):
        self._some_not_ok = True
        self._status(folder, "folder not found")

    def no_datamap_file(self, folder):
        self._some_not_ok = True
        self._status(folder, "have no .datamap file")

    def visit(self, folder, props):
        ok = True

        if not "description" in props:
            self._status(folder, "[FATAL] No 'description' property set")
            ok = False

        if not "category" in props:
            self._status(folder, "[FATAL] No 'category' property set")
            ok = False

        if not ok:
            self._some_not_ok = False

    def run(self):
        self._check_required_properties_on_default_properties()

        self._some_not_ok = False
        visit_mappings(self)

        print()

        print("Errors were found" if self._some_not_ok else "No errors were found")


class DatamapFolderCreator(object):

    def not_found(self, folder):
        self._some_not_ok = True
        print("'{}' not found".format(folder))

    def no_datamap_file(self, folder):
        self._make_link("none", folder)

    def visit(self, folder, props):
        self._make_link(props["category"], folder)

    def _datamap_folder_location(self):
        # TODO Put this in a config file
        return os.path.expandvars("${HOME}/datamap")

    def _make_link(self, category, folder):
        basename = os.path.basename(folder)

        basepath = "{}/{}".format(self._datamap_folder_location(), "no category" if category == "none" else category)

        source = "{}/{}".format(basepath, basename)

        if os.path.exists(source):
            os.unlink(source)
        elif not os.path.exists(basepath):
            os.makedirs(basepath)

        os.symlink(folder, source)

    def run(self):
        self._some_not_ok = False

        visit_mappings(self)

        print()

        print("Errors were found" if self._some_not_ok else "No errors were found")


def error(message):
    print("Error: " + message)
    sys.exit(1)


def main():
    global args
    args = parse_command_line()

    if args.verbose:
        print(args)

    if args.list:
        ShowMaps().run()
    elif args.update_bookmarks:
        BookmarkUpdater().run()
    elif args.create_datamap_files:
        DatamapFileCreator().run()
    elif args.check:
        DatamapChecker().run()
    elif args.create_datamap_folder:
        DatamapFolderCreator().run()
    else:
        error("At least one action must be specified")

if __name__ == '__main__':
    main()
