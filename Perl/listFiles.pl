use strict;
use warnings;
use File::Find;
use Cwd;
use File::Copy;
use Image::ExifTool;
use Time::Local;

#指定フォルダ以下のファイルの更新日時などのリストを出力する。

# 対象ディレクトリ名(相対パスでもOKです)
#my $dir = "G:/BACKUP_PC/Toshiyuki.tmp.delete/Pictures/史織/fromHDD";
my $dir = "Z:/HOKAN/Pictures/史織"; #getcwd; 

open(LOG,">listFiles.csv") or die "cannot open file\n";
find(\&print_file, $dir);

print LOG "File,Path,ModDate,ExifCDate\n";
sub print_file {
    my $file = $_;
    my $path = $File::Find::name;
    print $path,"\n";
    my $modtime = (stat($path))[9] ;
    my $mod = localtime($modtime);

    printf LOG "%s,%s,%s", $file, $path, $mod;

#    my $exifTool = new Image::ExifTool;
#    my $info = $exifTool->ImageInfo($path, 'CreateDate');
#    my $create_date = $info->{'CreateDate'};
#    $create_date = "" unless defined($create_date);
#   print LOG ",$create_date"; 

    print LOG "\n";
}

