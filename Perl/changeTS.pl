# Change Time Stamp of files

use strict;
use warnings;
use File::Find;
use Cwd;
use File::Copy;
use Time::Local;

# inDirフォルダ以下のファイルの更新日時を取得し、
# outDirフォルダ以下のファイルの更新日時に設定する。

# 対象フォルダ名
my $inDir = "C:\\Users\\sdkn1\\Desktop\\test"; 
my $outDir = "C:\\Users\\sdkn1\\Desktop\\test - コピー"; 

find(\&print_file, $inDir);

sub print_file {
    if( ! -f ) { return 0; } #ファイル以外は除く
    my $file = $_;
    my $inPath = $File::Find::name;
    my $outPath = "$outDir/$file";
    print "--- $file : $inPath -> $outPath\n";

    my $mtime = (stat($inPath))[9] ;
    my $atime = time;
    my $mt = localtime($mtime);
    my $at = localtime($atime);

    #print "$mt, $at\n";

    utime $atime, $mtime, $outPath or die "error: fail to update ctime $outPath\n";
}

