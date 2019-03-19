# Datamap

Manages folder mappings to help organize huge ammounts of data.

Works reading mappings from a "mappings" file located at datamap home folder.

## Datamap home folder

Is located on $XDG_CONFIG_HOME/datamap, or, if folder doesnt exists, is on $HOME/.config/datamap


## "mappings" file format

Empty lines and lines starting with "#" are ignored. Each line is the full path of a "mapped" folder, ie, must contain a ".datamap" file. Its possible use environment variables on folder names (they are expanded via python's "os.path.expandvars").


## ".datamap" file format

Lines not containing a "=" char are ignored

Lines starting with "#" are ignored

All other lines are read in "key=value" format


### Properties

"description" and "category" are required properties. If not present a error will be throw. Is very recommended this property be set on "default_properties" file.

"folder" always exists and contains full path of mapping (even when explicitly set to something else).

"disable_bookmark" defaults to "no". In listing this property will be printed only when have "yes" value.

"gtk_bookmark" is the user friendly name of GTK 3 bookmark created. Defaults to base name of folder (throught python's 3 "os.path.basename")


## "default_properties" file

Contains "global" properties appended to ones read from ".datamap" files. Its located at datamap home folder, and is named "default_properties.datamap". Has the same format of ".datamap" file


## TODO

- Filter list by category **#next**
- Extract classes to their own files **#quick** **#next**
- Rename category to categories and turn it into a list **#backlog**
- Creata a \--create-datamap command, must create .datamap file with the properties and entry on mappings file **#backlog**
- Find mappings on a specified folder **#backlog**
- Filter list by property existence **#backlog**
- Filter list by property + value **#backlog**
- Mappings of URLs, usefull to describe repositories not cloned locally **#backlog**
- List all existing categories **#backlog**
- List all existing properties **#backlog**
- Dynamically find .datamap files on folder specified on mappings **#backlog**