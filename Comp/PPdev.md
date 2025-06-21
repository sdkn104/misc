## Resources
- [connector ref](https://learn.microsoft.com/en-us/connectors/connector-reference/connector-reference-powerautomate-connectors)
- [actions ref](https://learn.microsoft.com/en-us/power-automate/desktop-flows/actions-reference)

## Forms to DB
* Forms
  - Privacy indication
  - set notification destination mail address
* Power Automate
  - function:
    1. when submitted, copy to excel log, create file
    1. daily, check ids in excel log,
        1. if id is lack, try to get the id
            1. if gotten, insert to excel log, create file
            1. else insert dummy entry for excel log
    1. daily, delete old items in excel log
    * when error, mail to admin, and raise error
    * write copy date time, which program writes to excel log

* PAD
    * periodically runs
    1. Get file metadata using path
    1. List folder
    1. for each file
        1. get iraiNo and date from file name
        1. write to DB
        1. delete the file

## sharepoint list to local csv file
1. get items
1. select
1. create CSV table
1. decodeUriComponent('%EF%BB%BF')  (https://zenn.dev/karamem0/articles/2020_09_30_120000)
1. create file

## download lists and files
### Lists
1. get all lists and libraries
1. for each
    1. if document library
        1. Get files (properties only)
        1. for each file
            1. Get file content
            1. create file name
            1. convert binary to file
    1. else f list
        1. Get items
        1. For each item
            1. formatting file
            1. create file
            1. get attachments
            1. for each att
                create file