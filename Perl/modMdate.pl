use strict;
use warnings;
use File::Find;
use Cwd;
use File::Copy;
use Image::ExifTool;
use Time::Local;

#指定フォルダ以下の、
#   .jpgファイルの更新日時をExif撮影日時に設定する。
#   VID_yyyymmdd_hhmmdd.mp4形式フィアルの更新日時をyyyymmddhhmmddに設定する。(freetel format)

# 対象ディレクトリ名(相対パスでもOKです)
#my $dir = "G:/BACKUP_PC/Toshiyuki.tmp.delete/Pictures/史織/fromHDD";
#my $dir = "Z:/HOKAN/Pictures/史織/fromHDD"; #getcwd; 
my $dir = getcwd; 

find(\&print_file, $dir);

sub print_file {
    my $file = $_;
    my $path = $File::Find::name;

    printf "%s,%s,", $file, $path;
    #my $modtime = (stat($path))[9] ;
    #my $mod = localtime($modtime);
    #print "[更新日：$mod]" , ","; 

    if( $file =~ /.(jpg|JPG)$/ ) {

      my $exifTool = new Image::ExifTool;
      my $info = $exifTool->ImageInfo($path, 'CreateDate');
      my $create_date = $info->{'CreateDate'};
      if(!defined($create_date)){ print "no exif\n"; return; }
      print "[撮影日：$create_date]" , ","; 
      $create_date =~ m/^(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)$/ or die "illegal exif time: $path\n";
      my $ctime = timelocal($6, $5, $4, $3, $2-1, $1-1900);
      utime $ctime, $ctime, $path or die "error: fail to update ctime $path\n";
      print "ok\n";
    } elsif( $file =~ /^VID_(20\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d).(MP4|mp4)$/ ) { # freetel video format
      my $ctime = timelocal($6, $5, $4, $3, $2-1, $1-1900);
      my $s = localtime($ctime); print $s . ",";
      utime $ctime, $ctime, $path or die "error: fail to update ctime $path\n";
      print "ok\n";

    } else {
      print "skip\n"; return; 
    }
}

